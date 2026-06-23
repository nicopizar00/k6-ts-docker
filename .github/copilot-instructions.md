# GitHub Copilot — Repository Instructions (always-on)

Rules apply **every** Copilot session this repo. Deliberately short. Detail in
`docs/ai/operating-model.md` + path-specific files under
`.github/instructions/`.

## Critical Rules

Violate = break reproducibility, safety, or trust. Stop and ask
before bending.

1. **Docker First execution** — canonical: [`CLAUDE.md` §Rules](../CLAUDE.md#rules). Never propose host-side `npm`, `k6`, or `pip` commands.
2. **Python orchestration façade** — `bin/punch` stdlib-only Python (same source as #1). No host-side Node, npm, k6, or pip-installed package.
3. **Validation evidence mandatory** — see [`CLAUDE.md` §For AI assistants](../CLAUDE.md#for-ai-assistants) and [`docs/workflows/validation.md`](../docs/workflows/validation.md). Change not "done" until `reports/state/punch-run.json` records run.
4. **Human approves Ship.** Agent Mode MUST stop after opening PR. Merge, release, push tags = human-only.
   *WHY:* irreversible + externally visible. PR boundary = where human judgment enters.
5. **No secrets, no private URLs, no internal business context** in source, docs, prompts, or test inputs. Use env vars for any external base URL.

## Architecture ownership

Each layer owns one decision domain; Build prompts refuse cross-layer without
approved Plan. Layers: Bash wrapper · Python orchestrator (`src/punch/**`) ·
Docker Compose · Dockerfiles · k6 tests (`src/tests/**`) · Artifacts (`reports/**`).
Full ownership table + Review anti-patterns in always-on
[`punch-architecture.instructions.md`](instructions/punch-architecture.instructions.md)
(`applyTo: **`) and [`docs/architecture/punch-boundaries.md`](../docs/architecture/punch-boundaries.md)
— not restated here.

CI/CD **external** to Punch — does not own GitHub Actions workflows.

## Agentic-coding rules

Custom agents bounded at runtime by shared
[`agent-guards.md`](../docs/ai/agent-guards.md) discipline (tool surface, serial
phases, approval-before-write). Build delegates via the Punch Builder → engineer
→ cavecrew chain (the engineer, or the coordinator directly, spawns bounded
cavecrew leaf workers — **nested**, `chat.subagents.allowInvocationsFromSubagents:
true`, lazy default) on GitHub Copilot's default sub-agent behavior. Depth is
roster-bounded: cavecrew workers carry no `agents:`.

- **Never broad edits during Build.** Each Build prompt declares
  allowed / read-only / forbidden paths. Edit only allowed paths.
- **Never modify Python orchestration, Docker Compose, and k6 tests in
  one task** unless explicitly planned as integration task with
  multiple per-layer Build calls.
- **Never bypass Docker Compose** by running local `k6` or
  `docker run` directly unless user explicitly asks.
- **Never introduce CI/CD ownership into Punch** unless explicitly
  requested. `.github/workflows/` outside Build scope by default.
- **Never change service names, artifact paths, or public commands**
  without updating docs + dependents (see [`docs/ai/maintenance-matrix.md`](../docs/ai/maintenance-matrix.md)).
- **Prefer small diffs.** One scoped task per Build call.
- **Prefer explicit validation commands.** Test uses
  `./bin/punch doctor` and `./bin/punch run …` — not ad-hoc shell.
- **Preserve DX**: low-noise terminal output plus complete logs +
  artifacts under `reports/`.

## Default verification

- Use official Punch commands when available (`./bin/punch …`).
- Use Docker Compose **through** Punch when possible.
- Unit tests only complement, not replace runtime
  contract validation.

## Engineering Principles

6. **Lifecycle-driven work.** Every change goes Spec → Plan →
   Build → Test → Review → Ship (Spec absorbs former Define step).
   Use matching prompt in `.github/prompts/`.
7. **Mode discipline.** Read-only requests (audits, reviews,
   explanations) stay **Ask Mode**. Planning stays **Ask Mode**
   with Plan discipline. Edits only in **Agent Mode** within
   scoped Plan task. Phase→mode mapping:
   [`docs/ai/copilot-mode-mapping.md`](../docs/ai/copilot-mode-mapping.md).
8. **No duplication of AI guidance.** New instructions, prompts,
   skills, or agents must not restate content already in `docs/ai/` or
   `CLAUDE.md`. Link instead.

## Lifecycle entry points

| Phase | Prompt | Mode | Agent |
|---|---|---|---|
| Spec     | [`punch-spec`](prompts/punch-spec.prompt.md)                   | Ask (writes spec doc)    | `punch-architect-readonly` |
| Plan     | [`punch-plan`](prompts/punch-plan.prompt.md)                   | Ask (Plan discipline)    | `punch-planner` |
| Build    | [`punch-build`](prompts/punch-build.prompt.md)                  | Agent (scoped, via dispatch) | `punch-builder` → one engineer |
| Test     | [`punch-test`](prompts/punch-test.prompt.md)                  | Agent / Ask              | `punch-test-engineer` |
| Review   | [`punch-review`](prompts/punch-review.prompt.md)               | Ask                      | `punch-reviewer` |
| Ship     | [`punch-ship`](prompts/punch-ship.prompt.md)                   | Agent (mechanical only)  | `punch-reviewer` |

Spec absorbs former Define phase (opens with clarify/refine step).
Build = single `punch-build` prompt bound to the `punch-builder` dispatcher, which
classifies the approved Plan task and delegates the complete build to
`punch-runtime-engineer` (Python/Compose/harvest) or `punch-performance-test-engineer`
(k6 + TS bundle); engineers (or the Builder directly) may invoke bounded cavecrew
workers — nested. `punch-test` (TDD/Prove-It)
is the verification phase — done proven by `reports/state/punch-run.json`.

**Orthogonal phases (both via `punch-ai-governance`, enforced):**
[`punch-init`](prompts/punch-init.prompt.md) — one-time bootstrap/adoption guard
(`./bin/punch init`) gating repo into lifecycle; and
[`punch-document`](prompts/punch-document.prompt.md) — recurring documentation
reconciliation. Init prepares; Document reconciles.

## Change cascade (when X changes, update Y)

When change touches one area, several others usually need update in
lockstep. Full file-level cascade in
[`docs/ai/maintenance-matrix.md`](../docs/ai/maintenance-matrix.md) —
consult during Plan + Review.

## PR description

Copy checklist from [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md)
literally — don't paraphrase or invent extra items. Criteria change →
update template, not this file.

## When in doubt

Refer to `docs/ai/operating-model.md`, `docs/ai/workflow.md`, and
instruction fragments under `.github/instructions/`. Proposing
changes touching multiple matrix rows → document verification plan
in PR description.

## graphify

For any question about this repo's architecture, structure, components, or how to add/modify/find
code, your first action should be `graphify query "<question>"` when `graphify-out/graph.json`
exists. Use `graphify path "<A>" "<B>"` for relationship questions and `graphify explain "<concept>"`
for focused-concept questions. These return a scoped subgraph, usually much smaller than the full
report or raw grep output.

Triggers: "how do I…", "where is…", "what does … do", "add/modify a <component>",
"explain the architecture", or anything that depends on how files or classes relate.

If `graphify-out/wiki/index.md` exists, use it for broad navigation. Read `graphify-out/GRAPH_REPORT.md`
only for broad architecture review or when query/path/explain do not surface enough context. Only read
source files when (a) modifying/debugging specific code, (b) the graph lacks the needed detail, or
(c) the graph is missing or stale.

Type `/graphify` in Copilot Chat to build or update the graph.

## Caveman (concise comms — default `lite`)

Caveman compresses assistant **prose only**; repo default **`lite`**, every
Copilot session. Per-phase voice: Spec **`lite`** · Plan **`full`** · Build (to
humans) **`full`** · Review/Ship **`full`** · Document **`lite`** · Test
**`ultra`**. Build execution sub-agents speak **`wenyan-lite`**; when an engineer
or coordinator invokes **cavecrew**, the brief is **`wenyan-full`** and cavecrew workers report
**`wenyan-ultra`**. **Wenyan lives only in sub-agent reports — never in persistent
artifacts** (docs, ADRs, specs, plans, skills, prompts, registries). Drop to
normal prose for security/irreversible/ambiguous/architecture content. Caveman =
output style only;
never changes tools, access, or delegation. Critical Rules above take precedence.
Canon: [`punch-build-caveman`](skills/punch-build-caveman/SKILL.md).
