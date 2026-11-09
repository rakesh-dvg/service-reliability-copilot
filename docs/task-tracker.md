# Task Tracker — Service Reliability Copilot

Local working tracker. **Not yet publicly accessible** until published as GitHub Issues from the second laptop using `docs/github-issues-import.md`.

**Status values:** Todo | In Progress | Review | Done | Blocked

| Task ID | Title | Owner | AC | Status | Implementation notes | Test evidence | Refs |
|---------|-------|-------|----|--------|----------------------|---------------|------|
| T-001 | Product spec and acceptance criteria | Architect | AC-001–AC-025 | Done | Spec docs created | Spec review | `docs/product-spec.md` |
| T-002 | Architecture and agent process | Architect | AC-016, AC-019 | Done | Architecture + agent docs | Spec review | `docs/architecture.md` |
| T-003 | Backend models, migrations, APIs | Backend | AC-001–AC-005, AC-021–AC-022, AC-024 | Done | FastAPI + Alembic | 11 backend pytest | `backend/` |
| T-004 | Frontend request form and dashboards | Frontend | AC-001, AC-004, AC-023 | Done | React + Vite | 4 vitest (via Docker) | `frontend/` |
| T-005 | Unit and integration tests | QA | AC-017 | Done | pytest + vitest + scripts | backend 11, responder 3, frontend 4 | `scripts/test-all.ps1` |
| T-006 | Docker Compose one-command start | SRE | AC-016 | Done | Compose + start script | `docker compose up --build -d` healthy | `docker-compose.yml` |
| T-007 | Observability stack and dashboards | SRE | AC-006–AC-008 | Done | OTel/Prom/Grafana/Tempo | traces in collector; Grafana DS provisioned | `observability/` |
| T-008 | User-impact alert + Alertmanager | SRE | AC-009–AC-010 | Done | Demo alert fired | `docs/evidence/20261109-demo-incident.md` | `observability/prometheus` |
| T-009 | Runtime responder service | Responder | AC-011–AC-015 | Done | Allowlisted recovery verified | incident resolved + verified | `responder/` |
| T-010 | CI/CD workflows and rollback docs | SRE | AC-018–AC-019 | Done | Workflows prepared | Files present; remote CD NOT VERIFIED | `.github/workflows` |
| T-011 | Demo script and runbooks | Architect | AC-020 | Done | Demo walkthrough | demo script exit 0 | `docs/demo-script.md` |
| T-012 | Transfer ZIP and second-laptop docs | SRE | AC-025 | Done | Packaging scripts | verify-transfer after fix | `scripts/package-transfer.ps1` |
| T-013 | Rubric evidence mapping | Architect | All | Done | Honest statuses | `docs/rubric-evidence.md` | `docs/rubric-evidence.md` |

---

## Update log

| Date | Change |
|------|--------|
| 2026-11-09 | Tracker initialized through completion; demo incident verified locally |
