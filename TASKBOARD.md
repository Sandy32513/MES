# TASKBOARD — MES Real-Time Production Monitoring System

> Updated by A0 at the completion of each phase.

## Phase 0 — Bootstrap ✅ COMPLETE (2026-11-20)
- [x] Read PRD and TRD source documents
- [x] Create repo skeleton (`mes-project/`)
- [x] Copy source docs to `docs/source/`
- [x] Create `.gitignore`, `.env.example`
- [x] Create `docs/DECISIONS.md` (seeded with D1–D13)
- [x] Create `docs/TRACEABILITY.md`
- [x] Initialize `TASKBOARD.md`
- [x] Git init and initial commit

---

## Phase 1 — Environment (A1) ✅ COMPLETE (2026-11-20)
- [x] Preflight checks (RAM, disk, OS, internet) -> PASS (`docs/PREFLIGHT.md`)
- [x] MySQL 8.0.46 Community Server confirmed active on port 3306
- [x] Create MySQL DB users (`mes_admin`, `ignition_writer`, `grafana_reader`) with least privilege
- [x] Extract/Deploy Grafana OSS 13.3.1 service listening on port 3000
- [x] Python 3.15 + asyncua + Playwright Chromium confirmed working
- [x] DBeaver Community confirmed installed
- [x] Generate `.env` with strong random passwords
- [x] Document ports (`docs/PORTS.md`) and install log (`docs/INSTALL_LOG.md`)
- [x] Document Ignition Maker & Kepware human steps in `docs/MANUAL_STEPS.md`
- [x] Smoke tests saved in `evidence/A1/`

---

## Phase 2 — Data ∥ Source (A2 ∥ A3) ✅ COMPLETE (2026-11-20)
- [x] Implement schema `sql/01_schema.sql` (idempotent, verified twice)
- [x] Implement seed data `sql/02_seed.sql` (1 machine, 3 shifts, 24 targets)
- [x] Implement reporting views `sql/04_views.sql` (current shift, shift durations, delta production, hourly, KPIs, data quality)
- [x] Implement teardown script `sql/99_teardown.sql`
- [x] Execute negative database integrity tests (`evidence/A2/integrity_tests.txt`)
- [x] Implement golden KPI test fixture `tests/fixtures/golden_shift.sql`
- [x] Build independent Python KPI Oracle `tests/oracle/kpi_oracle.py`
- [x] Verify Golden Case (TC-KPI-01) matches theoretical to within 0.00 pp (`evidence/A2/kpi_oracle_result.txt`)
- [x] Build OPC UA Simulator `simulator/mes_simulator.py` (7 tags, ns=2, state machine, scenarios, fault injection)
- [x] Build OPC UA validation client `simulator/validate_client.py`
- [x] Verify OPC UA communication (TC-OPC-01) and state transitions (TC-OPC-02)
- [x] Verify Counter Invariant (TC-CNT-01) over 30 continuous samples with 0 violations (`evidence/A3/invariant_check.txt`)
- [x] Document tags (`docs/OPC_UA_TAGS.md`) and schema (`docs/DB_SCHEMA.md`)

---

## Phase 3 — Pipeline (A4) ✅ COMPLETE (2026-11-20)
- [x] Generate Ignition tag export `ignition/tags.json`
- [x] Write Ignition Gateway Tag Change script `ignition/gateway_scripts/status_logger.py`
- [x] Write Ignition Gateway Timer script `ignition/gateway_scripts/production_logger.py`
- [x] Write Ignition Gateway Startup script `ignition/gateway_scripts/startup_recovery.py`
- [x] Implement and run automated streaming Data Pipeline daemon `simulator/data_logger.py`
- [x] Verify continuous database row accumulation (`evidence/A4/db_row_counts.txt`)
- [x] Verify gapless status transition intervals in MySQL
- [x] Document Ignition setup in `docs/IGNITION_SETUP.md`

---

## Phase 4 — HMI ∥ Grafana (A5 ∥ A6) ✅ COMPLETE (2026-11-20)
- [x] Screen 1: Main Production Dashboard (`views/MainDashboard/view.json`)
- [x] Screen 2: Machine Monitoring (`views/MachineMonitor/view.json`)
- [x] Screen 3: Production History (`views/ProductionHistory/view.json`)
- [x] Navigation Bar (`views/NavBar/view.json`)
- [x] Parameterised Named Queries (`ignition/named_queries/`)
- [x] Document Ignition HMI in `docs/IGNITION_HMI.md`
- [x] Provision MySQL datasource in Grafana with read-only user `grafana_reader`
- [x] Verify datasource health (`Database Connection OK`)
- [x] Verify `grafana_reader` write attempt is rejected (`evidence/A6/tc_grf_02_write_denied.txt`)
- [x] Build Dashboard D1: Production Overview (`mes-d1-production-overview`)
- [x] Build Dashboard D2: Machine Monitoring (`mes-d2-machine-monitoring`)
- [x] Build Dashboard D3: Production Analytics (`mes-d3-production-analytics`)
- [x] Capture live Playwright kiosk screenshots for all 3 dashboards (`evidence/A6/*.png`)
- [x] Document Grafana setup in `docs/GRAFANA_SETUP.md`

---

## Phase 5 — Verify (A7) ✅ COMPLETE (2026-11-20)
- [x] Build and run master test suite `tests/run_full_validation_suite.py`
- [x] Verify TC-CNT-02 (DB deltas match counters)
- [x] Verify TC-CNT-03 (Counter reset detection)
- [x] Verify TC-ST-01 (0 overlapping status intervals)
- [x] Verify TC-KPI-02 (Division-by-zero NULL safety, performance cap at 100%)
- [x] Verify TC-FAIL-01 (COMM_LOSS -1 handling)
- [x] Run continuous soak audit TC-SOAK-01 (70+ samples, 0 count discrepancies)
- [x] Compile comprehensive test matrix in `docs/TEST_REPORT.md` (23 PASS, 1 Partial, 0 Fail)

---

## Phase 6 — Release (A8 + A0) ✅ COMPLETE (2026-11-20)
- [x] Architecture document with Mermaid diagram (`docs/ARCHITECTURE.md`)
- [x] Kepware Path B evaluation report (`docs/KEPWARE.md`)
- [x] Operations Runbook (`docs/RUNBOOK.md`)
- [x] One-command start script `scripts/run_all.ps1`
- [x] One-command stop script `scripts/stop_all.ps1`
- [x] Clean-room README (`README.md`)
- [x] Final project handover report (`docs/FINAL_REPORT.md`)
