# Product Specification — Service Reliability Copilot

**Tagline:** From User-Impact Detection to AI-Assisted Incident Recovery

**Version:** 1.0  
**Status:** Approved for implementation  
**Owner:** Product Architect Agent

---

## 1. Problem statement

Small service businesses rely on digital request forms to receive customer work. When a customer submits a service request and the backend fails, the business may lose that customer. Infrastructure metrics such as CPU utilization alone do not tell the business whether customers can complete their requests.

## 2. Business value

| Stakeholder | Value |
|-------------|-------|
| Customer | Reliable request submission; faster recovery when failures occur |
| Service business | Visibility into real customer-impacting failures; reduced lost work |
| On-call operator | Automated diagnosis and safe remediation for a known failure mode |
| Reviewer / course assessor | End-to-end, reproducible incident demonstration |

## 3. Product goals

1. Accept and persist customer service requests.
2. Display requests and operational status in a clear web UI.
3. Measure success and failure of the request-submission journey.
4. Detect customer-impacting failures via Prometheus alerting.
5. Create actionable incidents and notify an automated responder.
6. Diagnose a known demo failure mode and apply an allowlisted recovery action.
7. Verify the customer journey works again after remediation.
8. Preserve a full audit trail.
9. Remain useful when no incident is occurring (normal request workflow).

## 4. Out of scope (MVP)

- Multi-tenant SaaS billing
- Arbitrary LLM-generated shell or infrastructure changes
- Kubernetes orchestration
- Full CMDB / ITSM integration
- Real mobile apps
- Payment processing

## 5. Personas

- **Customer:** Submits a service request via the web form.
- **Service coordinator:** Views and updates request status on the dashboard.
- **Reliability operator:** Reviews reliability metrics, incidents, and Grafana.
- **Automated responder:** Runtime agent that receives alerts and remediates the known demo fault.

## 6. Core user journeys

### Journey A — Happy path request submission

1. Customer opens the request form.
2. Customer fills required fields and submits.
3. Backend validates and persists to PostgreSQL.
4. UI confirms success and shows the request on the dashboard.
5. Metrics and traces record a successful submission.

### Journey B — Controlled failure and recovery

1. Demo operator enables failure injection (authorized).
2. Customer submissions return HTTP 503.
3. Metrics show elevated failure rate.
4. Prometheus fires a user-impact alert.
5. Alertmanager delivers the alert to the responder webhook.
6. Responder deduplicates, creates an incident, diagnoses demo fault.
7. Responder executes `DISABLE_DEMO_FAILURE_MODE`.
8. Responder runs a synthetic request and verifies success.
9. Incident is marked resolved; audit trail is persisted.
10. UI reliability dashboard reflects recovery.

## 7. Functional requirements

See `docs/acceptance-criteria.md` (AC-001 through AC-025).

## 8. Non-functional requirements

- Portable single-host Docker Compose deployment.
- No hardcoded secrets; configuration via environment variables.
- Structured JSON logging without PII in logs or metric labels.
- Deterministic recovery without requiring paid AI APIs.
- One-command local startup and one-command test execution.
- Safe demo fault injection only when explicitly enabled.

## 9. Success metrics (product)

- Request submission success rate visible in Grafana.
- Mean time to detect (demo alert fires within configured window).
- Mean time to remediate known demo fault (responder completes allowlisted action).
- Zero uncontrolled remediations for duplicate alerts (idempotency / cooldown).
