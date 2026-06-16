# AI Workflow — Step-by-step lifecycle

This is the practical walkthrough of the seven phases. For *why* the model
is shaped this way, read [`operating-model.md`](operating-model.md) first.

## The seven phases at a glance

```
Define ─▶ Spec ─▶ Plan ─▶ Build ─▶ Verify ─▶ Review ─▶ Ship
  │        │       │       │         │         │        │
  Ask      Ask     Ask    Agent   Agent/Ask   Ask    Agent (mech.)
  read     spec    plan    one      run         no    git + gh
  only     doc     doc    task    Punch cmd   edits   only
```

## Phase 1 — Define

**Prompt:** [`punch-define`](../../.github/prompts/punch-define.prompt.md)
**Agent:** `punch-architect-readonly`

Translate a request, issue, or symptom into a clean problem statement.
Read broadly. Edit nothing.

**Output:** a Define note with:

- Problem summary (one paragraph).
- Relevant repository areas (file paths).
- Current behavior vs desired behavior.
- Architectural boundaries involved (from [`punch-boundaries.md`](../architecture/punch-boundaries.md)).
- Risks and open questions.
- Suggested next step (almost always Spec).

**Gate:** a narrow, specific problem statement.

## Phase 2 — Spec

**Prompt:** [`punch-spec`](../../.github/prompts/punch-spec.prompt.md)
**Agent:** `punch-architect-readonly`

Convert the Define note into a specification. Still no code edits (except
the spec document itself, if you choose to write it down).

**Output:** Goal · Non-goals · Functional requirements · Technical
constraints · Affected layers · Artifact/log/reporting implications ·
Acceptance criteria.

**Gate:** goals and acceptance criteria are agreed.

## Phase 3 — Plan

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
- Which Build prompt handles it (orchestrator / compose / k6-http /
  k6-browser / data-harvest).

**Gate:** plan approved by a human.

## Phase 4 — Build

**Prompts:** one of —

- [`punch-build-orchestrator`](../../.github/prompts/punch-build-orchestrator.prompt.md)
- [`punch-build-compose`](../../.github/prompts/punch-build-compose.prompt.md)
- [`punch-build-k6-http`](../../.github/prompts/punch-build-k6-http.prompt.md)
- [`punch-build-k6-browser`](../../.github/prompts/punch-build-k6-browser.prompt.md)
- [`punch-build-data-harvest`](../../.github/prompts/punch-build-data-harvest.prompt.md)

**Agent:** `punch-builder-scoped`

Implement **one** task from the approved plan. Edit **only** the allowed
paths. If the change requires touching anything outside scope, stop and
return to Plan — do not silently expand.

**Output:** a focused diff. Report every file changed.

**Gate:** diff stays inside the plan's allowed paths.

## Phase 5 — Verify

**Prompt:** [`punch-verify`](../../.github/prompts/punch-verify.prompt.md)
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

## Phase 6 — Review

**Prompt:** [`punch-review`](../../.github/prompts/punch-review.prompt.md)
**Agent:** `punch-reviewer` (activates `punch-governance-review` skill if
the diff touches `.github/` or `docs/ai/`)

Read-only critique of the diff against the plan.

**Output:** files changed · boundary compliance · risk assessment ·
test/validation coverage · unintended coupling · missing docs · required
follow-up tasks · approval recommendation.

**Gate:** verdict = Approve.

## Phase 7 — Ship

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

### Phase 1 — Define

> The CLI currently always streams Docker output to the terminal. When
> running in CI with `--collect-logs`, this duplicates the log content
> visibly. Users want a quieter terminal while preserving the file log.

Relevant files: `src/punch/__main__.py`, `bin/punch`.
Layers: Python orchestrator (control flow).
Risks: log-tail consumers that grep terminal output.

### Phase 2 — Spec

- Goal: a `--quiet` flag on `./bin/punch run` that mutes terminal output.
- Non-goals: not changing log file contents; not adding a verbosity scale.
- Constraint: stdlib-only; do not buffer subprocess (still stream, just to
  the log file).
- Affected layers: Python orchestrator only.
- Acceptance: `./bin/punch run smoke --quiet` produces no per-line terminal
  output but `reports/logs/smoke.log` is identical to the non-quiet run.

### Phase 3 — Plan

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
Build via:   punch-build-orchestrator
```

### Phase 4 — Build

Run `punch-build-orchestrator` with task O-01. Edit only
`src/punch/__main__.py`. Report the diff.

### Phase 5 — Verify

```
./bin/punch doctor
./bin/punch run smoke              # baseline: terminal output present
./bin/punch run smoke --quiet      # quiet: no terminal output
diff reports/logs/smoke.log         # log file identical between runs
```

Confirm `reports/state/punch-run.json` shows `passed: true`.

### Phase 6 — Review

Diff touches only `src/punch/__main__.py`. No new imports. Boundary check
passes. Verify evidence present. Approve.

### Phase 7 — Ship

Commit `feat(orchestrator): add --quiet flag to bin/punch run`, push, open
PR with the Verify evidence link in the test plan. Human merges.

## Phase rename map (for navigating older PRs)

This redesign renamed/restructured some phases. Old PRs and commits may use
the previous names — map them as follows.

| Old (pre-redesign) | New |
|---|---|
| Understand | Define |
| Shape | Spec **+** Plan (split into two phases) |
| Build (single `punch-build-slice` prompt) | Build (five domain prompts) |
| Verify | Verify (unchanged) |
| Review | Review (unchanged) |
| Ship | Ship (unchanged) |

The "Ship" name is intentionally preserved — only the prompts/skills around
it were restructured.
