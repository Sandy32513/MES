# ============================================================
# 10_start_sim.ps1 — Start MES OPC UA Simulator
# ============================================================

param(
    [string]$Scenario = "normal",
    [float]$TimeScale = 1.0,
    [int]$Seed = -1,
    [switch]$ResetCounters
)

$root = "D:\MES\mes-project"
$seedArg = if ($Seed -ge 0) { "--seed $Seed" } else { "" }
$resetArg = if ($ResetCounters) { "--reset-counters" } else { "" }

Write-Host "Starting MES OPC UA Simulator (scenario=$Scenario, timescale=$TimeScale)..." -ForegroundColor Cyan

# Stop existing simulator if running
$existing = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "mes_simulator.py" }
if ($existing) {
    Write-Host "Stopping existing simulator PID $($existing.Id)..."
    Stop-Process -Id $existing.Id -Force
    Start-Sleep 1
}

$proc = Start-Process python -ArgumentList "$root\simulator\mes_simulator.py --scenario $Scenario --time-scale $TimeScale $seedArg $resetArg" -WorkingDirectory $root -NoNewWindow -PassThru

$proc.Id | Out-File "$root\logs\sim.pid"
Write-Host "MES Simulator started with PID $($proc.Id)." -ForegroundColor Green

Start-Sleep 3
python "$root\simulator\validate_client.py"
