# Spec — health-smoke as the canonical Verify gate

> **Golden artifact (filled, real).** Phase 1 of worked lifecycle.
> Pattern source: `.github/prompts/punch-spec.prompt.md`. Caveman `lite`.

- **Goal** — Confirm reference stack health smoke pass via
  `./bin/punch run smoke`. Establish smallest re-runnable Verify gate that
  emit trackable evidence.
- **Non-goals**
  - No add, rename, alter any k6 test or threshold.
  - No perf-gating (that `catalog-gate`) or journey validation.
  - No change services, Compose, or orchestrator.
- **Functional requirements**
  - One official command produce machine-readable pass/fail record.
  - Smoke exercise gateway → catalog/orders health, report check pass rate.
- **Technical constraints** — Docker-First; run **only** through `./bin/punch`
  (no host `k6`, no raw `docker run`); orchestrator stay stdlib-only.
- **Affected layers** — k6 tests (`src/tests/smoke.ts`, read-only here) · Python
  orchestrator (run it) · Artifacts (`reports/**`). See `punch-boundaries.md`.
- **Artifact / log / reporting implications** — write
  `reports/state/punch-run.json` (canonical evidence) + `reports/smoke.json` +
  `reports/smoke-report.html` + `reports/logs/k6-smoke.log`. No schema change.
- **Acceptance criteria**
  1. `reports/state/punch-run.json` show `"passed": true`, `"exitCode": 0`.
  2. `reports/smoke.json` show `checkPassRate: 1` and `errorRate: 0`.

**Gate:** ✅ approved — Goal, Non-goals, Acceptance criteria agreed → Plan.
