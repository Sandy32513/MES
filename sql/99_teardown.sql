-- ============================================================
-- 99_teardown.sql — Complete Teardown of MES Database
-- Idempotent & safe
-- ============================================================

USE mes_production_db;
SET FOREIGN_KEY_CHECKS=0;

DROP VIEW IF EXISTS v_data_quality_issues;
DROP VIEW IF EXISTS v_kpi_by_shift;
DROP VIEW IF EXISTS v_hourly_production;
DROP VIEW IF EXISTS v_production_by_shift;
DROP VIEW IF EXISTS v_status_durations_by_shift;
DROP VIEW IF EXISTS v_current_shift;

DROP TABLE IF EXISTS production_log;
DROP TABLE IF EXISTS machine_status_log;
DROP TABLE IF EXISTS production_target;
DROP TABLE IF EXISTS shift_master;
DROP TABLE IF EXISTS machine_master;

SET FOREIGN_KEY_CHECKS=1;
-- DROP DATABASE IF EXISTS mes_production_db;
