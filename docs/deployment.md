# Deployment — Service Reliability Copilot

## Recommended topology

Single Linux VM + Docker Compose + reverse proxy (Caddy or Nginx) + HTTPS.

Estimated low-cost footprint: 1 vCPU / 2–4 GB RAM VM is enough for the MVP stack.

## Prerequisites

- Docker Engine + Compose plugin
- DNS record pointing to the VM
- Firewall allowing 80/443 only publicly; keep Prometheus/Alertmanager/Admin ports private or VPN-only

## Secrets handling

1. Copy `.env.example` to `.env` on the server.
2. Replace all `*-change-me` tokens.
3. Ensure `.env` is not committed.
4. Restrict file mode: `chmod 600 .env`.

## Startup

```bash
cp .env.example .env
# edit secrets
docker compose up --build -d
docker compose ps
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/ready
```

Backend entrypoint runs Alembic migrations automatically.

## Reverse proxy (example Caddy)

```caddy
service.example.com {
  reverse_proxy frontend:80
}

api.service.example.com {
  reverse_proxy backend:8000
}
```

Do **not** expose `/api/v1/demo/*`, `/api/v1/internal/*`, Prometheus, or Alertmanager on the public internet without additional auth / network controls.

## Verification checklist

- [ ] `/health` and `/ready` return OK
- [ ] Submit a service request through the UI
- [ ] Row appears in PostgreSQL / Requests dashboard
- [ ] `/metrics` scraped by Prometheus
- [ ] Grafana dashboard shows traffic after submissions
- [ ] Demo incident script recovers successfully on a private network

## Backup

- Named volume `src_pgdata`
- Periodic `pg_dump` (see `docs/rollback.md`)

## Cost considerations

- One small VM + volume storage
- Optional Groq API only if narrative summaries are enabled
- No Kubernetes control plane cost

## Deployment status for this repository build

**NOT VERIFIED** — no public URL and no cloud VM credentials were available during project creation. All deployment files and commands are prepared for use from the second laptop.
