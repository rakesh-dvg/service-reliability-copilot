$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$OutDir = Join-Path $Root "transfer-output"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ZipPath = Join-Path $OutDir "service-reliability-copilot-$Stamp.zip"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$excludeDirs = @(
    "\.git\\",
    "\\node_modules\\",
    "\\.venv\\",
    "\\venv\\",
    "\\__pycache__\\",
    "\\.pytest_cache\\",
    "\\dist\\",
    "\\build\\",
    "\\transfer-output\\",
    "\\.tmp-verify\\",
    "\\.ruff_cache\\"
)

$files = Get-ChildItem -Path $Root -Recurse -File | Where-Object {
    $full = $_.FullName
    $rel = $full.Substring($Root.Length)
    foreach ($ex in $excludeDirs) {
        if ($rel -match $ex) { return $false }
    }
    if ($_.Name -eq ".env") { return $false }
    if ($_.Extension -in @(".zip", ".log")) { return $false }
    return $true
}

if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::Open($ZipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($file in $files) {
        $entryName = $file.FullName.Substring($Root.Length).TrimStart("\").Replace("\", "/")
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $file.FullName, $entryName) | Out-Null
    }
}
finally {
    $zip.Dispose()
}

$sizeMb = [math]::Round((Get-Item $ZipPath).Length / 1MB, 2)
Write-Host "Created transfer ZIP: $ZipPath ($sizeMb MB)"
Write-Host "Next: .\scripts\verify-transfer.ps1 -ZipPath `"$ZipPath`""
