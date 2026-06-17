# BFF Checkout Journey CLI Wiring Spec

## Goal

Add `bff-checkout-journey` as a valid Punch CLI test target by wiring it into `src/punch/__main__.py` so `./bin/punch run bff-checkout-journey` executes the existing bundled k6 script.

## Non-goals

- Do not modify `docker-compose.yml`, `docker/**`, or any repo service implementation.
- Do not change the k6 test contents in `src/tests/bff-checkout-journey.ts`.
- Do not add host-side execution paths or require host-installed `k6`/`npm`.
- Do not change reporting helpers or artifact schema.

## Functional requirements

- Add a new entry in the `TESTS` mapping inside `src/punch/__main__.py`:
  - `"bff-checkout-journey": "/scripts/bff-checkout-journey.js"`
- Allow `./bin/punch run bff-checkout-journey` as a valid `test` argument.
- Preserve existing `./bin/punch run <test>` semantics:
  - build Docker images via `docker compose build`
  - run `docker compose run --rm k6 run <script>`
  - write `reports/state/punch-run.json`
- Ensure the new test name is included in `all` execution automatically via the existing `TESTS` dict iteration.

## Technical constraints

- Only edit the Python orchestrator layer: `src/punch/__main__.py`.
- Keep the orchestrator stdlib-only and shell out to Docker Compose as before.
- Do not modify `docker-compose.yml`, `docker/k6.Dockerfile`, or any Docker service definitions.
- The new mapping must reference the existing Docker build artifact path `/scripts/bff-checkout-journey.js`.

## Affected layers

- Python orchestrator: `src/punch/__main__.py`

## Artifact / reporting implications

- No schema changes to `reports/state/punch-run.json`.
- New run results may add a `bff-checkout-journey` entry to the `tests` array in `reports/state/punch-run.json`.
- No changes to HTML/JSON report contract in `src/tests/support/report.ts`.

## Acceptance criteria

- `src/punch/__main__.py` contains `bff-checkout-journey` in `TESTS` mapped to `/scripts/bff-checkout-journey.js`.
- `./bin/punch run bff-checkout-journey` is accepted by the CLI parser.
- `./bin/punch run bff-checkout-journey` proceeds through Docker Compose build and k6 execution.
- `reports/state/punch-run.json` is produced for the run and contains the new test result.
- No compose or service code changes were required.
