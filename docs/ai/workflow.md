# AI Workflow — Step-by-step lifecycle

Practical walkthrough of six phases. For *why* model shaped this way, read [`operating-model.md`](operating-model.md) first.

## The six phases at a glance

```
Spec ─▶ Plan ─▶ Build ─▶ Test ─▶ Review ─▶ Ship
  │       │       │         │         │        │
  Ask     Ask    Agent   Agent/Ask    Ask    Agent (mech.)
 spec    plan    one      run         no    git + gh
 doc     doc    task    Punch cmd   edits   only
```

Spec absorbs former **Define** phase — opens with clarify/refine step (`punch-idea-refine` skill) before specifying.

## Phase 1 — Spec (absorbs the former Define)

**Prompt:** [`punch-spec`](../../.github/prompts/punch-spec.prompt.md)
**Agent:** `punch-architect`

Clarify request into clean problem statement — read broad, trace execution chain, use `punch-idea-refine` skill when idea still vague — then crystallize into spec. Only file this phase may write: spec doc itself.

**Output:**

- Problem statement (former Define note — one paragraph naming real problem, with relevant file paths and current-vs-desired behavior).
- Goal · Non-goals · Functional requirements · Technical constraints.
- Affected architectural layers (from [`punch-boundaries.md`](../architecture/punch-boundaries.md)).
- Artifact / log / reporting implications (explicit, even if "none").
- Acceptance criteria — conditions Test will check.

**Gate:** goals and acceptance criteria agreed.

## Phase 2 — Plan

**Prompt:** [`punch-plan`](../../.github/prompts/punch-plan.prompt.md)
**Agent:** `punch-architect`

Convert spec into one or more scoped tasks. Each task = smallest unit Build executes. Plan = *contract* Build bound to.

**Output:** per task —

- Task ID.
- Goal.
- **Allowed edit paths** (Build may only touch these).
- **Read-only context paths** (Build may read, not edit).
- **Forbidden paths** (Build refuses to touch).
- Expected diff size.
- Validation commands (run by Test).
- Rollback notes.
- Human checkpoint.
- Which engineer `punch-builder` routes to (`punch-runtime-engineer` for orchestrator / compose / data-harvest; `punch-performance-test-engineer` for k6 http / browser).

**Gate:** plan approved by human.

## Phase 3 — Build

**Prompt:** [`punch-build`](../../.github/prompts/punch-build.prompt.md) → `punch-builder`, which classifies task and delegates (depth-1) to one engineer:

- `punch-runtime-engineer` — Python orchestration, Compose, data harvest.
- `punch-performance-test-engineer` — k6 HTTP/Browser, TS bundle, lint.

Each engineer carries that domain's allowed/read-only/forbidden scope. Engineers may run Docker/Punch-mediated commands for evidence; maintainer never does.

Implement **one** task from approved plan. Edit **only** allowed paths. If change requires touching anything outside scope, stop and return to Plan — do not silently expand.

**Output:** focused diff. Report every file changed.

**Gate:** diff stays inside plan's allowed paths.

## Phase 4 — Test

**Prompt:** [`punch-test`](../../.github/prompts/punch-test.prompt.md) — the verification phase (TDD/Prove-It; confirm a check/threshold goes RED→GREEN, produce `reports/state/punch-run.json`).
**Agent:** `punch-test-engineer`

Run official Punch commands. No invented shortcuts, no k6 on host. Failures classified (implementation-related, environment-related, pre-existing); do not silently patch.

**Typical sequence:**

1. `./bin/punch doctor`
2. `./bin/punch run smoke`
3. Test relevant to change (`./bin/punch run gate|journey`).
4. Confirm `reports/state/punch-run.json` exists and `passed: true`.

**Output:** commands run · results · failure classification · minimal next action.

**Gate:** verified pass, or explicit failure with return to Plan.

## Phase 5 — Review

**Prompt:** [`punch-review`](../../.github/prompts/punch-review.prompt.md)
**Agent:** `punch-code-reviewer` (activates `punch-ai-governance` skill if diff touches `.github/` or `docs/ai/`)

Read-only critique of diff against plan.

**Output:** files changed · boundary compliance · risk assessment · test/validation coverage · unintended coupling · missing docs · required follow-up tasks · approval recommendation.

**Gate:** verdict = Approve.

## Phase 6 — Ship

**Prompt:** [`punch-ship`](../../.github/prompts/punch-ship.prompt.md)
**Agent:** `punch-release-captain` (fan-out → GO/NO-GO + rollback, then mechanical commit/push/PR) — *humans merge.*

Mechanical only: `git add` in-scope files, commit with tight message, push, open PR. **Never merge.** **Never push tags.** **Never `--no-verify`.**

**Output:** PR URL and one-line ship summary (completed tasks, validation status, known risks, recommendation).

**Gate:** human-merged PR.

## A practical scoped task

**Request:** "Add a `--quiet` flag to `bin/punch run` that suppresses streaming subprocess output but still writes full logs to `reports/logs/<test>.log`."

### Phase 1 — Spec (clarify, then specify)

> CLI currently always streams Docker output to terminal. When running in CI with `--collect-logs`, this duplicates log content visibly. Users want quieter terminal while preserving file log.

Relevant files: `src/punch/__main__.py`, `bin/punch`.
Layers: Python orchestrator (control flow).
Risks: log-tail consumers that grep terminal output.

Then specify:

- Goal: `--quiet` flag on `./bin/punch run` that mutes terminal output.
- Non-goals: not changing log file contents; not adding verbosity scale.
- Constraint: stdlib-only; do not buffer subprocess (still stream, just to log file).
- Affected layers: Python orchestrator only.
- Acceptance: `./bin/punch run smoke --quiet` produces no per-line terminal output but `reports/logs/smoke.log` identical to non-quiet run.

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
Build via:   punch-build → punch-builder → punch-runtime-engineer
```

### Phase 3 — Build

Run `punch-build` (dispatcher `punch-builder` → `punch-runtime-engineer`) with task O-01. Edit only `src/punch/__main__.py`. Report diff.

### Phase 4 — Test

```
./bin/punch doctor
./bin/punch run smoke              # baseline: terminal output present
./bin/punch run smoke --quiet      # quiet: no terminal output
diff reports/logs/smoke.log         # log file identical between runs
```

Confirm `reports/state/punch-run.json` shows `passed: true`.

### Phase 5 — Review

Diff touches only `src/punch/__main__.py`. No new imports. Boundary check passes. Test evidence present. Approve.

### Phase 6 — Ship

Commit `feat(orchestrator): add --quiet flag to bin/punch run`, push, open PR with Test evidence link in test plan. Human merges.

## Phase rename map (for navigating older PRs)

Lifecycle restructured. Old PRs and commits may use previous names — map as follows.

| Old | New |
|---|---|
| Understand | Spec (clarify step) |
| Shape | Spec **+** Plan (split into two phases) |
| Define (separate phase) | Folded into **Spec** (its opening clarify/refine step) |
| Build (single `punch-build-slice` prompt) | Build (five domain prompts + five builder agents) |
| Verify | Test (`punch-test`) |
| Review | Review (unchanged) |
| Ship | Ship (unchanged) |

"Ship" name intentionally preserved — only prompts/skills/agents around it restructured.
