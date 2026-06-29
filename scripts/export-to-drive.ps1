# PlantMind — Export whitelist to local staging for Google Drive / NotebookLM
# Manual step: upload staging folder contents to Drive folder in continuity/STATE.json
# Drive folder ID: 13DzACqPywL2AD4mVjhDMYpAqxcBYXI3A

param(
    [string]$Root = "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live",
    [string]$Staging = "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live\continuity\drive-export-staging"
)

$ErrorActionPreference = "Stop"
Set-Location $Root

# NotebookLM / team knowledge whitelist
$Whitelist = @(
    "00-START-HERE.md",
    "LOCKED_STATE.md",
    "ROADMAP.md",
    "AI-OPERATING-SYSTEM.md",
    "docs\IMPLEMENTATION-GUIDE-ULTRA.md",
    "docs\CONSOLIDATED-PROJECT-BLUEPRINT.md",
    "docs\WIN-STRATEGY-ASSESSMENT.md",
    "docs\architecture\08_DEMO_SCENARIOS.md",
    "docs\research\PAIN_REGISTER_2026_25th_June.md",
    "docs\research\COMPETITIVE_MAP_2026_25th_June.md",
    "docs\research\DATABRICKS_MAP_2026_30th_June.md",
    "docs\research\DATA_REALITY_2026_30th_June.md",
    "docs\research\ROI_BENCHMARKS_2026_30th_June.md",
    "docs\research\ARCHITECTURE_LOCK_2026_30th_June.md",
    "ops\OPERATIONS-MANUAL.md",
    "ops\TEAM-CHAT-GUIDE.md",
    "ops\ROUTING.md",
    "ops\prompts\lanes\README.md"
)

if (Test-Path $Staging) {
    Remove-Item $Staging -Recurse -Force
}
New-Item -ItemType Directory -Path $Staging | Out-Null

$copied = 0
$missing = @()

foreach ($rel in $Whitelist) {
    $src = Join-Path $Root $rel
    if (-not (Test-Path $src)) {
        $missing += $rel
        continue
    }
    $destDir = Join-Path $Staging (Split-Path $rel -Parent)
    if ($destDir -and -not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    Copy-Item $src (Join-Path $Staging $rel) -Force
    $copied++
}

$manifest = @{
    exported_at = (Get-Date).ToString("o")
    project     = "PlantMind"
    copied      = $copied
    missing     = $missing
    drive_folder_id = "13DzACqPywL2AD4mVjhDMYpAqxcBYXI3A"
    manual_step = "Upload continuity/drive-export-staging to Google Drive NotebookLM-Sources folder"
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $Staging "manifest.json") -Encoding UTF8

Write-Host ""
Write-Host "PlantMind Drive export staging ready" -ForegroundColor Green
Write-Host "  Copied : $copied files"
Write-Host "  Staging: $Staging"
if ($missing.Count -gt 0) {
    Write-Host "  Missing: $($missing -join ', ')" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Manual: upload staging folder to Drive, then sync NotebookLM sources." -ForegroundColor Cyan