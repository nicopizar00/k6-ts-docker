# Test — health-smoke as the canonical Test gate

> **Golden artifact (filled, real).** Phase 4 — evidence anchor.
> Source: `punch-test.prompt.md`. Evidence verbatim; curated/anonymized.

- **Commands run** — `./bin/punch doctor` → exit `0`; `./bin/punch run smoke` → exit `0`
- **Artifacts produced** — [`evidence/punch-run.json`](evidence/punch-run.json) ·
  [`evidence/smoke-summary.json`](evidence/smoke-summary.json) (curated copies of
  `reports/state/punch-run.json` + `reports/smoke.json`)
- **Result** — ✅ pass
- **Minimal next action** — continue to Review.

## Evidence (decisive, verbatim)

```
punch-run.json   → passed: true, exitCode: 0, test: smoke
smoke.json       → checkPassRate: 1, errorRate: 0, totalRequests: 34380, p90Ms: 0.42
```

Acceptance criteria met → ✅. Full curated records in [`evidence/`](evidence/).

**Gate:** ✅ pass → Review. (Fail: implementation → Plan; environment/pre-existing → human triage.)
