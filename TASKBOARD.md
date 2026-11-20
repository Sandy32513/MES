# TASKBOARD — MES Real-Time Production Monitoring System

> Updated by A0 at the end of each phase.

## Phase 0 — Bootstrap ✅ COMPLETE (2026-11-20)

- [x] Read PRD and TRD source documents
- [x] Create repo skeleton (`mes-project/`)
- [x] Copy source docs to `docs/source/`
- [x] Create `.gitignore`, `.env.example`
- [x] Create `docs/DECISIONS.md` (seeded with D1–D13)
- [x] Create `docs/TRACEABILITY.md`
- [x] Initialize `TASKBOARD.md`
- [x] Git init and initial commit

**A0 Status (Phase 0):** Repository skeleton is in place. All 13 pre-made decisions seeded. Traceability matrix initialised. Source docs copied. Git repo initialised with `.gitignore` protecting secrets. Proceeding to spawn A1 (Environment & Acquisition) for Phase 1 in parallel with seeding A2/A3 for Phase 2.

---

## Phase 1 — Environment (A1) 🔄 IN PROGRESS

| Task | Owner | Status |
|---|---|---|
| Preflight check (RAM, disk, OS) | A1 | 🔄 |
| Install MySQL Community Server | A1 | 🔄 |
| Install DBeaver Community | A1 | 🔄 |
| Install Ignition (Maker) | A1 | 🔄 |
| Install Grafana OSS | A1 | 🔄 |
| Install Python 3 + asyncua | A1 | 🔄 |
| Install Playwright | A1 | 🔄 |
| Create DB users (mes_admin, ignition_writer, grafana_reader) | A1 | 🔄 |
| Smoke tests per product | A1 | 🔄 |

---

## Phase 2 — Data ∥ Source (A2 ∥ A3) ⬜ Queued

| Task | Owner | Status |
|---|---|---|
| SQL schema (01_schema.sql) | A2 | ⬜ |
| Seed data (02_seed.sql) | A2 | ⬜ |
| DB users SQL (03_users.sql) | A2 | ⬜ |
| Reporting views (04_views.sql) | A2 | ⬜ |
| Teardown script (99_teardown.sql) | A2 | ⬜ |
| Golden test fixture | A2 | ⬜ |
| OPC UA simulator (Python asyncua) | A3 | ⬜ |
| Simulator scenarios + fault injection | A3 | ⬜ |
| OPC UA tag validation client | A3 | ⬜ |

---

## Phase 3 — Pipeline (A4) ⬜ Queued

| Task | Owner | Status |
|---|---|---|
| Ignition OPC UA connection (MES_SIM) | A4 | ⬜ |
| Tag provider + 7 OPC tags + Comm_OK + LogIntervalSec | A4 | ⬜ |
| DB connection (MES_DB, ignition_writer) | A4 | ⬜ |
| Status logger (Tag Change script) | A4 | ⬜ |
| Production logger (Timer script, D13) | A4 | ⬜ |
| Startup recovery script | A4 | ⬜ |
| Failure handling (retry queue) | A4 | ⬜ |
| 15-min logging verification | A4 | ⬜ |

---

## Phase 4 — HMI ∥ Grafana (A5 ∥ A6) ⬜ Queued

| Task | Owner | Status |
|---|---|---|
| Screen 1: Main Production Dashboard | A5 | ⬜ |
| Screen 2: Machine Monitoring | A5 | ⬜ |
| Screen 3: Production History | A5 | ⬜ |
| Screenshots (all 4 states) | A5 | ⬜ |
| Grafana datasource provisioning | A6 | ⬜ |
| Dashboard D1: Production Overview | A6 | ⬜ |
| Dashboard D2: Machine Monitoring | A6 | ⬜ |
| Dashboard D3: Production Analytics | A6 | ⬜ |
| Dashboard screenshots | A6 | ⬜ |

---

## Phase 5 — Verify (A7) ⬜ Queued

| Task | Owner | Status |
|---|---|---|
| KPI oracle (Python, independent) | A7 | ⬜ |
| All test cases TC-OPC-01..TC-SOAK-01 | A7 | ⬜ |
| TEST_REPORT.md | A7 | ⬜ |

---

## Phase 6 — Release (A8 + A0) ⬜ Queued

| Task | Owner | Status |
|---|---|---|
| Architecture diagram (Mermaid) | A8 | ⬜ |
| README.md | A8 | ⬜ |
| RUNBOOK.md | A8 | ⬜ |
| run_all.ps1 / stop_all.ps1 | A8 | ⬜ |
| Clean-room verification | A8 | ⬜ |
| FINAL_REPORT.md | A0 | ⬜ |
