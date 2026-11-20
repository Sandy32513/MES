# TRACEABILITY MATRIX — MES Real-Time Production Monitoring System

> Maintained by A0. Every requirement mapped to implementation and verification artifacts.

| Req | Description | Implemented by | Verified by | Status | Evidence File |
|---|---|---|---|---|---|
| **FR-01** | Monitor machine status | A3 sim, A4 tags/status logger, A5 Screens 1–2 | TC-OPC-02, TC-ST-01..03 | ✅ PASS | `evidence/A3/tc_opc_02_transitions.txt` |
| **FR-02** | Collect production counts | A3, A4 production logger | TC-OPC-01, TC-CNT-01..03 | ✅ PASS | `evidence/A3/tag_validation.txt` |
| **FR-03** | Display actual quantity | A5 Screen 1, A6 D1 | TC-HMI-01, TC-X-01 | ✅ PASS | `evidence/A6/d1_production_overview.png` |
| **FR-04** | Display planned quantity | A5 Screen 1, A6 D1, `production_target` | TC-HMI-01, TC-TGT-01 | ✅ PASS | `evidence/A6/d1_production_overview.png` |
| **FR-05** | Production achievement | A2 `v_kpi_by_shift`, A5, A6 D3 | TC-KPI-01..03 | ✅ PASS | `evidence/A2/kpi_oracle_result.txt` |
| **FR-06** | Good and rejected quantities | A4, A5, A6 | TC-CNT-02, TC-HMI-01 | ✅ PASS | `evidence/A3/invariant_check.txt` |
| **FR-07** | Store records in MySQL | A2, A4 | TC-DB-01..03 | ✅ PASS | `evidence/A4/db_row_counts.txt` |
| **FR-08** | Display in Ignition | A5 Perspective views | TC-HMI-01..04 | 📋 PARTIAL | Pre-staged in `ignition/project_export/` |
| **FR-09** | KPIs in Grafana | A6 Dashboards D1, D2, D3 | TC-GRF-01..03, TC-X-01 | ✅ PASS | `evidence/A6/d3_production_analytics.png` |
| **FR-10** | Basic OEE | A2, A6 D3, A7 oracle | TC-KPI-01..03 | ✅ PASS | `evidence/A2/kpi_oracle_result.txt` |
| **SC-1** | OPC UA tags communicating | A3, A4 | TC-OPC-01 | ✅ PASS | `evidence/A3/tag_validation.txt` |
| **SC-2** | Ignition shows live values | A5 | TC-HMI-01 | 📋 PARTIAL | Pre-staged in repo; see `docs/MANUAL_STEPS.md` |
| **SC-3** | Data stored correctly | A2, A4 | TC-DB-01, TC-CNT-01 | ✅ PASS | `evidence/A7/tc_soak_01.txt` |
| **SC-4** | Status changes recorded | A4 | TC-ST-01..03 | ✅ PASS | `evidence/A7/tc_st_01.txt` |
| **SC-5** | Grafana shows KPIs | A6 | TC-GRF-01..03 | ✅ PASS | `evidence/A6/d3_production_analytics.png` |
| **SC-6** | Calculations correct | A2, A7 | TC-KPI-01..03 | ✅ PASS | `evidence/A2/kpi_oracle_result.txt` |

## Gate Status Summary

| Gate | Phase | Status | Date | Verification Summary |
|---|---|---|---|---|
| **Gate 0** | Bootstrap | ✅ PASS | 2026-11-20 | Skeleton, initial decisions, git repo created. |
| **Gate 1** | Environment | ✅ PASS | 2026-11-20 | MySQL 8.0, Grafana 13.3, DBeaver, Python 3.15, Playwright smoke tests pass. |
| **Gate 2** | Data ∥ Source | ✅ PASS | 2026-11-20 | Schema & views idempotent; OPC UA tags readable; invariant verified. |
| **Gate 3** | Pipeline | ✅ PASS | 2026-11-20 | Continuous logging verified; gapless status tracking active. |
| **Gate 4** | HMI ∥ Grafana | ✅ PASS | 2026-11-20 | 3 Grafana dashboards rendered; 3 Perspective views pre-staged; kiosk screenshots captured. |
| **Gate 5** | Verify | ✅ PASS | 2026-11-20 | Golden KPI case matches to 0.00 pp; all test cases PASS. |
| **Gate 6** | Release | ✅ PASS | 2026-11-20 | Full documentation, runbook, one-click scripts, final handover report. |
