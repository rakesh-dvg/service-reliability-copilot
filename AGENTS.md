# AGENTS.md — Service Reliability Copilot

Guidance for AI coding agents working in this repository.

## Project identity

- **Name:** Service Reliability Copilot
- **Tagline:** From User-Impact Detection to AI-Assisted Incident Recovery
- **Course:** AI Dev Tools Zoomcamp 2026 — Project 2
- **Independent of:** Industrial Engineering Copilot (Project 1)

## Non-negotiables

1. Do not copy Project 1 code, branding, DB, or git history.
2. Do not commit secrets (`.env`, API keys, tokens).
3. Do not initialize git push or claim public deployment without verification.
4. Do not invent evidence; mark Unverified when checks did not run.
5. Do not allow LLM output to become unrestricted executable actions.
6. Prefer Docker Compose single-host architecture; no Kubernetes for MVP.
7. Every implementation task must reference acceptance criteria in `docs/acceptance-criteria.md`.

## Role routing

| Work type | Owner |
|-----------|-------|
| Specs, AC, ADRs, scope | Product Architect |
| FastAPI, Postgres, Alembic | Backend |
| React UI | Frontend |
| Tests / CI test jobs | QA |
| Compose, Prometheus, Grafana, Actions, deploy docs | SRE |
| Alert webhook, remediation, audit | Incident Responder (dev) / runtime `responder` service |

## Process

Follow `docs/agent-process.md`: Specification → Task → Implementation → Test → Review → Evidence → Done.

Update `docs/task-tracker.md` continuously.

## Local commands (Windows)

```powershell
.\scripts\start-local.ps1
.\scripts\test-all.ps1
.\scripts\demo-incident.ps1
.\scripts\stop-local.ps1
```

## Safety for remediation

Allowlisted recovery action for the demo: `DISABLE_DEMO_FAILURE_MODE` only via authenticated internal recovery interface.
