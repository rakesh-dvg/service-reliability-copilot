# GitHub Issues Import — Service Reliability Copilot

Use these templates after creating the **new** GitHub repository from the second laptop.  
Do **not** claim the public task tracker is live until these issues exist in the remote repository.

Suggested labels: `phase-1-spec`, `backend`, `frontend`, `qa`, `sre`, `responder`, `docs`, `acceptance-criteria`

---

## Issue: T-001 Product specification and acceptance criteria

**Title:** `[T-001] Product specification and acceptance criteria`

**Labels:** `phase-1-spec`, `docs`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Define product scope, business problem, and stable acceptance criteria IDs.

## Acceptance criteria
- AC-001 through AC-025 documented with testable wording
- Product spec covers journeys A (happy path) and B (failure/recovery)

## Definition of done
- [ ] `docs/product-spec.md` merged
- [ ] `docs/acceptance-criteria.md` merged
- [ ] Linked from README
```

---

## Issue: T-002 Architecture and agent team

**Title:** `[T-002] Architecture, agent team, and process`

**Labels:** `phase-1-spec`, `docs`

**Body:**

```markdown
## Summary
Document system architecture, development agent roles vs runtime responder, and handoff process.

## Acceptance criteria
- AC-016, AC-019 architecture/deployment intent documented

## Definition of done
- [ ] `docs/architecture.md`
- [ ] `docs/agent-team.md`
- [ ] `docs/agent-process.md`
- [ ] `AGENTS.md`
```

---

## Issue: T-003 Backend APIs and persistence

**Title:** `[T-003] Backend models, Alembic migrations, and versioned APIs`

**Labels:** `backend`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Implement FastAPI service with PostgreSQL persistence for service requests, incidents, remediations, and audit events.

## Acceptance criteria
- AC-001, AC-002, AC-003, AC-005, AC-021, AC-022, AC-024

## Definition of done
- [ ] Alembic migrations (no create_all as production init)
- [ ] Versioned `/api/v1` endpoints
- [ ] Demo failure injection gated
- [ ] Unit/integration tests passing
```

---

## Issue: T-004 Frontend UI

**Title:** `[T-004] React request form and dashboards`

**Labels:** `frontend`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Build customer request form, service request dashboard, reliability dashboard, and gated demo controls.

## Acceptance criteria
- AC-001, AC-004, AC-023, AC-024

## Definition of done
- [ ] Form validation UX
- [ ] Dashboards render live API data
- [ ] Frontend tests passing
```

---

## Issue: T-005 Automated tests

**Title:** `[T-005] Unit, integration, and frontend tests with single-command runner`

**Labels:** `qa`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Provide comprehensive automated tests and `scripts/test-all.ps1`.

## Acceptance criteria
- AC-017

## Definition of done
- [ ] Backend unit + integration tests
- [ ] Frontend Vitest/RTL tests
- [ ] One-command test script documented
```

---

## Issue: T-006 Docker Compose startup

**Title:** `[T-006] One-command Docker Compose local stack`

**Labels:** `sre`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Containerize all services with health checks and automatic migrations.

## Acceptance criteria
- AC-016

## Definition of done
- [ ] `docker compose up --build -d` starts full stack
- [ ] `scripts/start-local.ps1` documented
```

---

## Issue: T-007 Observability

**Title:** `[T-007] Correlated logs, metrics, traces, and Grafana dashboards`

**Labels:** `sre`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Instrument request journey; provision Prometheus, Tempo, Grafana dashboards.

## Acceptance criteria
- AC-006, AC-007, AC-008

## Definition of done
- [ ] Structured JSON logs with trace_id
- [ ] Prometheus metrics scraped
- [ ] Grafana dashboards show real data after traffic
```

---

## Issue: T-008 Alerting

**Title:** `[T-008] User-impact Prometheus alert and Alertmanager webhook`

**Labels:** `sre`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Alert on failing request-submission journey; route to responder.

## Acceptance criteria
- AC-009, AC-010

## Definition of done
- [ ] Alert rule based on submission failure ratio
- [ ] Demo-accelerated config available
- [ ] Alertmanager delivers to responder webhook
```

---

## Issue: T-009 Runtime responder

**Title:** `[T-009] Incident responder with allowlisted recovery`

**Labels:** `responder`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Implement runtime responder: authenticate, dedupe, diagnose, remediate, verify, audit.

## Acceptance criteria
- AC-011, AC-012, AC-013, AC-014, AC-015

## Definition of done
- [ ] `DISABLE_DEMO_FAILURE_MODE` allowlisted only
- [ ] Idempotent handling / cooldown
- [ ] Synthetic verification after recovery
```

---

## Issue: T-010 CI/CD and rollback

**Title:** `[T-010] GitHub Actions CI/CD and rollback procedure`

**Labels:** `sre`, `acceptance-criteria`

**Body:**

```markdown
## Summary
CI on PR/push; CD prepared with SHA tags; rollback documented.

## Acceptance criteria
- AC-018, AC-019

## Definition of done
- [ ] CI workflow runs lint/tests/build
- [ ] CD skips safely without secrets
- [ ] `docs/rollback.md` complete
```

---

## Issue: T-011 Demo script

**Title:** `[T-011] Demo script and incident runbook`

**Labels:** `docs`, `acceptance-criteria`

**Body:**

```markdown
## Summary
5–7 minute demo plus 3-minute fallback with exact commands.

## Acceptance criteria
- AC-020

## Definition of done
- [ ] `docs/demo-script.md`
- [ ] `docs/runbooks/` incident runbook
- [ ] `scripts/demo-incident.ps1`
```

---

## Issue: T-012 Portability package

**Title:** `[T-012] Transfer ZIP and second-laptop setup`

**Labels:** `sre`, `docs`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Package portable ZIP excluding secrets and local artifacts.

## Acceptance criteria
- AC-025

## Definition of done
- [ ] `scripts/package-transfer.ps1`
- [ ] `scripts/verify-transfer.ps1`
- [ ] `docs/second-laptop-setup.md`
```

---

## Issue: T-013 Rubric evidence

**Title:** `[T-013] Rubric evidence matrix with honest verification status`

**Labels:** `docs`, `acceptance-criteria`

**Body:**

```markdown
## Summary
Map course rubric criteria to files, commands, and evidence without inventing results.

## Definition of done
- [ ] `docs/rubric-evidence.md`
- [ ] Statuses are Verified / Partially Verified / Not Verified only as appropriate
```
