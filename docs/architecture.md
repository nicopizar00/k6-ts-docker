# Architecture

## Execution chain

```
TypeScript source  →  esbuild (inside Docker build stage)  →  k6 image  →  run  →  reports
```

This linear flow is preserved by every change. Do not add branches or shortcuts.

## Reference application

The k6 suite runs against a four-service reference application that lives entirely inside Docker Compose:

```
k6  →  gateway-api:3000
            ├──  catalog-api:3001   (in-memory product catalog)
            └──  orders-api:3002    (Postgres-backed order service)
                      └──  postgres:5432
```

All services communicate over Docker Compose's internal bridge network using service names as hostnames.

## Folder map

| Path | Responsibility |
|---|---|
| `src/tests/` | k6 test scenarios (TypeScript). One file per scenario. |
| `src/tests/support/` | Minimal shared helpers (HTML report builder). |
| `src/services/gateway/` | gateway-api — Node.js HTTP, no external deps. |
| `src/services/catalog/` | catalog-api — Node.js HTTP, in-memory data. |
| `src/services/orders/` | orders-api — Node.js HTTP + `pg` for Postgres. |
| `docker/` | One Dockerfile per service plus `postgres/init.sql`. |
| `docker-compose.yml` | Single source of truth for how all services run together. |
| `dist/` | Bundled k6-ready JavaScript — one file per test. Gitignored. |
| `reports/` | Test output: HTML, JSON, state files, Docker logs. Gitignored. |
| `bin/` | Docker First shell scripts for local and CI use. |
| `docs/` | Architecture, how-tos, roadmaps, AI context. |

## Tech stack

- **k6** — Load testing runtime (executes bundled JS).
- **TypeScript** — Authoring tests with types and editor support.
- **esbuild** — Bundles TypeScript to separate ES module files k6 can run. Runs inside the Docker build stage; not required on the host.
- **Docker / Docker Compose** — Primary interface. Multi-stage build handles bundling and execution. Host requires only Docker.
- **GitHub Actions** — CI: builds images, starts app, runs all three tests, collects artifacts, validates transfer.
- **Postgres 16** — Persistence for the orders service. Seeded via `docker/postgres/init.sql`.
- **pg (Node.js)** — Postgres client used only by `orders-api`. Installed inside the orders Docker image; not a host dependency.

## Why this shape

- **Docker First** — Host requires only Docker. Node, esbuild, and pg run inside their respective Docker build or runtime stages.
- **One compose file** — `docker-compose.yml` is the single source of truth. `depends_on` with `condition: service_healthy` enforces startup order. `docker compose run --rm k6` honours those conditions, so bin scripts don't need manual wait loops.
- **One bundle file per test** — Keeps the k6 image simple. The builder stage copies all `dist/` files; the compose command picks which script to run.
- **Shared report builder** — `src/tests/support/report.ts` is bundled into each test by esbuild. Not an entrypoint — no separate output file.
- **State files over logs** — `reports/state/test-context.json` is machine-readable. Docker logs go to `reports/logs/` for human debugging. Automation reads the state file; humans read the logs and HTML reports.
