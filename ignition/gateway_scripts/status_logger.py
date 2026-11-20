# ============================================================
# Ignition Gateway Tag Change Script: Machine_Status
# Attached to tag: [default]MES/Machine01/Machine_Status
# Closes previous open interval and opens a new interval.
# Handles COMM_LOSS (-1) on bad quality.
# ============================================================

import system

MACHINE_ID = 1  # MC-001
DB_CONN = "MES_DB"
LOGGER_NAME = "MES.StatusLogger"


def valueChanged(tag, tagPath, previousValue, currentValue, initialChange, missedEvents):
    logger = system.util.getLogger(LOGGER_NAME)
    try:
        now_utc = system.date.now()
        
        # Check OPC quality
        if currentValue is None or not currentValue.quality.isGood():
            new_status = -1  # COMM_LOSS
            logger.warn("OPC tag quality is BAD; opening COMM_LOSS interval (-1)")
        else:
            new_status = int(currentValue.value)
            
        # 1. Close any currently open status interval for this machine
        close_sql = """
            UPDATE machine_status_log
            SET end_time = ?
            WHERE machine_id = ? AND end_time IS NULL
        """
        system.db.runPrepUpdate(close_sql, [now_utc, MACHINE_ID], DB_CONN)
        
        # 2. Insert new status interval
        open_sql = """
            INSERT INTO machine_status_log (machine_id, machine_status, start_time, end_time)
            VALUES (?, ?, ?, NULL)
        """
        system.db.runPrepUpdate(open_sql, [MACHINE_ID, new_status, now_utc], DB_CONN)
        
        logger.info("Recorded status change: machine_id={} status={} at {}".format(
            MACHINE_ID, new_status, now_utc
        ))
        
    except Exception as e:
        logger.error("Exception in StatusLogger: {}".format(str(e)))
