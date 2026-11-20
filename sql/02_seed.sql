-- ============================================================
-- 02_seed.sql — MES Production Seed Data
-- Idempotent: safe to run multiple times without duplicating rows
-- ============================================================

USE mes_production_db;

-- 1. Machine: MC-001
INSERT INTO machine_master (machine_name, machine_code, machine_location, is_active, ideal_cycle_time_sec)
VALUES ('Machine 01', 'MC-001', 'Production Line 1', 1, 5.000)
ON DUPLICATE KEY UPDATE machine_name = VALUES(machine_name), ideal_cycle_time_sec = VALUES(ideal_cycle_time_sec);

-- 2. Shifts: A (06:00-14:00), B (14:00-22:00), C (22:00-06:00, crosses midnight)
INSERT INTO shift_master (shift_name, start_time, end_time) VALUES
  ('Shift A', '06:00:00', '14:00:00'),
  ('Shift B', '14:00:00', '22:00:00'),
  ('Shift C', '22:00:00', '06:00:00')
ON DUPLICATE KEY UPDATE start_time = VALUES(start_time), end_time = VALUES(end_time);

-- 3. Production targets: 4800 per shift for today and the next 7 days
SET @mid = (SELECT machine_id FROM machine_master WHERE machine_code = 'MC-001');
SET @today = CURDATE();

INSERT IGNORE INTO production_target (machine_id, production_date, shift_name, target_quantity)
SELECT @mid, DATE_ADD(@today, INTERVAL n.num DAY), s.shift_name, 4800
FROM shift_master s
CROSS JOIN (
  SELECT 0 AS num UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
  UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7
) n;
