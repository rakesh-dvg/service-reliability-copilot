param(
    [switch]$Build
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
}

Write-Host "Starting Service Reliability Copilot stack..."
if ($Build) {
    docker compose up --build -d
} else {
    docker compose up --build -d
}

Write-Host ""
Write-Host "Waiting for backend health..."
$deadline = (Get-Date).AddMinutes(3)
do {
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 3
        if ($resp.StatusCode -eq 200) { break }
    } catch {
        Start-Sleep -Seconds 3
    }
} while ((Get-Date) -lt $deadline)

Write-Host "App UI:          http://localhost:8088"
Write-Host "Backend API:     http://localhost:8000"
Write-Host "Grafana:         http://localhost:3000 (admin/admin)"
Write-Host "Prometheus:      http://localhost:9090"
Write-Host "Alertmanager:    http://localhost:9093"
Write-Host "Responder:       http://localhost:8080/health"
