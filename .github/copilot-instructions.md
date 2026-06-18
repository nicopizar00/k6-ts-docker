# GitHub Copilot — Repository Instructions (always-on)

These rules apply to **every** Copilot session in this repository. They
are deliberately short. Detailed guidance lives in
`docs/ai/operating-model.md` and the path-specific files under
`.github/instructions/`.

## Critical Rules

Violating these breaks reproducibility, safety, or trust. Stop and ask
before bending one.

1. **Docker First execution** — canonical: [`CLAUDE.md` §Rules](../CLAUDE.md#rules). Never propose host-side `npm`, `k6`, or `pip` commands.
2. **Python orchestration façade** — `bin/punch` is stdlib-only Python (same source as #1). Do not introduce host-side Node, npm, k6, or any pip-installed package.
3. **Validation evidence is mandatory** — see [`CLAUDE.md` §For AI assistants](../CLAUDE.md#for-ai-assistants) and [`docs/workflows/validation.md`](../docs/workflows/validation.md). A change is not "done" until `reports/state/punch-run.json` records the run.
4. **Human approves Ship.** Agent Mode MUST stop after opening a PR. Merging, releasing, and pushing tags are human-only actions.
   *WHY:* these actions are irreversible and visible externally. The PR boundary is where human judgment must enter.
5. **No secrets, no private URLs, no internal business context** in source, docs, prompts, or test inputs. Use environment variables for any external base URL.

## Architecture ownership

Each layer owns one decision domain; Build prompts refuse to cross
layers without an approved Plan. The full ownership map lives in
[`docs/architecture/punch-boundaries.md`](../docs/architecture/punch-boundaries.md).

| Layer | Owns | Lives in |
|---|---|---|
| Bash wrapper | route shell calls to Python | `bin/punch`, `bin/*` |
| Python orchestrator | argparse, subprocess, exit codes, evidence | `src/punch/**` |
| Docker Compose | services, networks, env, healthchecks (runtime boundary) | `docker-compose.yml` |
| Dockerfiles | how each service is built | `docker/*.Dockerfile` |
| k6 tests | scenarios, thresholds, `handleSummary` | `src/tests/**` |
| Artifacts / reports | the contract with downstream consumers | `reports/**` |

CI/CD is **external** to Punch. Punch provides reusable local/CI-compatible
container contracts; it does not own GitHub Actions workflows.

## Agentic-coding rules

Custom agents are bounded at runtime by the shared
[`agent-guards.md`](../docs/ai/agent-guards.md) discipline (tool surface, serial
phases, approval-before-write, depth-1 delegation).

- **Never make broad edits during Build.** Each Build prompt declares
  allowed / read-only / forbidden paths. Edit only allowed paths.
- **Never modify Python orchestration, Docker Compose, and k6 tests in
  one task** unless explicitly planned as an integration task with
  multiple per-layer Build calls.
- **Never bypass Docker Compose** by running local `k6` or
  `docker run` directly unless the user explicitly asks.
- **Never introduce CI/CD ownership into Punch** unless explicitly
  requested. `.github/workflows/` is outside Build scope by default.
- **Never change service names, artifact paths, or public commands**
  without updating docs and dependents (see [`docs/ai/maintenance-matrix.md`](../docs/ai/maintenance-matrix.md)).
- **Prefer small diffs.** One scoped task per Build call.
- **Prefer explicit validation commands.** Verify uses
  `./bin/punch doctor` and `./bin/punch run …` — not ad-hoc shell.
- **Preserve DX**: low-noise terminal output plus complete logs and
  artifacts under `reports/`.

## Default verification

- Use official Punch commands when available (`./bin/punch …`).
- Use Docker Compose **through** Punch when possible.
- Use unit tests only as a complement, not a replacement for runtime
  contract validation.

## Engineering Principles

6. **Lifecycle-driven work.** Every change goes through Spec → Plan →
   Build → Verify → Review → Ship (Spec absorbs the former Define step).
   Use the matching prompt in `.github/prompts/`.
7. **Mode discipline.** Read-only requests (audits, reviews,
   explanations) stay in **Ask Mode**. Planning stays in **Ask Mode**
   with Plan discipline. Edits happen only in **Agent Mode** within a
   scoped Plan task. Phase→mode mapping reference:
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
| Verify   | [`punch-verify`](prompts/punch-verify.prompt.md) / [`punch-test`](prompts/punch-test.prompt.md) | Agent / Ask | `punch-verifier` |
| Review   | [`punch-review`](prompts/punch-review.prompt.md)               | Ask                      | `punch-reviewer` |
| Ship     | [`punch-ship`](prompts/punch-ship.prompt.md)                   | Agent (mechanical only)  | `punch-reviewer` |

Spec absorbs the former Define phase (it opens with the clarify/refine step).
Build is a single `punch-build` prompt bound to the `punch-builder` dispatcher,
which classifies the approved Plan task and delegates (depth-1) to
`punch-runtime-engineer` (Python/Compose/harvest) or `punch-performance-test-engineer`
(k6 + TS bundle). `punch-test` is the TDD/Prove-It companion to Verify.

## Change cascade (when X changes, update Y)

When a change touches one area, several others usually need updating in
lockstep. The full file-level cascade lives in
[`docs/ai/maintenance-matrix.md`](../docs/ai/maintenance-matrix.md) —
consult it during Plan and Review.

## PR description

Copy the checklist from [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md)
literally — don't paraphrase or invent extra items. If criteria change,
update the template, not this file.

## When in doubt

Refer to `docs/ai/operating-model.md`, `docs/ai/workflow.md`, and the
instruction fragments under `.github/instructions/`. When proposing
changes that touch multiple matrix rows, document the verification plan
in the PR description.

## graphify (optional documentation mapping)

`graphify` maps this repo into a knowledge graph (`graphify-out/`) — **optional**,
used only as *evidence* to orient analysis. It is **not** the source of truth, and
not every session's first action: **Context Engineering owns when it runs**. See the
Graphify gate in [`punch-context-engineering`](skills/punch-context-engineering/SKILL.md)
— `/graphify .` only when `graphify-out/graph.json` is absent or a broad refresh is
needed; otherwise prefer `graphify query|path|explain`. Graphify orients; **source
validates, tests confirm**.

Host `graphify` is a scoped Rule-1 exception ([ADR 0002](../docs/ai/decisions/0002-graphify-host-tool.md));
`graphify-out/` is throwaway evidence, never canonical. Not installed? Run
`uv tool install graphifyy`. Build or refresh with `/graphify .` in Copilot Chat.

## Caveman (optional concise comms — Punch Build only)

The [`punch-build-caveman`](skills/punch-build-caveman/SKILL.md) adapter lets the
**Build** phase compress assistant **prose** on request (`/caveman lite|full|ultra`,
default `lite`). It is **opt-in, off by default, and never mandatory**. It does
**not** apply to Spec, Plan, Verify, Review, Ship, Governance, documentation, or
architecture reasoning unless the user explicitly asks — those keep normal prose.
The Critical Rules above always take precedence.

Caveman compresses prose only. It must **never** compress, rewrite, summarize, or
omit code, commands, file paths, Python orchestration details, Docker Compose
output, k6 output, JSON/YAML/CSV, logs, stack traces, errors, exit codes, test
evidence (`reports/state/punch-run.json`), acceptance criteria, or risk notes —
quote those verbatim. **Priority: correctness > evidence > maintainability >
brevity.** If brevity harms clarity or risk explanation, stop Caveman.

Adopted as a scoped adapter (the official multi-agent installer was **not** run —
it would make Caveman global and append to these Critical Rules; see
[ADR 0003](../docs/ai/decisions/0003-caveman-build-comms.md) and
[`.ai-upstream/caveman/`](../.ai-upstream/caveman/UPSTREAM.md)).
