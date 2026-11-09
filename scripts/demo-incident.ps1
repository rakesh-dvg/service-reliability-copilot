param(
    [string]$AdminToken = $env:ADMIN_API_TOKEN,
    [int]$FailureCount = 12,
    [int]$IntervalSeconds = 5
)

$ErrorActionPreference = "Stop"

if (-not $AdminToken) {
    $AdminToken = "dev-admin-token-change-me"
}

$headers = @{ Authorization = "Bearer $AdminToken" }
$base = "http://localhost:8000"

Write-Host "1) Enabling controlled demo failure..."
Invoke-RestMethod -Method POST -Uri "$base/api/v1/demo/failure/enable" -Headers $headers | Out-Null

Write-Host "2) Generating $FailureCount failing submissions across scrapes (every ${IntervalSeconds}s)..."
for ($i = 1; $i -le $FailureCount; $i++) {
    $payload = @{
        customer_name = "Demo User $i"
        customer_email = "demo.user$i@example.com"
        service_category = "Technical Support"
        title = "Demo failure request $i"
        description = "Intentional failing submission for alert demonstration."
        priority = "high"
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Method POST -Uri "$base/api/v1/requests" -ContentType "application/json" -Body $payload | Out-Null
        Write-Host "  unexpected success on attempt $i"
    } catch {
        Write-Host "  expected failure $i"
    }
    Start-Sleep -Seconds $IntervalSeconds
}

Write-Host "3) Waiting for Prometheus alert + Alertmanager webhook + responder recovery..."
Write-Host "   Watch: http://localhost:9090/alerts  and  http://localhost:9093"
Write-Host "   Reliability UI: http://localhost:8088/reliability"

$deadline = (Get-Date).AddMinutes(4)
$resolved = $false
$pulse = 0
do {
    # Keep the failure series warm until remediation succeeds
    $pulse++
    $pulsePayload = @{
        customer_name = "Pulse $pulse"
        customer_email = "pulse$pulse@example.com"
        service_category = "Technical Support"
        title = "Pulse failure $pulse"
        description = "Keep failure rate elevated until alert fires and recovery completes."
        priority = "high"
    } | ConvertTo-Json
    try {
        Invoke-RestMethod -Method POST -Uri "$base/api/v1/requests" -ContentType "application/json" -Body $pulsePayload | Out-Null
    } catch {
        # expected while failure mode is on
    }

    try {
        $incidents = Invoke-RestMethod -Uri "$base/api/v1/incidents"
        $hit = @($incidents | Where-Object { $_.incident_type -eq "DEMO_FAILURE_MODE" -and $_.status -eq "resolved" })
        if ($hit.Count -gt 0) {
            $resolved = $true
            Write-Host "4) Responder resolved incident: $($hit[0].id)"
            break
        }
        $active = @($incidents | Where-Object { $_.incident_type -eq "DEMO_FAILURE_MODE" })
        if ($active.Count -gt 0) {
            Write-Host "   incident status: $($active[0].status)"
        }
    } catch {
        # keep polling
    }
    Start-Sleep -Seconds 8
} while ((Get-Date) -lt $deadline)

if (-not $resolved) {
    Write-Host "Incident not resolved yet within timeout. Check Prometheus/Alertmanager/responder logs."
    Write-Host "Manual disable: POST $base/api/v1/demo/failure/disable with admin token"
    exit 2
}

Write-Host "5) Verifying fresh successful submission..."
$okPayload = @{
    customer_name = "Recovery Check"
    customer_email = "recovery.check@example.com"
    service_category = "General Service"
    title = "Post-recovery verification"
    description = "Confirming journey works after automated remediation."
    priority = "medium"
} | ConvertTo-Json

$created = Invoke-RestMethod -Method POST -Uri "$base/api/v1/requests" -ContentType "application/json" -Body $okPayload
Write-Host "Recovery verification request id: $($created.id)"
Write-Host "Demo incident walkthrough complete."
