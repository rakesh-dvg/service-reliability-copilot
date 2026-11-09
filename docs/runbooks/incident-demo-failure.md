# Runbook — Demo request-submission failure

## Symptom

Customer service request submissions return HTTP 503. Prometheus alert `ServiceRequestSubmissionUserImpact` is firing. Reliability dashboard shows elevated failures.

## Likely cause (demo)

Controlled demo failure mode is enabled (`demo_failure_mode_enabled=true`).

## Immediate checks

1. Backend health: `GET http://localhost:8000/health`
2. Metrics: `service_request_submission_failures_total` increasing
3. Grafana: Service Request Journey dashboard
4. Incidents API: `GET http://localhost:8000/api/v1/incidents`

## Automated recovery

The runtime responder should:

1. Receive Alertmanager webhook
2. Classify as `DEMO_FAILURE_MODE`
3. Execute `DISABLE_DEMO_FAILURE_MODE`
4. Verify with synthetic POST `/api/v1/requests`
5. Resolve incident

## Manual recovery

```powershell
$headers = @{ Authorization = "Bearer $env:ADMIN_API_TOKEN" }
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/api/v1/demo/failure/disable" -Headers $headers
```

Then submit a test request and confirm HTTP 201.

## Escalation

If remediation fails twice within cooldown:

1. Disable fault manually
2. Capture logs with matching `trace_id`
3. Mark incident as `escalated` in the UI/API notes
