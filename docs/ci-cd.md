# CI/CD — Service Reliability Copilot

## CI (`.github/workflows/ci.yml`)

Triggers: pull requests and pushes to `main`/`master`.

Jobs:

1. Backend — Ruff + pytest
2. Responder — pytest
3. Frontend — Vitest + production build
4. Docker — `docker compose config` + image builds

No secrets are required for CI.

## CD (`.github/workflows/cd.yml`)

Triggers:

- `workflow_dispatch` (manual production/development deploy)
- push to `main`/`master` (development intent)

Behavior:

- Uses immutable tag = commit SHA (or manual input)
- If `DEPLOY_HOST`, `DEPLOY_USER`, and `DEPLOY_SSH_KEY` are missing, the workflow **skips deployment safely** and reports the skip
- Never prints secret values

### Required GitHub secrets (when ready to deploy)

| Secret | Purpose |
|--------|---------|
| `DEPLOY_HOST` | VM hostname/IP |
| `DEPLOY_USER` | SSH user |
| `DEPLOY_SSH_KEY` | Private key |
| `DEPLOY_PATH` | Optional remote project path |

### Required variables / env on the VM

Mirror `.env.example` on the host. Do not store production secrets in the repository.

## Status

**Deployment from this development laptop: NOT VERIFIED** (no target VM credentials configured in this build session).
