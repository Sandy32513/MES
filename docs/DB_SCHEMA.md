# DATABASE SCHEMA SPECIFICATION — `mes_production_db`

The database design implements the five core tables specified in TRD §6, plus additive-only columns and views required by Decision **D4** (ideal cycle time, data quality flag, consistent count virtual column, COMM_LOSS status -1, and unique targets).

## Entity-Relationship Diagram

```mermaid
erDiagram
    machine_master ||--o{ production_target : "plans"
    machine_master ||--o{ production_log : "records"
    machine_master ||--o{ machine_status_log : "logs"
    shift_master ||--o{ production_target : "schedules"

    machine_master {
        int machine_id PK "AUTO_INCREMENT"
        varchar machine_name "Machine Display Name"
        varchar machine_code UK "Unique Identifier (e.g. MC-001)"
        varchar machine_location "Shopfloor Area"
        tinyint is_active "1=Active, 0=Inactive"
        decimal ideal_cycle_time_sec "Required for OEE Performance (D4)"
    }

    shift_master {
        int shift_id PK "AUTO_INCREMENT"
        varchar shift_name UK "Shift A, Shift B, Shift C"
        time start_time "Start time"
        time end_time "End time (crosses midnight if end < start)"
    }

    production_target {
        bigint target_id PK "AUTO_INCREMENT"
        int machine_id FK "References machine_master"
        date production_date "Planned Production Date"
        varchar shift_name "Shift identifier"
        int target_quantity "Target pieces"
    }

    production_log {
        bigint log_id PK "AUTO_INCREMENT"
        int machine_id FK "References machine_master"
        int total_count "Cumulative total counter"
        int good_count "Cumulative good counter"
        int reject_count "Cumulative reject counter"
        decimal cycle_time "Cycle time in seconds"
        decimal temperature "Temperature in deg C"
        datetime recorded_at "UTC timestamp (D5)"
        varchar data_quality "GOOD, BAD, COMM_LOSS"
        tinyint is_consistent "VIRTUAL: good+reject == total"
    }

    machine_status_log {
        bigint status_id PK "AUTO_INCREMENT"
        int machine_id FK "References machine_master"
        tinyint machine_status "0=STOP, 1=RUN, 2=IDLE, -1=COMM_LOSS"
        datetime start_time "Interval start (UTC)"
        datetime end_time "Interval end (NULL if open)"
    }
```

## Reporting Views

| View Name | Primary Function |
|---|---|
| `v_current_shift` | Determines the active shift for any timestamp considering plant timezone (`+05:30`) and midnight-crossing shifts. |
| `v_status_durations_by_shift` | Aggregates duration in seconds spent in RUN, STOP, IDLE, and COMM_LOSS per shift. |
| `v_production_by_shift` | Computes delta production quantities per shift using window functions (`LAG()`) with reset detection (D6). |
| `v_hourly_production` | Groups delta production into hourly buckets for time-series trend analysis. |
| `v_kpi_by_shift` | Calculates Availability, Performance, Quality, OEE, and Production Achievement with division-by-zero protection. |
| `v_data_quality_issues` | Surfaces inconsistent counter rows (`good + reject != total`) and overlapping intervals. |
