# One-shot push script. Run this once after authenticating.
# Usage:
#   1. Either:  gh auth login --web       (then this script auto-creates the repo)
#      Or:     create github.com/srqt2/STUPIDMEI manually first
#   2. Run:    .\push.ps1

Set-Location -Path $PSScriptRoot

$ghPath = (Get-Command gh -ErrorAction SilentlyContinue)
if ($ghPath) {
    Write-Host "gh detected at $($ghPath.Source). Checking auth..."
    gh auth status 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Not authenticated. Run: gh auth login --web"
        Write-Host "Then re-run this script."
        exit 1
    }
    Write-Host "Auth OK. Creating repo and pushing..."
    gh repo create STUPIDMEI --public --source=. --remote=origin --push
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Pushed. Live at https://github.com/srqt2/STUPIDMEI"
    }
} else {
    Write-Host "gh CLI not found. Falling back to manual remote setup."
    Write-Host ""
    Write-Host "1) Create the repo at https://github.com/new"
    Write-Host "   Name: STUPIDMEI  Visibility: Public  (do NOT add README/gitignore/license)"
    Write-Host ""
    $ready = Read-Host "Press Enter once the repo is created on GitHub"
    git remote add origin https://github.com/srqt2/STUPIDMEI.git
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Pushed. Live at https://github.com/srqt2/STUPIDMEI"
    }
}
