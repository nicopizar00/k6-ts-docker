---
name: punch-k6-performance
description: Owns k6 test conventions — HTTP vs Browser separation, thresholds, scenarios, shared data, handleSummary contract, evidence file naming, and performance pass/fail semantics.
applies-to: src/tests/**, docker/k6.Dockerfile
---

# Skill: punch-k6-performance

## Responsibility

This skill is the authority on **how performance is validated**.

It owns:

- The shape of a k6 TypeScript test (default function, options, thresholds,
  scenarios).
- HTTP vs Browser separation (see [`http-template.ts`](http-template.ts)
  and [`browser-template.ts`](browser-template.ts)).
- Threshold semantics: what counts as PASS vs FAIL for smoke, gate, and
  journey patterns (see [`thresholds.md`](thresholds.md)).
- The `handleSummary` contract (HTML + JSON + optional state file).
- The shared HTML builder in `src/tests/support/report.ts`.
- Shared data sources (`SharedArray` discipline; no mid-iteration `__ENV`).
- The k6 Browser deferral and the placeholder file at
  `src/tests/browser-smoke.ts.example`.
- The pin of `grafana/k6` in `docker/k6.Dockerfile`.
- The principle that **k6 does not own orchestration** — tests never start
  containers, poll state, shell out, or write outside `/reports/`.

It does **not** own:

- How the test is launched (see `punch-python-orchestration`).
- Docker Compose service wiring (see `punch-docker-compose`).
- The HTML/JSON report's storage contract (see `punch-data-harvest`).
- Whether AI assets are well-formed (see `punch-governance-review`).

## When to use

- Authoring a new test under `src/tests/`.
- Changing thresholds in an existing test.
- Modifying `src/tests/support/report.ts`.
- Bumping the `grafana/k6` pin.
- Considering whether to revive the Browser placeholder.

## Inputs expected

- The approved Plan task with allowed/read-only/forbidden paths.
- The test category (smoke / gate / journey / browser).

## Procedure

1. Confirm the test category — it picks the threshold profile (see
   [`thresholds.md`](thresholds.md)).
2. Start from one of the templates as a structural hint
   ([`http-template.ts`](http-template.ts) or
   [`browser-template.ts`](browser-template.ts)). The templates are
   intentionally minimal — real tests in `src/tests/` are stronger
   examples; do not overwrite their conventions.
3. Keep the thresholds at the top of the file. They are the gate; they
   should be visible without scrolling.
4. Use `SharedArray` for fixtures. No mid-iteration data loading.
5. Read the target from `__ENV.TARGET_BASE_URL` with an in-network default.
6. Implement `handleSummary` that writes:
   - `/reports/<test>.html` (via `support/report.ts`).
   - `/reports/<test>.json` (compact summary).
   - `/reports/state/test-context.json` (only for journey tests).
7. Do not import Node-only APIs or use dynamic `import()`.

## Output format

A focused diff under `src/tests/` (and possibly `src/tests/support/` if
the helper genuinely needs a third caller). Report:

- Every file changed.
- The thresholds declared.
- Confirmation that `handleSummary` writes the contracted artifacts.

## Safety / boundary rules

- **One bundled file per test.** esbuild output is the contract; do not
  load Node modules at k6 runtime.
- **Configurable base URL.** `__ENV.TARGET_BASE_URL` is the standard knob.
- **Thresholds for gates and journeys.** Smoke is exempt; everything else
  declares at least `http_req_failed`, `http_req_duration` p95, and
  `checks`.
- **Deterministic data.** Fixed IDs (`prod-001`, …). No PII; no real
  customer data; no production URLs.
- **Browser is deferred.** Do not enable k6 Browser in built tests without
  a Plan that accepts the image-size / build-time / CI-cost trade.

## Why this is a separate skill

Performance semantics (what "fast enough" means, what thresholds gate a
release) are a different decision domain from CLI ergonomics or container
plumbing. Splitting this skill keeps each domain reviewable on its own.
