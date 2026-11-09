# Second-Laptop Setup — Service Reliability Copilot

This project was packaged for transfer. Use a **different GitHub account** on the second laptop. Do not reuse credentials from the first machine.

## 1. Extract

```powershell
Expand-Archive -Path ".\service-reliability-copilot-YYYYMMDD-HHMMSS.zip" -DestinationPath "C:\src\service-reliability-copilot"
cd C:\src\service-reliability-copilot
```

## 2. Prerequisites

- Windows 10/11
- Docker Desktop running
- PowerShell 5+ / 7+
- Optional for local non-Docker tests: Python 3.12, Node.js 20

## 3. Configure environment

```powershell
Copy-Item .env.example .env
# Edit tokens if desired (keep Alertmanager webhook token in sync with observability/alertmanager/alertmanager.yml)
```

## 4. Start stack

```powershell
.\scripts\start-local.ps1
```

Or:

```powershell
docker compose up --build -d
```

Verify:

- http://localhost:8088
- http://localhost:8000/health
- http://localhost:3000
- http://localhost:9090
- http://localhost:9093

## 5. Run tests

```powershell
.\scripts\test-all.ps1
```

## 6. Demo incident

```powershell
.\scripts\demo-incident.ps1
```

## 7. Initialize a NEW Git repository (placeholders)

```powershell
git init
git branch -M main
git config user.name "YOUR_NEW_GITHUB_USERNAME"
git config user.email "YOUR_NEW_EMAIL@example.com"
git add .
git commit -m "Initial commit: Service Reliability Copilot"
```

## 8. Create GitHub repo and push (second laptop only)

```powershell
# After creating an empty repo in the new GitHub account:
git remote add origin https://github.com/YOUR_NEW_GITHUB_USERNAME/YOUR_NEW_REPO.git
git push -u origin main
```

## 9. Publish task tracker issues

Use `docs/github-issues-import.md` to create GitHub Issues.  
Only then claim a publicly accessible task tracker.

## 10. Optional: configure CD secrets

See `docs/ci-cd.md` for `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`.
