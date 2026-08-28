# GitHub Copilot — Repository Instructions (always-on)

Rules apply **every** Copilot session this repo. Deliberately short. Detail in
`docs/ai/operating-model.md` + path-specific files under
`.github/instructions/`.

## Critical Rules

Violate = break reproducibility, safety, or trust. Stop and ask
before bending.

1. **Docker First execution** — Docker is the only host requirement (plus stdlib Python 3). Never propose host-side `npm`, `k6`, or `pip` commands, **except** the narrow `punch-performance-test-engineer` authoring exception — host `npm`/`pnpm`/esbuild/lint, and host `k6` only for the `npm run smoke:local` pre-check, while authoring the k6 TS toolchain; off the evidence path, shipped chain unchanged ([ADR 0001](../docs/ai/decisions/0001-perf-engineer-host-npm.md)). Always-on contract: [`punch-architecture.instructions.md`](instructions/punch-architecture.instructions.md).
2. **Python orchestration façade** — `bin/punch` stdlib-only Python (same source as #1). No host-side Node, npm, k6, or pip-installed package for the orchestrator itself — the sole exception is Rule 1's scoped `punch-performance-test-engineer` authoring carve-out, not a general allowance.
3. **Validation evidence mandatory** — a change is not "done" until it meets its class's evidence bar. Runtime-affecting → `reports/state/punch-run.json` (`passed: true`). Documentation/Copilot-only → diff review + governance parity, no runtime run expected. Canonical evidence matrix: [`docs/workflows/validation.md`](../docs/workflows/validation.md). Artifact contract: [`artifacts-reporting.instructions.md`](instructions/artifacts-reporting.instructions.md).
4. **Human approves Ship.** Agent Mode MUST stop after opening PR. Merge, release, push tags = human-only.
   *WHY:* irreversible + externally visible. PR boundary = where human judgment enters.
5. **No secrets, no private URLs, no internal business context** in source, docs, prompts, or test inputs. Use env vars for any external base URL.

## Discovery boundary (this workspace)

VS Code Copilot Chat discovers repository customizations from
`.github/instructions`, `.github/prompts`, `.github/agents`, and
`.github/skills` only — [`.vscode/settings.json`](../.vscode/settings.json) is
the enforced guard. Root `AGENTS.md`, `CLAUDE.md`, `.agents/**`, and
`.claude/**` are disabled for this workspace and are not Punch Chat canon;
they may still serve other hosts untouched.

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
its two engineers only**. Review/Test/Security coordinators carry no `agent`
tool either — reference search and diff pre-scan happen inline.
`chat.subagents.allowInvocationsFromSubagents` **stays at its default (`false`)** —
VS Code's own default disables a subagent spawning further subagents; Punch
relies on that default rather than overriding it.

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
   Use matching prompt in `.github/prompts/`. Doc-only changes with no
   runtime-contract impact skip Build (straight Plan → PR) — scoped
   exception, see [`documentation.instructions.md`](instructions/documentation.instructions.md#build-prompt).
7. **Mode discipline.** Read-only requests (audits, reviews,
   explanations) stay **Ask Mode**. Planning stays **Ask Mode**
   with Plan discipline. Edits only in **Agent Mode** within
   scoped Plan task. Phase→mode mapping:
   [`docs/ai/copilot-mode-mapping.md`](../docs/ai/copilot-mode-mapping.md).
8. **No duplication of AI guidance.** New instructions, prompts,
   skills, or agents must not restate content already in `docs/ai/` or
   another instruction file. Link instead.
9. **Surface assumptions before non-trivial work.** State them; don't silently
   fill ambiguous requirements — cheaper to correct now than after the diff.
10. **Manage confusion actively.** Inconsistency, conflicting spec/code, or an
    unclear requirement → stop, name the confusion, ask — don't guess and
    proceed.
11. **Push back when warranted.** Not a yes-machine — flag a flawed approach
    with a quantified downside and propose an alternative; accept an informed
    override.
12. **Enforce simplicity and scope discipline.** Fewer lines, earned
    abstractions, boring over clever; touch only what the task's allowed paths
    cover — no drive-by cleanup of orthogonal code.
13. **Verify, don't assume.** "Seems right" isn't done — every change needs
    its class's evidence (`reports/state/punch-run.json`, build/lint output,
    or a clean `punch-ai-governance` pass), per Rule 3.

(Absorbed from the retired `punch-using-agent-skills` meta-skill — its
skill-discovery decision tree lives in
[`docs/ai/skill-registry.md`](../docs/ai/skill-registry.md)'s "Skill
discovery" table; delegation-depth/roster canon lives in
[`agent-guards.md`](../docs/ai/agent-guards.md).)

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
(k6 + TS bundle).
`punch-test` (TDD/Prove-It)
is the verification phase — done proven by `reports/state/punch-run.json`.

**Orthogonal maintenance phase (via `punch-ai-governance`, enforced):**
[`punch-document`](prompts/punch-document.prompt.md) — recurring documentation
reconciliation.

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
[ADR 0002](../docs/ai/decisions/0002-graphify-host-tool.md)).
**Explicit-only** — `/graphify` never auto-loads and no Punch prompt builds,
updates, gates, or owns it; terminal stays approval-gated like every other
command. Full install/security/local-vs-committed-baseline policy:
[`docs/ai/graphify-install.md`](../docs/ai/graphify-install.md).

## Caveman (concise comms — explicit-only, VS Code GitHub Copilot Chat only)

Caveman compresses assistant **prose only**, in **VS Code GitHub Copilot Chat**
— **explicit-only**: normal prose is the default and complete fallback until
the user invokes `/caveman lite|full|ultra|wenyan-*`, which loads the
[`caveman`](skills/caveman/SKILL.md) skill and sets the level for the
conversation; `stop caveman` / `normal mode` disables it again. **Build never
uses Caveman.** Never compresses code, commands, paths, logs, errors, exit
codes, thresholds, JSON/YAML/CSV, or `reports/state/punch-run.json` — those
stay verbatim at every level; drop to normal prose for security warnings,
irreversible-action confirmations, or ambiguous content. Output style only —
never changes tools, access, evidence, or delegation; Critical Rules above
take precedence. Not active for any other host (Claude Code, Codex, Cursor,
Windsurf, Copilot CLI, Copilot coding agent). Full mode semantics:
[`caveman`](skills/caveman/SKILL.md).
