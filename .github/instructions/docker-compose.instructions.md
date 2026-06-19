---
applyTo: "docker-compose.yml,docker/**"
description: Behavior rules for Docker and Docker Compose changes.
---
# Docker & Docker Compose — Path Instructions

Scope: `docker-compose.yml` and all under `docker/`. Compose own runtime boundaries; this file its contract.

## Rules

- **Services are contracts.** Service names, image names, exposed ports,
  env vars, `depends_on`, healthchecks, volume mounts = public surface. Rename any
  cascade to k6 tests, orchestrator, CI, docs (see [`docs/ai/maintenance-matrix.md`](../../docs/ai/maintenance-matrix.md)).
- **Do not mutate service names casually.** Rename = own Plan with
  dependents grep + update across `src/tests/`, `src/punch/`,
  `.github/workflows/`, docs.
- **Single compose file.** No split into multiple compose files, no
  profiles unless Plan justify.
- **Healthchecks gate startup.** Every service has healthcheck.
  `depends_on: { condition: service_healthy }` only ordering
  mechanism. No `sleep` loops in bin scripts or orchestrator.
- **No CMD in Dockerfiles for k6.** Compose `command:` single
  source of truth for how k6 invoked.
- **Multi-stage builds for Node services.** Bundling (esbuild) run in
  builder stage; runtime images carry only artifacts.
- **Pin `grafana/k6`** to explicit version. Never `:latest`.
- **No secret bake-ins.** Use env vars passed through
  compose, never `ARG`s that hardcode credentials.
- **Volumes are read-only by default.** Only `./reports:/reports`
  writable. Mounts needing write access must justify in Plan.
- **No hidden host dependencies.** Fresh clone with only Docker
  installed must run full suite via `./bin/punch`. Change needing
  host-side tool goes in `bin/punch doctor`.
- **Local reproducibility.** Compose run must be deterministic enough
  that two contributors get same artifact set from same commit.

## When the orchestrator changes

If `bin/punch` add new test target, this layer change too: add new
bundle to `docker/k6.Dockerfile` COPY step, ensure compose
`command:` accept script path. Coordinate via Plan.

## Build prompt

Use [`punch-build`](../prompts/punch-build.prompt.md) — dispatcher routes Compose tasks to `punch-runtime-engineer`.
