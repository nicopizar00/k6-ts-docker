# Ship — health-smoke as the canonical Test gate

> **Golden artifact (filled, real).** Phase 6. Pattern source:
> `.github/prompts/punch-ship.prompt.md`. Caveman `full`. Mechanical only; humans merge.

```
Summary: Establishes the health smoke (`./bin/punch run smoke`) as the smallest
re-runnable Test gate and captures its real, anonymized evidence as the canonical
golden-lifecycle worked example. No product code changed; documentation only.

Completed tasks:
  - V-01 — run the health smoke and capture evidence (verification-only)

Validation status:
  - reports/state/punch-run.json: passed: true
  - Tests run: smoke (exit 0, checkPassRate 1, errorRate 0)

Known risks:
  - none (no product mutation)

Operational impact:
  - artifacts changed: none (evidence vendored under docs/ai/golden-lifecycle/evidence/)
  - service contract changed: none
  - host requirements changed: none

Documentation status: updated (golden-lifecycle set + lifecycle templates added)

Recommendation: ship
  Reason: green Test evidence; documentation-only; canon-ready template set.
```

**Gate:** open PR with this summary; CI re-runs Test; human merges. ✅
