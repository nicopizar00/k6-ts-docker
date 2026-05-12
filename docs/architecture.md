# Architecture

## Execution chain

TypeScript source → bundle (single JS file) → Docker image → k6 execution → reports

## Folder map

| Path | Role |
|---|---|
| `src/tests/` | k6 test scenarios authored in TypeScript |
| `dist/` | Bundler output — single JS file consumed by k6 |
| `docker/Dockerfile` | Builds the k6 runner image from `grafana/k6` |
| `reports/` | JSON and summary output from k6 runs |
| `docs/` | AI-friendly documentation and decision log |

## Decision log

- **Bundler TBD** — k6 cannot consume Node modules directly; a bundler (esbuild or similar) will produce a single ES module in `dist/`.
- **No GitHub Actions yet** — CI workflow will be added as a separate step.
