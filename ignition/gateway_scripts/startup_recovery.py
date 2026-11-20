# ============================================================
# Ignition Gateway Startup Script: Startup Recovery
# Closes any orphaned open status intervals upon Gateway restart.
# Queries the live status tag and opens a clean new interval.
# ============================================================

import system

MACHINE_ID = 1  # MC-001
DB_CONN = "MES_DB"
LOGGER_NAME = "MES.StartupRecovery"


def run():
    logger = system.util.getLogger(LOGGER_NAME)
    now_utc = system.date.now()
    
    try:
        # 1. Close orphaned open intervals
        close_sql = """
            UPDATE machine_status_log
            SET end_time = ?
            WHERE machine_id = ? AND end_time IS NULL
        """
        closed_count = system.db.runPrepUpdate(close_sql, [now_utc, MACHINE_ID], DB_CONN)
        logger.info("Startup recovery closed {} open intervals.".format(closed_count))
        
        # 2. Read live status and open initial interval
        qvs = system.tag.readBlocking(["[default]MES/Machine01/Machine_Status"])
        if qvs and qvs[0].quality.isGood():
            current_status = int(qvs[0].value)
        else:
            current_status = -1  # COMM_LOSS
            
        open_sql = """
            INSERT INTO machine_status_log (machine_id, machine_status, start_time, end_time)
            VALUES (?, ?, ?, NULL)
        """
        system.db.runPrepUpdate(open_sql, [MACHINE_ID, current_status, now_utc], DB_CONN)
        logger.info("Startup recovery opened new interval with status={} at {}".format(current_status, now_utc))
        
    except Exception as e:
        logger.error("Startup recovery failed: {}".format(str(e)))

run()
