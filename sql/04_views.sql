-- ============================================================
-- 04_views.sql — MES Reporting Views
-- Idempotent: uses CREATE OR REPLACE VIEW
-- ============================================================

USE mes_production_db;

-- 1. Current Shift View (Plant timezone UTC+05:30)
CREATE OR REPLACE VIEW v_current_shift AS
SELECT
  s.shift_id,
  s.shift_name,
  s.start_time,
  s.end_time,
  CASE
    WHEN s.end_time > s.start_time THEN
      TIME(CONVERT_TZ(UTC_TIMESTAMP(), '+00:00', '+05:30')) BETWEEN s.start_time AND s.end_time
    ELSE
      TIME(CONVERT_TZ(UTC_TIMESTAMP(), '+00:00', '+05:30')) >= s.start_time
      OR TIME(CONVERT_TZ(UTC_TIMESTAMP(), '+00:00', '+05:30')) < s.end_time
  END AS is_current
FROM shift_master s;

-- 2. Status Durations by Machine, Date and Shift
CREATE OR REPLACE VIEW v_status_durations_by_shift AS
SELECT
  sl.machine_id,
  DATE(CONVERT_TZ(sl.start_time, '+00:00', '+05:30')) AS production_date,
  sm.shift_name,
  sl.machine_status,
  SUM(
    TIMESTAMPDIFF(SECOND,
      sl.start_time,
      COALESCE(sl.end_time, UTC_TIMESTAMP())
    )
  ) AS duration_seconds
FROM machine_status_log sl
JOIN shift_master sm ON (
  CASE WHEN sm.end_time > sm.start_time
    THEN TIME(CONVERT_TZ(sl.start_time, '+00:00', '+05:30')) BETWEEN sm.start_time AND sm.end_time
    ELSE TIME(CONVERT_TZ(sl.start_time, '+00:00', '+05:30')) >= sm.start_time
      OR TIME(CONVERT_TZ(sl.start_time, '+00:00', '+05:30')) < sm.end_time
  END
)
WHERE sl.start_time <= COALESCE(sl.end_time, UTC_TIMESTAMP())
GROUP BY sl.machine_id, production_date, sm.shift_name, sl.machine_status;

-- 3. Production Summary by Shift (Delta-based, reset-aware)
CREATE OR REPLACE VIEW v_production_by_shift AS
WITH ordered AS (
  SELECT
    pl.log_id,
    pl.machine_id,
    pl.total_count,
    pl.good_count,
    pl.reject_count,
    pl.recorded_at,
    DATE(CONVERT_TZ(pl.recorded_at, '+00:00', '+05:30')) AS production_date,
    sm.shift_name,
    LAG(pl.total_count) OVER (PARTITION BY pl.machine_id ORDER BY pl.recorded_at) AS prev_total,
    LAG(pl.good_count)  OVER (PARTITION BY pl.machine_id ORDER BY pl.recorded_at) AS prev_good,
    LAG(pl.reject_count) OVER (PARTITION BY pl.machine_id ORDER BY pl.recorded_at) AS prev_reject
  FROM production_log pl
  JOIN shift_master sm ON (
    CASE WHEN sm.end_time > sm.start_time
      THEN TIME(CONVERT_TZ(pl.recorded_at, '+00:00', '+05:30')) BETWEEN sm.start_time AND sm.end_time
      ELSE TIME(CONVERT_TZ(pl.recorded_at, '+00:00', '+05:30')) >= sm.start_time
        OR TIME(CONVERT_TZ(pl.recorded_at, '+00:00', '+05:30')) < sm.end_time
    END
  )
),
deltas AS (
  SELECT
    machine_id,
    production_date,
    shift_name,
    CASE WHEN prev_total IS NULL OR total_count < prev_total THEN total_count ELSE total_count - prev_total END AS delta_total,
    CASE WHEN prev_good IS NULL  OR good_count  < prev_good  THEN good_count  ELSE good_count  - prev_good  END AS delta_good,
    CASE WHEN prev_reject IS NULL OR reject_count < prev_reject THEN reject_count ELSE reject_count - prev_reject END AS delta_reject
  FROM ordered
)
SELECT
  machine_id,
  production_date,
  shift_name,
  COALESCE(SUM(delta_total), 0)  AS total_produced,
  COALESCE(SUM(delta_good), 0)   AS good_produced,
  COALESCE(SUM(delta_reject), 0) AS reject_produced
FROM deltas
GROUP BY machine_id, production_date, shift_name;

-- 4. Hourly Production
CREATE OR REPLACE VIEW v_hourly_production AS
WITH ordered AS (
  SELECT
    pl.machine_id,
    pl.total_count,
    pl.good_count,
    pl.reject_count,
    pl.recorded_at,
    DATE_FORMAT(CONVERT_TZ(pl.recorded_at, '+00:00', '+05:30'), '%Y-%m-%d %H:00:00') AS hour_bucket,
    LAG(pl.total_count) OVER (PARTITION BY pl.machine_id ORDER BY pl.recorded_at) AS prev_total,
    LAG(pl.good_count)  OVER (PARTITION BY pl.machine_id ORDER BY pl.recorded_at) AS prev_good,
    LAG(pl.reject_count) OVER (PARTITION BY pl.machine_id ORDER BY pl.recorded_at) AS prev_reject
  FROM production_log pl
),
deltas AS (
  SELECT
    machine_id,
    hour_bucket,
    CASE WHEN prev_total IS NULL OR total_count < prev_total THEN total_count ELSE total_count - prev_total END AS delta_total,
    CASE WHEN prev_good  IS NULL OR good_count  < prev_good  THEN good_count  ELSE good_count  - prev_good  END AS delta_good,
    CASE WHEN prev_reject IS NULL OR reject_count < prev_reject THEN reject_count ELSE reject_count - prev_reject END AS delta_reject
  FROM ordered
)
SELECT
  machine_id,
  hour_bucket,
  COALESCE(SUM(delta_total), 0)  AS total_produced,
  COALESCE(SUM(delta_good), 0)   AS good_produced,
  COALESCE(SUM(delta_reject), 0) AS reject_produced
FROM deltas
GROUP BY machine_id, hour_bucket;

-- 5. KPI by Shift (Availability, Performance, Quality, OEE, Achievement)
CREATE OR REPLACE VIEW v_kpi_by_shift AS
SELECT
  pb.machine_id,
  pb.production_date,
  pb.shift_name,
  mm.ideal_cycle_time_sec,
  pb.total_produced,
  pb.good_produced,
  pb.reject_produced,
  pt.target_quantity,
  -- Run duration (status 1)
  COALESCE((
    SELECT duration_seconds FROM v_status_durations_by_shift sd
    WHERE sd.machine_id = pb.machine_id AND sd.production_date = pb.production_date
      AND sd.shift_name = pb.shift_name AND sd.machine_status = 1
  ), 0) AS run_seconds,
  -- Planned production time in seconds (8 hours = 28800s)
  CASE
    WHEN sm.end_time > sm.start_time THEN TIME_TO_SEC(TIMEDIFF(sm.end_time, sm.start_time))
    ELSE TIME_TO_SEC(TIMEDIFF(sm.end_time, sm.start_time)) + 86400
  END AS planned_seconds,
  -- Availability % = Run Time / Planned Time * 100
  ROUND(
    COALESCE((
      SELECT duration_seconds FROM v_status_durations_by_shift sd
      WHERE sd.machine_id = pb.machine_id AND sd.production_date = pb.production_date
        AND sd.shift_name = pb.shift_name AND sd.machine_status = 1
    ), 0) /
    NULLIF(CASE
      WHEN sm.end_time > sm.start_time THEN TIME_TO_SEC(TIMEDIFF(sm.end_time, sm.start_time))
      ELSE TIME_TO_SEC(TIMEDIFF(sm.end_time, sm.start_time)) + 86400
    END, 0) * 100
  , 2) AS availability_pct,
  -- Performance % = min(1, ideal_cycle_time * total_produced / run_seconds) * 100
  ROUND(
    LEAST(1.0,
      (mm.ideal_cycle_time_sec * pb.total_produced) /
      NULLIF(COALESCE((
        SELECT duration_seconds FROM v_status_durations_by_shift sd
        WHERE sd.machine_id = pb.machine_id AND sd.production_date = pb.production_date
          AND sd.shift_name = pb.shift_name AND sd.machine_status = 1
      ), 0), 0)
    ) * 100
  , 2) AS performance_pct,
  -- Quality % = Good / Total * 100
  ROUND(
    pb.good_produced / NULLIF(pb.total_produced, 0) * 100
  , 2) AS quality_pct,
  -- OEE % = (Availability/100) * (Performance/100) * (Quality/100) * 100
  ROUND(
    (COALESCE((
      SELECT duration_seconds FROM v_status_durations_by_shift sd
      WHERE sd.machine_id = pb.machine_id AND sd.production_date = pb.production_date
        AND sd.shift_name = pb.shift_name AND sd.machine_status = 1
    ), 0) /
    NULLIF(CASE
      WHEN sm.end_time > sm.start_time THEN TIME_TO_SEC(TIMEDIFF(sm.end_time, sm.start_time))
      ELSE TIME_TO_SEC(TIMEDIFF(sm.end_time, sm.start_time)) + 86400
    END, 0)) *
    LEAST(1.0, (mm.ideal_cycle_time_sec * pb.total_produced) /
      NULLIF(COALESCE((
        SELECT duration_seconds FROM v_status_durations_by_shift sd2
        WHERE sd2.machine_id = pb.machine_id AND sd2.production_date = pb.production_date
          AND sd2.shift_name = pb.shift_name AND sd2.machine_status = 1
      ), 0), 0)
    ) *
    (pb.good_produced / NULLIF(pb.total_produced, 0)) * 100
  , 2) AS oee_pct,
  -- Production Achievement % = Total / Target * 100
  ROUND(
    pb.total_produced / NULLIF(pt.target_quantity, 0) * 100
  , 2) AS achievement_pct
FROM v_production_by_shift pb
JOIN machine_master mm ON mm.machine_id = pb.machine_id
JOIN shift_master sm ON sm.shift_name = pb.shift_name
LEFT JOIN production_target pt ON pt.machine_id = pb.machine_id
  AND pt.production_date = pb.production_date
  AND pt.shift_name = pb.shift_name;

-- 6. Data Quality Issues View
CREATE OR REPLACE VIEW v_data_quality_issues AS
SELECT
  'inconsistent_count' AS issue_type,
  log_id AS record_id,
  recorded_at AS issue_time,
  CONCAT('total=', total_count, ' good=', good_count, ' reject=', reject_count) AS detail
FROM production_log
WHERE is_consistent = 0
UNION ALL
SELECT
  'overlapping_status' AS issue_type,
  sl1.status_id AS record_id,
  sl1.start_time AS issue_time,
  CONCAT('status_id=', sl1.status_id, ' overlaps with status_id=', sl2.status_id) AS detail
FROM machine_status_log sl1
JOIN machine_status_log sl2 ON sl1.machine_id = sl2.machine_id
  AND sl1.status_id < sl2.status_id
  AND sl1.start_time < sl2.start_time
  AND COALESCE(sl1.end_time, UTC_TIMESTAMP()) > sl2.start_time;
