# PlantMind — Notion + Drive sync stub (Wave 2+)
# IDs from continuity/STATE.json — run manually after credentials configured

param(
    [string]$Root = "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live"
)

$statePath = Join-Path $Root "continuity\STATE.json"
$state = Get-Content $statePath -Raw | ConvertFrom-Json

Write-Host ""
Write-Host "PlantMind sync stub" -ForegroundColor Cyan
Write-Host "  Notion database : $($state.notion_database_id)"
Write-Host "  Drive folder    : $($state.drive_folder_id)"
Write-Host "  Git remote      : $($state.git_remote)"
Write-Host ""
Write-Host "Steps (manual until API keys wired):" -ForegroundColor Yellow
Write-Host "  1. Run .\scripts\export-to-drive.ps1"
Write-Host "  2. Upload continuity\drive-export-staging to Drive folder above"
Write-Host "  3. Update Notion dashboard from ROADMAP NOW + latest Chat Context"
Write-Host "  4. Set last_synced_to_notion / last_archived_to_drive in STATE.json"
Write-Host ""
Write-Host "Future: integrate project-continuity skill + Notion API token." -ForegroundColor Green