---
name: test-driven-development
description: Drives changes with tests. In Punch a "test" is a k6 check or threshold run via ./bin/punch, proven by reports/state/punch-run.json. Use when changing test behavior or fixing a perf/contract bug — write the failing check first (Prove-It), then make it pass.
applies-to: src/tests/**, lifecycle/Test+Build — backs punch-test and the punch-build prompt
---

# Test-Driven Development

## In Punch

This is the **method** behind [`punch-test`](../../prompts/punch-test.prompt.md)
(the RED→GREEN Test/verification phase, agent `punch-test-engineer`) and the `punch-build`
prompt (k6 tasks → `punch-performance-test-engineer`). Punch redefines "test":

- A **test = a k6 `check()` or a threshold** in `src/tests/*.ts`, run via
  `./bin/punch run <test>`; **proof = `reports/state/punch-run.json`
  (`passed: true`)** — never `npm test`. Authoring the check is a Build task;
  running and judging it is the `punch-test` gate (`punch-test-engineer`); the
  builder may lazy-load this skill while building but is not the final authority.
- **Test levels** are Punch's k6 categories: **smoke** (health), **gate** (perf
  threshold), **journey** (create→read→validate). Unit tests are a *complement,
  not a replacement* for runtime-contract validation (`copilot-instructions.md`).
- Browser / Core-Web-Vitals testing is **deferred** (the `punch-performance-test-engineer`
  Browser path) — out of scope here.

## Overview

Write a failing check before the code that makes it pass. For a bug, reproduce it
with a failing threshold/check first. Tests are proof — "seems right" is not done.

## When to Use

- Changing k6 test behavior, thresholds, or checks.
- Fixing a perf regression or a contract bug (the Prove-It pattern).
- Any change that could break an existing threshold or the evidence contract.

**When NOT to use:** pure docs/config changes with no behavioral impact.

## The TDD Cycle (k6)

```
   RED                  GREEN                  REFACTOR
 add a check/         implement until         tidy the scenario,
 threshold that  ──►  ./bin/punch run    ──►  keep checks green  ──► (repeat)
 fails                shows passed: true
```

### RED — a failing check

A check that passes immediately proves nothing. Example check that fails until the
endpoint returns the new field:

```typescript
import http from 'k6/http';
import { check } from 'k6';
export default function () {
  const res = http.get(`${__ENV.TARGET_BASE_URL}/orders/prod-001`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'has createdAt': (r) => r.json('createdAt') !== undefined, // fails → behavior missing
  });
}
```

Or a threshold that fails until performance improves:

```typescript
export const options = { thresholds: { http_req_duration: ['p(95)<300'] } }; // RED until fast enough
```

Run `./bin/punch run <test>` and confirm it fails **for the right reason** — a
failing check/threshold, not a setup or connection error.

### GREEN — make it pass

Implement the minimum (in the appropriate Build domain) until
`reports/state/punch-run.json` shows `passed: true`. Don't over-engineer.

### REFACTOR — tidy with checks green

Improve scenario readability without changing what's asserted; re-run after each
change to confirm nothing broke.

## The Prove-It Pattern (bug fixes)

Don't start by fixing. Start by reproducing with a failing check — this is exactly
what `punch-test` drives:

```
Bug report ─► write a check/threshold that FAILS (bug confirmed)
           ─► Build implements the fix
           ─► ./bin/punch run shows passed: true (fix proven, regression guarded)
```

## Writing Good Checks (general principles, applied to k6)

- **Test outcomes, not internals.** Assert on the HTTP response and thresholds,
  not on how the service produced them. Interaction-based assertions break on
  refactor.
- **DAMP over DRY.** A check name reads like a spec: `'gate p95 under 300ms'`, not
  `'check1'`. Repetition that makes each check self-explanatory is fine.
- **Deterministic and isolated.** Use `SharedArray` with fixed fixture IDs
  (`prod-001`); pre-resolve `__ENV` in `setup()`. A flaky threshold erodes trust —
  fix the flakiness, don't re-run.
- **One concept per check.** Name each check for the single behavior it verifies.

## Test Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Threshold that never fails | proves nothing | first set it where current code actually fails |
| Flaky / timing-dependent checks | erode trust | deterministic fixtures, pre-resolved env |
| Asserting on logs or internal calls | breaks on refactor | assert on the HTTP response + thresholds |
| k6 that starts containers or writes outside `/reports/` | wrong layer | orchestration is `src/punch`'s job |

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll add the check after it works" | You won't — and a check written after the fact tests the implementation, not the behavior. |
| "I tested it manually" | Manual runs don't persist. `reports/state/punch-run.json` does. |
| "This threshold is too simple to bother" | The threshold documents the expected performance contract. |
| "Tests slow me down" | They slow you down once; they catch every future regression in the gate. |
| "Let me run it again just to be sure" | After a clean run, repeating `./bin/punch run` with no edit adds no information. |

## Red Flags

- Changing a threshold/check without running `./bin/punch run`.
- A bug "fix" with no failing-check-first reproduction.
- "passed" claimed but no run produced `reports/state/punch-run.json`.
- A check that passed on its first run (it may not test what you think).
- k6 code that shells out, starts containers, or writes outside `/reports/`.

## Verification

After completing any test-driven change:

- [ ] Every new behavior has a k6 check or threshold that **failed before** the change.
- [ ] `./bin/punch run <test>` produced `reports/state/punch-run.json` with `passed: true`.
- [ ] Bug fixes include a RED→GREEN reproduction (via `punch-test`).
- [ ] Checks/thresholds are deterministic; no host `k6`/`npm` was used.
