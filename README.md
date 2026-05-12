# k6-ts-docker

A clean proof-of-concept for running k6 performance tests written in TypeScript, packaged in Docker, and executed in CI.

## Goal

Demonstrate a maintainable, end-to-end performance testing pipeline that is easy to read, extend, and reason about.

## Quick start

```bash
npm install
npm run build          # TypeScript → bundled JS
npm run docker:build   # Build k6 Docker image
npm run test:smoke     # Run smoke test via Docker
```

Results appear in `reports/` (after k6 outputs them).

## Execution chain

Every change preserves this linear pipeline:

```
TypeScript source  →  esbuild  →  Docker image  →  k6 run  →  reports
```

If a change doesn't fit this flow, discuss it first.

## What's where

| Path | Purpose |
|------|---------|
| `src/tests/` | k6 test scenarios (TypeScript) |
| `dist/` | Bundled, k6-ready JavaScript |
| `docker/Dockerfile` | Builds the runtime image |
| `reports/` | Test output (JSON, summaries) |
| `docs/` | Architecture, how-tos, AI context |

## Next steps

- Add more test scenarios in `src/tests/`
- Set up GitHub Actions workflow to run on push/PR
- Configure output reports (JSON export, live summaries)

See `CLAUDE.md` for contribution rules.
