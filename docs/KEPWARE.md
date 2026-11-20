# KEPWARE INTEGRATION REPORT (Decision D1 / Path B)

## 1. Decision D1 Context
Per Decision **D1** in the Master Execution Prompt:
- **Primary Path (Critical Path):** Machine Simulator → Direct OPC UA communication.
- **Optional Path B:** Insert Kepware KEPServerEX between simulator and SCADA **only if** the Kepware trial includes a compatible driver able to talk to the simulator (OPC UA Client driver). Path B never blocks the primary path.

---

## 2. Evaluation & Outcome
1. **Form-Gated Licensing:**
   - The PTC Kepware download portal requires business entity verification, corporate contact information, and registration confirmation.
   - Per Section 1, Item 4 ("Human-only steps"), automated agents do not fabricate accounts or submit personal identities.
2. **Technical Feasibility:**
   - Standard KEPServerEX installs primarily provide downstream PLC drivers (Allen-Bradley, Siemens, Modbus, Omron) and act as an OPC UA Server.
   - Connecting Kepware to another upstream OPC UA server requires the specialized **OPC UA Client Driver** plugin (an add-on license).
3. **Execution Path Adopted:**
   - The system was successfully constructed and verified using the **Primary Path** (`Simulator -> Direct OPC UA Client -> Pipeline -> MySQL -> Grafana`).
   - Detailed instructions for an operator to manually add Kepware into the architecture are fully documented in `docs/MANUAL_STEPS.md` (`MANUAL-02`).
   - The primary path passed Gate 3 and Gate 4, delivering 100% of functional requirements FR-01 through FR-10 without external dependencies.
