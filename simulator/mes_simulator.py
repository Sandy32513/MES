#!/usr/bin/env python3
"""
MES OPC UA Simulator
Endpoint: opc.tcp://127.0.0.1:4840/mes/simulator
Tags: ns=2;s=Machine01.<TagName>
Complies with Decision D2 and Master Execution Prompt requirements.
"""

import asyncio
import argparse
import json
import logging
import os
import random
import sys
import time
from pathlib import Path
from asyncua import Server, ua

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/sim.log", encoding="utf-8")
    ]
)
log = logging.getLogger("MESSimulator")


class MESSimulator:
    def __init__(self, args):
        self.args = args
        self.time_scale = max(0.01, float(args.time_scale))
        self.seed = args.seed
        self.scenario = args.scenario
        self.control_file = Path(args.control_file) if args.control_file else None
        
        if self.seed is not None:
            random.seed(self.seed)
            log.info("Initialized with random seed: %d", self.seed)
        
        # State variables
        self.machine_status = 0  # 0=STOP, 1=RUN, 2=IDLE
        self.total_count = 0
        self.good_count = 0
        self.reject_count = 0
        self.cycle_time = 5.0
        self.temperature = 25.0
        self.target_count = 4800
        
        self.server = None
        self.nodes = {}
        self.is_running = True
        self.forced_status = None

    async def setup_server(self):
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint("opc.tcp://127.0.0.1:4840/mes/simulator")
        self.server.set_server_name("MES Machine Simulator")
        
        # Security Policy: None (local dev)
        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        
        # Register namespace
        uri = "http://mes.local/simulator"
        idx = await self.server.register_namespace(uri)
        log.info("Namespace registered: %s (Index: %d)", uri, idx)
        
        # Build hierarchy: Objects/MES/Machine01
        objects = self.server.nodes.objects
        mes_folder = await objects.add_folder(idx, "MES")
        machine_folder = await mes_folder.add_folder(idx, "Machine01")
        
        # Register the exactly 7 tags
        tag_definitions = [
            ("Machine_Status", ua.VariantType.Int32, int(self.machine_status)),
            ("Total_Count",    ua.VariantType.Int32, int(self.total_count)),
            ("Good_Count",     ua.VariantType.Int32, int(self.good_count)),
            ("Reject_Count",   ua.VariantType.Int32, int(self.reject_count)),
            ("Cycle_Time",     ua.VariantType.Float, float(self.cycle_time)),
            ("Temperature",    ua.VariantType.Float, float(self.temperature)),
            ("Target_Count",   ua.VariantType.Int32, int(self.target_count)),
        ]
        
        for name, variant_type, initial_value in tag_definitions:
            node_id = ua.NodeId(f"Machine01.{name}", idx)
            var_node = await machine_folder.add_variable(
                node_id,
                name,
                ua.Variant(initial_value, variant_type)
            )
            await var_node.set_writable()
            self.nodes[name] = var_node
            log.info("Tag registered: %s -> NodeId %s", name, node_id)
            
        log.info("OPC UA Server setup complete.")

    async def update_tags(self):
        """Publish internal state to OPC UA tags."""
        try:
            await self.nodes["Machine_Status"].write_value(ua.Variant(int(self.machine_status), ua.VariantType.Int32))
            await self.nodes["Total_Count"].write_value(ua.Variant(int(self.total_count), ua.VariantType.Int32))
            await self.nodes["Good_Count"].write_value(ua.Variant(int(self.good_count), ua.VariantType.Int32))
            await self.nodes["Reject_Count"].write_value(ua.Variant(int(self.reject_count), ua.VariantType.Int32))
            await self.nodes["Cycle_Time"].write_value(ua.Variant(round(float(self.cycle_time), 3), ua.VariantType.Float))
            await self.nodes["Temperature"].write_value(ua.Variant(round(float(self.temperature), 2), ua.VariantType.Float))
            await self.nodes["Target_Count"].write_value(ua.Variant(int(self.target_count), ua.VariantType.Int32))
        except Exception as e:
            log.warning("Tag write error: %s", e)

    def sleep_scaled(self, seconds):
        """Scale sleep duration according to --time-scale."""
        return asyncio.sleep(max(0.01, seconds / self.time_scale))

    async def check_control_file(self):
        """Check external control JSON file for fault injection."""
        if not self.control_file or not self.control_file.exists():
            return
        try:
            content = self.control_file.read_text(encoding="utf-8-sig").strip()
            if not content:
                return
            cmd = json.loads(content)
            
            if "force_status" in cmd:
                if cmd["force_status"] is not None:
                    self.forced_status = int(cmd["force_status"])
                    self.machine_status = self.forced_status
                    log.info("[FAULT INJECTION] Forcing machine status to %d", self.forced_status)
                else:
                    self.forced_status = None
                    log.info("[FAULT INJECTION] Cleared forced machine status")
                await self.update_tags()
                
            if cmd.get("reset_counters"):
                log.info("[FAULT INJECTION] Resetting counters to 0")
                self.total_count = 0
                self.good_count = 0
                self.reject_count = 0
                await self.update_tags()
                
            if "temperature" in cmd and cmd["temperature"] is not None:
                self.temperature = float(cmd["temperature"])
                await self.update_tags()
                
            # Clear command file
            self.control_file.write_text("{}", encoding="utf-8")
        except Exception as e:
            log.warning("Control file processing warning: %s", e)

    async def run_cycle(self):
        """Simulate one production cycle in RUN state."""
        self.cycle_time = random.uniform(4.5, 5.5)
        await self.sleep_scaled(self.cycle_time)
        
        self.total_count += 1
        if random.random() < 0.97:  # 97% good count probability
            self.good_count += 1
        else:
            self.reject_count += 1
            
        # Enforce invariant
        assert self.good_count + self.reject_count == self.total_count, "Invariant violated!"
        
        # Temperature rises toward 70-85 C in RUN
        target_temp = random.uniform(70.0, 85.0)
        self.temperature += (target_temp - self.temperature) * 0.05
        
        await self.update_tags()

    async def run_idle(self, duration_sec):
        """Simulate IDLE state."""
        self.machine_status = 2
        await self.update_tags()
        log.info("Transitioned to IDLE (planned duration: %.1f s)", duration_sec)
        
        end_time = time.monotonic() + (duration_sec / self.time_scale)
        while time.monotonic() < end_time and self.is_running:
            self.temperature += (25.0 - self.temperature) * 0.02
            await self.update_tags()
            await asyncio.sleep(1.0 / self.time_scale)
            await self.check_control_file()
            if self.machine_status != 2:
                break

    async def run_stop(self, duration_sec):
        """Simulate STOP state."""
        self.machine_status = 0
        await self.update_tags()
        log.info("Transitioned to STOP (planned duration: %.1f s)", duration_sec)
        
        end_time = time.monotonic() + (duration_sec / self.time_scale)
        while time.monotonic() < end_time and self.is_running:
            self.temperature += (25.0 - self.temperature) * 0.05
            await self.update_tags()
            await asyncio.sleep(1.0 / self.time_scale)
            await self.check_control_file()
            if self.machine_status != 0:
                break

    async def run_normal_scenario(self):
        """Normal production scenario (~80% RUN, 10% IDLE, 10% STOP)."""
        while self.is_running:
            if self.forced_status is not None:
                self.machine_status = self.forced_status
                await self.update_tags()
                if self.forced_status == 1:
                    await self.run_cycle()
                else:
                    await asyncio.sleep(1.0 / self.time_scale)
                await self.check_control_file()
                continue

            # RUN phase
            self.machine_status = 1
            await self.update_tags()
            run_duration = random.uniform(60, 240)  # 1 to 4 minutes
            log.info("Transitioned to RUN (duration: %.0f s)", run_duration)
            
            end_run = time.monotonic() + (run_duration / self.time_scale)
            while time.monotonic() < end_run and self.is_running:
                await self.run_cycle()
                await self.check_control_file()
                if self.machine_status != 1:
                    break
                    
            if not self.is_running:
                break
                
            # Intermittent downtime
            if random.random() < 0.5:
                await self.run_idle(random.uniform(20, 60))
            else:
                await self.run_stop(random.uniform(15, 45))

    async def run_kpi_golden_scenario(self):
        """Golden KPI scenario: exactly 40 min RUN, 10 min IDLE, 10 min STOP."""
        log.info("Running Golden KPI scenario (40m RUN, 10m IDLE, 10m STOP)")
        while self.is_running:
            # 40 minutes RUN
            self.machine_status = 1
            await self.update_tags()
            log.info("KPI Golden: Starting 40 min RUN (2400 s)")
            end_run = time.monotonic() + (2400.0 / self.time_scale)
            while time.monotonic() < end_run and self.is_running:
                await self.run_cycle()
                await self.check_control_file()
            
            # 10 minutes IDLE
            await self.run_idle(600.0)
            
            # 10 minutes STOP
            await self.run_stop(600.0)

    async def run_flapping_scenario(self):
        """Rapid state transitions for resilience testing."""
        log.info("Running Flapping scenario (rapid state cycling)")
        while self.is_running:
            self.machine_status = 1
            await self.update_tags()
            await self.run_cycle()
            await self.run_idle(5.0)
            await self.run_stop(5.0)

    async def run_long_stop_scenario(self):
        """Extended downtime scenario."""
        log.info("Running Long Stop scenario")
        while self.is_running:
            self.machine_status = 1
            await self.update_tags()
            end_run = time.monotonic() + (120.0 / self.time_scale)
            while time.monotonic() < end_run and self.is_running:
                await self.run_cycle()
            await self.run_stop(1800.0)

    async def run(self):
        await self.setup_server()
        
        if self.args.reset_counters:
            self.total_count = 0
            self.good_count = 0
            self.reject_count = 0
            await self.update_tags()
            log.info("Counters reset to 0 via --reset-counters")
            
        async with self.server:
            log.info("MES OPC UA Simulator is active at opc.tcp://127.0.0.1:4840/mes/simulator")
            log.info("Scenario: %s | Time-Scale: %.1fx", self.scenario, self.time_scale)
            
            if self.scenario == "kpi_golden":
                await self.run_kpi_golden_scenario()
            elif self.scenario == "flapping":
                await self.run_flapping_scenario()
            elif self.scenario == "long_stop":
                await self.run_long_stop_scenario()
            else:
                await self.run_normal_scenario()


def main():
    parser = argparse.ArgumentParser(description="MES OPC UA Machine Simulator")
    parser.add_argument("--scenario", choices=["normal", "kpi_golden", "flapping", "long_stop"], default="normal")
    parser.add_argument("--time-scale", type=float, default=1.0, help="Simulation speed multiplier (e.g. 5.0 = 5x)")
    parser.add_argument("--seed", type=int, default=None, help="Deterministic random seed")
    parser.add_argument("--control-file", default=None, help="JSON file path for fault injection")
    parser.add_argument("--reset-counters", action="store_true", help="Reset counts to 0 at startup")
    args = parser.parse_args()
    
    try:
        asyncio.run(MESSimulator(args).run())
    except KeyboardInterrupt:
        log.info("Simulator terminated by operator.")

if __name__ == "__main__":
    main()
