# How to Run

## Prerequisites

Docker only. No Node, no k6 on the host.

## Local execution

### 1. Build all images

```bash
./bin/build
```

Builds four Docker images:
- **k6** — two-stage build: Node/esbuild bundles TypeScript, then `grafana/k6` copies the output.
- **gateway-api**, **catalog-api**, **orders-api** — Node.js services for the reference application.

Postgres is pulled from the public registry; no build step needed.

### 2. Run a single test

```bash
./bin/test-smoke     # Health smoke — checks all three services are reachable
./bin/test-gate      # Catalog performance gate — p95, error rate, check pass rate thresholds
./bin/test-journey   # Order create-read journey — POST /orders → GET /orders/:id → validate
```

Each script builds images if needed, starts the full reference app (postgres → orders-api → catalog-api → gateway-api), waits for healthchecks, then runs the specified k6 test. After the test, app services remain running for fast re-runs. Call `./bin/clean` to tear down.

### 3. Run the full suite

```bash
./bin/test-suite
```

Builds images, starts the app once, runs all three tests in sequence, collects Docker logs to `reports/logs/`, then tears down. Results appear in `reports/`.

### 4. Clean up

```bash
./bin/clean
```

Stops containers and removes locally-built images. Run this before a clean rebuild, or after a failed test to ensure a clean state.

## Report output

After any test run, `reports/` contains:

| File | Contents |
|---|---|
| `smoke-report.html` | HTML report — service health smoke |
| `smoke.json` | Compact JSON summary |
| `catalog-gate-report.html` | HTML report — catalog read gate |
| `catalog-gate.json` | Compact JSON summary |
| `order-journey-report.html` | HTML report — order create-read journey |
| `order-journey.json` | Compact JSON summary |
| `state/test-context.json` | Machine-readable journey metadata |
| `logs/*.log` | Docker service logs (test-suite only) |

## Troubleshooting

- **Build fails** — Ensure `src/tests/*.ts` and `tsconfig.json` are present. The k6 builder stage runs `npm run build` internally.
- **Services don't start** — Run `docker compose ps` to see health status. Postgres must become healthy before orders-api starts; orders-api and catalog-api must become healthy before gateway-api starts.
- **reports/ is empty** — Check that the `reports/` directory exists and is writable. The container mounts `./reports:/reports`.
- **Orphan container warning** — Run `./bin/clean` or `docker compose down --remove-orphans`.
