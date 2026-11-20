# DECISIONS LOG — MES Real-Time Production Monitoring System

> Maintained by A0 (Orchestrator). Append new entries; never edit existing IDs.

| ID | Context | Decision | Alternatives | Reason |
|---|---|---|---|---|
| **D1** | Architecture path | *Primary (critical path):* Simulator → Ignition OPC UA client, direct. *Optional Path B:* insert Kepware between them **only if** Kepware trial includes OPC UA Client driver and after Gate 3 passes. Never blocks primary path. | Kepware-first | Kepware is form-gated and trial-limited; primary path is fully free |
| **D2** | Simulator choice | Preference: (1) Python `asyncua` OPC UA server written by A3, (2) Prosys OPC UA Simulation Server, (3) Ignition built-in simulator. Endpoint `opc.tcp://127.0.0.1:4840/mes/simulator`, NodeIds `ns=2;s=Machine01.<TagName>` | Fixed binary simulator | Custom Python gives full scenario control, fault injection, `--time-scale` |
| **D3** | Data logging mechanism | Ignition Gateway Scripts (Jython): Tag Change script for status intervals, Timer script for production snapshots. Transaction Groups are allowed alternative. | Transaction Groups | Scripts give explicit control of intervals, failure handling, retry queue |
| **D4** | Schema additions | Five TRD tables plus: `machine_master.ideal_cycle_time_sec DECIMAL(8,3)`, `production_log.data_quality VARCHAR(10)`, `production_log.is_consistent` generated column, status code -1 = COMM_LOSS, indexes, UNIQUE key on `production_target`, reporting views | Minimal TRD schema | Needed for Performance KPI (ideal cycle time), data quality tracking, OEE accuracy |
| **D5** | Timestamps | All timestamps stored in UTC `DATETIME(3)`. Shift windows interpreted in configurable `PLANT_TIMEZONE`. Both Grafana and Ignition verified for correct display. | Local time | UTC is unambiguous across DST changes and midnight-crossing shifts |
| **D6** | Counter handling | `Total_Count` is cumulative. Deltas computed with reset detection (new < previous → new value = delta). `Total = Good + Reject` invariant flagged by `is_consistent`, never silently corrected. | Reset to zero each shift | Preserves raw data integrity; reset detection is robust |
| **D7** | KPI rules | Planned Production Time = shift length (complete) or elapsed (live). Operating Time = RUN only. Performance = min(1, IdealCycle×Total/RUNtime)×100. Quality = Good/Total. OEE = A×P×Q. Any /0 → NULL/N/A. | Simpler formulas | Matches TRD §9 with explicit caps and NULL safety |
| **D8** | Target source | `production_target` table is authoritative. `Target_Count` tag drives live HMI. At shift start logger upserts the row from tag if none exists; mismatch logged as warning. | Tag-only | DB is durable; tag is live; both needed |
| **D9** | DB roles | `mes_admin` (setup), `ignition_writer` (SELECT/INSERT/UPDATE on MES tables), `grafana_reader` (SELECT only). Random passwords in `.env` only. | Single shared user | Least-privilege principle |
| **D10** | HMI technology | Ignition Perspective (browser-based, Playwright-testable). Config exported to repo. | Vision | Perspective is modern, browser-native, easier to automate |
| **D11** | Grafana as code | File provisioning (YAML datasource + dashboard JSON with fixed UIDs). Version-controlled. | Manual UI | Reproducible, clean-room verifiable |
| **D12** | Default ports | MySQL 3306, Ignition HTTP 8088 / HTTPS 8043, Grafana 3000, OPC UA 4840. If taken, choose next free and update `docs/PORTS.md`. | None | Standard defaults; documented fallback |
| **D13** | Logging interval | Configurable; default 5 s. Stored in Ignition memory tag `MES/Config/LogIntervalSec`. Timer runs at 1 s, logs only when interval has elapsed. | Fixed interval | Operational flexibility without code changes |
