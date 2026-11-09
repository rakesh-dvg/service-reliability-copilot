# ADR 0003 — Persist demo failure flag in PostgreSQL

**Status:** Accepted  
**Date:** 2026-11-09  
**Owner:** Backend Agent

## Context

The demo failure flag must be visible to both the API process and the responder recovery path, and must survive API worker restarts during demos.

## Decision

Store the flag in a `runtime_settings` table (`key`, `value`, `updated_at`) with key `demo_failure_mode_enabled`.

## Consequences

- Cross-process consistency without Redis.
- Responder can disable the flag via authenticated internal API that updates the same row.
