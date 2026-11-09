# Rubric Evidence Matrix — Service Reliability Copilot

Statuses are honest for this build session (2026-11-09).

| Rubric area | Relevant files | Implemented functionality | Verification command | Evidence | Status |
|-------------|----------------|---------------------------|----------------------|----------|--------|
| 1. Problem Description | `docs/product-spec.md`, `README.md` | Business problem + value | Doc review | `docs/product-spec.md` | Verified |
| 2. Product Specification | `docs/product-spec.md`, `docs/acceptance-criteria.md` | AC-001–AC-025 | Doc review | `docs/acceptance-criteria.md` | Verified |
| 3. Agent Team Specification | `docs/agent-team.md`, `AGENTS.md` | Dev roles vs runtime responder | Doc review | `docs/agent-team.md` | Verified |
| 4. Context Management | `docs/task-tracker.md`, `docs/agent-process.md`, `docs/decisions/` | Tracker + ADRs + process | Doc review | `docs/task-tracker.md` | Partially Verified (local tracker done; GitHub Issues not published yet) |
| 5. Full-Stack Application | `backend/`, `frontend/`, `docker-compose.yml` | Request form, API, dashboards | `.\scripts\start-local.ps1` | Live stack on :8088/:8000 | Verified |
| 6. Testing | `backend/tests`, `frontend/src/**/*.test.tsx`, `scripts/test-all.ps1` | Unit/integration/frontend | backend pytest; frontend vitest via Docker | 11 + 3 + 4 tests passed | Verified |
| 7. Containerization | Dockerfiles, Compose | One-command start | `docker compose up --build -d` | All key services healthy | Verified |
| 8. Deployment | `docs/deployment.md`, `deploy/` | Plan + templates | Doc review | `docs/deployment.md` | Not Verified (no cloud VM/credentials) |
| 9. CI/CD | `.github/workflows/*`, `docs/ci-cd.md`, `docs/rollback.md` | CI + CD skip-safe | Workflow files present | Files in repo | Partially Verified (not yet executed on GitHub) |
| 10. Observability | `observability/`, backend instrumentation | Logs/metrics/traces + Grafana | submit requests; Grafana DS | Collector traces logged; Prometheus scrape; Grafana datasources | Verified |
| 11. Alerting on User Impact | `observability/prometheus/alerts-demo.yml`, Alertmanager | Journey failure alert | `.\scripts\demo-incident.ps1` | Alert firing + webhook | Verified |
| 12. On-Call Agent | `responder/` | Webhook → diagnose → recover → verify | `.\scripts\demo-incident.ps1` | `docs/evidence/20261109-demo-incident.md` | Verified |
