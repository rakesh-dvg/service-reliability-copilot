# Service Reliability Copilot

**From User-Impact Detection to AI-Assisted Incident Recovery**

AI Dev Tools Zoomcamp 2026 — Project 2 (independent from Project 1).

## Problem statement

Small service businesses depend on digital request forms. If submission fails, customers and revenue are lost. CPU dashboards alone do not answer: *Can customers submit requests right now?*

## Business value

- Persist and manage customer service requests
- Measure the real customer submission journey
- Alert on user-impacting failure rates
- Automatically diagnose and remediate a known demo failure mode safely
- Keep an audit trail of detection → recovery → verification

## Main features

- Customer service request form with validation
- Service request dashboard (status + recent submissions)
- Reliability dashboard (success rate, incidents, remediation)
- Controlled demo failure injection (authorized, demo-gated)
- Prometheus user-impact alert → Alertmanager → runtime responder
- Allowlisted recovery (`DISABLE_DEMO_FAILURE_MODE`) + synthetic verification
- OpenTelemetry traces, Prometheus metrics, structured JSON logs, Grafana dashboards

## Architecture

See `docs/architecture.md` for the component diagram and API contracts.

```
React UI → FastAPI Backend → PostgreSQL
                ↓
         OTel Collector → Prometheus / Tempo → Grafana
                ↓
         Alertmanager → Responder → allowlisted recovery → verify
```

## Tech stack

React, TypeScript, Vite, TanStack Query, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, OpenTelemetry, Prometheus, Grafana, Alertmanager, Tempo, Docker Compose, GitHub Actions.

## Screenshots

Capture live screenshots after startup into `docs/evidence/` (do not invent images). Suggested:

- Request form success
- Requests dashboard
- Grafana Service Request Journey
- Firing Prometheus alert
- Resolved incident on Reliability dashboard

## One-command local startup

```powershell
.\scripts\start-local.ps1
```

Equivalent: `docker compose up --build -d`

| Service | URL |
|---------|-----|
| Application UI | http://localhost:8088 |
| Backend API / docs | http://localhost:8000/docs |
| Grafana | http://localhost:3000 (admin/admin) |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |
| Responder health | http://localhost:8080/health |

## Tests

```powershell
.\scripts\test-all.ps1
```

## Demo incident walkthrough

```powershell
.\scripts\demo-incident.ps1
```

Full narration: `docs/demo-script.md`.

## Observability

- Grafana dashboard: **Service Request Journey** (auto-provisioned)
- Metrics: `service_request_submissions_total`, failures, duration, incidents, remediations
- Traces: OTLP → Collector → Tempo
- Logs: structured JSON on stdout (no customer PII fields)

## Responder agent

Runtime service (`responder`) receives Alertmanager webhooks, deduplicates by fingerprint, classifies the known demo fault, executes only allowlisted action `DISABLE_DEMO_FAILURE_MODE`, verifies with a synthetic request, and persists incident/remediation/audit records via the backend. Optional Groq explanations are narrative-only and disabled by default.

## Deployment / CI/CD / rollback

- `docs/deployment.md` — VM + Compose plan (**public deploy NOT VERIFIED** in this build)
- `docs/ci-cd.md` — GitHub Actions CI + safe-skip CD
- `docs/rollback.md` — SHA-based rollback

## Agent team and task tracker

- `docs/agent-team.md`, `docs/agent-process.md`, `AGENTS.md`
- Local tracker: `docs/task-tracker.md`
- GitHub import templates: `docs/github-issues-import.md` (publish after second-laptop push)

## Acceptance criteria

See `docs/acceptance-criteria.md` (AC-001–AC-025).

## Limitations

- Single known automated remediation path (demo failure mode)
- Local Compose observability ports are open for learning; harden for public deploy
- Groq is optional and not used for action selection
- Public cloud deployment requires credentials not present in this session
- Public GitHub task tracker exists only after you publish issues

## Future improvements

- Additional allowlisted remediations with stronger policy controls
- SSO for admin/demo controls
- Long-term log store (Loki)
- Multi-service journey SLOs

## Course rubric evidence

See `docs/rubric-evidence.md`.

## Second-laptop transfer

```powershell
.\scripts\package-transfer.ps1
.\scripts\verify-transfer.ps1 -ZipPath .\transfer-output\<zip-name>.zip
```

Follow `docs/second-laptop-setup.md` to extract, run, init git, and push to a **new** GitHub repository/account.
