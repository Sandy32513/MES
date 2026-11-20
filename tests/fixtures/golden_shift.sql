-- ============================================================
-- golden_shift.sql — Golden KPI Test Fixture (Section 6.4)
-- ============================================================

USE mes_production_db;

-- 1. Create Golden Test Machine (MC-GOLDEN)
INSERT INTO machine_master (machine_name, machine_code, machine_location, is_active, ideal_cycle_time_sec)
VALUES ('Golden Test Machine', 'MC-GOLDEN', 'QA Test Cell', 1, 5.000)
ON DUPLICATE KEY UPDATE ideal_cycle_time_sec = 5.000;

SET @gmid = (SELECT machine_id FROM machine_master WHERE machine_code = 'MC-GOLDEN');
SET @test_date = '2026-11-20';

-- 2. Target: 480 pieces for Shift A
INSERT INTO production_target (machine_id, production_date, shift_name, target_quantity)
VALUES (@gmid, @test_date, 'Shift A', 480)
ON DUPLICATE KEY UPDATE target_quantity = 480;

-- Clean existing logs for golden machine on this date
DELETE FROM production_log WHERE machine_id = @gmid;
DELETE FROM machine_status_log WHERE machine_id = @gmid;

-- 3. Status Intervals:
-- Shift A in local time (UTC+5:30) is 06:00:00 to 14:00:00.
-- In UTC, 06:00 IST is 00:30 UTC.
-- We place the 60-minute golden window from 01:00:00 UTC to 02:00:00 UTC (06:30 to 07:30 IST).
-- RUN: 40 min = 01:00:00 to 01:40:00 UTC (2400 s)
-- IDLE: 10 min = 01:40:00 to 01:50:00 UTC (600 s)
-- STOP: 10 min = 01:50:00 to 02:00:00 UTC (600 s)

INSERT INTO machine_status_log (machine_id, machine_status, start_time, end_time) VALUES
  (@gmid, 1, '2026-11-20 01:00:00.000', '2026-11-20 01:40:00.000'),
  (@gmid, 2, '2026-11-20 01:40:00.000', '2026-11-20 01:50:00.000'),
  (@gmid, 0, '2026-11-20 01:50:00.000', '2026-11-20 02:00:00.000');

-- 4. Production Logs:
-- Total 400, Good 380, Reject 20
-- Start of shift baseline log (0 total)
INSERT INTO production_log (machine_id, total_count, good_count, reject_count, cycle_time, temperature, recorded_at, data_quality)
VALUES (@gmid, 0, 0, 0, 5.000, 25.0, '2026-11-20 01:00:00.000', 'GOOD');

-- Intermediate samples accumulating to 400 total
INSERT INTO production_log (machine_id, total_count, good_count, reject_count, cycle_time, temperature, recorded_at, data_quality) VALUES
  (@gmid, 100, 95, 5, 5.000, 72.0, '2026-11-20 01:10:00.000', 'GOOD'),
  (@gmid, 200, 190, 10, 5.000, 75.0, '2026-11-20 01:20:00.000', 'GOOD'),
  (@gmid, 300, 285, 15, 5.000, 78.0, '2026-11-20 01:30:00.000', 'GOOD'),
  (@gmid, 400, 380, 20, 5.000, 80.0, '2026-11-20 01:40:00.000', 'GOOD');
