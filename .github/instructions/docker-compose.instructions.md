---
applyTo: "docker-compose.yml,docker/**"
description: Behavior rules for Docker and Docker Compose changes.
---

# Docker & Docker Compose — Path Instructions

Scope: `docker-compose.yml` and everything under `docker/`.

## Rules

- **Single compose file.** Do not split into multiple compose files or
  introduce profiles unless a Shape plan justifies it.
- **Healthchecks gate startup.** Every service has a healthcheck.
  `depends_on: { condition: service_healthy }` is the only ordering mechanism.
  Do not add `sleep` loops in bin scripts or in the orchestrator.
- **No CMD in Dockerfiles for k6.** The compose `command:` is the single source
  of truth for how k6 is invoked.
- **Multi-stage builds for Node services.** Bundling (esbuild) runs in a
  builder stage; runtime images carry only artifacts.
- **Pin grafana/k6** to an explicit version. Never `:latest`.
- **No secret bake-ins.** Use environment variables passed through compose,
  never `ARG`s that hardcode credentials.
- **Volumes are read-only by default.** Only `./reports:/reports` is writable.

## When the orchestrator changes

If `bin/punch` adds a new test target, this layer changes too:
add the new bundle to `docker/k6.Dockerfile` COPY step and ensure the
compose `command:` accepts the script path. Coordinate via a Shape plan.
