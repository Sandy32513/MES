# MANUAL STEPS REQUIRED FROM OPERATOR / OWNER

> As per Section 1 (Autonomy Contract, Item 4) and Section 3 (Decisions D1/D2), vendor account registration, license key issuance, and form-gated software downloads require human identity and consent. All code, configs, views, scripts, and databases have been pre-staged.

---

## MANUAL-01: Ignition Maker Edition Installation & Commissioning

**Context:** Inductive Automation requires a user account to obtain a Maker Edition license key and token.

### Steps to Download & Install:
1. Open a browser and visit: `https://inductiveautomation.com/downloads/`
2. Download the **Ignition 8.1 Windows 64-bit Installer** (`Ignition-8.1.x-windows-x64-installer.exe`).
3. Run the installer with default options:
   - Install directory: `C:\Program Files\Inductive Automation\Ignition`
   - Ports: HTTP `8088`, HTTPS `8043`
4. When installation finishes, the Ignition Commissioning web page opens at `http://localhost:8088`.

### Steps to Commission:
1. On the welcome screen, select **Maker Edition** (⚠️ **CRITICAL:** Do NOT choose Standard Edition. A gateway commissioned as Standard cannot take a Maker license; you would have to reinstall).
2. Create your administrative gateway credentials (username / password).
3. Sign in to your Inductive Automation account (or register at `https://account.inductiveautomation.com/`).
4. Generate a free **Maker Edition License Key & Activation Token** from your IA account portal.
5. Paste the License Key and Activation Token into the commissioning wizard.
6. Complete setup. The Gateway will show active and licensed.

### Steps to Import Pre-Staged MES Configuration:
1. Open the Ignition Designer at `http://localhost:8088`.
2. Connect to the Gateway using your admin credentials.
3. **OPC UA Connection:**
   - Go to Config > OPC UA > Connections > Add Connection.
   - Type: OPC UA Client.
   - Endpoint: `opc.tcp://127.0.0.1:4840/mes/simulator`
   - Name: `MES_SIM`
   - Security Policy: None. Save changes.
4. **Database Connection:**
   - Go to Config > Databases > Connections > Add Connection.
   - Type: MySQL (Connector/J).
   - Name: `MES_DB`
   - Connect URL: `jdbc:mysql://127.0.0.1:3306/mes_production_db`
   - Username: `ignition_writer`
   - Password: (copy from `D:\MES\mes-project\.env` `IGNITION_WRITER_PASSWORD`)
5. **Import Tags:**
   - In Designer Tag Browser, right-click `Tags` > Import.
   - Select `D:\MES\mes-project\ignition\tags.json`.
6. **Import Perspective Views:**
   - Perspective views are located at `D:\MES\mes-project\ignition\project_export\perspective\views\`.
   - Copy or import `MainDashboard`, `MachineMonitor`, and `ProductionHistory`.
7. **Gateway Scripts:**
   - In Designer Gateway Events:
     - Tag Change Script: copy `D:\MES\mes-project\ignition\gateway_scripts\status_logger.py` to tag `[default]MES/Machine01/Machine_Status`.
     - Timer Script: copy `D:\MES\mes-project\ignition\gateway_scripts\production_logger.py` (set delay to 1000 ms).
     - Startup Script: copy `D:\MES\mes-project\ignition\gateway_scripts\startup_recovery.py`.

---

## MANUAL-02: Kepware OPC Server Trial (Optional Path B, Decision D1)

**Context:** Decision D1 specifies that Simulator → Ignition direct is the primary critical path. Kepware is an optional intermediate hop if an OPC UA Client driver trial is available.

### Steps (Optional):
1. Visit `https://www.ptc.com/en/products/kepware/kepserverex`.
2. Register for the KEPServerEX 2-hour demonstration trial download.
3. Install KEPServerEX with the **OPC UA Client Driver**.
4. In Kepware, add a new channel with driver `OPC UA Client`:
   - Endpoint: `opc.tcp://127.0.0.1:4840/mes/simulator`
   - Security: None
5. Add device `Machine01` and browse/map the 7 simulator tags.
6. Reconfigure Ignition's `MES_SIM` OPC connection to point to Kepware's endpoint `opc.tcp://127.0.0.1:49320`.
7. Verify all 7 tags read Good quality.
