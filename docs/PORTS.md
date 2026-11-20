# Port Allocations — MES Real-Time Production Monitoring System

| Service | Port | Protocol | Bound to | Status | Service/Process |
|---|---|---|---|---|---|
| **MySQL Server** | 3306 | TCP | `127.0.0.1` / `::` | Active (Listening) | Windows Service `MySQL80` (PID 8032) |
| **OPC UA Simulator** | 4840 | TCP (OPC UA binary) | `127.0.0.1` | Configured / Ready | Python `asyncua` server (`simulator/mes_simulator.py`) |
| **Grafana OSS** | 3000 | HTTP | `127.0.0.1` | Configured / Ready | `D:\MES\grafana\bin\grafana-server.exe` |
| **Ignition Gateway** | 8088 | HTTP | `127.0.0.1` | Staged (Manual commissioning) | Standard Ignition Gateway default port |
| **Ignition HTTPS** | 8043 | HTTPS | `127.0.0.1` | Staged (Manual commissioning) | Standard Ignition Gateway SSL port |

*All ports conform to Decision D12. If any port conflicts occur, document the new port and update this file.*
