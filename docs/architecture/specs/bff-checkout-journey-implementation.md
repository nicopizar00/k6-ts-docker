# BFF Checkout Journey Implementation

## Implemented features

- Added `src/tests/bff-checkout-journey.ts` as a new HTTP journey test targeting an external BFF via `TARGET_BASE_URL`.
- Updated `package.json` build script to bundle `src/tests/bff-checkout-journey.ts` into `dist/bff-checkout-journey.js`.
- Wired `src/punch/__main__.py` so `./bin/punch run bff-checkout-journey` resolves to `/scripts/bff-checkout-journey.js`.

## Findings

- The repo’s smoke test passes, confirming the Docker-based stack and orchestrator are healthy.
- The k6 image build now includes the new bundled script.
- Current `./bin/punch run bff-checkout-journey` fails because the default `TARGET_BASE_URL=http://localhost:3001` is not reachable from inside the k6 container.
- The new test must be executed against a Docker-accessible external host, not the container-local `localhost` address.

## Expected artifacts

- `/reports/bff-checkout-journey-report.html`
- `/reports/bff-checkout-journey.json`
- `/reports/state/test-context.json`
- `/reports/state/punch-run.json`

## Execution note

Use a Docker-accessible target URL when running the test.

```bash
TARGET_BASE_URL=http://host.docker.internal:3001 ./bin/punch run bff-checkout-journey
```

Or substitute the appropriate host for your Docker network.

## Related docs

- `docs/architecture/specs/bff-checkout-journey-test.md`
- `docs/architecture/specs/plan-bff-checkout-journey.md`
- `docs/architecture/specs/plan-bff-checkout-journey-test.md`
