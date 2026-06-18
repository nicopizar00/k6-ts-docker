# Plan: BFF Checkout Journey k6 Test

> **Historical.** This plan predates the consolidation to a single `punch-build`
> prompt + `punch-builder` dispatcher; the per-task Build-prompt reference below
> was updated to the current model (see `docs/ai/prompt-registry.md`).

## Goal

Implement the approved spec by adding a new HTTP k6 test that exercises an external containerized BFF checkout journey via `TARGET_BASE_URL`, using the repository’s existing Docker-first test framework.

## Tasks

### K-01
- Goal: Add a new k6 HTTP journey test under `src/tests/` that covers catalog browse, cart add, checkout, order retrieval, and order management against an externally hosted BFF.
- Allowed edit paths:
  - `src/tests/*.ts`
  - `src/tests/support/**`
- Read-only context paths:
  - `docker-compose.yml`
  - `docker/k6.Dockerfile`
  - `src/services/**`
- Forbidden paths:
  - `src/punch/**`
  - `docker/**`
  - `docker-compose.yml` (compose changes are a different domain)
  - `src/tests/browser-*.ts*`
- Expected diff size: ~120 lines
- Validation commands:
  - `./bin/punch run journey`
  - optionally `./bin/punch run bff-checkout-journey` once the new test is wired in
- Rollback notes:
  - Remove the new test file or revert the diff if the run fails or the external API contract changes.
- Human checkpoint: human approval required before Build.
- Build prompt: `punch-build` (via `punch-performance-test-engineer`)

## Order of execution

1. K-01: implement the HTTP test alone.

This is a single-layer task: no orchestrator or compose changes are required by the approved spec.

## Cross-cutting risks

- The k6 container may not be able to reach `http://localhost:3001` from inside Docker. If that occurs, the task must be revised to document the proper container host access method (`host.docker.internal` or equivalent) or to update the test wiring.
- The external BFF API contract may differ from the curl examples; the test should use defensive checks and clear error reporting.
- If the external runtime requires auth or a different base URL format, the plan may need a second task to document environment setup or add a small orchestrator helper.

## Rollback plan

If Verify fails, revert the new test file and any associated report artifact references. No Compose or orchestration rollback is needed because only a k6 test file is added.
