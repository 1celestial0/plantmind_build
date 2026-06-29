# PlantMind-Live — Session Start Script
# Run at the beginning of every work session (any AI tool)

$Root = "C:\Users\hp\Claude\Projects\PlantMind-Live"
Set-Location $Root

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PlantMind-Live — Session Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Workspace: $Root" -ForegroundColor Green
Write-Host ""

# Latest Chat Context
$ctxDir = Join-Path $Root "Chat Context"
$latest = Get-ChildItem $ctxDir -Filter "*_project-context.md" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -notmatch "archive" } |
    Sort-Object { if ($_.Name -match '_v(\d+)\.(\d+)_') { [int]$Matches[1]*1000+[int]$Matches[2] } else { 0 } } -Descending |
    Select-Object -First 1

if ($latest) { Write-Host "Latest context: $($latest.Name)" -ForegroundColor Yellow }

# ROADMAP NOW items
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

# Git status
Write-Host ""
Write-Host "Git status:" -ForegroundColor Yellow
git -C $Root status --short 2>$null | Select-Object -First 8

Write-Host ""
Write-Host "Read order for AI:" -ForegroundColor Cyan
Write-Host "  1. 00-START-HERE.md"
Write-Host "  2. LOCKED_STATE.md"
Write-Host "  3. ROADMAP.md"
Write-Host "  4. docs/IMPLEMENTATION-GUIDE-ULTRA.md (if building)"
Write-Host ""
Write-Host "v1 demo: streamlit run src\legacy\forge-v1\app.py" -ForegroundColor Green
Write-Host "Close: tell AI 'close session'" -ForegroundColor Green
Write-Host ""