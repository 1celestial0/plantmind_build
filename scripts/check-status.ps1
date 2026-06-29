# PlantMind — one-screen project status (human or AI reference)

param(
    [string]$Root = "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live"
)

Set-Location $Root

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PlantMind — Status Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# STATE.json
$statePath = Join-Path $Root "continuity\STATE.json"
if (Test-Path $statePath) {
    $state = Get-Content $statePath -Raw | ConvertFrom-Json
    Write-Host "Context : $($state.latest_context_version) — $($state.latest_context_file)" -ForegroundColor Yellow
    Write-Host "Open items (last close): $($state.roadmap_open_items_last_close)"
}

# ROADMAP NOW
$roadmap = Join-Path $Root "ROADMAP.md"
if (Test-Path $roadmap) {
    Write-Host ""
    Write-Host "ROADMAP NOW:" -ForegroundColor Yellow
    $inNow = $false
    Get-Content $roadmap | ForEach-Object {
        if ($_ -match '^## NOW') { $inNow = $true; return }
        if ($_ -match '^## ') { $inNow = $false }
        if ($inNow -and $_ -match '^- \[ \]') { Write-Host "  $_" }
    }
}

# Git
Write-Host ""
Write-Host "Git:" -ForegroundColor Yellow
git -C $Root log -1 --oneline 2>$null
git -C $Root status --short 2>$null | Select-Object -First 6

# Test log tail
$testLog = Join-Path $Root "continuity\test-log.json"
if (Test-Path $testLog) {
    $tl = Get-Content $testLog -Raw | ConvertFrom-Json
    if ($tl.runs.Count -gt 0) {
        $last = $tl.runs[-1]
        Write-Host ""
        Write-Host "Last test run:" -ForegroundColor Yellow
        Write-Host "  $($last.timestamp) — passed $($last.passed) / failed $($last.failed)"
    } else {
        Write-Host ""
        Write-Host "Last test run: (none — run scripts/run-tests.ps1)" -ForegroundColor DarkGray
    }
}

# Goal log tail
$goalLog = Join-Path $Root "continuity\goal-log.json"
if (Test-Path $goalLog) {
    $gl = Get-Content $goalLog -Raw | ConvertFrom-Json
    $lastGoal = $gl.entries[-1]
    Write-Host ""
    Write-Host "Last goal log:" -ForegroundColor Yellow
    Write-Host "  $($lastGoal.id): $($lastGoal.title) [$($lastGoal.status)]"
}

Write-Host ""
Write-Host "Playbook: ops/TEAM-OPERATIONS-PLAYBOOK.md" -ForegroundColor Green
Write-Host "Parallel status: docs/parallel/STATUS.md" -ForegroundColor Green
Write-Host ""