# Demo Script — Service Reliability Copilot (5–7 minutes)

Prerequisites: `.\scripts\start-local.ps1` completed successfully.

| Surface | URL |
|---------|-----|
| App UI | http://localhost:8088 |
| API | http://localhost:8000/docs |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |

---

## Full demo (5–7 min)

1. **Show the application** — Open http://localhost:8088 and explain the tagline.
2. **Submit a valid request** — Use the form; expect success confirmation.
3. **Show persistence** — Open Requests dashboard; request appears. Optionally: `GET /api/v1/requests`.
4. **Show Grafana** — Open Service Request Journey dashboard; success series increases.
5. **Enable controlled failure** — Demo Controls → Simulate Request Submission Failure (admin token from `.env`).
6. **Generate failures** — Run `.\scripts\demo-incident.ps1` or submit a few requests that return 503.
7. **Show alert firing** — Prometheus → Alerts → `ServiceRequestSubmissionUserImpact` pending/firing.
8. **Show Alertmanager** — http://localhost:9093 shows notification to responder webhook.
9. **Show responder incident** — Reliability dashboard / `GET /api/v1/incidents` shows `DEMO_FAILURE_MODE`.
10. **Show remediation** — Incident remediations include `DISABLE_DEMO_FAILURE_MODE`.
11. **Show recovery verification** — Incident `recovery_verified=true`; new submissions succeed.
12. **Show audit trail** — Mention `audit_events` persistence and incident history in UI.
13. **Show CI/CD + rollback docs** — Briefly open `docs/ci-cd.md` and `docs/rollback.md`.

---

## 3-minute fallback

1. Submit a successful request; show Requests dashboard.
2. Enable demo failure; show one 503.
3. Run `.\scripts\demo-incident.ps1`.
4. Show resolved incident on Reliability dashboard.
5. Point to Grafana + CI workflow files.

---

## Expected commands

```powershell
.\scripts\start-local.ps1
.\scripts\demo-incident.ps1
Invoke-RestMethod http://localhost:8000/api/v1/reliability/summary
```
