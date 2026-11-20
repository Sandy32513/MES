-- Parameterised Named Query: GetShiftTotals
-- Parameters: :machine_id (INT), :production_date (DATE)
SELECT
  machine_id,
  production_date,
  shift_name,
  total_produced,
  good_produced,
  reject_produced
FROM v_production_by_shift
WHERE machine_id = :machine_id
  AND production_date = :production_date
ORDER BY shift_name;
