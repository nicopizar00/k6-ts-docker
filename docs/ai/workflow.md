# AI Workflow — Step-by-step lifecycle

This is the practical walkthrough of the six phases. For *why* the model
is shaped this way, read [`operating-model.md`](operating-model.md) first.

## The six phases at a glance

```
Spec ─▶ Plan ─▶ Build ─▶ Verify ─▶ Review ─▶ Ship
  │       │       │         │         │        │
  Ask     Ask    Agent   Agent/Ask    Ask    Agent (mech.)
 spec    plan    one      run         no    git + gh
 doc     doc    task    Punch cmd   edits   only
```

Spec absorbs the former **Define** phase — it opens with a clarify/refine step
(the `idea-refine` skill) before specifying.

## Phase 1 — Spec (absorbs the former Define)

**Prompt:** [`punch-spec`](../../.github/prompts/punch-spec.prompt.md)
**Agent:** `punch-architect-readonly`

Clarify the request into a clean problem statement — read broadly, trace the
execution chain, and use the `idea-refine` skill when the idea is still vague —
then crystallize it into a specification. The only file this phase may write is
the spec doc itself.

**Output:**

- Problem statement (the former Define note — one paragraph naming the real
  problem, with relevant file paths and current-vs-desired behavior).
- Goal · Non-goals · Functional requirements · Technical constraints.
- Affected architectural layers (from [`punch-boundaries.md`](../architecture/punch-boundaries.md)).
- Artifact / log / reporting implications (explicit, even if "none").
- Acceptance criteria — the conditions Verify will check.

**Gate:** goals and acceptance criteria are agreed.

## Phase 2 — Plan

**Prompt:** [`punch-plan`](../../.github/prompts/punch-plan.prompt.md)
**Agent:** `punch-planner`

Convert the spec into one or more scoped tasks. Each task is the smallest
unit Build will execute. The plan is the *contract* Build is bound to.

**Output:** for each task —

- Task ID.
- Goal.
- **Allowed edit paths** (Build may only touch these).
- **Read-only context paths** (Build may read but not edit).
- **Forbidden paths** (Build refuses to touch).
- Expected diff size.
- Validation commands (run by Verify).
- Rollback notes.
- Human checkpoint.
- Which Build prompt + builder agent handles it (orchestrator / compose /
  k6-http / k6-browser / data-harvest).

**Gate:** plan approved by a human.

## Phase 3 — Build

**Prompts:** one of —

- [`punch-build-orchestrator`](../../.github/prompts/punch-build-orchestrator.prompt.md) → `punch-builder-orchestrator`
- [`punch-build-compose`](../../.github/prompts/punch-build-compose.prompt.md) → `punch-builder-compose`
- [`punch-build-k6-http`](../../.github/prompts/punch-build-k6-http.prompt.md) → `punch-builder-k6-http`
- [`punch-build-k6-browser`](../../.github/prompts/punch-build-k6-browser.prompt.md) → `punch-builder-k6-browser`
- [`punch-build-data-harvest`](../../.github/prompts/punch-build-data-harvest.prompt.md) → `punch-builder-data-harvest`

Each Build prompt binds to its own **builder agent**, whose `tools:` scope is
`edit` + `search` (no terminal — running commands is Verify's job).

Implement **one** task from the approved plan. Edit **only** the allowed
paths. If the change requires touching anything outside scope, stop and
return to Plan — do not silently expand.

**Output:** a focused diff. Report every file changed.

**Gate:** diff stays inside the plan's allowed paths.

## Phase 4 — Verify

**Prompts:** [`punch-verify`](../../.github/prompts/punch-verify.prompt.md)
(full evidence gate) and [`punch-test`](../../.github/prompts/punch-test.prompt.md)
(the TDD/Prove-It companion — confirm a check/threshold goes RED→GREEN).
**Agent:** `punch-verifier`

Run the official Punch commands. Do not invent shortcuts or run k6 on the
host. Failures are classified (implementation-related, environment-related,
pre-existing); do not silently patch.

**Typical sequence:**

1. `./bin/punch doctor`
2. `./bin/punch run smoke`
3. The test relevant to the change (`./bin/punch run gate|journey`).
4. Confirm `reports/state/punch-run.json` exists and `passed: true`.

**Output:** commands run · results · failure classification · minimal next
action.

**Gate:** verified pass, or explicit failure with a return to Plan.

## Phase 5 — Review

**Prompt:** [`punch-review`](../../.github/prompts/punch-review.prompt.md)
**Agent:** `punch-reviewer` (activates `punch-ai-governance` skill if
the diff touches `.github/` or `docs/ai/`)

Read-only critique of the diff against the plan.

**Output:** files changed · boundary compliance · risk assessment ·
test/validation coverage · unintended coupling · missing docs · required
follow-up tasks · approval recommendation.

**Gate:** verdict = Approve.

## Phase 6 — Ship

**Prompt:** [`punch-ship`](../../.github/prompts/punch-ship.prompt.md)
**Agent:** `punch-reviewer` (mechanical handoff) — *humans merge.*

Mechanical only: `git add` the in-scope files, commit with a tight message,
push, open a PR. **Never merge.** **Never push tags.** **Never `--no-verify`.**

**Output:** PR URL and a one-line ship summary (completed tasks, validation
status, known risks, recommendation).

**Gate:** human-merged PR.

## A practical scoped task

**Request:** "Add a `--quiet` flag to `bin/punch run` that suppresses
streaming subprocess output but still writes full logs to
`reports/logs/<test>.log`."

### Phase 1 — Spec (clarify, then specify)

> The CLI currently always streams Docker output to the terminal. When
> running in CI with `--collect-logs`, this duplicates the log content
> visibly. Users want a quieter terminal while preserving the file log.

Relevant files: `src/punch/__main__.py`, `bin/punch`.
Layers: Python orchestrator (control flow).
Risks: log-tail consumers that grep terminal output.

Then specify:

- Goal: a `--quiet` flag on `./bin/punch run` that mutes terminal output.
- Non-goals: not changing log file contents; not adding a verbosity scale.
- Constraint: stdlib-only; do not buffer subprocess (still stream, just to
  the log file).
- Affected layers: Python orchestrator only.
- Acceptance: `./bin/punch run smoke --quiet` produces no per-line terminal
  output but `reports/logs/smoke.log` is identical to the non-quiet run.

### Phase 2 — Plan

```
Task O-01
Goal:        Add --quiet flag to `punch run` subcommand
Allowed:     src/punch/__main__.py
Read-only:   bin/punch, docker-compose.yml
Forbidden:   src/tests/**, docker/**, .github/**
Diff size:   ~30 lines
Validation:  ./bin/punch run smoke --quiet (terminal empty, log file populated)
Rollback:    revert single commit; no schema/contract changes
Checkpoint:  human confirms before Build
Build via:   punch-build-orchestrator → punch-builder-orchestrator
```

### Phase 3 — Build

Run `punch-build-orchestrator` (agent `punch-builder-orchestrator`) with task
O-01. Edit only `src/punch/__main__.py`. Report the diff.

### Phase 4 — Verify

```
./bin/punch doctor
./bin/punch run smoke              # baseline: terminal output present
./bin/punch run smoke --quiet      # quiet: no terminal output
diff reports/logs/smoke.log         # log file identical between runs
```

Confirm `reports/state/punch-run.json` shows `passed: true`.

### Phase 5 — Review

Diff touches only `src/punch/__main__.py`. No new imports. Boundary check
passes. Verify evidence present. Approve.

### Phase 6 — Ship

Commit `feat(orchestrator): add --quiet flag to bin/punch run`, push, open
PR with the Verify evidence link in the test plan. Human merges.

## Phase rename map (for navigating older PRs)

This lifecycle has been restructured. Old PRs and commits may use previous
names — map them as follows.

| Old | New |
|---|---|
| Understand | Spec (clarify step) |
| Shape | Spec **+** Plan (split into two phases) |
| Define (separate phase) | Folded into **Spec** (its opening clarify/refine step) |
| Build (single `punch-build-slice` prompt) | Build (five domain prompts + five builder agents) |
| Verify | Verify (+ `punch-test` companion) |
| Review | Review (unchanged) |
| Ship | Ship (unchanged) |

The "Ship" name is intentionally preserved — only the prompts/skills/agents
around it were restructured.
