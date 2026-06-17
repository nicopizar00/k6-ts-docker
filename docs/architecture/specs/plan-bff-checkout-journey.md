# Plan: BFF Checkout Journey

## Summary
- Implement a runnable `bff-checkout-journey` test: source → bundle → image → run → reports.
- Order: K-02 (bundle) → K-01 (test file already added) → O-01 (orchestrator wiring; already implemented).
- Human approval required before Build.

## Goal
Add runnable k6 journey test `bff-checkout-journey` so `./bin/punch run bff-checkout-journey` executes the bundled script and produces the expected reports.

## Tasks

### K-02: Ensure bundling includes the new test
- Task ID: K-02
- Goal: Make esbuild include `src/tests/bff-checkout-journey.ts` so the Docker build emits `/scripts/bff-checkout-journey.js`.
- Allowed edit paths: `package.json`, `tsconfig.json`
- Read-only context paths: `docker/k6.Dockerfile`, `docker-compose.yml`, `src/services/**`
- Forbidden paths: `src/punch/**`, `docker/**`, `src/tests/**` (beyond the already-added test file)
- Expected diff size: ~5 lines
- Validation commands:
  - `./bin/punch doctor`
  - `./bin/punch run bff-checkout-journey`
- Rollback notes: revert `package.json`/build changes
- Human checkpoint: approval required before Build
- Build prompt: `punch-build-k6-http`

### K-01: k6 test file (implemented)
- Task ID: K-01
- Goal: Provide `src/tests/bff-checkout-journey.ts` implementing the journey and report outputs.
- Allowed edit paths: `src/tests/*.ts`, `src/tests/support/**`
- Read-only context paths: `docker-compose.yml`, `docker/k6.Dockerfile`, `src/services/**`
- Forbidden paths: `src/punch/**`, `docker/**`
- Expected diff size: ~120 lines
- Validation commands: `./bin/punch run bff-checkout-journey`
- Rollback: remove `src/tests/bff-checkout-journey.ts`
- Human checkpoint: required
- Build prompt: `punch-build-k6-http`
- Status: implemented (file present)

### O-01: Orchestrator wiring (implemented)
- Task ID: O-01
- Goal: Add mapping so the CLI accepts `bff-checkout-journey` and runs `/scripts/bff-checkout-journey.js`.
- Allowed edit paths: `src/punch/**/*.py`
- Read-only context paths: `docker-compose.yml`, `src/tests/**`, `docker/k6.Dockerfile`
- Forbidden paths: `docker/**`, `src/services/**`
- Expected diff size: ~2 lines
- Validation commands: `./bin/punch run bff-checkout-journey`
- Rollback: revert `src/punch/__main__.py`
- Human checkpoint: required
- Build prompt: `punch-build-orchestrator`
- Status: implemented

## Order of execution
1. K-02 (update build to bundle new test)
2. K-01 (verify test is bundled and runs)
3. O-01 (already applied; final verify)
4. Verify via `./bin/punch doctor && ./bin/punch run bff-checkout-journey`

## Cross-cutting risks
- esbuild invocation may enumerate entry points explicitly; it must include the new file (K-02).
- k6 container may not reach `http://localhost:3001` from inside Docker; Verify must confirm reachable `TARGET_BASE_URL` or document using `host.docker.internal`.
- CI may rely on explicit build entries; keep change minimal and document in PR.

## Validation
- Primary: `./bin/punch run bff-checkout-journey` completes and `reports/state/punch-run.json` shows `passed: true`.
- Artifacts from `handleSummary`:
  - `/reports/bff-checkout-journey-report.html`
  - `/reports/bff-checkout-journey.json`
  - `/reports/state/test-context.json`

## Rollback plan
- Revert `package.json` and `src/punch/__main__.py` changes and remove `src/tests/bff-checkout-journey.ts` if Verify fails.

---

Human approval required to proceed with Task K-02 (update build script).