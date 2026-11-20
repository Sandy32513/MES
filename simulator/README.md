# MES OPC UA Simulator

## Overview
A purpose-built Python `asyncua` OPC UA server designed according to Decision **D2** of the MES architecture. It provides an endpoint and tags matching the technical specifications.

## Endpoint & Namespace
- **Endpoint URL:** `opc.tcp://127.0.0.1:4840/mes/simulator`
- **Security Policy:** None (NoSecurity)
- **Namespace URI:** `http://mes.local/simulator` (Namespace Index 2)
- **Object Path:** `Objects/MES/Machine01`

## Tags

| Tag Name | OPC UA Type | NodeId | Description |
|---|---|---|---|
| `Machine_Status` | Int32 | `ns=2;s=Machine01.Machine_Status` | 0=STOP, 1=RUN, 2=IDLE, -1=COMM_LOSS |
| `Total_Count` | Int32 | `ns=2;s=Machine01.Total_Count` | Cumulative total production count |
| `Good_Count` | Int32 | `ns=2;s=Machine01.Good_Count` | Cumulative accepted units |
| `Reject_Count` | Int32 | `ns=2;s=Machine01.Reject_Count` | Cumulative rejected units |
| `Cycle_Time` | Float | `ns=2;s=Machine01.Cycle_Time` | Cycle time in seconds (~4.5–5.5s) |
| `Temperature` | Float | `ns=2;s=Machine01.Temperature` | Machine temperature in °C |
| `Target_Count` | Int32 | `ns=2;s=Machine01.Target_Count` | Planned shift quantity (default 4800) |

## Invariant
`Good_Count + Reject_Count == Total_Count` is strictly enforced on every cycle.

## Usage
```powershell
# Normal operation (1x real-time)
python simulator/mes_simulator.py --scenario normal

# 10x accelerated simulation (for fast soak and validation tests)
python simulator/mes_simulator.py --scenario normal --time-scale 10

# Golden KPI scenario (40m RUN, 10m IDLE, 10m STOP)
python simulator/mes_simulator.py --scenario kpi_golden

# With fault injection control file
python simulator/mes_simulator.py --control-file simulator/control.json
```

## Fault Injection
Write a JSON command to `control.json`:
```json
{
  "force_status": 0,
  "reset_counters": true
}
```
The simulator will apply the override immediately and clear the file.
