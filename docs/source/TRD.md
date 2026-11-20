# TECHNICAL REQUIREMENTS DOCUMENT (TRD)

## Project Title
Real-Time Production Monitoring System – MES

## 1. Technical Architecture

Machine Simulator → Kepware OPC UA → Ignition SCADA → MySQL Database → Grafana OSS

The OPC UA simulator generates simulated machine data. Kepware acts as the OPC UA communication layer where compatible drivers and licensing are available. Ignition reads the machine tags, handles data collection and stores production information in MySQL. Grafana reads the database and displays production dashboards.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Free OPC UA Simulator | Simulate machine data |
| Kepware | OPC UA communication |
| Ignition Maker Edition | SCADA and HMI development |
| MySQL Community Edition | Production database |
| Grafana OSS | Production dashboards |
| DBeaver Community | Database management |

## 3. Hardware Requirements
- Windows 10/11 computer.
- Minimum 8 GB RAM recommended.
- 10 GB free storage recommended.
- Internet connection for downloading software.

## 4. Software Requirements
- MySQL Community Server.
- MySQL Workbench or DBeaver.
- Ignition Maker Edition.
- Kepware trial version.
- Compatible free OPC UA simulator.
- Grafana OSS.

Note: Free educational and trial editions have licensing restrictions. Use only within their permitted terms. Kepware's simulator connection requires a compatible OPC UA client driver. If unavailable, use direct simulator-to-Ignition communication as the free fallback.

## 5. OPC UA Tag Configuration

| Tag Name | Data Type | Description |
|---|---|---|
| Machine_Status | Integer | 0=STOP, 1=RUN, 2=IDLE |
| Total_Count | Integer | Total production count |
| Good_Count | Integer | Accepted production |
| Reject_Count | Integer | Rejected production |
| Cycle_Time | Float | Machine cycle time |
| Temperature | Float | Machine temperature |
| Target_Count | Integer | Planned production quantity |

## 6. Database Design

Database Name: mes_production_db

### Table 1: machine_master
- machine_id (Primary Key)
- machine_name
- machine_code
- machine_location
- is_active

### Table 2: production_target
- target_id (Primary Key)
- machine_id (Foreign Key)
- production_date
- shift_name
- target_quantity

### Table 3: production_log
- log_id (Primary Key)
- machine_id (Foreign Key)
- total_count
- good_count
- reject_count
- cycle_time
- temperature
- recorded_at

### Table 4: machine_status_log
- status_id (Primary Key)
- machine_id (Foreign Key)
- machine_status
- start_time
- end_time

### Table 5: shift_master
- shift_id (Primary Key)
- shift_name
- start_time
- end_time

## 7. Ignition HMI Requirements

### Screen 1: Main Production Dashboard
- Machine status indicator.
- Total production count.
- Good production count.
- Rejected production count.
- Target quantity.
- Production achievement percentage.

### Screen 2: Machine Monitoring
- Live machine status.
- Temperature.
- Cycle time.
- Production count.
- Communication status.

### Screen 3: Production History
- Production records.
- Date and time filters.
- Machine-wise production history.
- Shift-wise production information.

## 8. Grafana Dashboard Requirements

### Dashboard 1: Production Overview
- Total production.
- Good quantity.
- Rejected quantity.
- Target versus actual production.

### Dashboard 2: Machine Monitoring
- Machine RUN/STOP/IDLE status.
- Machine temperature trend.
- Cycle time trend.
- Machine availability.

### Dashboard 3: Production Analytics
- Hourly production trend.
- Shift-wise production.
- Production achievement percentage.
- Basic OEE.

## 9. Basic KPI Calculations

Production Achievement:

Actual Production / Target Production × 100

Availability:

Operating Time / Planned Production Time × 100

Performance:

Ideal Cycle Time × Total Production / Operating Time × 100

Quality:

Good Production / Total Production × 100

OEE:

Availability × Performance × Quality

## 10. Non-Functional Requirements
- Data should be stored reliably.
- Machine data should refresh at a configurable interval.
- Database tables should maintain data integrity.
- The application should handle OPC communication failures.
- Dashboard information should be easy to understand.
- System components should be modular and maintainable.

## 11. Testing Requirements
- OPC UA communication testing.
- Machine status change testing.
- Production count validation.
- MySQL database connectivity testing.
- Ignition tag monitoring testing.
- Grafana database connectivity testing.
- KPI calculation validation.
- Communication failure testing.

## 12. Expected Technical Deliverables
- Project architecture diagram.
- OPC UA tag configuration.
- Kepware communication configuration.
- Ignition HMI screens.
- MySQL database schema and SQL scripts.
- Grafana dashboards.
- Test cases and results.
- Final project documentation.