---
applyTo: "src/tests/browser-*.ts,src/tests/browser-*.ts.example"
description: Behavior rules for k6 Browser tests (currently deferred).
---

# k6 Browser Tests — Path Instructions

Scope: any browser-flavored test file under `src/tests/`.

## Current status: **deferred placeholder**

The reference k6 image (`grafana/k6:0.55.0`) does not ship Chromium and the
project explicitly defers Browser execution to keep image size, build time,
and CI cost predictable. The MVP placeholder is
`src/tests/browser-smoke.ts.example` — it documents the intended shape but
**is not built** and **must not be added to the esbuild entry list** until a
Shape plan accepts the cost.

## Rules

- **Do not enable browser execution silently.** Switching to `grafana/k6:0.55.0-with-browser`,
  installing Chromium, or adding a new compose service requires a Shape plan
  with an explicit cost/benefit note.
- **No `import { browser } from "k6/browser"` in built tests.** The `.example`
  placeholder may contain it for documentation; production tests under
  `src/tests/` (that esbuild bundles) must remain HTTP-only.
- **If browser tests are enabled:** they get their own bundle, their own
  compose service, and their own thresholds (`browser_web_vital_*`). Reuse the
  same `handleSummary` evidence contract as HTTP tests.

## Why deferred

- The k6 browser runtime requires a Chromium binary in the image.
- Browser metrics (FCP, LCP, CLS) need separate threshold semantics.
- The current four-service reference app has no rendered UI to test.

Reopen this decision only when there is a real, named UI to validate.
