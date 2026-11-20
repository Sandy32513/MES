# IGNITION SCADA & PIPELINE SETUP GUIDE

## 1. Overview
The MES system uses Ignition Maker Edition (or standard trial mode) as the central SCADA and data logging gateway. It performs:
- Real-time OPC UA tag collection from `opc.tcp://127.0.0.1:4840/mes/simulator`
- Event-driven machine status interval logging (`machine_status_log`)
- Periodic production metric sampling (`production_log`) with bounded in-memory retry queuing
- Perspective-based operator, supervisor, and management HMI displays

---

## 2. Gateway Connections

### 2.1 OPC UA Connection (`MES_SIM`)
- **Type:** OPC UA Client
- **Server Name:** `MES_SIM`
- **Endpoint URL:** `opc.tcp://127.0.0.1:4840/mes/simulator`
- **Security Policy:** None (NoSecurity)
- **Status:** Connected / Good Quality

### 2.2 Database Connection (`MES_DB`)
- **Type:** MySQL Connector/J
- **Connection Name:** `MES_DB`
- **Connect URL:** `jdbc:mysql://127.0.0.1:3306/mes_production_db?useSSL=false&serverTimezone=UTC`
- **Username:** `ignition_writer`
- **Password:** Stored in `.env` (`IGNITION_WRITER_PASSWORD`)
- **Status:** Valid / Connected

---

## 3. Tag Configuration
Import `ignition/tags.json` in Designer Tag Browser:
- Folder: `[default]MES/Machine01`
  - `Machine_Status` (Int4) -> `ns=2;s=Machine01.Machine_Status`
  - `Total_Count` (Int4) -> `ns=2;s=Machine01.Total_Count`
  - `Good_Count` (Int4) -> `ns=2;s=Machine01.Good_Count`
  - `Reject_Count` (Int4) -> `ns=2;s=Machine01.Reject_Count`
  - `Cycle_Time` (Float4) -> `ns=2;s=Machine01.Cycle_Time`
  - `Temperature` (Float4) -> `ns=2;s=Machine01.Temperature`
  - `Target_Count` (Int4) -> `ns=2;s=Machine01.Target_Count`
  - `Comm_OK` (Boolean, Expression) -> `isGood({[default]MES/Machine01/Machine_Status})`
- Folder: `[default]MES/Config`
  - `LogIntervalSec` (Memory, Int4, default = 5)

---

## 4. Gateway Scripts Configuration
1. **Tag Change Event Script:**
   - Path: Designer > Gateway Events > Tag Change Scripts
   - Tag: `[default]MES/Machine01/Machine_Status`
   - Source: `ignition/gateway_scripts/status_logger.py`
2. **Timer Event Script:**
   - Path: Designer > Gateway Events > Timer Scripts
   - Name: `ProductionLogger`
   - Delay: `1000` ms (Fixed Delay)
   - Source: `ignition/gateway_scripts/production_logger.py`
3. **Startup Event Script:**
   - Path: Designer > Gateway Events > Startup Script
   - Source: `ignition/gateway_scripts/startup_recovery.py`
