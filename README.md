# k6-ts-docker

A didactic performance testing playground for k6 written in TypeScript, packaged in Docker, and executed via GitHub Actions.

## Goal

Demonstrate a maintainable, end-to-end performance testing pipeline — from a multi-service reference application through to GitHub Actions artifact transfer — that is easy to read, extend, and adopt.

## Quick start

Requires only Docker. No Node, no k6, no other runtimes on the host.

```bash
./bin/build          # Build all images (bundles TypeScript internally)
./bin/test-smoke     # Health smoke across all services
./bin/test-gate      # Catalog read performance gate
./bin/test-journey   # Order create-read journey (writes state/test-context.json)
./bin/test-suite     # All three tests in sequence + log collection + teardown
./bin/clean          # Stop containers and remove locally-built images
```

## Reference application

The suite runs against a small four-service reference app:

| Service | Port | Role |
|---|---|---|
| `gateway-api` | 3000 | BFF / API gateway — proxies catalog and order requests |
| `catalog-api` | 3001 | Read-only product catalog — demonstrates GET gates |
| `orders-api` | 3002 | Create/read orders backed by Postgres |
| `postgres` | 5432 | Relational persistence with healthcheck and seed schema |

## k6 test suite

| Test | What it demonstrates |
|---|---|
| `smoke` | All services are reachable and healthy |
| `catalog-gate` | p95 latency and error-rate thresholds on catalog reads |
| `order-journey` | Create an order, read it back, validate consistency; writes a state file |

## Execution chain

```
TypeScript source  →  esbuild (inside Docker)  →  k6 image  →  run  →  reports
```

Every change preserves this linear pipeline.

## Reports and artifacts

After a test run, `reports/` contains:

```
reports/
  smoke-report.html
  smoke.json
  catalog-gate-report.html
  catalog-gate.json
  order-journey-report.html
  order-journey.json
  state/
    test-context.json        # serialized journey metadata
  logs/
    gateway-api.log
    catalog-api.log
    orders-api.log
    postgres.log
```

GitHub Actions uploads all of these as the `performance-suite-reports` artifact. A second CI job downloads the artifact and validates that every expected file is present — demonstrating serialized state transfer between jobs without live containers.

## Next steps

- Track A roadmap: [`docs/roadmap-track-a-performance-gate.md`](docs/roadmap-track-a-performance-gate.md)
- Track B roadmap: [`docs/roadmap-track-b-reference-app.md`](docs/roadmap-track-b-reference-app.md)
- Contribution rules: [`CLAUDE.md`](CLAUDE.md)
