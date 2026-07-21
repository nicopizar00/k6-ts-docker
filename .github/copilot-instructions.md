# GitHub Copilot — Repository Instructions (always-on)

Rules apply **every** Copilot session this repo. Deliberately short. Detail in
`docs/ai/operating-model.md` + path-specific files under
`.github/instructions/`.

## Critical Rules

Violate = break reproducibility, safety, or trust. Stop and ask
before bending.

1. **Docker First execution** — Docker is the only host requirement (plus stdlib Python 3). Never propose host-side `npm`, `k6`, or `pip` commands. Always-on contract: [`punch-architecture.instructions.md`](instructions/punch-architecture.instructions.md).
2. **Python orchestration façade** — `bin/punch` stdlib-only Python (same source as #1). No host-side Node, npm, k6, or pip-installed package.
3. **Validation evidence mandatory** — a change is not "done" until `reports/state/punch-run.json` records the run. Artifact + evidence contract: [`artifacts-reporting.instructions.md`](instructions/artifacts-reporting.instructions.md).
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
phases, approval-before-write). Build delegates via the Punch Builder → **one of
its two engineers only** — Build never spawns cavecrew. Review/Test/Security
coordinators may optionally spawn bounded, read-only cavecrew leaf workers
directly (`chat.subagents.allowInvocationsFromSubagents: true`, lazy default) on
GitHub Copilot's default sub-agent behavior. Depth is roster-bounded: cavecrew
workers carry no `agents:`.

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
   another instruction file. Link instead.

## Lifecycle entry points

| Phase | Prompt | Mode | Agent |
|---|---|---|---|
| Spec     | [`punch-spec`](prompts/punch-spec.prompt.md)                   | Ask (writes spec doc)    | `punch-architect` |
| Plan     | [`punch-plan`](prompts/punch-plan.prompt.md)                   | Ask (Plan discipline)    | `punch-architect` |
| Build    | [`punch-build`](prompts/punch-build.prompt.md)                  | Agent (scoped, via dispatch) | `punch-builder` → one engineer |
| Test     | [`punch-test`](prompts/punch-test.prompt.md)                  | Agent / Ask              | `punch-test-engineer` |
| Review   | [`punch-review`](prompts/punch-review.prompt.md)               | Ask                      | `punch-code-reviewer` |
| Ship     | [`punch-ship`](prompts/punch-ship.prompt.md)                   | Agent (gate + mechanical) | `punch-release-captain` |

Spec absorbs former Define phase (opens with clarify/refine step).
Build = single `punch-build` prompt bound to the `punch-builder` dispatcher, which
classifies the approved Plan task and delegates the complete build to
`punch-runtime-engineer` (Python/Compose/harvest) or `punch-performance-test-engineer`
(k6 + TS bundle) — neither Builder nor either engineer ever invokes cavecrew.
`punch-test` (TDD/Prove-It)
is the verification phase — done proven by `reports/state/punch-run.json`.

**Orthogonal phases (both via `punch-ai-governance`, enforced):**
[`punch-init`](prompts/punch-init.prompt.md) — read-only GitHub Copilot asset
enablement sweep (on-demand) gating repo into lifecycle; and
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

Native, upstream Graphify Agent Skill ([`.github/skills/graphify/`](skills/graphify/SKILL.md))
— adopted as-is, no Punch fork (scoped Rule-1 host-tool exception —
[ADR 0002](../docs/ai/decisions/0002-graphify-host-tool.md)). Install, security,
version, and sharing policy: [`docs/ai/graphify-install.md`](../docs/ai/graphify-install.md).

- **Explicit-only.** `/graphify` never auto-loads for unrelated work — invoke
  it directly when a repo/corpus map or query is wanted. No Punch prompt
  builds, updates, gates, or owns it.
- **Local-first by default.** No hooks, watchers, MCP server, URL ingestion,
  cloud semantic backends, or external graph-database push run
  automatically — each is a separate, explicit user decision.
- **Terminal stays approval-gated**, same as every other command — no
  standing shell pre-approval for `graphify` (the skill does not declare
  `allowed-tools: shell`/`bash`).
- Outputs under `graphify-out/` are throwaway evidence, never canonical,
  except the committed shared baseline (`graph.json`, `GRAPH_REPORT.md`,
  `.graphifyignore`) after passing the leakage validation checklist.

## Caveman (concise comms — default `lite`, optional)

Caveman compresses assistant **prose only** — a fully **optional**, user-invoked
convenience; normal prose is the complete fallback when it is absent or
inactive. Repo default **`lite`** for phases that opt in. Per-phase voice: Spec
**`lite`** · Plan **`full`** · Review/Ship **`full`** · Document **`lite`**
persisted (**`full`** working comms) · Test **`ultra`**. **Build never uses
Caveman or cavecrew** — it is fully decoupled. Review/Test/Security coordinators
may optionally brief a cavecrew worker in **`wenyan-ultra`**; cavecrew worker
reports are **non-guarded (lazy)**. Wenyan stays only in sub-agent reports —
**avoid it in committed docs/registries**. Drop to normal prose for
security/irreversible/ambiguous/architecture content. Caveman = output style
only; never changes tools, access, or delegation. Critical Rules above take
precedence. Canon: [`punch-comms-policy`](skills/punch-comms-policy/SKILL.md).
