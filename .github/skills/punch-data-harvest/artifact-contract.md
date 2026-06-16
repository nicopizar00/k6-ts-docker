# Artifact Contract Template

Every artifact Punch writes (or proposes to write) must be describable in
this template. The template lives next to `punch-data-harvest` so it is
visible whenever someone changes reporting.

## The template

```markdown
### <artifact name>

| Field | Value |
|---|---|
| Path | `reports/<...>` (absolute under repo root) |
| Format | JSON / CSV / HTML / plain log |
| Produced by | `src/punch/__main__.py:<function>` or `src/tests/<test>.ts:handleSummary` |
| Produced when | every `run`, or per-test, or only on failure, or `--collect-logs` |
| Schema | one paragraph or a small example; stable across patch versions |
| Read by | who downstream depends on this artifact (CI job name, dashboard, human) |
| Stability | "stable contract" (rename = Plan) or "internal" (may change freely) |
| Sensitivity | PII risk, secret risk, sanitization required (yes/no + how) |
```

## Current artifacts

### `reports/state/punch-run.json`

| Field | Value |
|---|---|
| Path | `reports/state/punch-run.json` |
| Format | JSON |
| Produced by | `src/punch/__main__.py` (the `run` subcommand) |
| Produced when | every `./bin/punch run` invocation, pass or fail |
| Schema | `{ "tests": [{"name": str, "exit_code": int}], "passed": bool, "started_at": iso8601, "finished_at": iso8601 }` |
| Read by | CI validation job, future automation, the Verify gate |
| Stability | **stable contract** — rename or schema change requires a Plan |
| Sensitivity | none (test names + exit codes only) |

### `reports/state/test-context.json`

| Field | Value |
|---|---|
| Path | `reports/state/test-context.json` |
| Format | JSON |
| Produced by | `src/tests/order-journey.ts` `handleSummary` |
| Produced when | every journey run |
| Schema | `{ "created_order_ids": [str], "created_at": iso8601 }` (see file for current shape) |
| Read by | downstream assertions within the same journey; humans debugging a journey failure |
| Stability | **stable contract** within journey tests |
| Sensitivity | none (fixture IDs only — no real customer data) |

### `reports/<test>.html`

| Field | Value |
|---|---|
| Path | `reports/<test-name>.html` |
| Format | HTML, self-contained (inline CSS, no remote fetches) |
| Produced by | `src/tests/support/report.ts` (called from each test's `handleSummary`) |
| Produced when | every test run |
| Schema | Free-form HTML; structure stable enough that users can grep for thresholds |
| Read by | humans only |
| Stability | internal — visual changes allowed without a Plan; structural breaks should mention in PR |
| Sensitivity | sanitize URLs in the rendered output |

### `reports/<test>.json`

| Field | Value |
|---|---|
| Path | `reports/<test-name>.json` |
| Format | JSON |
| Produced by | k6 `handleSummary` (compact summary) |
| Produced when | every test run |
| Schema | k6's summary JSON shape, **filtered** to aggregates (counts, thresholds, durations). Do not write raw per-iteration data. |
| Read by | humans, future automation |
| Stability | tracks k6 upstream changes; absorb upgrades in `punch-k6-performance` |
| Sensitivity | sanitize headers/env from any error sections |

### `reports/logs/<service>.log`

| Field | Value |
|---|---|
| Path | `reports/logs/<service-name>.log` |
| Format | plain text |
| Produced by | `src/punch/__main__.py` when `--collect-logs` is set |
| Produced when | per-run, one file per service |
| Schema | raw container stdout+stderr, line-ordered |
| Read by | humans debugging a failure |
| Stability | log content tracks the service; file name is a contract |
| Sensitivity | container logs may include URLs / headers — review before sharing externally |

## When to write a new contract entry

A change adds a new artifact, splits an existing one, or moves an
existing one. Fill in a new template block in the Plan, land it here in
the same PR.
