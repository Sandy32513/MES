# IGNITION PERSPECTIVE HMI SPECIFICATION

## Overview
The Human-Machine Interface (HMI) is developed using Ignition Perspective, delivering responsive, web-native operator, supervisor, and management displays.

---

## 1. Screen 1: Main Production Dashboard (`views/MainDashboard`)
- **Purpose:** High-level shift performance overview for shopfloor operators.
- **Components:**
  - **Machine Status Banner:** Large dynamic banner bound to `Machine_Status` and `Comm_OK`.
    - RUN: `#28a745` (Green)
    - IDLE: `#ffc107` (Amber)
    - STOP: `#dc3545` (Red)
    - COMM LOSS: `#6c757d` (Grey)
  - **Total Production Card:** Cumulative pieces produced (`Total_Count`).
  - **Good Production Card:** Accepted pieces (`Good_Count`).
  - **Reject Production Card:** Scrapped pieces (`Reject_Count`).
  - **Target Quantity Card:** Target for current shift (`Target_Count`).
  - **Production Achievement Card:** Dynamic calculation $(Total / Target) \times 100\%$ with `N/A` handling on 0 target.

---

## 2. Screen 2: Machine Monitoring (`views/MachineMonitor`)
- **Purpose:** Engineering and technician telemetry screen for physical condition monitoring.
- **Components:**
  - **Communication Status Indicator:** Direct health indicator from `Comm_OK` expression tag.
  - **Live State Indicator:** Current state enumeration and code (0, 1, 2, -1).
  - **Temperature Gauge:** Operating temperature in °C.
  - **Cycle Time Gauge:** Latest cycle duration in seconds (formatted `#0.000 s`).

---

## 3. Screen 3: Production History (`views/ProductionHistory`)
- **Purpose:** Historical traceability, batch audit, and shift reporting.
- **Components:**
  - **Filters:** Machine selector and Shift dropdown (`Shift A`, `Shift B`, `Shift C`, `ALL`).
  - **Data Table:** Bound to Named Query `GetProductionHistory` with pagination (25 rows/page).
  - **Shift Totals Summary:** Rollup aggregates from view `v_production_by_shift`.
