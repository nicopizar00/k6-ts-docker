---
name: punch-compose-runtime
description: Owns Docker Compose and Dockerfile rules — services as runtime contracts, stable service names, healthcheck gating, env contracts, container-first execution.
applies-to: docker-compose.yml, docker/**
---

# Skill: punch-compose-runtime

## Responsibility

This skill is the authority on **how the runtime is composed**.

It owns:

- The service contract: name, image, exposed ports, env vars, depends_on,
  healthcheck, volumes (see [`compose-contract.md`](compose-contract.md)).
- The single-compose-file rule.
- Container-first execution (everything runs in a container; host owns
  only Docker + Python stdlib).
- Local reproducibility — a fresh clone with only Docker must run the full
  suite via `./bin/punch`.
- The Dockerfile multi-stage pattern (builder stage with esbuild/`npm ci`,
  runtime stage with only artifacts).
- The grafana/k6 pin.
- No-hidden-host-dependencies discipline.

It does **not** own:

- Orchestration control flow (see `punch-python-orchestration`).
- k6 test logic or thresholds (see `punch-k6-performance`).
- The artifact contract for what k6 writes (see `punch-data-harvest`).

## When to use

- Editing `docker-compose.yml`.
- Adding, removing, or renaming a service.
- Adjusting healthchecks or `depends_on`.
- Changing image versions (especially `grafana/k6`).
- Editing any `docker/*.Dockerfile`.

## Inputs expected

- The approved Plan task with allowed/read-only/forbidden paths.
- The intent (new service / image bump / port change / etc.).

## Procedure

1. Read [`compose-contract.md`](compose-contract.md) — confirm the change
   either *adds* a service following the contract or *modifies* an
   existing service within its contract.
2. If the change renames a service or changes a port:
   - Grep for the old name/port across `src/tests/**`, `src/punch/**`,
     `.github/workflows/**`, and docs.
   - List every dependent in the Plan; the rename is incomplete until all
     dependents are updated.
3. Implement the minimum diff inside `docker-compose.yml` and/or
   `docker/`.
4. Preserve healthchecks. No service ships without a healthcheck.
5. Preserve the no-CMD rule for the k6 image (compose `command:` is the
   single source of truth).
6. Pin image tags (no `:latest`).

## Output format

A focused diff under `docker-compose.yml` and `docker/`. Report:

- Every file changed.
- New/changed/removed service names with their contract fields.
- Any dependent file that still needs an update (which should be empty if
  the Plan covered the cascade).

## Safety / boundary rules

- **Service names are contracts.** No casual renames.
- **No secret bake-ins.** Use env vars, never `ARG`s with credentials.
- **Volumes read-only by default.** Only `./reports:/reports` is writable
  (and any future explicitly-justified writable mount).
- **No host dependencies sneaking in.** A change that requires a host
  tool fails the contract — add it to `doctor` or push back.

## Why this is a separate skill

Compose changes are *contract changes*. The cost of mishandling them
(service rename without dependents update, port collision in CI, missing
healthcheck causing flaky CI) is concentrated and expensive. Isolating
the rules makes the cost visible.
