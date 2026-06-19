# Plan — health-smoke as the canonical Verify gate

> **Golden artifact (filled, real).** Phase 2. Pattern source:
> `.github/prompts/punch-plan.prompt.md`. Caveman `full`.

- **Goal** (from Spec): trackable pass/fail evidence from health smoke
  via one official command. No product code change.

## Tasks

### V-01 — run the health smoke and capture evidence
- **Goal** — run `./bin/punch run smoke`, confirm acceptance criteria.
- **Allowed edit paths** — _none_ (verify-only; no source edits).
- **Read-only context paths** — `src/tests/smoke.ts`, `docker-compose.yml`,
  `reports/**`.
- **Forbidden paths** — `src/**` edits, `docker/**`, `docker-compose.yml` edits,
  `.github/**` (task change nothing).
- **Expected diff size** — 0 lines (evidence only).
- **Validation commands** — `./bin/punch doctor` then `./bin/punch run smoke`.
- **Rollback notes** — none needed (no mutation); `./bin/punch clean` reset stack.
- **Human checkpoint** — human approval required before Build.
- **Build prompt** — `punch-build` (expect no-op — verify-class task).

## Order of execution
Single task. (Integration changes would order k6 → compose → orchestrator.)

## Cross-cutting risks
- Environment-only: Docker daemon down or stack unhealthy → classify as
  *environment*, not implementation.

## Rollback plan
No code mutation; nothing to roll back. `./bin/punch clean` tears down containers.

**Gate:** ✅ confirmed → Build (task V-01).
