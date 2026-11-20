# ============================================================
# Ignition Gateway Timer Script: Production Logger
# Runs at 1000 ms rate. Checks LogIntervalSec (Decision D13).
# Buffers records in memory on DB failure (up to 1000 rows).
# Upserts production_target at shift start (Decision D8).
# ============================================================

import system

MACHINE_ID = 1  # MC-001
DB_CONN = "MES_DB"
LOGGER_NAME = "MES.ProductionLogger"
LOG_INTERVAL_TAG = "[default]MES/Config/LogIntervalSec"


def execute():
    globals_ = system.util.getGlobals()
    if "mes_last_log_time" not in globals_:
        globals_["mes_last_log_time"] = None
        globals_["mes_retry_queue"] = []
        
    logger = system.util.getLogger(LOGGER_NAME)
    now = system.date.now()
    
    try:
        # Read interval setting
        qvs = system.tag.readBlocking([LOG_INTERVAL_TAG])
        log_interval = qvs[0].value if (qvs and qvs[0].value) else 5
        
        # Check elapsed time
        last_log = globals_["mes_last_log_time"]
        if last_log is not None:
            elapsed_sec = system.date.secondsBetween(last_log, now)
            if elapsed_sec < log_interval:
                return  # Interval not yet elapsed
                
        # Read the 7 tags + Comm_OK
        tags = [
            "[default]MES/Machine01/Machine_Status",
            "[default]MES/Machine01/Total_Count",
            "[default]MES/Machine01/Good_Count",
            "[default]MES/Machine01/Reject_Count",
            "[default]MES/Machine01/Cycle_Time",
            "[default]MES/Machine01/Temperature",
            "[default]MES/Machine01/Target_Count",
            "[default]MES/Machine01/Comm_OK"
        ]
        results = system.tag.readBlocking(tags)
        
        status_qv, total_qv, good_qv, reject_qv, cycle_qv, temp_qv, target_qv, comm_ok_qv = results
        
        # Skip row insertion on bad quality (COMM_LOSS is tracked in machine_status_log)
        if not status_qv.quality.isGood():
            logger.warn("Skipping production log row: OPC quality is bad")
            return
            
        total_val = int(total_qv.value)
        good_val = int(good_qv.value)
        reject_val = int(reject_qv.value)
        cycle_val = float(cycle_qv.value)
        temp_val = float(temp_qv.value)
        target_val = int(target_qv.value)
        
        # Upsert target at shift start (D8)
        shift_name = get_active_shift(now)
        if shift_name:
            upsert_shift_target(MACHINE_ID, now, shift_name, target_val, DB_CONN)
            
        row_params = [MACHINE_ID, total_val, good_val, reject_val, cycle_val, temp_val, now, 'GOOD']
        insert_sql = """
            INSERT INTO production_log 
            (machine_id, total_count, good_count, reject_count, cycle_time, temperature, recorded_at, data_quality)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Flush retry queue first
        queue = globals_["mes_retry_queue"]
        remaining_queue = []
        for queued_row in queue:
            try:
                system.db.runPrepUpdate(insert_sql, queued_row, DB_CONN)
            except Exception as ex:
                remaining_queue.append(queued_row)
        globals_["mes_retry_queue"] = remaining_queue
        
        # Insert current sample
        try:
            system.db.runPrepUpdate(insert_sql, row_params, DB_CONN)
            globals_["mes_last_log_time"] = now
        except Exception as db_err:
            logger.error("DB insert failed; appending to in-memory retry queue: {}".format(str(db_err)))
            if len(globals_["mes_retry_queue"]) < 1000:
                globals_["mes_retry_queue"].append(row_params)
            globals_["mes_last_log_time"] = now
            
    except Exception as e:
        logger.error("Unexpected error in ProductionLogger: {}".format(str(e)))


def get_active_shift(utc_dt):
    """Determine shift from timestamp in Plant Timezone (+05:30)."""
    # Offset by 5.5 hours
    local_dt = system.date.addMinutes(utc_dt, 330)
    hour = system.date.getHour24(local_dt)
    minute = system.date.getMinute(local_dt)
    mins = hour * 60 + minute
    
    if 360 <= mins < 840:      # 06:00 to 14:00
        return "Shift A"
    elif 840 <= mins < 1320:   # 14:00 to 22:00
        return "Shift B"
    else:                      # 22:00 to 06:00
        return "Shift C"


def upsert_shift_target(machine_id, utc_dt, shift_name, target_quantity, db_conn):
    """Upsert production_target row for active shift."""
    local_dt = system.date.addMinutes(utc_dt, 330)
    prod_date = system.date.format(local_dt, "yyyy-MM-dd")
    sql = """
        INSERT INTO production_target (machine_id, production_date, shift_name, target_quantity)
        VALUES (?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE target_quantity = VALUES(target_quantity)
    """
    try:
        system.db.runPrepUpdate(sql, [machine_id, prod_date, shift_name, target_quantity], db_conn)
    except Exception:
        pass
