-- Parameterised Named Query: GetProductionHistory
-- Parameters: :machine_id (INT), :start_time (DATETIME), :end_time (DATETIME)
SELECT
  pl.log_id,
  pl.recorded_at,
  pl.total_count,
  pl.good_count,
  pl.reject_count,
  pl.cycle_time,
  pl.temperature,
  pl.data_quality
FROM production_log pl
WHERE pl.machine_id = :machine_id
  AND pl.recorded_at BETWEEN :start_time AND :end_time
ORDER BY pl.recorded_at DESC
LIMIT 500;
