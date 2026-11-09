# Agent Process — Service Reliability Copilot

## Handoff pipeline

```
Specification → Task → Implementation → Test → Review → Evidence → Done
```

### 1. Specification

- Product Architect updates product spec, AC, architecture, ADRs.
- Output: stable AC IDs and scope boundaries.

### 2. Task

- Architect (or implementing agent) creates/updates a row in `docs/task-tracker.md`.
- Task must reference one or more AC IDs, an owner agent, and a clear definition of done.
- Optional: publish as GitHub Issue using `docs/github-issues-import.md` (after repo creation on second laptop).

### 3. Implementation

- Owner agent implements only the scoped change.
- No secrets committed; contracts stay versioned under `/api/v1`.

### 4. Test

- QA Agent (or owner) adds/updates automated tests.
- Run `.\scripts\test-all.ps1` or the relevant subset.
- Failure blocks Done.

### 5. Review

- Cross-role checklist: AC coverage, safety boundaries, observability impact, docs update.

### 6. Evidence

- Record commands, outputs, screenshots (when available), and file paths under `docs/evidence/`.
- Update task tracker Test Evidence and Status fields.
- Update `docs/rubric-evidence.md` verification status honestly (Verified / Partially Verified / Not Verified).

### 7. Done

- Status = Done only when tests pass and evidence is linked.
- Do not mark public task-tracker credit until GitHub Issues are actually published.

---

## Distinguishing development roles vs runtime responder

| | Development agents | Runtime responder |
|--|--------------------|-------------------|
| Where | Cursor / human workflow | Docker service `responder` |
| Trigger | Developer task assignment | Alertmanager webhook |
| Output | Code, tests, docs | Incident records + remediation |
| LLM use | Optional coding assistance | Optional Groq narrative only |

---

## Change control

- Breaking API changes require AC update + test update in the same change set.
- New remediation actions require allowlist update + safety review note in an ADR.
