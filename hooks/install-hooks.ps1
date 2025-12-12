# Install git hooks for this repository
# Run this script once after cloning the repo

$hookSource = Join-Path $PSScriptRoot "pre-push"
$repoRoot = Split-Path $PSScriptRoot -Parent
$hookDest = Join-Path $repoRoot ".git\hooks\pre-push"

Copy-Item -Path $hookSource -Destination $hookDest -Force

Write-Host "✅ Git hooks installed successfully." -ForegroundColor Green
Write-Host "   Pre-push hook will run unit tests before each push."
