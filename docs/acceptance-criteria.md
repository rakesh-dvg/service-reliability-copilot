# Acceptance Criteria — Service Reliability Copilot

Stable IDs used by the task tracker, tests, and rubric evidence.

**Status legend:** Pending | Implemented | Verified | Blocked

---

## Application core

| ID | Criterion | Status |
|----|-----------|--------|
| AC-001 | A user can submit a valid service request through the frontend. | Verified |
| AC-002 | The backend persists the request in PostgreSQL. | Verified |
| AC-003 | A submitted request remains available after the backend restarts. | Verified |
| AC-004 | The frontend displays request status and recent submissions. | Verified |
| AC-005 | A controlled failure causes request submission to fail (HTTP 503). | Verified |

## Observability

| ID | Criterion | Status |
|----|-----------|--------|
| AC-006 | The failure generates structured logs, request metrics, and traces with a shared trace ID. | Verified |
| AC-007 | Prometheus collects request success/failure metrics. | Verified |
| AC-008 | Grafana displays the customer request journey. | Partially Verified (dashboard + datasources provisioned; live panels confirmed after traffic) |

## Alerting and responder

| ID | Criterion | Status |
|----|-----------|--------|
| AC-009 | An alert fires when the request-submission journey is failing. | Verified |
| AC-010 | Alertmanager delivers the incident to the responder service. | Verified |
| AC-011 | The responder diagnoses the known injected failure. | Verified |
| AC-012 | The responder applies an allowlisted recovery action. | Verified |
| AC-013 | The responder verifies that a fresh synthetic request succeeds. | Verified |
| AC-014 | Incident status and remediation history are persisted. | Verified |
| AC-015 | Repeated alerts do not cause uncontrolled or repeated remediation. | Implemented (fingerprint dedupe + cooldown + max attempts; regression covered in unit/classifier tests) |

## Delivery and operations

| ID | Criterion | Status |
|----|-----------|--------|
| AC-016 | The complete application starts through one documented command. | Verified |
| AC-017 | Unit and integration tests pass through one documented command. | Verified |
| AC-018 | CI executes tests automatically on pull requests. | Implemented (workflow present; not yet run on GitHub) |
| AC-019 | A deployment and rollback procedure exists and is documented. | Implemented (docs present; remote deploy NOT VERIFIED) |
| AC-020 | A reviewer can reproduce the incident demonstration using documented commands. | Verified |

## Extended criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-021 | Request validation rejects invalid email, missing fields, and invalid priority/category with clear errors. | Verified |
| AC-022 | Service request status transitions follow an allowlisted state machine. | Verified |
| AC-023 | Reliability dashboard shows submission rates, incidents, and recovery metadata. | Verified |
| AC-024 | Demo failure injection is disabled by default and requires authorization / demo mode. | Verified |
| AC-025 | Transfer ZIP is portable, free of secrets, and includes second-laptop setup instructions. | Verified |

---

## Mapping notes

- Every implementation task in `docs/task-tracker.md` references one or more AC IDs.
- Verification commands and evidence paths live in `docs/rubric-evidence.md` and `docs/evidence/`.
