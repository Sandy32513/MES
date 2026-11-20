# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Project Title
Real-Time Production Monitoring System – MES

## 1. Project Overview
The Real-Time Production Monitoring System is a basic Manufacturing Execution System (MES) application designed to monitor machine production activities in a manufacturing environment.

The application collects machine data through OPC UA communication, stores production information in a MySQL database, displays machine conditions through Ignition SCADA and provides production performance dashboards using Grafana OSS.

## 2. Problem Statement
In traditional manufacturing environments, production information is often recorded manually. This makes it difficult to monitor machine status, production quantities, downtime and production performance in real time.

This project aims to develop a basic digital monitoring solution to improve production visibility and provide accurate production reports.

## 3. Project Objectives
- Monitor machine status in real time.
- Collect actual production counts automatically.
- Monitor production targets against actual production.
- Track good and rejected quantities.
- Identify machine running and stopped conditions.
- Store machine production information in MySQL.
- Display production KPIs using Grafana dashboards.

## 4. Project Scope

### In Scope
- One simulated manufacturing machine.
- Machine RUN, STOP and IDLE monitoring.
- Actual production count collection.
- Good and rejected quantity monitoring.
- Production target monitoring.
- SQL database integration.
- Ignition HMI development.
- Grafana dashboard development.
- Basic OEE calculation.

### Out of Scope
- Actual PLC hardware integration.
- ERP integration.
- Advanced predictive maintenance.
- Multi-factory monitoring.
- Production scheduling optimization.

## 5. Main Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | System shall monitor machine status. |
| FR-02 | System shall collect machine production counts. |
| FR-03 | System shall display actual production quantity. |
| FR-04 | System shall display planned production quantity. |
| FR-05 | System shall calculate production achievement. |
| FR-06 | System shall monitor good and rejected quantities. |
| FR-07 | System shall store production records in MySQL. |
| FR-08 | System shall display production information in Ignition. |
| FR-09 | System shall display KPIs in Grafana. |
| FR-10 | System shall calculate basic OEE. |

## 6. Users
- MES Engineer
- Production Operator
- Production Supervisor
- Manufacturing Manager

## 7. Expected Business Output
- Real-time machine monitoring.
- Improved production visibility.
- Automated production data collection.
- Reduced manual reporting.
- Better understanding of machine performance.
- Production performance reports.

## 8. Project Success Criteria
The project will be considered successful when:
- OPC UA machine tags are communicating successfully.
- Ignition displays live machine values.
- Production data is stored correctly in MySQL.
- Machine status changes are recorded.
- Grafana displays production KPIs.
- Production achievement and basic OEE calculations produce correct results.