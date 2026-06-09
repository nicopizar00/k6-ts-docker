---
applyTo: "src/tests/**/*.ts"
description: Behavior rules for k6 HTTP TypeScript tests.
---

# k6 HTTP Tests — Path Instructions

Scope: all `.ts` files under `src/tests/` **except** browser tests
(see `k6-browser.instructions.md`).

## Rules

- **TypeScript, ESM, single-file bundles.** esbuild produces one ES module per
  test. Do not introduce dynamic `import()` or Node-only APIs.
- **Configurable base URL.** Every test reads its target from `__ENV.TARGET_BASE_URL`
  (with an in-network default like `http://gateway-api:3000`). Never hardcode
  hostnames or ports outside Docker Compose's internal network.
- **Thresholds are the gate.** Each gate or journey test declares at least:
  - `http_req_failed` rate threshold
  - `http_req_duration` p95 threshold
  - `checks` pass-rate threshold
  Smoke tests may skip thresholds but must include `check()` calls.
- **handleSummary writes evidence.** Every test exports `handleSummary` and
  writes both an HTML report (via `support/report.ts`) and a compact JSON
  summary under `/reports/`. Journey tests also write `state/test-context.json`.
- **No secrets, no real customer data.** Use deterministic fixture IDs
  (`prod-001`, `prod-002`, …). Never embed tokens, real URLs, or PII.
- **Shared helpers live in `src/tests/support/`.** Do not duplicate the HTML
  builder. If a helper is needed in two tests, wait for a third real caller
  before extracting; otherwise inline.

## Naming

`<feature>-<kind>.ts` where kind is `smoke`, `gate`, or `journey`.
Bundle name in `dist/` mirrors the source name.
