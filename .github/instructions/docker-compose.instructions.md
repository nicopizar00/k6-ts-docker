---
applyTo: "docker-compose.yml,docker/**"
description: Behavior rules for Docker and Docker Compose changes.
---

# Docker & Docker Compose — Path Instructions

Scope: `docker-compose.yml` and everything under `docker/`. Compose owns
runtime boundaries; this file is its contract.

## Rules

- **Services are contracts.** Service names, image names, exposed ports,
  env vars, `depends_on`, healthchecks, and volume mounts are part of the
  public surface. Renaming any of them cascades to k6 tests, the
  orchestrator, CI, and docs (see [`docs/ai/maintenance-matrix.md`](../../docs/ai/maintenance-matrix.md)).
- **Do not mutate service names casually.** A rename is its own Plan with a
  dependents grep + update across `src/tests/`, `src/punch/`,
  `.github/workflows/`, and docs.
- **Single compose file.** Do not split into multiple compose files or
  introduce profiles unless a Plan justifies it.
- **Healthchecks gate startup.** Every service has a healthcheck.
  `depends_on: { condition: service_healthy }` is the only ordering
  mechanism. No `sleep` loops in bin scripts or in the orchestrator.
- **No CMD in Dockerfiles for k6.** The compose `command:` is the single
  source of truth for how k6 is invoked.
- **Multi-stage builds for Node services.** Bundling (esbuild) runs in a
  builder stage; runtime images carry only artifacts.
- **Pin `grafana/k6`** to an explicit version. Never `:latest`.
- **No secret bake-ins.** Use environment variables passed through
  compose, never `ARG`s that hardcode credentials.
- **Volumes are read-only by default.** Only `./reports:/reports` is
  writable. Mounts that need write access must be justified in the Plan.
- **No hidden host dependencies.** A fresh clone with only Docker
  installed must be able to run the full suite via `./bin/punch`. If a
  change requires a host-side tool, it goes in `bin/punch doctor`.
- **Local reproducibility.** The Compose run must be deterministic enough
  that two contributors get the same artifact set from the same commit.

## When the orchestrator changes

If `bin/punch` adds a new test target, this layer changes too: add the new
bundle to `docker/k6.Dockerfile` COPY step and ensure the compose
`command:` accepts the script path. Coordinate via a Plan.

## Build prompt

Use [`punch-build-compose`](../prompts/punch-build-compose.prompt.md).
