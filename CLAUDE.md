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
    │   └── tests/
    │       ├── smoke.ts           # health smoke across all services
    │       ├── catalog-gate.ts    # performance gate for catalog reads
    │       ├── order-journey.ts   # create → read → validate journey
    │       └── support/
    │           └── report.ts      # shared HTML report builder
    ├── dist/                      # bundled k6-ready JS (gitignored)
    ├── reports/                   # k6 output (gitignored)
    │   ├── state/                 # machine-readable state files
    │   └── logs/                  # Docker service logs
    ├── docker/
    │   ├── gateway.Dockerfile
    │   ├── catalog.Dockerfile
    │   ├── orders.Dockerfile
    │   ├── k6.Dockerfile
    │   └── postgres/
    │       └── init.sql
    ├── docker-compose.yml         # all services + k6 in one file
    ├── bin/
    │   ├── build
    │   ├── test-smoke
    │   ├── test-gate
    │   ├── test-journey
    │   ├── test-suite
    │   └── clean
    └── .github/
        └── workflows/
            └── k6.yml

Anything not listed here needs justification before being added.

## Rules

1. **Docker First.** Docker is the primary interface for building, running, and
   validating the project. The host requires only Docker — no Node, no k6, no
   other runtimes. `npm`/bundler/`pg` invocations happen inside Docker build
   stages and are implementation details, not user-facing commands.
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

- `./bin/build` — build all Docker images (bundles TypeScript internally).
- `./bin/test-smoke` — run health smoke test; results in `reports/`.
- `./bin/test-gate` — run catalog performance gate.
- `./bin/test-journey` — run order create-read journey.
- `./bin/test-suite` — run full suite, collect logs, tear down.
- `./bin/clean` — stop containers and remove locally-built images.

## For AI assistants

- Read this file first, then `docs/architecture.md` and `docs/ai-context.md`.
- Before adding files, dependencies, or abstractions, confirm they fit the
  execution chain and the structure above.
- `src/services/` contains Node.js services for the reference application.
  They run inside Docker — the host never installs their dependencies.
- `src/tests/` contains k6 TypeScript. esbuild bundles each test file into
  `dist/`. The support module is bundled into each test, not a separate output.
- Propose changes in small, reviewable steps. Do not implement a full feature
  in one pass unless explicitly asked.
- When in doubt, ask.
