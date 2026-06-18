---
name: planning-and-task-breakdown
description: Breaks work into ordered, verifiable tasks. Use in the Punch Plan phase when you have a spec and need scoped tasks, when a task feels too large to start, or when cross-layer work needs sequencing. The method here is stack-neutral; Punch's task contract lives in scoped-build-policy and the punch-planner agent.
applies-to: lifecycle/Plan — the method the punch-plan prompt activates; not path-scoped
---

# Planning and Task Breakdown

## In Punch

This is the **method** the [`punch-plan`](../../prompts/punch-plan.prompt.md) prompt
activates (agent `punch-planner`). Punch overrides the generic format below:

- **Task contract:** every Punch task declares **allowed / read-only / forbidden
  paths**, validation commands, rollback notes, a human checkpoint, and which
  `punch-build-*` prompt handles it. That contract is defined in
  [`scoped-build-policy.md`](../../../docs/ai/scoped-build-policy.md) and the
  `punch-planner` agent — use it, don't restate it here.
- **Verification = Punch commands:** tasks verify via `./bin/punch run <test>` and
  `reports/state/punch-run.json`, never `npm test`/`npm run build`.
- **Layer order:** Punch's dependency direction is k6 test → Compose service →
  orchestrator subcommand → reporting; CI is external and out of scope.

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria.
Good breakdown is the difference between reliable completion and a tangled mess.
Every task should be small enough to implement, verify, and review in one focused
session.

## When to Use

- You have a spec and need to break it into implementable units.
- A task feels too large or vague to start.
- Cross-layer work needs an explicit order.
- You need to communicate scope to a human before any edit.

**When NOT to use:** single-file changes with obvious scope, or when the spec
already contains well-defined tasks.

## The Planning Process

### Step 1: Plan mode (read-only)

Before any code: read the spec and the relevant code, identify existing patterns,
map dependencies, note risks. **The output is a plan document, not edits** — the
`punch-planner` agent carries no code-edit tool.

### Step 2: Map the dependency graph

In Punch, dependencies usually run along the execution chain:

```
k6 test (src/tests/*.ts)
    │  needs a target to hit
    └── Compose service (docker-compose.yml, docker/**)
            │  needs to be runnable
            └── orchestrator subcommand (src/punch/**, bin/punch)
                    │  produces evidence
                    └── reporting / artifact (src/tests/support/**, reports/**)
```

Build foundations first; implement bottom-up along the chain.

### Step 3: Slice vertically, one layer at a time

Don't build "all of compose, then all of k6". Slice one complete path, and in
Punch a cross-layer slice becomes an **integration task** = one Build call per
layer, in order (see `scoped-build-policy.md` § Cross-layer tasks):

**Good (Punch integration slice — "add a new `cart` gate test"):**
```
Task K-01: add src/tests/cart-gate.ts with thresholds + handleSummary   (punch-build → performance-test-engineer)
Task C-01: expose the cart route in compose if a new service is needed   (punch-build → runtime-engineer)
Task O-01: wire `./bin/punch run cart` into the CLI                      (punch-build → runtime-engineer)
```
Each task respects its own allowed/read-only/forbidden scope; Verify runs the
whole suite, not just the new test.

### Step 4: Write tasks (Punch contract)

Each task follows the `punch-planner` output contract. Minimum fields:

```markdown
## Task [ID e.g. K-01 / C-01 / O-01 / D-01]: [short title]

**Goal:** one sentence.
**Allowed edit paths:** <globs>
**Read-only context paths:** <globs>
**Forbidden paths:** <globs — every layer this task does not own>
**Validation:** ./bin/punch doctor; ./bin/punch run <test>  → reports/state/punch-run.json passed: true
**Rollback:** how to undo if Verify fails (usually: revert the single commit)
**Expected diff size:** rough line count
**Human checkpoint:** approval required before Build
**Build via:** which punch-build-* prompt + builder agent
```

### Step 5: Order and checkpoint

1. Satisfy dependencies (foundation first).
2. Each task leaves the system runnable (`./bin/punch run smoke` still green).
3. A human checkpoint precedes Build (mandatory in Punch).
4. Put high-risk tasks early (fail fast).

## Task Sizing Guidelines

| Size | Files | Scope | Punch example |
|------|-------|-------|---------------|
| **XS** | 1 | single function/config | bump a threshold value |
| **S** | 1-2 | one component | add a new k6 HTTP test |
| **M** | 3-5 | one feature slice | new test + compose route + CLI subcommand |
| **L** | 5-8 | multi-component | reporting schema change + every consumer |
| **XL** | 8+ | **too large — break it down** | — |

Break a task down further when: it would take more than one focused session; you
can't state acceptance in ≤3 bullets; it touches two independent subsystems; or
you're writing "and" in the title (a sign it's two tasks).

## Parallelization

- **Safe to parallelize:** independent test slices, docs.
- **Must be sequential:** Compose service renames, shared-state/reporting-contract
  changes, dependency chains.
- **Needs coordination:** anything that shares an artifact contract — define the
  contract first (see `punch-data-harvest`), then parallelize.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | That's how you get a tangled mess and rework. 10 minutes of planning saves hours. |
| "The tasks are obvious" | Write them down anyway — explicit tasks surface hidden cross-layer dependencies. |
| "Planning is overhead" | Planning *is* the task. Implementation without a plan is just typing. |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries. |

## Red Flags

- Starting implementation without a written task list.
- Tasks like "implement the feature" with no acceptance criteria.
- A task with no allowed/read-only/forbidden paths, or no validation command.
- A cross-layer task collapsed into one Build call (must be one call per layer).
- No human checkpoint before Build.

## Verification

Before starting Build, confirm:

- [ ] Every task has a goal, acceptance criteria, and a `./bin/punch` validation command.
- [ ] Every task declares allowed / read-only / forbidden paths.
- [ ] Dependencies are ordered (bottom-up along the execution chain).
- [ ] No single task touches more than ~5 files.
- [ ] A human has reviewed and approved the plan.
