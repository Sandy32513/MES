# OPC UA TAG SPECIFICATION — MES Real-Time Production Monitoring System

| Tag Name | OPC UA Data Type | Node Identifier | Read/Write | Engineering Units | Expected Range | Description |
|---|---|---|---|---|---|---|
| `Machine_Status` | `Int32` | `ns=2;s=Machine01.Machine_Status` | Read / Write | Enumeration | `0, 1, 2, -1` | `0` = STOP (Red), `1` = RUN (Green), `2` = IDLE (Amber), `-1` = COMM_LOSS (Grey) |
| `Total_Count` | `Int32` | `ns=2;s=Machine01.Total_Count` | Read / Write | Pieces | `0 .. 2,147,483,647` | Cumulative total production counter |
| `Good_Count` | `Int32` | `ns=2;s=Machine01.Good_Count` | Read / Write | Pieces | `0 .. 2,147,483,647` | Cumulative accepted/passed units |
| `Reject_Count` | `Int32` | `ns=2;s=Machine01.Reject_Count` | Read / Write | Pieces | `0 .. 2,147,483,647` | Cumulative rejected/scrapped units |
| `Cycle_Time` | `Float` | `ns=2;s=Machine01.Cycle_Time` | Read / Write | Seconds | `4.500 .. 5.500` | Duration required to complete the latest unit |
| `Temperature` | `Float` | `ns=2;s=Machine01.Temperature` | Read / Write | °C | `20.0 .. 95.0` | Operating temperature of the machine |
| `Target_Count` | `Int32` | `ns=2;s=Machine01.Target_Count` | Read / Write | Pieces | `0 .. 100,000` | Target production quantity for the active shift (Default: 4800) |

## Mathematical Invariants
1. **Count Consistency:**
   $$\text{Total\_Count} = \text{Good\_Count} + \text{Reject\_Count}$$
   Violations indicate data corruption or missing packets and are recorded in `v_data_quality_issues`.

2. **Quality Ratio:**
   $$\text{Quality \%} = \frac{\text{Good\_Count}}{\text{Total\_Count}} \times 100$$
