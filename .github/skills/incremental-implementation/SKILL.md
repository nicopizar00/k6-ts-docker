---
name: incremental-implementation
description: Delivers changes in thin vertical slices. Use in the Punch Build phase for any task touching more than one file or more than ~100 lines. The method is stack-neutral; Punch's scope contract and phase split (Build edits, Verify runs, Ship commits) override the generic loop.
applies-to: lifecycle/Build — the method the punch-build-* prompts + builder agents activate; not path-scoped
---

# Incremental Implementation

## In Punch

This is the **method** the five `punch-build-*` prompts and their builder agents
activate (Build phase). Punch reshapes the generic loop:

- **Phase-distributed loop:** a builder **edits one scoped slice** (builders carry
  no terminal tool); **Verify** runs `./bin/punch run …`; **Ship** commits
  (human-gated). So the loop is *Implement → Verify → next slice*, with commits
  deferred to Ship — builders do not run tests or commit.
- **Scope is the contract:** each slice stays inside the task's allowed /
  read-only / forbidden paths
  ([`scoped-build-policy.md`](../../../docs/ai/scoped-build-policy.md)). Scope
  expansion → **stop, return to Plan**.
- **Stack:** Docker-first, stdlib Python, k6 — never host `npm`/`k6`/`pip`.

## Overview

Build in thin vertical slices — implement one piece, let Verify confirm it, then
expand. Each increment leaves the system runnable (`./bin/punch run smoke` stays
green). This is the execution discipline that makes large changes manageable.

## When to Use

- A Build task touching more than one file.
- Any time you're tempted to write more than ~100 lines before Verify.

**When NOT to use:** single-file, single-function changes already minimal.

## The Increment Cycle (Punch)

```
Build one slice ──► Verify (./bin/punch run) ──► next slice ──► … ──► Ship (commit, human-gated)
  (scoped edit)        (evidence: reports/state/punch-run.json)
```

For each slice:

1. **Implement** the smallest complete piece, inside the task's allowed paths.
2. **Verify** runs `./bin/punch run <test>` and checks
   `reports/state/punch-run.json` — the builder hands off; it does not run commands.
3. **Carry forward** to the next slice — don't restart.

Commits happen once, at Ship.

## Slicing Strategies

### Vertical slices (preferred)

One complete path through the Punch execution chain:

```
Slice 1: add the k6 test (src/tests/<name>-gate.ts)   → Verify: ./bin/punch run <name>
Slice 2: expose the route/service in compose           → Verify: ./bin/punch run smoke
Slice 3: wire `./bin/punch run <name>` into the CLI    → Verify: full run
```

Each is an integration sub-task with its own scope (see
`planning-and-task-breakdown`). Each slice delivers working, verifiable behavior.

### Risk-first slicing

Tackle the riskiest piece first — e.g. prove a new Compose service health-gates
correctly before building tests against it. If it fails, you learn before
investing in the dependent slices.

## Implementation Rules

### Rule 0 — Simplicity first

Before writing code: "what is the simplest thing that could work?" After: can this
be fewer lines? Are the abstractions earning their complexity? This is `CLAUDE.md`'s
"no premature abstraction / three similar lines beat a clever helper" — implement
the naive, obviously-correct version first.

### Rule 0.5 — Scope discipline

Touch only what the task requires — this *is* Punch's allowed/forbidden contract.
Do not "clean up" adjacent code, modernize files you're only reading, or add
unspec'd features. If you notice something worth fixing outside scope, **note it,
don't touch it**:

```
NOTICED BUT NOT TOUCHING:
- docker/k6.Dockerfile pins an old tag (separate task)
→ Want me to flag these for Plan?
```

### Rule 1 — One thing at a time

Each increment changes one logical thing. Don't mix a new test, a refactor, and a
compose tweak in one slice.

### Rule 2 — Keep it runnable

After each slice, `./bin/punch run smoke` must still pass. Don't leave the stack
broken between slices.

### Rule 3 — Defer incomplete work

Punch's analog of a feature flag is the **deferred-domain** pattern: e.g. the k6
Browser placeholder stays out of the esbuild entry list until a Plan accepts its
cost. Don't expose half-built behavior.

### Rule 4 — Safe defaults

New configuration defaults to safe/off. `__ENV.TARGET_BASE_URL` keeps an
in-network default so a test runs with no env vars.

### Rule 5 — Rollback-friendly

Prefer additive over destructive changes; keep each slice independently revertable
so it matches the Plan's rollback notes. Don't delete-and-replace in the same slice.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll verify it all at the end" | Bugs compound — a flaw in slice 1 makes 2-5 wrong. Verify each slice. |
| "It's faster to do it all at once" | It *feels* faster until something breaks and you can't tell which of 500 changed lines caused it. |
| "This refactor is small enough to include" | Refactors mixed with behavior make both harder to review. Separate them (return to Plan). |
| "Let me just quickly add this too" | That's scope expansion. Note it; don't do it. |

## Red Flags

- More than ~100 lines written before a Verify run.
- Multiple unrelated changes in one slice.
- `./bin/punch run smoke` broken between slices.
- Touching files outside the task scope "while I'm here".
- Building an abstraction before the third real use demands it.

## Verification

After completing all slices for a task:

- [ ] Each slice was individually verified via `./bin/punch run …`.
- [ ] `./bin/punch run smoke` is green; `reports/state/punch-run.json` shows `passed: true`.
- [ ] No file outside the task's allowed paths was edited.
- [ ] The change does what the task specified — nothing extra.
