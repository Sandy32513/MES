# ============================================================
# run_all.ps1 — Start all MES components
# Usage: powershell -ExecutionPolicy Bypass -File scripts\run_all.ps1
# ============================================================

$root = "D:\MES\mes-project"
Set-Location $root
$ErrorActionPreference = "Continue"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "     Starting MES Production System       " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check MySQL
$mysql = Get-Service -Name "*mysql*" -ErrorAction SilentlyContinue
if ($mysql -and $mysql.Status -eq "Running") {
    Write-Host "[1/4] MySQL Service ($($mysql.Name)) is Running." -ForegroundColor Green
} else {
    Write-Host "[1/4] Starting MySQL..." -ForegroundColor Yellow
    Start-Service -Name "MySQL80" -ErrorAction SilentlyContinue
}

# 2. Check Grafana
$grafana = Get-Service -Name "*grafana*" -ErrorAction SilentlyContinue
if ($grafana -and $grafana.Status -eq "Running") {
    Write-Host "[2/4] Grafana Service is Running (http://localhost:3000)." -ForegroundColor Green
} else {
    Write-Host "[2/4] Starting Grafana..." -ForegroundColor Yellow
    Start-Service -Name "Grafana" -ErrorAction SilentlyContinue
}

# 3. Start Simulator Daemon
Write-Host "[3/4] Launching OPC UA Simulator..." -ForegroundColor Cyan
$pyProcs = Get-CimInstance Win32_Process -Filter "name = 'python.exe'" -ErrorAction SilentlyContinue
$existingSim = $pyProcs | Where-Object { $_.CommandLine -match "mes_simulator.py" }
if (-not $existingSim) {
    Start-Process python -ArgumentList "$root\simulator\mes_simulator.py --scenario normal --time-scale 5.0 --control-file $root\simulator\control.json" -WorkingDirectory $root
    Start-Sleep 2
} else {
    Write-Host "  Simulator already running (PID $($existingSim.ProcessId))." -ForegroundColor Green
}

# 4. Start Pipeline Logger Daemon
Write-Host "[4/4] Launching Data Pipeline Logger..." -ForegroundColor Cyan
$pyProcs = Get-CimInstance Win32_Process -Filter "name = 'python.exe'" -ErrorAction SilentlyContinue
$existingLog = $pyProcs | Where-Object { $_.CommandLine -match "data_logger.py" }
if (-not $existingLog) {
    Start-Process python -ArgumentList "$root\simulator\data_logger.py" -WorkingDirectory $root
    Start-Sleep 2
} else {
    Write-Host "  Pipeline logger already running (PID $($existingLog.ProcessId))." -ForegroundColor Green
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "System is active! Running smoke test..." -ForegroundColor Yellow
Start-Sleep 3
python "$root\simulator\validate_client.py"

Write-Host "`nDashboards available at: http://localhost:3000" -ForegroundColor Green
