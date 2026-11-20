# Preflight check script for MES stack
$ErrorActionPreference = "Continue"

Write-Host "=========================================="
Write-Host "  MES Production Monitoring Preflight"
Write-Host "=========================================="

# 1. OS & Hardware
$os = [System.Environment]::OSVersion.VersionString
$ram = [math]::Round(((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB), 2)
$disk = [math]::Round(((Get-PSDrive D).Free / 1GB), 2)
$net = Test-NetConnection -ComputerName 8.8.8.8 -Port 53 -InformationLevel Quiet

Write-Host "OS: $os" -ForegroundColor Cyan
Write-Host "RAM: $ram GB (Target >= 8 GB)" -ForegroundColor $(if ($ram -ge 7.5) { "Green" } else { "Yellow" })
Write-Host "D: Free: $disk GB (Target >= 10 GB)" -ForegroundColor $(if ($disk -ge 10) { "Green" } else { "Red" })
Write-Host "Internet reachable: $net" -ForegroundColor $(if ($net) { "Green" } else { "Red" })

# 2. Python
$pyVer = python --version 2>&1
Write-Host "Python: $pyVer" -ForegroundColor Green

# 3. Python asyncua
$asyncuaCheck = python -c "import asyncua; print('OK')" 2>&1
Write-Host "asyncua: $asyncuaCheck" -ForegroundColor $(if ($asyncuaCheck -match "OK") { "Green" } else { "Red" })

# 4. Playwright
$pwCheck = python -c "from playwright.sync_api import sync_playwright; print('OK')" 2>&1
Write-Host "Playwright: $pwCheck" -ForegroundColor $(if ($pwCheck -match "OK") { "Green" } else { "Red" })

# 5. MySQL Server
$mysqlCheck = & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root --password="Root@123" -e "SELECT VERSION();" 2>&1
Write-Host "MySQL: $($mysqlCheck -join ' ')" -ForegroundColor $(if ($LASTEXITCODE -eq 0) { "Green" } else { "Red" })

Write-Host "Preflight check completed."
