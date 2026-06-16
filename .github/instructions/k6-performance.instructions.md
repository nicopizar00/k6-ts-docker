---
applyTo: "src/tests/**/*.ts,src/tests/**/*.ts.example"
description: Behavior rules for k6 tests (HTTP today, Browser deferred).
---

# k6 Performance Tests — Path Instructions

Scope: all `.ts` files under `src/tests/`. HTTP and Browser tests share this
file but live in separate sub-sections.

## Shared rules (apply to all k6 tests)

- **k6 does not own orchestration.** A test must not start containers,
  poll compose state, shell out, or write outside `/reports/`. Those belong
  to `src/punch/` and `docker-compose.yml`.
- **TypeScript, ESM, single-file bundles.** esbuild produces one ES module
  per test. No dynamic `import()`, no Node-only APIs at k6 runtime.
- **Configurable base URL.** Every test reads its target from
  `__ENV.TARGET_BASE_URL`. The in-network default (e.g. `http://gateway-api:3000`)
  must work without any env vars. Never hardcode external URLs.
- **Thresholds are the gate.** Each gate or journey test declares, at
  minimum:
  - `http_req_failed` rate threshold
  - `http_req_duration` p95 threshold (or the Browser equivalent below)
  - `checks` pass-rate threshold
  Smoke tests may skip thresholds but must include `check()` calls.
  Keep thresholds visible at the top of the file, not buried.
- **handleSummary writes evidence.** Every test exports `handleSummary` and
  writes a self-contained HTML report (via `support/report.ts`) and a
  compact JSON summary under `/reports/`. Journey tests also write
  `reports/state/test-context.json`.
- **No secrets, no real customer data.** Use deterministic fixture IDs
  (`prod-001`, …). Never embed tokens, real URLs, or PII.
- **Shared helpers live in `src/tests/support/`.** Do not duplicate the
  HTML builder. If a helper is needed in two tests, wait for a third real
  caller before extracting; otherwise inline.
- **Readable scenarios over clever abstractions.** Three similar `default
  function` bodies are better than a metaprogrammed factory. The test
  reader is often debugging a perf regression at 2am.
- **Shared data sources are explicit.** Use `SharedArray` with a named
  loader function. Never read from `__ENV` mid-iteration; pre-resolve in
  `setup()`.

## HTTP test rules

Applies to `src/tests/*.ts` that are **not** `browser-*.ts`.

- File naming: `<feature>-<kind>.ts` where kind is `smoke`, `gate`, or
  `journey`. Bundle name in `dist/` mirrors the source name.
- Use the `http` module from k6 (`import http from 'k6/http'`).
- Build prompt: [`punch-build-k6-http`](../prompts/punch-build-k6-http.prompt.md).

## Browser test rules

Applies to `src/tests/browser-*.ts` and `src/tests/browser-*.ts.example`.

- **Currently deferred.** The reference k6 image (`grafana/k6:0.55.0`) does
  not ship Chromium. The MVP placeholder is
  `src/tests/browser-smoke.ts.example`; it documents the intended shape but
  is **not built** and must not be added to the esbuild entry list until a
  Plan accepts the cost.
- **No `import { browser } from 'k6/browser'` in built tests.** The
  `.example` placeholder may contain it for documentation; production tests
  bundled by esbuild must remain HTTP-only.
- When enabled (post-Plan), Browser tests:
  - Get their own bundle and their own compose service.
  - Use browser-specific thresholds (`browser_web_vital_lcp`,
    `browser_web_vital_fid`, `browser_web_vital_cls`).
  - Reuse the same `handleSummary` evidence contract as HTTP tests.
- Build prompt: [`punch-build-k6-browser`](../prompts/punch-build-k6-browser.prompt.md).

## When this file activates

- Authoring a new test under `src/tests/`.
- Changing thresholds.
- Modifying `src/tests/support/report.ts`.
- Bumping the `grafana/k6` pin in `docker/k6.Dockerfile`.
- Considering whether to revive the Browser placeholder.
