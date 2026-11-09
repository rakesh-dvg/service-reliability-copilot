# Evidence — Demo incident recovery (2026-11-09)

## Command

```powershell
.\scripts\demo-incident.ps1 -FailureCount 8 -IntervalSeconds 3
```

## Result

- Controlled demo failure enabled
- Eight failing submissions generated (HTTP 503 expected)
- Prometheus alert `ServiceRequestSubmissionUserImpact` entered firing state
- Alertmanager delivered webhook to responder
- Incident `9c8cae43-bacd-4728-8006-afd3521db96e` created as `DEMO_FAILURE_MODE`
- Allowlisted action `DISABLE_DEMO_FAILURE_MODE` succeeded
- Synthetic verification persisted request `76380f57-2232-47b0-9619-906a20c2b4ed`
- Incident marked `resolved` with `recovery_verified=true`
- Post-recovery request `42238634-7594-4bd1-92e3-13f80b7130c6` succeeded

## Status

**Verified** on local Docker Compose stack.
