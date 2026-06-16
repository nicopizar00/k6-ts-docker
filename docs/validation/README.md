# Validation Evidence

Validation evidence lives in `reports/` (gitignored). This directory exists
as a **landing page** for that evidence — it explains what a Verify run
produces and where to look.

For the workflow that generates the evidence, see
[`../workflows/validation.md`](../workflows/validation.md).

## What lands where

```
reports/
├── smoke-report.html              # human-readable smoke result
├── smoke.json                     # compact summary
├── catalog-gate-report.html       # human-readable gate result
├── catalog-gate.json              # compact summary
├── order-journey-report.html      # human-readable journey result
├── order-journey.json             # compact summary
├── state/
│   ├── punch-run.json             # canonical Punch evidence
│   └── test-context.json          # journey metadata (POST → GET)
└── logs/
    ├── k6-{smoke,gate,journey}.log   # streamed k6 output (Punch only)
    ├── gateway-api.log               # service log (--collect-logs only)
    ├── catalog-api.log
    ├── orders-api.log
    └── postgres.log
```

## How to read the canonical artifact

```bash
cat reports/state/punch-run.json
```

The two fields that matter:

- `passed` — boolean, the binary gate signal.
- `results[].exitCode` — non-zero identifies the failing test.

Everything else is metadata.

## What Verify must check

1. `reports/state/punch-run.json` exists.
2. `passed: true` (or `false` if Verify is exercising a failure scenario).
3. The test-specific HTML and JSON files exist for every test in `results`.

If any of these is missing, the orchestrator regressed — fix it in
`src/punch/__main__.py` (the `_write_evidence` and `cmd_run` paths).

## Why a separate file from `reports/`

`reports/` is gitignored — its contents change on every run and must not
land in the repo. This page is committed, so the evidence contract is
discoverable even when `reports/` is empty.
