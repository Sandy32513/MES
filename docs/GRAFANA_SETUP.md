# GRAFANA SETUP & DASHBOARD PROVISIONING GUIDE

## 1. Architecture & Security
Grafana OSS 13.3.1 connects to MySQL (`mes_production_db`) using the restricted database account `grafana_reader`.
- **Least Privilege:** `grafana_reader` possesses strictly read-only (`SELECT`) permissions. Write attempts (`INSERT`/`UPDATE`) are rejected with `ERROR 1142` (evidenced in `evidence/A6/tc_grf_02_write_denied.txt`).
- **Secret Management:** MySQL credentials are not committed. In file provisioning, environment variables or API injection are used.
- **Port:** HTTP 3000 (`http://localhost:3000`).

---

## 2. Datasource Configuration (`mes-mysql-ds`)
- **Type:** MySQL (`mysql`)
- **Host:** `127.0.0.1:3306`
- **Database:** `mes_production_db`
- **User:** `grafana_reader`
- **Timezone:** `+00:00` (UTC)
- **Status:** Health check verified: `Database Connection OK` (HTTP 200).

---

## 3. Provisioned Dashboards

| Dashboard Title | UID | File Path | Focus |
|---|---|---|---|
| **D1: Production Overview** | `mes-d1-production-overview` | `grafana/dashboards/d1_production_overview.json` | Real-time counts (Total, Good, Reject), Target vs Actual bar gauge, cumulative time-series. |
| **D2: Machine Monitoring** | `mes-d2-machine-monitoring` | `grafana/dashboards/d2_machine_monitoring.json` | State timeline (RUN, STOP, IDLE, COMM_LOSS), live temperature & cycle time gauges, temperature trend, cycle time trend. |
| **D3: Production Analytics** | `mes-d3-production-analytics` | `grafana/dashboards/d3_production_analytics.json` | Availability, Performance, Quality, Overall Equipment Effectiveness (OEE %), Production Achievement %, hourly bar chart, shift summary table. |

---

## 4. Visual Evidence
Live screenshots rendered via Chromium / Playwright:
- `evidence/A6/d1_production_overview.png`
- `evidence/A6/d2_machine_monitoring.png`
- `evidence/A6/d3_production_analytics.png`
