# BFF Checkout Journey k6 Test

## Goal

Add a new HTTP k6 journey test under `src/tests/bff-checkout-journey.ts` that exercises an external BFF checkout flow via `TARGET_BASE_URL`, using the repository’s existing Docker-first k6 test framework.

## Non-goals

- No changes to repo service implementation.
- No changes to `docker-compose.yml` or any Docker Compose services.
- No host-side `k6`, `npm`, or `pip` execution paths.
- No auth, telemetry, or unrelated API coverage beyond the checkout flow.

## Functional requirements

- New TypeScript test file: `src/tests/bff-checkout-journey.ts`.
- Target an external BFF via environment configuration (`TARGET_BASE_URL`).
- Journey steps:
  - `GET /catalog/products`
  - `POST /cart/items`
  - `GET /cart`
  - `POST /checkout` and capture returned `orderId`
  - `GET /orders/{orderId}`
  - `POST /orders/{orderId}/manage` with a management action such as `mark_prepared`
- Use existing k6 patterns from `src/tests/*` and `src/tests/support/report.ts`.
- Produce artifacts:
  - `/reports/bff-checkout-journey-report.html`
  - `/reports/bff-checkout-journey.json`
  - `/reports/state/test-context.json`

## Technical constraints

- Must remain Docker-first and runnable through the repo’s k6 image.
- Must use `TARGET_BASE_URL` for the external runtime; do not depend on repo-local service hostnames.
- No changes to `src/punch/**`, `docker/**`, or `docker-compose.yml` in this task.
- The new test should follow existing threshold and reporting conventions.

## Artifact / reporting contract

- HTML report via `buildHtml`.
- Compact JSON summary via `buildSummaryJson`.
- Persisted test context in `reports/state/test-context.json`.
- No schema changes to shared report helpers.

## Acceptance criteria

- `src/tests/bff-checkout-journey.ts` exists and implements the checkout journey.
- The test uses `TARGET_BASE_URL` as the external target.
- The new test writes:
  - `/reports/bff-checkout-journey-report.html`
  - `/reports/bff-checkout-journey.json`
  - `/reports/state/test-context.json`
- k6 checks assert HTTP status codes and JSON response shapes for each step.
- No repo service or Compose changes are required.

## Task breakdown

### Task K-01: Add BFF checkout journey k6 test

- Goal: implement the new journey test file and attach the existing report contract.
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
  - `docker-compose.yml`
  - `src/tests/browser-*.ts*`
- Validation:
  - `./bin/punch run journey` or once wired, `./bin/punch run bff-checkout-journey`
  - Confirm `reports/state/punch-run.json` records the run.
- Rollback:
  - Remove `src/tests/bff-checkout-journey.ts` and revert the diff if verification fails.
- Expected diff size: ~120 lines.
- Human checkpoint: approval required before Build.
- Build via: `punch-build` (via `punch-performance-test-engineer`).
