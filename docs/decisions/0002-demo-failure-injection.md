# ADR 0002 — Controlled demo failure injection

**Status:** Accepted  
**Date:** 2026-11-09  
**Owner:** Product Architect Agent / SRE Agent

## Context

We need a reproducible customer-impacting failure for alerting and responder demos without unsafe chaos tooling.

## Decision

- Provide an explicit demo fault: when enabled, `POST /api/v1/requests` returns HTTP 503.
- Disabled by default.
- Requires `DEMO_MODE=true` and admin token to enable.
- Responder remediates only via allowlisted action `DISABLE_DEMO_FAILURE_MODE` through an internal recovery endpoint authenticated with a recovery token.
- No arbitrary code execution, no destructive DB operations.

## Consequences

- Deterministic demos for AC-005 and AC-009–AC-015.
- Clear safety boundary for course reviewers.
