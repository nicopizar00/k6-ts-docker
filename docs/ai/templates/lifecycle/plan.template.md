# Plan — <topic>

> **Template.** Copy to `docs/architecture/specs/plan-<topic>.md`.
> Pattern source: `.github/prompts/punch-plan.prompt.md` (Caveman `full`).

- **Goal** (from Spec): <one sentence>

## Tasks

### <Task ID — e.g. O-01 / C-01 / K-01 / B-01 / D-01>
- **Goal** — <one sentence>
- **Allowed edit paths** — <globs>
- **Read-only context paths** — <globs>
- **Forbidden paths** — <globs; must include every layer the task does not own>
- **Expected diff size** — <~N lines>
- **Validation commands** — <official `./bin/punch …` commands Verify will run>
- **Rollback notes** — <how to undo if Verify fails>
- **Human checkpoint** — human approval required before Build
- **Build prompt** — `punch-build`

## Order of execution
<typically k6 → compose → orchestrator for integration changes>

## Cross-cutting risks
<single section for risks that span tasks>

## Rollback plan
<for the whole change>

**Gate:** approved when a human confirms it → Build (per task ID).
