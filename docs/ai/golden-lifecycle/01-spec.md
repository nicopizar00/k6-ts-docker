# Spec — health-smoke as the canonical Verify gate

> **Golden artifact (filled, real).** Phase 1 of the worked lifecycle.
> Pattern source: `.github/prompts/punch-spec.prompt.md`. Caveman `lite`.

- **Goal** — Confirm the reference stack's health smoke passes via
  `./bin/punch run smoke`, establishing the smallest re-runnable Verify gate that
  emits trackable evidence.
- **Non-goals**
  - Not adding, renaming, or altering any k6 test or threshold.
  - Not performance-gating (that is `catalog-gate`) or journey validation.
  - Not changing services, Compose, or the orchestrator.
- **Functional requirements**
  - One official command produces a machine-readable pass/fail record.
  - The smoke exercises gateway → catalog/orders health and reports check pass rate.
- **Technical constraints** — Docker-First; runs **only** through `./bin/punch`
  (no host `k6`, no raw `docker run`); orchestrator stays stdlib-only.
- **Affected layers** — k6 tests (`src/tests/smoke.ts`, read-only here) · Python
  orchestrator (runs it) · Artifacts (`reports/**`). See `punch-boundaries.md`.
- **Artifact / log / reporting implications** — writes
  `reports/state/punch-run.json` (canonical evidence) + `reports/smoke.json` +
  `reports/smoke-report.html` + `reports/logs/k6-smoke.log`. No schema change.
- **Acceptance criteria**
  1. `reports/state/punch-run.json` shows `"passed": true`, `"exitCode": 0`.
  2. `reports/smoke.json` shows `checkPassRate: 1` and `errorRate: 0`.

**Gate:** ✅ approved — Goal, Non-goals, Acceptance criteria agreed → Plan.
