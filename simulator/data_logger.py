#!/usr/bin/env python3
"""
MES Data Pipeline Logger Daemon
Reads the 7 tags from the OPC UA simulator (opc.tcp://127.0.0.1:4840/mes/simulator)
and logs production metrics and machine status intervals into MySQL (mes_production_db).
Implements the exact logic of the Ignition Gateway scripts (A4) with:
- Tag change event detection for Machine_Status (gapless intervals, COMM_LOSS = -1)
- Configurable periodic production snapshots (default 5s, Decision D13)
- In-memory retry queue on DB disconnection (up to 1000 rows)
- Shift-aware target upserts (Decision D8)
"""

import asyncio
import datetime
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from asyncua import Client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [LOGGER] [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/pipeline.log", encoding="utf-8")
    ]
)
log = logging.getLogger("PipelineLogger")

ENDPOINT = "opc.tcp://127.0.0.1:4840/mes/simulator"
MACHINE_ID = 1  # MC-001


def parse_env():
    env_file = Path("D:/MES/mes-project/.env")
    env = {}
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


class PipelineLogger:
    def __init__(self):
        self.env = parse_env()
        self.writer_password = self.env.get("IGNITION_WRITER_PASSWORD", "")
        self.mysql_bin = "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe"
        self.last_status = None
        self.last_log_time = None
        self.log_interval_sec = 5  # D13 default
        self.retry_queue = []
        self.is_running = True

    def run_sql(self, sql_statement):
        cmd = [
            self.mysql_bin,
            "-u", "ignition_writer",
            "-h", "127.0.0.1",
            f"--password={self.writer_password}",
            "mes_production_db",
            "-e", sql_statement
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"MySQL error: {res.stderr.strip()}")
        return res.stdout.strip()

    def get_current_shift(self, now_utc):
        # Local time = UTC + 5:30
        local_time = now_utc + datetime.timedelta(hours=5, minutes=30)
        mins = local_time.hour * 60 + local_time.minute
        if 360 <= mins < 840:
            return "Shift A", local_time.date()
        elif 840 <= mins < 1320:
            return "Shift B", local_time.date()
        else:
            return "Shift C", local_time.date()

    def handle_status_change(self, new_status, now_utc):
        now_str = now_utc.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log.info("Machine status changed from %s to %s", self.last_status, new_status)
        try:
            # 1. Close open interval
            close_sql = f"UPDATE machine_status_log SET end_time = '{now_str}' WHERE machine_id = {MACHINE_ID} AND end_time IS NULL;"
            self.run_sql(close_sql)
            
            # 2. Insert new interval
            open_sql = f"INSERT INTO machine_status_log (machine_id, machine_status, start_time, end_time) VALUES ({MACHINE_ID}, {new_status}, '{now_str}', NULL);"
            self.run_sql(open_sql)
            self.last_status = new_status
        except Exception as e:
            log.error("Failed to update status interval: %s", e)

    def log_production_row(self, total, good, reject, cycle_time, temp, target, now_utc):
        now_str = now_utc.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        shift_name, prod_date = self.get_current_shift(now_utc)
        
        # Upsert target
        upsert_target_sql = f"""
            INSERT INTO production_target (machine_id, production_date, shift_name, target_quantity)
            VALUES ({MACHINE_ID}, '{prod_date}', '{shift_name}', {target})
            ON DUPLICATE KEY UPDATE target_quantity = VALUES(target_quantity);
        """
        try:
            self.run_sql(upsert_target_sql)
        except Exception as e:
            log.warning("Target upsert warning: %s", e)
            
        insert_sql = f"""
            INSERT INTO production_log 
            (machine_id, total_count, good_count, reject_count, cycle_time, temperature, recorded_at, data_quality)
            VALUES ({MACHINE_ID}, {total}, {good}, {reject}, {cycle_time:.3f}, {temp:.2f}, '{now_str}', 'GOOD');
        """
        
        # Flush retry queue first
        if self.retry_queue:
            flushed = []
            for queued_sql in self.retry_queue[:]:
                try:
                    self.run_sql(queued_sql)
                    flushed.append(queued_sql)
                except Exception:
                    break
            for f in flushed:
                self.retry_queue.remove(f)
            if flushed:
                log.info("Flushed %d queued rows to MySQL", len(flushed))
                
        try:
            self.run_sql(insert_sql)
        except Exception as e:
            log.error("DB insert failed, queuing row: %s", e)
            if len(self.retry_queue) < 1000:
                self.retry_queue.append(insert_sql)

    async def run(self):
        log.info("Starting MES Pipeline Logger connecting to %s...", ENDPOINT)
        
        # Initial startup recovery: close orphaned intervals
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        now_str = now_utc.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        try:
            self.run_sql(f"UPDATE machine_status_log SET end_time = '{now_str}' WHERE machine_id = {MACHINE_ID} AND end_time IS NULL;")
            log.info("Startup recovery: closed orphaned status intervals.")
        except Exception as e:
            log.warning("Startup recovery warning: %s", e)

        while self.is_running:
            try:
                async with Client(url=ENDPOINT) as client:
                    log.info("Connected to OPC UA server.")
                    ns = await client.get_namespace_index("http://mes.local/simulator")
                    
                    node_status = client.get_node(f"ns={ns};s=Machine01.Machine_Status")
                    node_total  = client.get_node(f"ns={ns};s=Machine01.Total_Count")
                    node_good   = client.get_node(f"ns={ns};s=Machine01.Good_Count")
                    node_reject = client.get_node(f"ns={ns};s=Machine01.Reject_Count")
                    node_cycle  = client.get_node(f"ns={ns};s=Machine01.Cycle_Time")
                    node_temp   = client.get_node(f"ns={ns};s=Machine01.Temperature")
                    node_target = client.get_node(f"ns={ns};s=Machine01.Target_Count")
                    
                    while self.is_running:
                        loop_now = datetime.datetime.now(datetime.timezone.utc)
                        
                        try:
                            status_val = await node_status.read_value()
                            total_val  = await node_total.read_value()
                            good_val   = await node_good.read_value()
                            reject_val = await node_reject.read_value()
                            cycle_val  = await node_cycle.read_value()
                            temp_val   = await node_temp.read_value()
                            target_val = await node_target.read_value()
                        except Exception as tag_err:
                            log.error("Failed to read OPC tags (COMM_LOSS): %s", tag_err)
                            if self.last_status != -1:
                                self.handle_status_change(-1, loop_now)
                            break  # reconnect
                            
                        # Detect status change
                        if self.last_status != status_val:
                            self.handle_status_change(status_val, loop_now)
                            
                        # Check periodic log timer
                        if self.last_log_time is None or (time.monotonic() - self.last_log_time) >= self.log_interval_sec:
                            self.log_production_row(total_val, good_val, reject_val, cycle_val, temp_val, target_val, loop_now)
                            self.last_log_time = time.monotonic()
                            
                        await asyncio.sleep(1.0)
                        
            except Exception as conn_err:
                log.warning("OPC UA connection issue: %s. Retrying in 3s...", conn_err)
                now_utc = datetime.datetime.now(datetime.timezone.utc)
                if self.last_status != -1:
                    self.handle_status_change(-1, now_utc)
                await asyncio.sleep(3.0)


def main():
    try:
        asyncio.run(PipelineLogger().run())
    except KeyboardInterrupt:
        log.info("Pipeline logger stopped by operator.")

if __name__ == "__main__":
    main()
