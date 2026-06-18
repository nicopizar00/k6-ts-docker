AGENTS.md — AI Agents guide for this repository

Project Overview

k6-ts-docker is a didactic performance testing playground that bundles TypeScript k6 tests into Docker images and runs them against a small multi-service reference app via docker compose and GitHub Actions. The host requirements are only Docker and Python 3 (stdlib).

The orchestrator is called **Punch** (`bin/punch`, `src/punch/`).

Repository Structure

- src/services/ : reference services (gateway, catalog, orders)
- src/tests/ : k6 TypeScript test sources (smoke, gate, journey)
- src/punch/  : Python stdlib-based orchestrator used by ./bin/punch
- docker/    : Dockerfiles and postgres init SQL
- .github/   : workflows, prompts, skills, instructions, agents
- dist/      : esbuild output (gitignored)
- reports/   : run artifacts and validation state

Tech Stack

- k6 (execution) — tests written in TypeScript and bundled with esbuild during Docker image build
- TypeScript/Node (build only inside Docker)
- Docker Compose for local orchestration
- Python 3 (stdlib) for the thin CLI wrapper at bin/punch
- Postgres 16 for orders persistence

Build & Run

- Use the Python CLI: ./bin/punch run smoke | gate | journey | all
- Legacy bash helpers available in ./bin/ (build, test-*)
- CI builds images via docker compose build then runs the k6 suite inside the k6 service

Testing & Validation

- k6 tests produce HTML + JSON reports in reports/
- Validation job downloads artifacts and verifies expected files exist (see .github/workflows/k6.yml)
- Every verification run must produce reports/state/punch-run.json

CI / Workflows

- Primary workflow: .github/workflows/k6.yml — runs on push and pull_request to the default branch and validates artifact transfer between jobs
- AI setup workflow: .github/workflows/copilot-setup-steps.yml — helps contributors and Copilot-style agents prepare the repo environment

Key Patterns and Conventions

- Docker First: all builds and tests run inside Docker; do not assume node or k6 on host
- Python stdlib only for orchestration — no pip deps
- Keep the execution chain: TypeScript -> esbuild (in Docker) -> k6 image -> run -> reports

AI Operating Model

Punch uses a six-phase lifecycle for AI-assisted changes:

    Spec → Plan → Build → Verify → Review → Ship

Spec absorbs the former Define phase (it opens with a clarify/refine step). Each phase maps to one prompt under .github/prompts/ and one agent persona under .github/agents/; Build is driven by a single `punch-build` prompt and the `punch-builder` dispatcher, which delegates (depth-1) to two domain engineers (`punch-runtime-engineer`, `punch-performance-test-engineer`). The lifecycle is the operating system; the agents and skills are behavioral specializations within it.

Available agents

| Agent | Persona | Used by phases |
|---|---|---|
| punch-architect-readonly | Investigator (writes the spec doc) | Spec |
| punch-planner            | Scoped-task planner    | Plan |
| punch-builder            | Build dispatcher (routes to one engineer) | Build |
| punch-runtime-engineer   | Runtime engineer (Python orchestration / Compose / data harvest) | Build, Verify |
| punch-performance-test-engineer | Performance engineer (k6 HTTP/Browser + TS bundle/lint) | Build, Verify |
| punch-verifier           | Evidence collector     | Verify, Test |
| punch-reviewer           | Diff critic + ship mechanic | Review, Ship |
| security-auditor         | Security audit (specialist, on-demand) | Review security axis, `@security-auditor` |
| punch-ai-governance      | AI-config maintainer (user-direct; graphify-only terminal per ADR 0002; never a sub-agent) | `@punch-ai-governance`, Review AI-config axis |

Definitions live in .github/agents/*.agent.md.

**Build delegation.** `punch-builder` lists exactly its two engineers in
`agents:`; each engineer carries `agents: []` (depth-1, no recursion). The
`punch-ai-governance` maintainer is user-direct (`disable-model-invocation: true`)
and appears in no `agents:` allowlist.

**Specialist personas** (invoked on-demand via `@mention`, not bound to a phase) sit alongside the phase personas; `security-auditor` is the first. Upstream `code-reviewer` is folded into `punch-reviewer` + the `code-review-and-quality` skill; `test-engineer` (covered by `punch-verifier`) and `web-performance-auditor` (no frontend) are excluded.

Available skills

Skills come in two kinds: **domain skills** (one per Punch subsystem — context, orchestration, compose, k6-performance, data-harvest, governance) and **lifecycle skills** (engineering methods adapted from upstream — spec-driven-development, planning, incremental-implementation, test-driven-development, debugging, code-review, simplification, git-workflow, docs/ADRs, security, doubt-driven, source-driven, idea-refine).

The authoritative register (all 19, with a "which skill when" discovery index) is **docs/ai/skill-registry.md**; definitions live in .github/skills/<skill>/SKILL.md.

Lifecycle entry points

The phase → prompt → agent → mode mapping is tabled in .github/copilot-instructions.md and docs/ai/prompt-registry.md (9 prompts: spec, plan, build, test, verify, review, ship, document, init). `punch-init` (bootstrap/adoption guard) and `punch-document` (doc reconciliation) are orthogonal phases, both enforced to `punch-ai-governance`.

Rules for AI assistants

- Broad read before narrow write. Spec/Plan read widely; Build edits narrowly.
- No Build without Plan. Every Build call must reference an approved Plan task ID with allowed/read-only/forbidden paths.
- No scope expansion inside Build. If a Build needs to touch a file outside the task's allowed paths, stop and return to Plan.
- Verify through Punch official commands. ./bin/punch doctor and ./bin/punch run <test> are the verification contract — not host-side docker or k6.
- Review before Ship. Ship is mechanical only (git/gh); it never introduces new logic.
- Humans merge. Ship opens the PR; humans approve and merge.

Adding a new test

1. Add a TypeScript file under src/tests/
2. Ensure the file imports support/report.ts for shared reporting
3. Confirm the new test is bundled into dist/ by the Docker build
4. Add execution steps and artifact expectations to .github/workflows/k6.yml if the test is part of the CI suite

Common Pitfalls

- Editing dist/ directly: dist/ is generated by the build stage inside Docker — don't commit built bundles unless intentional
- Host-side tooling: avoid adding host-side npm/k6/pip assumptions. Use ./bin/punch which shells out to docker compose

Caveman comms

Caveman compresses concise assistant **prose** (canonical Copilot skill `.agents/skills/caveman/`, Punch single-source policy `.github/skills/punch-build-caveman/`). Project default is **`lite`**, with a per-phase canon: Document/Spec `lite` · Plan/Review/Ship `full` · Build/Test `ultra` (the enforced phases). **Sub-agent reports are `wenyan`** at every level; **Wenyan is forbidden in persistent artifacts** (docs, ADRs, specs, plans, maps, skills, prompts, registries, handoffs, `reports/**`). Non-Build/Test agents lead with **normal prose** for judgment-heavy work and keep all capabilities/constraints. Caveman is output style only — it never changes tools, access, or delegation. It never compresses code, commands, paths, logs, errors, exit codes, thresholds, k6/Docker Compose output, JSON/YAML/CSV, `reports/state/punch-run.json`, acceptance criteria, blockers, or next-action. `/caveman lite|full|ultra|wenyan-*`; `stop caveman` reverts. Full canon + depth policy: `.github/skills/punch-build-caveman/SKILL.md` + ADR 0003.

Claude Code reuse (Guard bridge)

GitHub Copilot VS Code is the primary host; `.github/` is the single source of truth. When the repo is opened in Claude Code, the project-scoped `guard` skill (`.claude/skills/guard/SKILL.md`) and thin command wraps (`.claude/commands/{spec,plan,build,test,review,ship,document,init}.md`) **reuse** the canonical `.github/` prompts/agents/skills — they never fork, duplicate, or override them. Rules change in `.github/` (Copilot First), never only in `.claude/`. See ADR 0004.

For deeper reading

- CLAUDE.md — project rules and architectural constitution
- docs/architecture/punch-boundaries.md — layered ownership map
- docs/ai/operating-model.md — the lifecycle and asset taxonomy
- docs/ai/workflow.md — lifecycle walkthrough with a worked example
- docs/ai/scoped-build-policy.md — allowed/forbidden paths by Build domain
- docs/ai/model-selection.md — which model class for which phase
