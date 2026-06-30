# git-sync.ps1 — user-invoked GitHub sync for PlantMind
# Usage (from CLI):  ! powershell -File scripts\git-sync.ps1 "optional commit message"
#   - no message  -> pull --rebase + push (sync only)
#   - with message-> stage all + commit + pull --rebase + push
param([string]$msg = "")

Set-Location (Split-Path $PSScriptRoot -Parent)
Write-Host "== PlantMind GitHub sync ==" -ForegroundColor Cyan

if ($msg -ne "") {
  git add -A
  git commit -m $msg
}

git fetch origin
git pull --rebase origin main
git push origin main

Write-Host "`n-- last 3 commits --" -ForegroundColor Cyan
git log --oneline -3
Write-Host "`nDone. Remote: https://github.com/1celestial0/plantmind_build" -ForegroundColor Green
