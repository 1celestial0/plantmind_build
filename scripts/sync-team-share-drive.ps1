# PlantMind — Stage team-share deliverables for Google Drive upload
# Drive folder ID: continuity/STATE.json -> drive_folder_id
# Target path in Drive: PlantMind / PlantMind_SourceOfTruth_v2_2026-07-01/

param(
    [string]$Root = "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live"
)

$ErrorActionPreference = "Stop"
Set-Location $Root

$statePath = Join-Path $Root "continuity\STATE.json"
$state = Get-Content $statePath -Raw | ConvertFrom-Json
$staging = Join-Path $Root "continuity\drive-export-staging\team-share"

if (Test-Path $staging) {
    Remove-Item $staging -Recurse -Force
}
New-Item -ItemType Directory -Path $staging -Force | Out-Null

$patterns = @(
    "team-share\*.pdf",
    "team-share\*.docx",
    "team-share\*.xlsx",
    "team-share\*.pptx",
    "team-share\*.md",
    "team-share\mockups\*"
)

$copied = 0
foreach ($pat in $patterns) {
    Get-ChildItem -Path (Join-Path $Root $pat) -ErrorAction SilentlyContinue | ForEach-Object {
        $rel = $_.FullName.Substring($Root.Length + 1)
        $dest = Join-Path $staging $rel.Substring("team-share\".Length)
        $destDir = Split-Path $dest -Parent
        if ($destDir -and -not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        Copy-Item $_.FullName $dest -Force
        $copied++
    }
}

$manifest = @{
    exported_at      = (Get-Date).ToString("o")
    project          = "PlantMind"
    drive_folder_id  = $state.drive_folder_id
    drive_path       = "PlantMind / PlantMind_SourceOfTruth_v2_2026-07-01/"
    files_copied     = $copied
    staging          = $staging
    manual_step      = "Upload contents of continuity/drive-export-staging/team-share to the Drive folder above (Claude CLI: say 'sync to drive' with Google Drive MCP enabled)"
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $staging "manifest.json") -Encoding UTF8

# Update STATE.json archive timestamp (local record of staging run)
$state.last_archived_to_drive = (Get-Date).ToString("o")
$state | ConvertTo-Json -Depth 4 | Set-Content $statePath -Encoding UTF8

Write-Host ""
Write-Host "PlantMind team-share Drive staging ready" -ForegroundColor Green
Write-Host "  Copied : $copied files"
Write-Host "  Staging: $staging"
Write-Host "  Drive  : $($state.drive_folder_id)"
Write-Host ""
Write-Host "Next: python scripts\upload_to_drive.py  (needs Drive OAuth scope)" -ForegroundColor Yellow
Write-Host "Or upload staging folder manually to Drive folder ID above." -ForegroundColor Cyan
Write-Host "Or from Claude CLI: say 'sync to drive' (Google Drive MCP enabled)." -ForegroundColor Cyan