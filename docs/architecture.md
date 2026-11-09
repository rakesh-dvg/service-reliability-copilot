# Architecture — Service Reliability Copilot

## 1. Overview

Service Reliability Copilot is a single-host Docker Compose application that accepts customer service requests, measures the success of that journey, alerts on customer impact, and runs an automated responder that remediates a known demo failure mode.

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│  React UI   │────▶│   FastAPI    │────▶│ PostgreSQL │
│  (Vite)     │     │   Backend    │     │            │
└─────────────┘     └──────┬───────┘     └────────────┘
                           │
              OTel traces / metrics / logs
                           │
                           ▼
                 ┌─────────────────┐
                 │ OTel Collector  │
                 └────────┬────────┘
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │ Prometheus │  │   Tempo    │  │   Loki*    │
   └─────┬──────┘  └─────┬──────┘  └────────────┘
         │               │
         ▼               ▼
   ┌────────────┐  ┌────────────┐
   │Alertmanager│  │  Grafana   │
   └─────┬──────┘  └────────────┘
         │ webhook
         ▼
   ┌────────────┐
   │ Responder  │──▶ disable demo fault ──▶ synthetic verify
   └────────────┘
```

\* Loki is optional; structured logs are always emitted to stdout for container collection. Tempo holds traces. Prometheus holds metrics.

## 2. Components

| Component | Responsibility |
|-----------|----------------|
| `frontend` | React + TypeScript UI: request form, request dashboard, reliability dashboard, demo controls (gated) |
| `backend` | FastAPI APIs, validation, persistence, metrics, demo fault flag, recovery interface |
| `responder` | Alert webhook, incident lifecycle, allowlisted remediation, verification |
| `postgres` | Durable storage for requests, incidents, remediations, audit events |
| `otel-collector` | Receives OTLP; exports metrics to Prometheus, traces to Tempo |
| `prometheus` | Scrapes metrics; evaluates user-impact alert rules |
| `alertmanager` | Routes firing alerts to responder webhook |
| `tempo` | Trace storage |
| `grafana` | Dashboards for journey metrics and traces |

## 3. API surface (versioned)

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/health` | none | Liveness |
| GET | `/ready` | none | Readiness (DB) |
| GET | `/metrics` | none (internal network) | Prometheus scrape |
| GET/POST | `/api/v1/requests` | none (public form) | List / create requests |
| GET | `/api/v1/requests/{id}` | none | Get request |
| PATCH | `/api/v1/requests/{id}/status` | admin token | Status transition |
| GET | `/api/v1/incidents` | none (read) | List incidents |
| GET | `/api/v1/incidents/{id}` | none (read) | Get incident |
| GET | `/api/v1/reliability/summary` | none | Reliability KPIs |
| POST | `/api/v1/demo/failure/enable` | admin + demo mode | Inject 503 |
| POST | `/api/v1/demo/failure/disable` | admin or internal recovery token | Clear fault |
| POST | `/api/v1/internal/recovery/disable-demo-failure` | recovery token | Responder-only recovery |
| POST | `/api/v1/alerts/webhook` | webhook token | Optional direct alert intake on backend (primary path is responder) |

Responder:

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/health` | none | Liveness |
| POST | `/webhook/alertmanager` | webhook token | Alertmanager receiver |
| GET | `/incidents` | none (read, local) | Local view of handled incidents |

## 4. Data model

See Alembic migrations for authoritative schema.

- `service_requests` — customer work items
- `incidents` — alert-derived incident records
- `remediation_actions` — allowlisted actions taken
- `audit_events` — immutable operational events

## 5. Failure injection model

- In-memory / DB-backed flag `demo_failure_mode_enabled` (persisted via backend settings table or Redis-free process state shared via DB).
- When enabled, `POST /api/v1/requests` returns HTTP 503 with a structured error.
- Disabled by default; requires `DEMO_MODE=true` and `ADMIN_API_TOKEN`.
- Responder recovery action: `DISABLE_DEMO_FAILURE_MODE` via internal recovery endpoint.

## 6. Observability design

- **Logs:** JSON to stdout; fields include timestamp, level, service_name, request_id, trace_id, route, response_status, duration_ms. No PII.
- **Metrics:** Counters and histograms with bounded labels (`status`, `action_type`, `result`). No customer IDs/emails/request IDs in labels.
- **Traces:** OpenTelemetry instrumentation on HTTP and DB spans; `trace_id` mirrored into logs.

## 7. Security boundaries

- Admin / demo / recovery endpoints require tokens.
- Responder actions are allowlisted; no LLM-executed shell.
- Groq (optional) only for narrative explanation behind a feature flag.
- Secrets via environment variables / Compose secrets; never committed.

## 8. Deployment topology

Prefer single Linux VM + Docker Compose + reverse proxy + HTTPS. Local development uses Compose on Docker Desktop (Windows).

## 9. Decisions

Architecture Decision Records live in `docs/decisions/`.
