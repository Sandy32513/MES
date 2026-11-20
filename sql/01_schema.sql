-- ============================================================
-- 01_schema.sql — MES Production Database Schema
-- Idempotent: safe to run multiple times
-- ============================================================

CREATE DATABASE IF NOT EXISTS mes_production_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE mes_production_db;

-- 1. Machine Master
CREATE TABLE IF NOT EXISTS machine_master (
  machine_id            INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  machine_name          VARCHAR(100) NOT NULL,
  machine_code          VARCHAR(30)  NOT NULL UNIQUE,
  machine_location      VARCHAR(100) NULL,
  is_active             TINYINT(1)   NOT NULL DEFAULT 1,
  ideal_cycle_time_sec  DECIMAL(8,3) NOT NULL DEFAULT 5.000 -- D4 addition for Performance KPI
) ENGINE=InnoDB;

-- 2. Shift Master
CREATE TABLE IF NOT EXISTS shift_master (
  shift_id    INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  shift_name  VARCHAR(30) NOT NULL UNIQUE,
  start_time  TIME NOT NULL,
  end_time    TIME NOT NULL -- end < start indicates midnight crossing
) ENGINE=InnoDB;

-- 3. Production Target
CREATE TABLE IF NOT EXISTS production_target (
  target_id        BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  machine_id       INT UNSIGNED NOT NULL,
  production_date  DATE NOT NULL,
  shift_name       VARCHAR(30) NOT NULL,
  target_quantity  INT UNSIGNED NOT NULL,
  UNIQUE KEY uq_target (machine_id, production_date, shift_name),
  CONSTRAINT fk_target_machine FOREIGN KEY (machine_id) REFERENCES machine_master(machine_id)
) ENGINE=InnoDB;

-- 4. Production Log
CREATE TABLE IF NOT EXISTS production_log (
  log_id        BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  machine_id    INT UNSIGNED NOT NULL,
  total_count   INT UNSIGNED NOT NULL,
  good_count    INT UNSIGNED NOT NULL,
  reject_count  INT UNSIGNED NOT NULL,
  cycle_time    DECIMAL(8,3) NULL,
  temperature   DECIMAL(6,2) NULL,
  recorded_at   DATETIME(3) NOT NULL,                               -- UTC (D5)
  data_quality  VARCHAR(10) NOT NULL DEFAULT 'GOOD',                -- D4 addition
  is_consistent TINYINT(1) AS (good_count + reject_count = total_count) STORED, -- D4 addition
  KEY ix_prod_machine_time (machine_id, recorded_at),
  CONSTRAINT fk_prod_machine FOREIGN KEY (machine_id) REFERENCES machine_master(machine_id)
) ENGINE=InnoDB;

-- 5. Machine Status Log
CREATE TABLE IF NOT EXISTS machine_status_log (
  status_id       BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  machine_id      INT UNSIGNED NOT NULL,
  machine_status  TINYINT NOT NULL,                                 -- -1 COMM_LOSS, 0 STOP, 1 RUN, 2 IDLE
  start_time      DATETIME(3) NOT NULL,                             -- UTC
  end_time        DATETIME(3) NULL,                                 -- NULL = interval still open
  KEY ix_status_machine_start (machine_id, start_time),
  KEY ix_status_machine_end   (machine_id, end_time),
  CONSTRAINT fk_status_machine FOREIGN KEY (machine_id) REFERENCES machine_master(machine_id)
) ENGINE=InnoDB;
