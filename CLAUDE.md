# k6-ts-docker

A didactic performance testing playground for k6 written in TypeScript, packaged in Docker, and executed via GitHub Actions. It includes a small multi-service reference application so that realistic testing patterns — health smoke, performance gate, create-read journey — can be demonstrated end-to-end.

## Purpose

Show how to build and run a Docker First k6 test suite against a realistic (but minimal) multi-service target, from local execution through GitHub Actions artifact collection.

Long-term goal: evolve into a reusable GitHub Actions-based performance gate that other service teams can consume without owning the pipeline internals. See the roadmap docs for the planned evolution path.

## Execution chain

The project follows a single, linear pipeline. Every change should preserve it:

    TypeScript source  →  esbuild (in builder stage)  →  Docker image  →
    k6 execution       →  reports (JSON / HTML / state)

If a proposed change does not fit this chain, stop and discuss before adding it.

## Tech stack

- **k6** — load testing runtime (executes the bundled JS).
- **TypeScript** — author tests with types and editor support.
- **esbuild** — bundles TypeScript to one ES module per test file. Runs inside the Docker build stage; not required on the host.
- **Docker / Docker Compose** — primary interface. Multi-stage build handles bundling and execution. Host requires only Docker.
- **Python 3 (stdlib only)** — thin orchestration façade at `bin/punch` (entry point) and `src/punch/` (CLI module). No pip dependencies; uses `argparse`, `subprocess`, `pathlib`, `json`, `os`, `sys` only.
- **GitHub Actions** — builds, runs the full test suite, collects artifacts, validates artifact transfer between jobs.
- **Postgres 16** — persistence for the orders reference service. Schema seeded via `docker/postgres/init.sql`.
- **pg** — Postgres client used only by `orders-api`, installed inside its Docker image.

## Project structure

    .
    ├── CLAUDE.md
    ├── README.md
    ├── package.json               # TypeScript + esbuild deps only
    ├── tsconfig.json
    ├── src/
    │   ├── services/
    │   │   ├── gateway/server.js  # BFF gateway, proxies catalog + orders
    │   │   ├── catalog/server.js  # read-only product catalog (in-memory)
    │   │   └── orders/
    │   │       ├── server.js      # create/read orders via Postgres
    │   │       └── package.json   # pg dependency (orders only)
    │   ├── tests/
    │   │   ├── smoke.ts                  # health smoke across all services
    │   │   ├── catalog-gate.ts           # performance gate for catalog reads
    │   │   ├── order-journey.ts          # create → read → validate journey
    │   │   ├── browser-smoke.ts.example  # deferred k6 Browser placeholder
    │   │   └── support/
    │   │       └── report.ts             # shared HTML report builder
    │   └── punch/                        # Python orchestrator (stdlib only)
    │       ├── __init__.py
    │       ├── __main__.py               # argparse CLI; streams docker compose
    │       └── init_scan.py              # `punch init` bootstrap scanner / readiness mapper
    ├── dist/                             # bundled k6-ready JS (gitignored)
    ├── reports/                          # k6 output (gitignored)
    │   ├── state/                        # machine-readable state files
    │   └── logs/                         # Docker service logs
    ├── docker/
    │   ├── gateway.Dockerfile
    │   ├── catalog.Dockerfile
    │   ├── orders.Dockerfile
    │   ├── k6.Dockerfile
    │   └── postgres/
    │       └── init.sql
    ├── docker-compose.yml                # all services + k6 in one file
    ├── bin/
    │   ├── punch                         # Python orchestrator entry point
    │   ├── build
    │   ├── test-smoke
    │   ├── test-gate
    │   ├── test-journey
    │   ├── test-suite
    │   └── clean
    ├── docs/
    │   ├── architecture.md               # existing — folder map, execution chain
    │   ├── ai-context.md                 # existing — project philosophy
    │   ├── how-to-run.md                 # existing — run commands
    │   ├── architecture/
    │   │   └── punch-boundaries.md       # layered ownership map
    │   ├── ai/                           # AI lifecycle docs + agent-skills absorption review/plan
    │   │   ├── operating-model.md
    │   │   ├── workflow.md
    │   │   ├── scoped-build-policy.md
    │   │   ├── model-selection.md
    │   │   ├── copilot-mode-mapping.md
    │   │   ├── maintenance-matrix.md
    │   │   ├── skill-registry.md
    │   │   └── prompt-registry.md
    │   ├── workflows/
    │   │   ├── lifecycle.md
    │   │   └── validation.md
    │   └── validation/
    │       └── README.md                 # how to read reports/
    └── .github/
        ├── copilot-instructions.md       # always-on global Copilot rules
        ├── instructions/                 # path-specific behavior rules
        ├── prompts/                      # 8 lifecycle prompts (Spec→Ship + punch-test + punch-document)
        ├── skills/                       # domain + lifecycle skills (docs/ai/skill-registry.md)
        ├── agents/                       # agent personas (lifecycle + punch-builder dispatcher + 2 engineers + specialists)
        └── workflows/
            └── k6.yml

Anything not listed here needs justification before being added.

## Rules

1. **Docker First.** Docker is the primary interface for building, running, and
   validating the project. The host requires only Docker and a stdlib Python 3
   runtime — no Node, no k6, no pip-installed packages.
   `npm`/bundler/`pg` invocations happen inside Docker build stages and are
   implementation details, not user-facing commands. The Python orchestrator
   is a thin façade that shells out to `docker compose`; it adds no execution
   semantics of its own.
   **Two scoped exceptions:** (a) the `punch-performance-test-engineer` agent may
   run host `npm`/`pnpm`/esbuild/lint — and host `k6` for the `npm run smoke:local`
   smoke pre-check — while *authoring* the k6 TS test toolchain
   ([ADR 0001](docs/ai/decisions/0001-perf-engineer-host-npm.md)); and (b) the
   `punch-ai-governance` agent may run host `graphify` for the `/punch-document`
   documentation map ([ADR 0002](docs/ai/decisions/0002-graphify-host-tool.md)).
   Both are *authoring/maintenance* conveniences off the evidence path; the shipped
   chain still bundles in `docker/k6.Dockerfile`, and `smoke:local`/`graphify-out/`
   are not the evidence path.
2. **Small, reviewable steps.** Each change must be understandable in one
   sitting. Prefer multiple small PRs over one large one.
3. **No unnecessary dependencies.** Every dependency must earn its place. If
   the standard library or a few lines of code suffice, use those.
4. **No premature abstraction.** Three similar lines are better than a clever
   helper. Wait for the third real use case before extracting.
5. **Preserve the execution chain.** Source → bundle → image → run → report.
   Don't shortcut or branch it.
6. **AI-friendly.** File names, directory layout, and scripts should be
   self-describing. Avoid hidden conventions.
7. **Don't implement ahead of the plan.** Follow the agreed step list; flag
   anything that requires going beyond it.

## Common commands

Preferred entry point (Python orchestrator):

- `./bin/punch doctor` — confirm host prerequisites.
- `./bin/punch init` — one-time, non-destructive first-wave scan that maps the
  repo's Copilot assets + docs readiness for Punch adoption (Punch = template
  origin; resolves a local governance key). Dry-run by default; `--write` to
  persist the disposable bootstrap reports under `docs/ai/governance/init/`. It
  prepares the repo for `/document`; it does **not** reconcile docs.
- `./bin/punch run smoke` — run health smoke test; results in `reports/`.
- `./bin/punch run gate` — run catalog performance gate.
- `./bin/punch run journey` — run order create-read journey.
- `./bin/punch run all --collect-logs` — full suite + collect service logs.
- `./bin/punch clean` — tear down containers and volumes.

Legacy bash equivalents (still supported, will be retired once the
Python CLI reaches feature parity):

- `./bin/build`, `./bin/test-smoke`, `./bin/test-gate`, `./bin/test-journey`,
  `./bin/test-suite`, `./bin/clean`.

## For AI assistants

- Read this file first, then `docs/ai/operating-model.md`,
  `docs/architecture.md`, `docs/architecture/punch-boundaries.md`,
  and `docs/ai-context.md`.
- **GitHub Copilot is the primary host;** `.github/` is the single source of
  truth for AI config. In **Claude Code**, activate the `guard` skill
  (`.claude/skills/guard/SKILL.md`) — it reuses the `.github/` prompts/agents/
  skills via the `.claude/commands/*` wraps (`/spec … /document`); it never
  forks or overrides them ([ADR 0004](docs/ai/decisions/0004-claude-code-guard-bridge.md)).
- The operating model is **Spec → Plan → Build → Test → Review →
  Ship** (Spec absorbs the former Define clarify step). Use the matching
  prompt in `.github/prompts/` and stay in the declared mode (Ask vs
  Agent). Build is a single `punch-build` prompt; the `punch-builder`
  dispatcher routes the approved task to `punch-runtime-engineer` or
  `punch-performance-test-engineer` — see
  `docs/ai/scoped-build-policy.md`. Each phase activates a lifecycle
  method skill + a domain skill; the *which skill when* index is in
  `docs/ai/skill-registry.md`.
- Before adding files, dependencies, or abstractions, confirm they fit the
  execution chain and the structure above.
- `src/services/` contains Node.js services for the reference application.
  They run inside Docker — the host never installs their dependencies.
- `src/tests/` contains k6 TypeScript. esbuild bundles each test file into
  `dist/`. The support module is bundled into each test, not a separate
  output. `browser-smoke.ts.example` is a deferred placeholder — do not
  build it.
- `src/punch/` is the Python orchestrator. Stdlib only — no pip
  dependencies, ever.
- A change is not "done" until `reports/state/punch-run.json` records the
  Test run. See `docs/workflows/validation.md`.
- Propose changes in small, reviewable steps. Do not implement a full feature
  in one pass unless explicitly asked.
- When in doubt, ask.
