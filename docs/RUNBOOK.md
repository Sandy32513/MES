# OPERATIONAL RUNBOOK — MES Real-Time Production Monitoring System

This runbook provides complete operational procedures for starting, stopping, maintaining, backing up, and troubleshooting the MES application.

---

## 1. Quick Start & Stop

### Starting the System
Open PowerShell (or CMD) and run:
```powershell
powershell -ExecutionPolicy Bypass -File D:\MES\mes-project\scripts\run_all.ps1
```
This script will:
1. Ensure the MySQL service (`MySQL80`) is running.
2. Start the Grafana service (or verify port 3000 is listening).
3. Start the OPC UA Simulator daemon (`simulator/mes_simulator.py`).
4. Start the Data Pipeline Logger daemon (`simulator/data_logger.py`).
5. Run a quick verification test across all components.

### Stopping the System
```powershell
powershell -ExecutionPolicy Bypass -File D:\MES\mes-project\scripts\stop_all.ps1
```
This stops the background simulator and data logger daemons.

---

## 2. Service Access Endpoints

| Component | URL / Endpoint | Credentials |
|---|---|---|
| **Grafana Dashboards** | `http://localhost:3000` | User: `admin` / Password: `admin` |
| **Ignition Gateway** | `http://localhost:8088` | Configured during commissioning |
| **OPC UA Simulator** | `opc.tcp://127.0.0.1:4840/mes/simulator` | No security / Anonymous |
| **MySQL Database** | `127.0.0.1:3306` (`mes_production_db`) | `mes_admin`, `ignition_writer`, `grafana_reader` (see `.env`) |

---

## 3. Database Backup & Restore

### Backup
Run `mysqldump` to create a point-in-time snapshot:
```powershell
$env = Get-Content D:\MES\mes-project\.env | ConvertFrom-StringData
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -u mes_admin -h 127.0.0.1 "--password=$($env.MES_ADMIN_PASSWORD)" --routines --triggers mes_production_db > "D:\MES\mes-project\backups\mes_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"
```

### Restore
To restore from a backup file:
```powershell
$env = Get-Content D:\MES\mes-project\.env | ConvertFrom-StringData
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u mes_admin -h 127.0.0.1 "--password=$($env.MES_ADMIN_PASSWORD)" mes_production_db < "D:\MES\mes-project\backups\mes_backup_YYYYMMDD_HHMMSS.sql"
```

---

## 4. Troubleshooting Guide

### Issue 1: Grafana Shows "No Data" or Red Panel Error
1. Verify MySQL service is active: `Get-Service MySQL80`.
2. Test database connectivity using `grafana_reader`:
   ```powershell
   & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u grafana_reader -h 127.0.0.1 "--password=<pw>" mes_production_db -e "SELECT 1;"
   ```
3. In Grafana UI, go to Connections > Data Sources > `MES_MySQL` > Save & test. Ensure timezone is set to `+00:00`.

### Issue 2: Simulator Stopped or Not Updating Counters
1. Check if simulator process is running: `Get-Process python`.
2. Inspect log file: `D:\MES\mes-project\logs\sim.log`.
3. Test OPC UA connectivity using the validation client:
   ```powershell
   python D:\MES\mes-project\simulator\validate_client.py
   ```

### Issue 3: Status Intervals Showing COMM_LOSS (-1)
- This occurs when the pipeline logger cannot establish a socket connection to `opc.tcp://127.0.0.1:4840/mes/simulator`.
- Start or restart the simulator:
  ```powershell
  python D:\MES\mes-project\simulator\mes_simulator.py --scenario normal
  ```
- The logger will automatically detect communication recovery and close the `-1` interval.
