$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$failed = $false

Write-Host "=== Backend lint (ruff) ==="
Push-Location "$Root\backend"
python -m pip install -q -r requirements.txt
python -m ruff check app tests
if ($LASTEXITCODE -ne 0) { $failed = $true }

Write-Host "=== Backend tests (pytest) ==="
$env:ENABLE_OTEL = "false"
$env:DEMO_MODE = "true"
$env:ADMIN_API_TOKEN = "test-admin-token"
$env:RECOVERY_API_TOKEN = "test-recovery-token"
$env:ALERT_WEBHOOK_TOKEN = "test-alert-token"
python -m pytest -q
if ($LASTEXITCODE -ne 0) { $failed = $true }
Pop-Location

Write-Host "=== Responder tests ==="
Push-Location "$Root\responder"
python -m pip install -q -r requirements.txt
python -m pytest -q
if ($LASTEXITCODE -ne 0) { $failed = $true }
Pop-Location

Write-Host "=== Frontend tests/build ==="
Push-Location "$Root\frontend"
# Prefer Linux container execution on Windows hosts where App Control may block Rollup native binaries.
$useDockerFrontend = $false
try {
    docker info | Out-Null
    if ($LASTEXITCODE -eq 0) { $useDockerFrontend = $true }
} catch {
    $useDockerFrontend = $false
}

if ($useDockerFrontend) {
    docker run --rm -v "${PWD}:/app" -w /app node:20-bookworm-slim bash -lc "npm install && npm run test && npm run build"
    if ($LASTEXITCODE -ne 0) { $failed = $true }
} else {
    if (-not (Test-Path "node_modules")) {
        npm install
    }
    npm run test
    if ($LASTEXITCODE -ne 0) { $failed = $true }
    npm run build
    if ($LASTEXITCODE -ne 0) { $failed = $true }
}
Pop-Location

Write-Host "=== Docker Compose config validation ==="
docker compose -f "$Root\docker-compose.yml" config | Out-Null
if ($LASTEXITCODE -ne 0) { $failed = $true }

if ($failed) {
    Write-Error "One or more test suites failed."
    exit 1
}

Write-Host "All local test suites passed."
