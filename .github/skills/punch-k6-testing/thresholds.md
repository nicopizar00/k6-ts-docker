# Threshold Cheatsheet

Punch tests come in three categories. Each has a different threshold
profile. Keep thresholds at the top of the test file, not buried in
helpers.

## Smoke

Smoke tests are the fastest signal that the stack is alive. They run a
handful of requests and check basic shape.

- **Thresholds**: optional. May skip declared thresholds entirely.
- **Required**: at least one `check()` per request — the run-time signal
  is the assertion pass rate.
- **Duration**: a few seconds. No `vus > 1` typically.
- **Use when**: a CI smoke gate, a `./bin/punch run smoke` quick check, or
  the first signal post-deploy.

## Gate (performance gate)

Gate tests enforce SLOs on a hot endpoint or a small set of endpoints. A
failed gate blocks a release.

- **Required thresholds**:
  - `http_req_failed: ['rate<0.01']` — < 1% errors.
  - `http_req_duration: ['p(95)<500']` — 95th percentile under 500ms.
    Tune the budget per endpoint, document the rationale next to the
    threshold.
  - `checks: ['rate>0.99']` — > 99% check pass.
- **Optional**: per-tag duration thresholds for sub-flows.
- **Duration**: 30s–2min sustained load; enough to populate p95.
- **Use when**: validating a hot path; merging a perf-sensitive change.

## Journey

Journey tests exercise a sequence: create → read → validate. They mix
correctness and performance.

- **Required thresholds**:
  - `http_req_failed: ['rate<0.01']`.
  - `http_req_duration: ['p(95)<800']` — slightly looser than gates;
    a journey is end-to-end and contains slower writes.
  - `checks: ['rate>0.99']` — assertions matter as much as latency.
- **Required artifact**: `reports/state/test-context.json` — captures the
  IDs created during the run for downstream assertions.
- **Duration**: enough iterations to make the create→read→validate flow
  meaningful; typically 1–2 minutes.

## Browser (deferred)

When enabled, Browser thresholds replace HTTP thresholds because the
runtime emits different metrics.

- `browser_web_vital_lcp: ['p(95)<2500']` — Largest Contentful Paint, ms.
- `browser_web_vital_cls: ['p(95)<0.1']` — Cumulative Layout Shift,
  unitless.
- `browser_web_vital_fid: ['p(95)<100']` — First Input Delay, ms.
- `checks: ['rate>0.99']`.

The Browser image is **deferred** today. Enabling it requires a Plan.

## What thresholds should NOT do

- Encode magic numbers without a comment. If `p(95)<500` is the SLO,
  the source of that number lives in a comment or in a linked doc.
- Hide failure modes. Always include `http_req_failed`; a run with zero
  failed requests but slow ones still passes the SLO check.
- Be tightened "to look better in CI". Threshold tuning is a Plan-level
  decision, not a Build hack.
