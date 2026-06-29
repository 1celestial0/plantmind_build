# PlantMind — run pytest and append results to continuity/test-log.json

param(
    [string]$Root = "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live",
    [string]$Trigger = "manual"
)

$ErrorActionPreference = "Stop"
Set-Location $Root

$junit = Join-Path $Root "continuity\last-test-results.xml"

Write-Host ""
Write-Host "PlantMind test run" -ForegroundColor Cyan
Write-Host "  Root: $Root"
Write-Host ""

py -3 -m pytest tests/ -v --tb=short --junitxml="$junit"
$pytestExit = $LASTEXITCODE

py -3 ops/testing/append_test_log.py "$junit" $Trigger
$logExit = $LASTEXITCODE

if ($pytestExit -ne 0) {
    Write-Host "Pytest reported failures (exit $pytestExit)" -ForegroundColor Yellow
    exit $pytestExit
}
if ($logExit -ne 0) {
    exit $logExit
}

Write-Host ""
Write-Host "Tests passed — log updated at continuity/test-log.json" -ForegroundColor Green
Write-Host ""
exit 0