---
name: punch-observability-and-instrumentation
description: Makes the reference services diagnosable from their telemetry. Use when adding a service, route, query, or external hop and you need evidence it works under k6 load. Adapts upstream agent-skills `punch-observability-and-instrumentation` to Punch's services + reports/** harvest; pairs with punch-data-harvest.
applies-to: lifecycle/Build — service instrumentation feeding reports/logs/** and the k6 evidence; not path-scoped
---

# Observability and Instrumentation (Punch)

Telemetry is written alongside the feature, like the k6 check is. In Punch the
durable signals are the **service logs** (`reports/logs/` via `--collect-logs`)
and the **k6 run evidence** (`reports/state/punch-run.json`, `reports/<test>.json`).
This skill instruments the services so a failing gate can be explained; reading
the harvested files is [`punch-data-harvest`](../punch-data-harvest/SKILL.md).

## Process

### 1. Define "working" before instrumenting

Write 2–4 questions an operator asks about the change, e.g. for `orders-api`:

```
1. What fraction of create-order requests succeed vs fail?
2. When one fails, why? (validation? Postgres error? timeout?)
3. Is the DB call slower than usual under load?
→ every log field / metric must answer one of these.
```

### 2. Structured logs, not prose

Each service log line = one JSON object with a stable event name + machine fields,
so it survives into `reports/logs/` and is greppable next to the k6 evidence.

```js
// BAD: logger.info(`order ${id} failed for ${userId}`)
// GOOD:
log({ event: 'order_create_failed', orderId: id, cause: err.code, ms: dur });
```

Levels used consistently: `error` (invariant broken) · `warn` (degraded but
handled) · `info` (business event: order placed) · `debug` (off by default).
Carry a request/correlation id from the gateway down through catalog/orders so one
request can be reconstructed from interleaved logs.

**Never log secrets, tokens, private URLs, or PII** (Critical Rule — telemetry is a
classic leak path). Allowlist fields; don't dump whole request bodies.

### 3. Metrics = RED, read from the k6 run

For each route/dependency think **R**ate · **E**rrors · **D**uration. In Punch you
read these from the k6 summary (`http_req_duration` p95/p99, `errorRate`,
`totalRequests`) rather than a separate metrics backend — k6 is the load-time
meter. Track **percentiles, never averages**.

### 4. Verify the telemetry itself

Instrumentation is code; it can be wrong. Before "done":

- Force a failure (e.g. bad order payload) → find the structured `*_failed` event
  in `reports/logs/` by correlation id; confirm fields are JSON, not `[object Object]`.
- Run `./bin/punch run journey --collect-logs` → logs + `reports/state/punch-run.json`
  line up with what the run did.

## Red flags

- A service path with retries/queries/external hops and zero new log events.
- Log lines built by string interpolation (unqueryable).
- No correlation id — each line is an orphan.
- Latency reported as an average.
- Secrets / full bodies / PII in any log line.

## Verification

- [ ] On-call questions written; each signal maps to one.
- [ ] All new service logs are structured JSON with stable event names + correlation id.
- [ ] No secrets/PII in any log line (spot-check actual `reports/logs/` output).
- [ ] Latency read as p95/p99 from the k6 summary, not an average.
- [ ] An induced failure was located from `reports/logs/` alone, without reading source.

(CI/CD alerting is external to Punch — this skill covers the in-service signals
that feed it, not pager rules.)
