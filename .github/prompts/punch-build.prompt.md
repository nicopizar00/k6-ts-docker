---
agent: punch-builder
description: Build — execute ONE approved Plan task. The punch-builder dispatcher classifies it and delegates to the runtime or performance-test engineer within scope.
---

# Punch — Build

**Lifecycle phase:** Build
**Mode:** Agent (scoped, via dispatch)
**Owner skill:** [`incremental-implementation`](../skills/incremental-implementation/SKILL.md) + [`test-driven-development`](../skills/test-driven-development/SKILL.md) + the task's domain skill
**Agent:** [`punch-builder`](../agents/punch-builder.agent.md) → delegates to one engineer

## Pre-conditions

- An approved Plan task (from `punch-plan`) with a named task ID.
- A human has confirmed the Plan.

If any is missing, **stop** and return to Plan.

## Inputs

- The approved Plan task: goal, allowed/read-only/forbidden paths, task ID.

## What to do

1. Classify the task into **one** domain and select the engineer + domain skill:
   - orchestrator / `bin/punch` / Compose / service images / data harvest →
     [`punch-runtime-engineer`](../agents/punch-runtime-engineer.agent.md)
     (`punch-python-orchestration` / `punch-compose-runtime` / `punch-data-harvest`).
   - k6 HTTP/Browser / thresholds / `package.json` / TS bundle / lint →
     [`punch-performance-test-engineer`](../agents/punch-performance-test-engineer.agent.md)
     (`punch-k6-testing`).
2. Hand the engineer the goal, scope, constraints, expected output, and required
   evidence (depth-1 — the engineer delegates to no one).
3. On return, consolidate the result, changed files, evidence, and next step.

## Expected output

Per the `punch-builder` evidence contract: **Result · Changed Files · Evidence ·
Unresolved Assumptions · Recommended Next Step**.

## Validation gate

Verify (`./bin/punch run <test>`) — do not claim success here. A change is done
when `reports/state/punch-run.json` records `passed: true`.

## Scope expansion rule

Any edit outside the task's allowed paths → **stop**, return to Plan.

## Mandatory engineer tools + skills scope (absorbed)

Both engineers are **leaf** agents (`agents: []`, depth-1, spawn nothing). When
the dispatcher selects one, it MUST hand over that engineer's **full mandatory
tools and skills scope** below. These mirror the canonical agent files — which
remain the source of truth — and are absorbed here so the Build contract is
self-contained and non-negotiable.

### `punch-runtime-engineer` — runtime domain (Python / Compose / harvest)

- **Tools (mandatory):** `search/codebase`, `search`, `read/problems`, `changes`,
  `edit/editFiles`, `execute/runInTerminal`, `read/terminalLastCommand`,
  `read/terminalSelection`, `execute/createAndRunTask`, `execute/runTask`,
  `read/getTaskOutput`.
- **Skills (mandatory):** always [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md);
  domain [`punch-python-orchestration`](../skills/punch-python-orchestration/SKILL.md)
  + [`punch-compose-runtime`](../skills/punch-compose-runtime/SKILL.md)
  + [`punch-data-harvest`](../skills/punch-data-harvest/SKILL.md);
  method [`incremental-implementation`](../skills/incremental-implementation/SKILL.md);
  proof [`test-driven-development`](../skills/test-driven-development/SKILL.md).
- **Paths:** Allowed `src/punch/**`, `bin/punch`, `docker-compose.yml`,
  `docker/*.Dockerfile` (service images — **not** `k6.Dockerfile`),
  `docker/postgres/**`. Read-only `src/tests/**`, `src/services/**`, `reports/**`.
  Forbidden `src/tests/*.ts`, `docker/k6.Dockerfile`, `package.json`,
  `tsconfig.json`, `.github/**`.

### `punch-performance-test-engineer` — performance-test domain (k6 / TS bundle)

- **Tools (mandatory):** `search/codebase`, `search`, `read/problems`, `changes`,
  `edit/editFiles`, `execute/runInTerminal`, `execute/createAndRunTask`,
  `execute/runTask`, `read/getTaskOutput`.
- **Skills (mandatory):** always [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md);
  domain [`punch-k6-testing`](../skills/punch-k6-testing/SKILL.md)
  (+ [`punch-data-harvest`](../skills/punch-data-harvest/SKILL.md), read-only, when wiring `handleSummary`);
  method [`incremental-implementation`](../skills/incremental-implementation/SKILL.md);
  proof [`test-driven-development`](../skills/test-driven-development/SKILL.md).
- **Paths:** Allowed `src/tests/*.ts` (HTTP and Browser kept separate),
  `src/tests/support/**`, `package.json`, `tsconfig.json`, esbuild/lint config,
  `docker/k6.Dockerfile`. Read-only `docker-compose.yml`, `src/services/**`,
  `reports/**`. Forbidden `src/punch/**`, `docker/*.Dockerfile` (non-k6),
  `docker-compose.yml` edits, `.github/**`. Owns host `npm`/esbuild/lint per
  [ADR 0001](../../docs/ai/decisions/0001-perf-engineer-host-npm.md).

The Plan may **narrow** these lists; it may not widen them past the Forbidden set
without re-planning.

## Default Build comms (Caveman, Build-only)

Build — and only Build — runs the
[`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md) adapter **on by
default** to keep **assistant prose** efficient (implementation updates,
sub-agent handoffs, post-evidence debug summaries, commit drafts). Other
lifecycle phases keep normal prose; Caveman never activates outside Build.

- **Default mode: `full`** (`/caveman full`). Drop to `/caveman lite` when prose
  must stay fully sentence-formed, or `/caveman ultra` only on explicit low-risk
  request. `stop caveman` / `normal mode` reverts.
- Apply it **only after** the Build task is understood — never as a substitute
  for reasoning.
- **Never** compress code, commands, paths, Python orchestration details, Docker
  Compose output, k6 output, JSON/YAML/CSV, logs, stack traces, errors, exit
  codes, test evidence (`reports/state/punch-run.json`), acceptance criteria, or
  risk notes — quote those verbatim. Caveman compresses prose **around** the
  evidence, not the evidence.
- **Priority:** Correctness > evidence > maintainability > brevity > Caveman
  style. If brevity harms clarity, uncertainty, or risk explanation, **stop
  Caveman and answer normally** (Auto-Clarity), then resume.

Scope, modes, and stop conditions: the adapter SKILL.md and
[ADR 0003](../../docs/ai/decisions/0003-caveman-build-comms.md).
