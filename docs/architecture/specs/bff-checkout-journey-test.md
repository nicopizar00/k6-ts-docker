# BFF Checkout Journey k6 Test

## Goal

Add a new k6 HTTP test that exercises the external containerized BFF at `http://localhost:3001` through a realistic checkout flow, using the existing repository’s Docker-first k6 test framework.

## Non-goals

- Not adding or modifying service implementation code in this repo.
- Not changing `docker-compose.yml` or adding new Compose services.
- Not introducing host-only execution paths or requiring host-installed `k6`/`npm`.
- Not building a full production load test; this is a focused functional journey test.
- Not adding auth, telemetry, or unrelated API coverage beyond the checkout flow.

## Functional requirements

- A new TypeScript test file under `src/tests/`, e.g. `src/tests/bff-checkout-journey.ts`.
- The test targets an externally hosted BFF via environment configuration, not a repo-local mock service.
- The journey covers:
  - `GET /catalog/products`
  - `POST /cart/items`
  - `GET /cart`
  - `POST /checkout` and capture returned `orderId`
  - `GET /orders/{orderId}`
  - `POST /orders/{orderId}/manage` with a management action like `mark_prepared`
- The test produces the same artifact contract as existing tests:
  - HTML report under `/reports/`
  - JSON summary under `/reports/`
- The test is implemented using existing k6 patterns from `src/tests/*` and `src/tests/support/report.ts`.

## Technical constraints

- Must remain Docker-first: the test should be runnable through the repo’s k6 image and orchestrator, not via host-side k6 or direct npm tooling.
- Must use only the existing repo test layer; no new Python orchestration or Compose runtime logic is required.
- Must support an external target host via env var, e.g. `TARGET_BASE_URL`, because the BFF lives outside this repo’s service domain.
- Must avoid renaming or depending on repo-local Docker service names.
- Must be compatible with the repository’s current reporting contract and not require schema changes in existing reports unless explicitly reviewed later.

## Affected layers

- `src/tests/` — k6 HTTP test layer
- `reports/` — reporting/artifact layer for new HTML/JSON outputs
- external runtime — the target BFF service is external to repo ownership and is consumed via env-configured URL

## Artifact / log / reporting implications

- New artifacts:
  - `/reports/bff-checkout-journey-report.html`
  - `/reports/bff-checkout-journey.json`
- Verification must still produce `reports/state/punch-run.json` as the contract artifact.
- Terminal noise should remain low and follow existing `handleSummary` patterns.
- No change to existing artifact paths unless a new test name is introduced intentionally.

## Acceptance criteria

- `src/tests/bff-checkout-journey.ts` exists and implements the checkout journey end-to-end.
- The test uses `TARGET_BASE_URL` (or equivalent env var) to target the external BFF.
- Running the test through the repo’s standard path succeeds.
- The run exits cleanly and writes:
  - `/reports/bff-checkout-journey-report.html`
  - `/reports/bff-checkout-journey.json`
  - `reports/state/punch-run.json`
- k6 checks assert expected HTTP status codes and JSON response shapes for each step in the journey.
- No changes are made to repo service code or `docker-compose.yml`.

## Notes

- Existing tests and report patterns were inspected in `src/tests/order-journey.ts`, `src/tests/catalog-gate.ts`, `src/tests/smoke.ts`, and `src/tests/support/report.ts`.
- The external BFF is treated as a runtime dependency reachable from the Dockerized k6 container; connection details must be configurable and validated during Verify.
