# Golden lifecycle — a real, verifiable worked example 🟢

Complete **real** pass through **Spec → Plan → Build → Verify → Review → Ship**,
one trackable artifact per phase, anchored to genuine anonymized evidence. Canon "golden test" teams copy when adopting Punch. Blank skeletons:
[`../templates/lifecycle/`](../templates/lifecycle/README.md).

**Subject:** simplest real verifiable smoke — confirm stack health smoke
passes via `./bin/punch run smoke`. No product code change (*verification-class*
path; also shows Build as documented no-op).

## Artifacts

| # | Phase | Artifact | Source prompt | Caveman |
|---|---|---|---|---|
| 1 | Spec   | [`01-spec.md`](01-spec.md)     | `punch-spec`   | `lite` |
| 2 | Plan   | [`02-plan.md`](02-plan.md)     | `punch-plan`   | `full` |
| 3 | Build  | [`03-build.md`](03-build.md)   | `punch-build`  | `ultra` |
| 4 | Verify | [`04-verify.md`](04-verify.md) | `punch-verify` | evidence verbatim |
| 5 | Review | [`05-review.md`](05-review.md) | `punch-review` | `full` |
| 6 | Ship   | [`06-ship.md`](06-ship.md)     | `punch-ship`   | `full` |

Minimal sanitized evidence in [`evidence/`](evidence/): `punch-run.json`, `smoke-summary.json`.

## Verified result

```
./bin/punch doctor    → exit 0
./bin/punch run smoke → exit 0
punch-run.json → passed: true   smoke.json → checkPassRate: 1, errorRate: 0
```

## Adopt

1. **Spec/Plan** — copy `spec.template.md` / `plan.template.md` into
   `docs/architecture/specs/`; fill Goal, Acceptance criteria, scoped task contracts.
2. **Build** — run `punch-build` per task ID (may be documented no-op).
3. **Verify** — `./bin/punch run <test>` must leave `reports/state/punch-run.json`
   `passed: true`; quote verbatim.
4. **Review → Ship** — read-only critique, then mechanical git/gh; **human merges**.

Each artifact ends with **gate** — don't advance until met.

## Governance

- **Canon.** These + `../templates/lifecycle/` = canonical output *shapes*;
  `.github/prompts/` files stay behavior source of truth.
- **`/punch-document`** maintains them as canon (lean; `lite`/`full`, never Wenyan).
- **`/punch-init`** detects them as `lifecycle_templates` readiness signal.

Evidence = real output, host paths → `<repo-root>`; no secrets
(`gateway-api:3000` = in-network Compose service). Regenerate via
`./bin/punch run smoke`.
