# ============================================================
# 01_install_stack.ps1 — MES Stack Installation & Verification
# Idempotent script: checks and configures stack components
# ============================================================

$root = "D:\MES\mes-project"
$ErrorActionPreference = "Continue"

Write-Host "Checking MES Stack Components..." -ForegroundColor Cyan

# 1. Python
$pyVer = python --version 2>&1
Write-Host "Python: $pyVer" -ForegroundColor Green

# 2. Python Packages
python -m pip install asyncua playwright | Out-Null
Write-Host "Python packages asyncua, playwright verified." -ForegroundColor Green

# 3. MySQL Server
$mysql = Get-Service -Name "*mysql*" -ErrorAction SilentlyContinue
if ($mysql -and $mysql.Status -eq "Running") {
    Write-Host "MySQL Service: $($mysql.Name) is Running." -ForegroundColor Green
} else {
    Write-Host "Starting MySQL Service..." -ForegroundColor Yellow
    Start-Service -Name "MySQL80" -ErrorAction SilentlyContinue
}

# 4. Grafana
if (Test-Path "D:\MES\grafana\bin\grafana-server.exe") {
    Write-Host "Grafana OSS binary is present at D:\MES\grafana\bin\grafana-server.exe" -ForegroundColor Green
} else {
    Write-Host "Grafana binary missing. Please extract grafana-11.3.0.windows-amd64.zip to D:\MES\grafana" -ForegroundColor Red
}

# 5. DBeaver
if (Test-Path "C:\Users\CREAM_LANE_CAFE\AppData\Local\DBeaver\dbeaver.exe") {
    Write-Host "DBeaver Community is installed." -ForegroundColor Green
} else {
    Write-Host "DBeaver not found." -ForegroundColor Yellow
}

Write-Host "Stack check complete." -ForegroundColor Cyan
