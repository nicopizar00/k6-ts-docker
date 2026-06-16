---
name: punch-performance-k6
description: Owns k6 test conventions — HTTP and Browser test shape, thresholds, handleSummary contract, the shared report builder, evidence file naming, and performance pass/fail semantics.
applies-to: src/tests/**, docker/k6.Dockerfile
---

# Skill: punch-performance-k6

## Responsibility

This skill is the authority on **how performance is validated**.

It owns:

- The shape of a k6 TypeScript test (default function, options, thresholds).
- The `handleSummary` contract (HTML + JSON + optional state file).
- The shared HTML builder in `src/tests/support/report.ts`.
- Threshold semantics: what counts as PASS vs FAIL for smoke, gate, and
  journey patterns.
- The k6 Browser deferral and the placeholder file at
  `src/tests/browser-smoke.ts.example`.
- The pin of `grafana/k6` in `docker/k6.Dockerfile`.

It does **not** own:

- How the test is launched (see `punch-orchestration`).
- Docker Compose service wiring (see `docker-compose.yml`).
- Whether AI assets are well-formed (see `punch-ai-governance-audit`).

## Behavioral rules

1. **One bundled file per test.** esbuild output is the contract; do not
   load Node modules at k6 runtime.
2. **Configurable base URL.** `__ENV.TARGET_BASE_URL` is the standard knob.
   In-network defaults must work without any env vars.
3. **Thresholds for gates and journeys.** Smoke tests are exempt; everything
   else declares `http_req_failed`, `http_req_duration` p95, and `checks`.
4. **handleSummary is mandatory.** Each test writes a self-contained HTML
   report + a compact JSON summary under `/reports/`.
5. **Deterministic data.** Tests use fixed IDs (`prod-001`, …). No PII,
   no real customer data, no production URLs.
6. **Browser is deferred.** Do not enable k6 Browser in built tests without
   a Shape plan that accepts the cost.

## When this skill activates

- Authoring a new test under `src/tests/`.
- Changing thresholds in an existing test.
- Modifying `src/tests/support/report.ts`.
- Bumping the `grafana/k6` pin.
- Considering whether to revive the Browser placeholder.

## Why this is a separate skill

Performance semantics (what "fast enough" means, what thresholds gate a
release) are a different decision domain from CLI ergonomics or container
plumbing. Splitting this skill keeps each domain reviewable on its own.
