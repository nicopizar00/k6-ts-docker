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

Spec absorbs the former Define phase (it opens with a clarify/refine step). Each phase maps to one prompt under .github/prompts/ and one agent persona under .github/agents/; Build fans out to five domain prompts and five matching builder agents. The lifecycle is the operating system; the agents and skills are behavioral specializations within it.

Available agents

| Agent | Persona | Used by phases |
|---|---|---|
| punch-architect-readonly | Investigator (writes the spec doc) | Spec |
| punch-planner            | Scoped-task planner    | Plan |
| punch-builder-orchestrator | Scope-bound builder (Python orchestrator) | Build |
| punch-builder-compose    | Scope-bound builder (Compose / runtime) | Build |
| punch-builder-k6-http    | Scope-bound builder (k6 HTTP) | Build |
| punch-builder-k6-browser | Scope-bound builder (k6 Browser — deferred) | Build |
| punch-builder-data-harvest | Scope-bound builder (artifacts / reports) | Build |
| punch-verifier           | Evidence collector     | Verify, Test |
| punch-reviewer           | Diff critic + ship mechanic | Review, Ship |

Definitions live in .github/agents/*.agent.md.

Available skills

Skills come in two kinds: **domain skills** (one per Punch subsystem) and **lifecycle skills** (engineering methods adapted from the upstream agent-skills set; more arrive via the absorption plan in docs/ai/agent-skills-absorption-plan.md).

Domain skills:

| Skill | Decision domain |
|---|---|
| punch-context              | Project-wide primer for new agents |
| punch-python-orchestration | The bin/punch CLI and subprocess control flow |
| punch-docker-compose       | Compose service contracts and Dockerfiles |
| punch-k6-performance       | k6 test conventions, thresholds, handleSummary |
| punch-data-harvest         | Artifact paths, schemas, terminal-vs-file noise |
| punch-governance-review    | AI configuration health |

Lifecycle skills:

| Skill | Method |
|---|---|
| idea-refine | Refine a raw idea before Spec (divergent → convergent) |

Definitions live in .github/skills/<skill>/SKILL.md. The register is docs/ai/skill-registry.md.

Lifecycle entry points

| Phase | Prompt | Mode |
|---|---|---|
| Spec   | punch-spec                                         | Ask (writes spec doc) |
| Plan   | punch-plan                                         | Ask (Plan discipline) |
| Build  | one of punch-build-orchestrator / -compose / -k6-http / -k6-browser / -data-harvest | Agent (scoped) |
| Verify | punch-verify (+ punch-test, the TDD companion)     | Agent / Ask |
| Review | punch-review                                       | Ask |
| Ship   | punch-ship                                         | Agent (mechanical only) |

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

For deeper reading

- CLAUDE.md — project rules and architectural constitution
- docs/architecture/punch-boundaries.md — layered ownership map
- docs/ai/operating-model.md — the lifecycle and asset taxonomy
- docs/ai/workflow.md — lifecycle walkthrough with a worked example
- docs/ai/scoped-build-policy.md — allowed/forbidden paths by Build domain
- docs/ai/model-selection.md — which model class for which phase
