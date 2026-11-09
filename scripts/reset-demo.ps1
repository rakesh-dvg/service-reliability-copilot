$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "Resetting demo state (containers + database volume)..."
docker compose down -v
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}
docker compose up --build -d
Write-Host "Demo stack reset complete."
