# Rollback Procedure

## Principle

Deploy immutable image tags (`<git-sha>`), never rely on `latest` alone.

## Local / Compose rollback

1. Identify previous known-good commit SHA.
2. Check out that commit (or set image tags to that SHA).
3. Redeploy:

```powershell
git checkout <known-good-sha>
docker compose up --build -d
```

4. Verify:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8000/ready
```

5. Confirm a test request succeeds:

```powershell
# POST /api/v1/requests with a valid payload
```

## Database considerations

- Prefer forward-safe Alembic migrations.
- If a migration must be reversed, run `alembic downgrade -1` only after backup and only when the downgrade path is tested.
- Application rollback without DB downgrade is preferred when schema remains compatible.

## Backup before risky changes

```bash
docker compose exec postgres pg_dump -U src_user src_db > backup-$(date +%Y%m%d).sql
```

## CD rollback (when secrets exist)

Re-run the CD workflow with `image_tag` set to the previous known-good SHA via `workflow_dispatch`.

## Status

Procedure documented. Remote production rollback: **NOT VERIFIED** (no deployed environment in this session).
