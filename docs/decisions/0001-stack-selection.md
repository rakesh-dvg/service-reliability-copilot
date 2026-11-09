# ADR 0001 — Technology stack selection

**Status:** Accepted  
**Date:** 2026-11-09  
**Owner:** Product Architect Agent

## Context

Project 2 requires a full-stack application with observability, alerting, and an on-call responder, deliverable as a portable Docker Compose project on Windows.

## Decision

Use:

- Frontend: React + TypeScript + Vite + TanStack Query + Vitest
- Backend: Python 3.12 + FastAPI + SQLAlchemy 2 + Alembic + PostgreSQL
- Responder: Python FastAPI service
- Observability: OpenTelemetry + Collector + Prometheus + Grafana + Alertmanager + Tempo
- Deployment: Docker Compose (single host), GitHub Actions for CI/CD

## Consequences

- Small, maintainable surface area suitable for course MVP.
- No Kubernetes complexity.
- Groq remains optional and non-authoritative for remediation.
