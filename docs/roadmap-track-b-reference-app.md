# Track B: Reference Application and GitHub Actions Playground

## Purpose

Track B expands the project from a single-service POC into a small, didactic reference application that demonstrates realistic performance testing patterns. The goal is to make it easy for other service teams to understand how to adopt the same approach without owning the pipeline internals.

This track does not replace Track A. It runs in parallel and provides the richer target application that Track A's gate patterns can run against.

## Reference application

The reference app consists of four services:

| Service | Port | Role |
|---|---|---|
| `gateway-api` | 3000 | Main entrypoint. Demonstrates the BFF / API gateway pattern. Proxies to catalog and orders. |
| `catalog-api` | 3001 | Read-only product catalog. Demonstrates GET endpoint performance gates. |
| `orders-api` | 3002 | Write/read order service backed by Postgres. Demonstrates create-read consistency. |
| `postgres` | 5432 | Relational persistence. Demonstrates healthcheck ordering, seeded state, real dependency. |

All services communicate over Docker Compose's internal network using service names as hostnames.

## k6 test suite

The suite is organized into three categories:

| Test | File | Pattern |
|---|---|---|
| Smoke | `src/tests/smoke.ts` | Health check across all three APIs. Validates the stack is reachable. |
| Catalog gate | `src/tests/catalog-gate.ts` | Performance gate for catalog reads. Thresholds on error rate, p95, check pass rate. |
| Order journey | `src/tests/order-journey.ts` | Create an order → read it back → validate consistency. Writes a state file. |

A shared HTML report builder lives in `src/tests/support/report.ts`. All three tests use it to produce self-contained, static HTML reports.

## Data handling

- **Catalog**: static, in-memory. Products are deterministic (`prod-001`, `prod-002`, `prod-003`).
- **Orders**: created during the test, read back immediately. The journey validates consistency within the same VU iteration. No cross-VU state sharing is required.
- **Journey state file** (`reports/state/test-context.json`): written by `handleSummary` in `order-journey.ts`. Contains journey-specific metadata (created order id, error rate, p95, journey pass/fail signal). Used for journey artifact inspection — not the canonical run evidence (see `reports/state/punch-run.json` for that).
- **Docker logs** (`reports/logs/*.log`): collected after the suite runs. Primary evidence for debugging failures.

## Compose strategy

A single `docker-compose.yml` handles all modes:

- **App services only**: `docker compose up -d --wait gateway-api` — starts postgres → orders-api → catalog-api → gateway-api in dependency order.
- **Single test**: `docker compose run --rm k6 run ... /scripts/<test>.js` — starts app services if needed (honoring healthcheck conditions), runs k6, removes the k6 container.
- **Full suite**: `./bin/test-suite` — builds, starts the app, runs all three tests sequentially, collects logs, tears down.
- **External target**: Set `TARGET_BASE_URL` env var to point k6 at an external service. The app services are not required in this mode, though you must start k6 manually or extend the compose command.

## Stages

### B1 — Reference app with gateway, catalog, orders, and Postgres ✓
Three Node.js services and Postgres. Pure `http` module for gateway and catalog; `pg` for orders. All services expose `/health`.

### B2 — Deterministic seed data ✓
Catalog products are static. Postgres schema initialized via `docker/postgres/init.sql`.

### B3 — Smoke test across all services ✓
Updated `smoke.ts` checks gateway, catalog, and orders health endpoints in one run.

### B4 — Catalog read performance gate ✓
`catalog-gate.ts` with thresholds: `http_req_failed < 1%`, `p95 < 500ms`, `checks > 99%`.

### B5 — Order create-read journey ✓
`order-journey.ts` creates an order, captures the ID, reads it back, and validates response consistency.

### B6 — Reports, logs, and state artifacts ✓
Each test produces an HTML report. The journey test also writes `reports/state/test-context.json`. Docker logs are collected to `reports/logs/`. All uploaded as a single GitHub Actions artifact.

### B7 — GitHub Actions artifact transfer and validation job ✓
A second CI job downloads the artifact and validates that every expected file is present. Proves serialized state transfer between jobs without live containers.

### B8 — External target mode (planned)
Allow k6 to run against a `TARGET_BASE_URL` without starting the reference app. Requires a compose profile or separate script that skips the app services.

### B9 — Reusable workflow integration (planned)
Expose the test suite as a `workflow_call` workflow so other repositories can invoke it with a `uses:` line. Only begins after Track A Stage 3 thresholds are stable.

## Non-goals

- No Kafka, Redis, or Kubernetes.
- No real authentication or JWT.
- No Datadog, Grafana, or Prometheus.
- No published GitHub Marketplace Action.
- No complex scenario orchestration or sustained load testing.
- No generic microservices platform.
