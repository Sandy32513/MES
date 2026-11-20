# Real-Time Production Monitoring System (MES)
### Simulator → (Kepware) → Ignition → MySQL → Grafana

An end-to-end Manufacturing Execution System (MES) application built for real-time machine production monitoring, downtime tracking, Overall Equipment Effectiveness (OEE) analytics, and shopfloor dashboards.

---

## 1. Quick Start
From a PowerShell terminal at `D:\MES\mes-project\`:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_all.ps1
```
Open your browser:
- **Grafana Production Dashboards:** `http://localhost:3000` (User: `admin` / Password: `admin`)
- **Ignition Gateway (when commissioned):** `http://localhost:8088`

To stop background daemons:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\stop_all.ps1
```

---

## 2. Technology Stack & Ports

| Technology | Purpose | Default Port | Bound Interface |
|---|---|---|---|
| **Python asyncua** | OPC UA Machine Simulator | `4840` | `127.0.0.1` |
| **Data Pipeline Logger** | Continuous SCADA & Status Logger | N/A | `127.0.0.1` |
| **MySQL Community Server** | Production Relational Storage | `3306` | `127.0.0.1` |
| **Grafana OSS 13.3** | Live Production & OEE Dashboards | `3000` | `127.0.0.1` |
| **Ignition Maker Edition** | SCADA Gateway & Perspective HMI | `8088` / `8043` | `127.0.0.1` |
| **DBeaver Community** | Database Administration | N/A | Local |

---

## 3. Directory Layout
```
mes-project/
├─ README.md                    # Project overview & quick start
├─ TASKBOARD.md                 # Gate & milestone tracking
├─ .env.example                 # Secrets template (.env is git-ignored)
├─ docs/
│  ├─ source/                   # PRD.md & TRD.md source specifications
│  ├─ DECISIONS.md              # Architectural decisions (D1–D13)
│  ├─ PREFLIGHT.md              # System preflight verification report
│  ├─ INSTALL_LOG.md            # Software installation audit log
│  ├─ PORTS.md                  # Port bindings and allocations
│  ├─ MANUAL_STEPS.md           # Human-only commissioning steps (Ignition Maker)
│  ├─ ARCHITECTURE.md           # Architecture diagram (Mermaid) & component specs
│  ├─ DB_SCHEMA.md              # ER diagram (Mermaid) & schema definitions
│  ├─ OPC_UA_TAGS.md            # The 7 OPC UA tags specification
│  ├─ KEPWARE.md                # Kepware evaluation & Path B report
│  ├─ IGNITION_SETUP.md         # SCADA gateway configuration guide
│  ├─ IGNITION_HMI.md           # Perspective HMI screens specification
│  ├─ GRAFANA_SETUP.md          # Grafana provisioning & dashboard guide
│  ├─ TRACEABILITY.md           # Requirements traceability matrix (FR-01..10, SC-1..6)
│  ├─ TEST_REPORT.md            # Comprehensive test matrix & evidence
│  ├─ RUNBOOK.md                # Start, stop, backup, restore, troubleshooting
│  └─ FINAL_REPORT.md           # Master executive report & handover
├─ scripts/                     # 00_preflight, 01_install_stack, run_all, stop_all
├─ simulator/                   # mes_simulator.py, validate_client.py, data_logger.py
├─ sql/                         # 01_schema.sql, 02_seed.sql, 03_users.sql, 04_views.sql, 99_teardown.sql
├─ ignition/                    # tags.json, gateway_scripts/, named_queries/, project_export/
├─ grafana/                     # provisioning/ (datasources, dashboards), dashboards/ (D1, D2, D3)
├─ tests/                       # fixtures/, oracle/ (kpi_oracle.py), test runners
├─ evidence/                    # Logs, query results, Playwright screenshots (A1–A7)
└─ handoffs/                    # Formal agent handoff notes
```

---

## 4. Key Performance Indicators (OEE) Formulas
- **Production Achievement:** $(\text{Total Production} / \text{Target Production}) \times 100\%$
- **Availability:** $(\text{RUN Operating Time} / \text{Planned Production Time}) \times 100\%$
- **Performance:** $\min(1.0, \frac{\text{Ideal Cycle Time} \times \text{Total Production}}{\text{RUN Operating Time}}) \times 100\%$ (capped at 100%)
- **Quality:** $(\text{Good Production} / \text{Total Production}) \times 100\%$
- **OEE:** $(\text{Availability}/100) \times (\text{Performance}/100) \times (\text{Quality}/100) \times 100\%$
*(Division-by-zero yields NULL/N/A, never runtime errors).*

---

## 5. Licences & Usage Notes
- Software editions installed and utilized conform to vendor trial/educational community terms.
- Ignition Maker Edition is for personal, educational, and non-commercial usage. A standard commercial license is required for live production factory deployments.
- Kepware trial operates in a 2-hour demonstration mode when deployed.
