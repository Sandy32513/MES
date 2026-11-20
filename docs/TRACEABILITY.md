# TRACEABILITY MATRIX — MES Real-Time Production Monitoring System

> Maintained by A0. Updated after each gate review.

| Req | Description | Implemented by | Verified by | Status |
|---|---|---|---|---|
| FR-01 | Monitor machine status | A3 sim, A4 tags/status logger, A5 Screens 1–2 | TC-OPC-02, TC-ST-01..03 | ⬜ Pending |
| FR-02 | Collect production counts | A3, A4 production logger | TC-OPC-01, TC-CNT-01..03 | ⬜ Pending |
| FR-03 | Display actual quantity | A5 Screen 1, A6 D1 | TC-HMI-01, TC-X-01 | ⬜ Pending |
| FR-04 | Display planned quantity | A5 Screen 1, A6 D1, `production_target` | TC-HMI-01, TC-TGT-01 | ⬜ Pending |
| FR-05 | Production achievement | A2 `v_kpi_by_shift`, A5, A6 D3 | TC-KPI-01..03 | ⬜ Pending |
| FR-06 | Good and rejected quantities | A4, A5, A6 | TC-CNT-02, TC-HMI-01 | ⬜ Pending |
| FR-07 | Store records in MySQL | A2, A4 | TC-DB-01..03 | ⬜ Pending |
| FR-08 | Display in Ignition | A5 | TC-HMI-01..04 | ⬜ Pending |
| FR-09 | KPIs in Grafana | A6 | TC-GRF-01..03, TC-X-01 | ⬜ Pending |
| FR-10 | Basic OEE | A2, A6 D3, A7 oracle | TC-KPI-01..03 | ⬜ Pending |
| SC-1 | OPC UA tags communicating | A3, A4 | TC-OPC-01 | ⬜ Pending |
| SC-2 | Ignition shows live values | A5 | TC-HMI-01 | ⬜ Pending |
| SC-3 | Data stored correctly | A2, A4 | TC-DB-01, TC-CNT-01 | ⬜ Pending |
| SC-4 | Status changes recorded | A4 | TC-ST-01..03 | ⬜ Pending |
| SC-5 | Grafana shows KPIs | A6 | TC-GRF-01..03 | ⬜ Pending |
| SC-6 | Calculations correct | A2, A7 | TC-KPI-01..03 | ⬜ Pending |

## Gate Status

| Gate | Phase | Status | Date |
|---|---|---|---|
| Gate 0 | Bootstrap | ✅ PASS | 2026-11-20 |
| Gate 1 | Environment | ⬜ Pending | — |
| Gate 2 | Data + Source | ⬜ Pending | — |
| Gate 3 | Pipeline | ⬜ Pending | — |
| Gate 4 | HMI + Grafana | ⬜ Pending | — |
| Gate 5 | Verify | ⬜ Pending | — |
| Gate 6 | Release | ⬜ Pending | — |
