# Agent Team Specification — Service Reliability Copilot

This document defines **development-time agent roles** used while building the product, and separately describes the **runtime Incident Responder Agent** that operates inside the deployed system.

These are not the same thing. Cursor may simulate development roles sequentially; the runtime responder is a real FastAPI service.

---

## Development-time agents

### Product Architect Agent

**Owns:** requirements, architecture, acceptance criteria, scope, ADRs, rubric mapping.

**Does not own:** production code changes unless clarifying contracts.

**Handoff out:** approved AC IDs + architecture + prioritized tasks in the task tracker.

---

### Backend Agent

**Owns:** FastAPI, PostgreSQL, SQLAlchemy, Alembic, API contracts, business logic, metrics instrumentation on the API path, demo fault flag, internal recovery interface.

**Acceptance criteria focus:** AC-001–AC-005, AC-014, AC-021–AC-022, AC-024.

---

### Frontend Agent

**Owns:** React + TypeScript UI, forms, dashboards, TanStack Query, Vitest / RTL tests.

**Acceptance criteria focus:** AC-001, AC-004, AC-023, AC-024 (UI gating).

---

### QA Agent

**Owns:** unit, integration, e2e/smoke, failure-mode, and regression tests; `scripts/test-all.ps1`; CI test jobs.

**Acceptance criteria focus:** AC-017, AC-018, plus verification of all functional ACs.

---

### SRE Agent

**Owns:** Dockerfiles, Compose, OTel Collector, Prometheus, Grafana, Alertmanager, Tempo, GitHub Actions, deployment/rollback docs, runbooks.

**Acceptance criteria focus:** AC-006–AC-010, AC-016, AC-018–AC-020, AC-025.

---

### Incident Responder Agent (development role for responder code)

**Owns:** responder service design, classifier, allowlist, idempotency, verification, audit trail, optional Groq explanation (non-authoritative).

**Acceptance criteria focus:** AC-011–AC-015, AC-020.

---

## Runtime agent (production behavior)

### Runtime Incident Responder Service

Wakes on Alertmanager webhook delivery. Responsibilities:

1. Authenticate alert
2. Deduplicate by fingerprint
3. Create/update incident
4. Gather bounded diagnostics
5. Identify known demo fault
6. Select allowlisted recovery action
7. Execute recovery
8. Synthetic request verification
9. Resolve or escalate
10. Persist audit trail

**Safety:** no arbitrary shell; no DB deletes; no credential changes; bounded retries; cooldown; escalation on failure.

---

## Responsibility matrix (RACI summary)

| Area | Architect | Backend | Frontend | QA | SRE | Responder |
|------|-----------|---------|----------|----|-----|-----------|
| Product spec / AC | A/R | C | C | C | C | C |
| API + DB | C | A/R | C | C | I | C |
| UI | C | C | A/R | C | I | I |
| Tests | C | C | C | A/R | C | C |
| Observability stack | C | C | I | C | A/R | C |
| Runtime remediation | C | C | I | C | C | A/R |

R = Responsible, A = Accountable, C = Consulted, I = Informed
