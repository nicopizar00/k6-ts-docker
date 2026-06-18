# Plan — health-smoke as the canonical Verify gate

> **Golden artifact (filled, real).** Phase 2. Pattern source:
> `.github/prompts/punch-plan.prompt.md`. Caveman `full`.

- **Goal** (from Spec): produce trackable pass/fail evidence from the health smoke
  via one official command, changing no product code.

## Tasks

### V-01 — run the health smoke and capture evidence
- **Goal** — execute `./bin/punch run smoke` and confirm the acceptance criteria.
- **Allowed edit paths** — _none_ (verification-only; no source edits).
- **Read-only context paths** — `src/tests/smoke.ts`, `docker-compose.yml`,
  `reports/**`.
- **Forbidden paths** — `src/**` edits, `docker/**`, `docker-compose.yml` edits,
  `.github/**` (this task changes nothing).
- **Expected diff size** — 0 lines (evidence only).
- **Validation commands** — `./bin/punch doctor` then `./bin/punch run smoke`.
- **Rollback notes** — none required (no mutation); `./bin/punch clean` resets the
  stack.
- **Human checkpoint** — human approval required before Build.
- **Build prompt** — `punch-build` (expected no-op — verification-class task).

## Order of execution
Single task. (For integration changes the order would be k6 → compose → orchestrator.)

## Cross-cutting risks
- Environment-only: Docker daemon down or stack unhealthy → classifies as
  *environment*, not implementation.

## Rollback plan
No code mutation; nothing to roll back. `./bin/punch clean` tears down containers.

**Gate:** ✅ confirmed → Build (task V-01).
