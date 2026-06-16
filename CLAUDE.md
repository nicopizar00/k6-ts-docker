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
    │       └── __main__.py               # argparse CLI; streams docker compose
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
    │   ├── ai/                           # AI lifecycle docs
    │   │   ├── operating-protocol.md
    │   │   ├── copilot-mode-mapping.md
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
        ├── prompts/                      # one prompt per lifecycle phase
        ├── skills/                       # three behavioral skills
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
2. **Small, reviewable steps.** Each change should be understandable in one
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

- Read this file first, then `docs/ai/operating-protocol.md`,
  `docs/architecture.md`, and `docs/ai-context.md`.
- The operating model is **Understand → Shape → Build → Verify → Review →
  Ship**. Use the matching prompt in `.github/prompts/` and stay in the
  declared mode (Ask vs Agent).
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
  Verify run. See `docs/workflows/validation.md`.
- Propose changes in small, reviewable steps. Do not implement a full feature
  in one pass unless explicitly asked.
- When in doubt, ask.
