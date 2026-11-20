# ============================================================
# stop_all.ps1 — Stop MES background processes
# Usage: powershell -ExecutionPolicy Bypass -File scripts\stop_all.ps1
# ============================================================

Write-Host "Stopping MES background processes..." -ForegroundColor Yellow

# Stop Python Simulator and Data Logger
$pyProcs = Get-Process python -ErrorAction SilentlyContinue
foreach ($p in $pyProcs) {
    try {
        $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($p.Id)").CommandLine
        if ($cmd -match "mes_simulator.py|data_logger.py") {
            Write-Host "Stopping PID $($p.Id) ($cmd)..." -ForegroundColor Cyan
            Stop-Process -Id $p.Id -Force
        }
    } catch {}
}

Write-Host "MES Simulator and Data Logger stopped." -ForegroundColor Green
Write-Host "Note: MySQL and Grafana services remain running in the background." -ForegroundColor Gray
