---
name: punch-data-harvest
description: Owns artifacts, logs, summaries, and reporting — stable paths, low-noise console, complete logs to files, and the JSON/CSV contract with downstream consumers.
applies-to: src/tests/support/**, src/punch/**, reports/**, docs/validation/**
---

# Skill: punch-data-harvest

## Responsibility

This skill is the authority on **what Punch writes and where**.

It owns:

- The stable artifact paths (`reports/state/punch-run.json`,
  `reports/state/test-context.json`, `reports/<test>.html`,
  `reports/<test>.json`, `reports/logs/<service>.log`).
- The low-noise console / complete file logs discipline.
- The JSON/CSV summary contract — compact, stable schema, no per-iteration
  dumps.
- Harvesting from Docker logs (when `--collect-logs` is set) without
  shaping them.
- The HTML report builder contract in `src/tests/support/report.ts`.
- The artifact contract template (see
  [`artifact-contract.md`](artifact-contract.md)) any new artifact must
  fill in.

It does **not** own:

- How the orchestrator runs the tests (see `punch-python-orchestration`).
- Threshold semantics (see `punch-k6-testing`).
- Compose service wiring (see `punch-compose-runtime`).

## When to use

- Adding a new artifact (JSON, CSV, HTML, log).
- Changing the schema or path of an existing artifact.
- Adjusting the terminal-noise / file-noise split.
- Modifying `src/tests/support/report.ts`.
- Touching the reporting/state-writing parts of `src/punch/`.

**Not for:** running the suite (`punch-python-orchestration`), compose/service wiring (`punch-compose-runtime`), or k6 test logic (`punch-k6-testing`).

## Inputs expected

- The approved Plan task with allowed/read-only/forbidden paths.
- The artifact's purpose and downstream consumers (a human; CI; a
  dashboard; a future automation).

## Procedure

1. Read the existing
   [`artifact-contract.md`](artifact-contract.md) template.
2. Fill in a contract for every artifact the change adds or modifies.
3. Update [`docs/ai/maintenance-matrix.md`](../../../docs/ai/maintenance-matrix.md)
   in the same change if a path or schema is moving.
4. Implement the producer code in the minimum allowed paths
   (`src/tests/support/**`, named reporting functions in `src/punch/**`).
5. Keep the terminal quiet by default. New verbose output goes to a file,
   not stdout, unless the Plan explicitly asks for terminal exposure.
6. Re-run `./bin/punch run smoke` (or the relevant test) and confirm the
   new/changed artifact is written.

## Output format

A focused diff under `src/tests/support/` and/or `src/punch/`. Report:

- Every file changed.
- The artifact contract entries added or modified (one block per
  artifact, following the template).
- Confirmation that downstream consumers (CI `validate-artifacts` job,
  this skill, etc.) still resolve.

## Safety / boundary rules

- **Paths are contracts.** Renames cascade. No path change without an
  explicit Plan and a maintenance-matrix update.
- **Terminal stays quiet.** Full logs go to `reports/logs/`. The terminal
  shows progress + pass/fail.
- **JSON summaries are compact.** No raw per-iteration dumps. Aggregates
  only.
- **HTML is self-contained.** No external CSS / fonts / fetches.
- **No secrets in artifacts.** Sanitize env vars and tokens out of every
  written file.
- **State files are canonical.** `passed: true|false` in
  `reports/state/punch-run.json` is the verification gate.

## Observability discipline (absorbed from the retired `punch-observability-and-instrumentation`)

Punch's reference services are a didactic demo, not a production system with
on-call — so OpenTelemetry tracing, a separate metrics backend, and symptom-based
alerting are **out of scope** and stay deferred until a real recurring service
use case is approved. The transferable discipline that *is* in scope:

- **Instrument with a question in mind.** Before adding a log line, write 2–4
  on-call-style questions it answers (e.g. "what fraction of create-order
  requests fail, and why?"). Telemetry without a question is noise.
- **Structured logs, not prose.** One JSON object per line, stable event name +
  machine fields (`{ event: 'order_create_failed', orderId, cause, ms }`), not
  string interpolation — so it survives into `reports/logs/` and stays
  greppable next to the k6 evidence. Levels: `error` (invariant broken) ·
  `warn` (degraded) · `info` (business event) · `debug` (off by default).
- **Carry a correlation id** from the gateway through catalog/orders so one
  request can be reconstructed from interleaved logs — an orphan log line
  (no correlation id) is a red flag.
- **RED, read from the k6 run.** Rate/Errors/Duration come from the k6 summary
  (`http_req_duration` p95/p99, `errorRate`, `totalRequests`), never a separate
  metrics backend. **Percentiles, never averages.**
- **Never log secrets/tokens/URLs/PII** into any artifact (the hard rule
  above) — allowlist fields, don't dump whole request bodies.
- **Verify the telemetry itself before "done."** Force a failure (e.g. a bad
  order payload), find the structured `*_failed` event in `reports/logs/` by
  correlation id, confirm fields are real JSON (not `[object Object]`); run
  `./bin/punch run journey --collect-logs` and confirm logs line up with
  `reports/state/punch-run.json`.
- **The run evidence is the telemetry.** `reports/state/punch-run.json` answers
  "did it pass?"; `reports/logs/<service>.log` answers "why not?" — keep the split.

**Red flags:** a service path with retries/queries/external hops and zero new
log events; log lines built by string interpolation; no correlation id;
latency reported as an average; secrets/full bodies/PII in any log line.

For diagnosing a live failure, use [`punch-debugging-and-error-recovery`](../punch-debugging-and-error-recovery/SKILL.md).

## Why this is a separate skill

Reporting is the contract surface between Punch and everyone downstream
(humans, CI validation, dashboards, future automation). Drift here is
silent until something breaks downstream. A dedicated skill makes the
cost of artifact changes visible at Plan time.
