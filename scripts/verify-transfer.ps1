param(
    [Parameter(Mandatory = $true)]
    [string]$ZipPath
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$VerifyRoot = Join-Path $Root ".tmp-verify"
$ExtractDir = Join-Path $VerifyRoot "extracted"

if (-not (Test-Path $ZipPath)) {
    throw "ZIP not found: $ZipPath"
}

if (Test-Path $VerifyRoot) {
    Remove-Item $VerifyRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $ExtractDir | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $ExtractDir)

$required = @(
    "README.md",
    "AGENTS.md",
    "docker-compose.yml",
    ".env.example",
    "docs/acceptance-criteria.md",
    "docs/architecture.md",
    "docs/task-tracker.md",
    "docs/second-laptop-setup.md",
    "backend/app/main.py",
    "backend/alembic/versions/0001_initial_schema.py",
    "frontend/package.json",
    "responder/app/main.py",
    "observability/prometheus/alerts-demo.yml",
    "observability/alertmanager/alertmanager.yml",
    ".github/workflows/ci.yml",
    "scripts/start-local.ps1",
    "scripts/demo-incident.ps1"
)

$missing = @()
foreach ($path in $required) {
    if (-not (Test-Path (Join-Path $ExtractDir $path))) {
        $missing += $path
    }
}

Write-Host "Secret scan (heuristic)..."
$secretHits = Select-String -Path (Get-ChildItem $ExtractDir -Recurse -File | Where-Object { $_.Length -lt 2MB } | Select-Object -ExpandProperty FullName) `
    -Pattern "sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}" `
    -ErrorAction SilentlyContinue

$envPresent = Test-Path (Join-Path $ExtractDir ".env")
$gitPresent = Test-Path (Join-Path $ExtractDir ".git")

Write-Host ""
Write-Host "ZIP: $ZipPath"
Write-Host "Size: $([math]::Round((Get-Item $ZipPath).Length / 1MB, 2)) MB"
Write-Host "Missing required files: $($missing.Count)"
if ($missing.Count -gt 0) { $missing | ForEach-Object { Write-Host "  - $_" } }
Write-Host ".env present in ZIP: $envPresent (must be False)"
Write-Host ".git present in ZIP: $gitPresent (must be False)"
Write-Host "Heuristic secret hits: $($secretHits.Count)"

Push-Location $ExtractDir
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}
docker compose config | Out-Null
$composeOk = ($LASTEXITCODE -eq 0)
Pop-Location
Write-Host "docker compose config OK: $composeOk"

if ($missing.Count -gt 0 -or $envPresent -or $gitPresent -or -not $composeOk) {
    throw "Transfer verification failed."
}

Write-Host "Transfer verification passed."
