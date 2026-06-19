---
agent: punch-builder
description: Build — execute ONE approved Plan task. The punch-builder dispatcher classifies it and delegates to the runtime or performance-test engineer within scope.
---
# Punch — Build

**Lifecycle phase:** Build
**Mode:** Agent (scoped, via dispatch)
**Owner skill:** [`incremental-implementation`](../skills/incremental-implementation/SKILL.md) + [`test-driven-development`](../skills/test-driven-development/SKILL.md) + task domain skill
**Agent:** [`punch-builder`](../agents/punch-builder.agent.md) → delegate one engineer
**Operating comms:** Caveman enforced — `ultra` here, `wenyan` for engineer sub-agents. See [Operating comms (enforced)](#operating-comms-enforced). Evidence never compressed.

## Pre-conditions

- Approved Plan task (from `punch-plan`) with named task ID.
- Human confirmed Plan.

Any missing → **stop**, return to Plan.

## Inputs

- Approved Plan task: goal, allowed/read-only/forbidden paths, task ID.

## What to do

1. Classify task into **one** domain, pick engineer + domain skill:
   - orchestrator / `bin/punch` / Compose / service images / data harvest →
     [`punch-runtime-engineer`](../agents/punch-runtime-engineer.agent.md)
     (`punch-python-orchestration` / `punch-compose-runtime` / `punch-data-harvest`).
   - k6 HTTP/Browser / thresholds / `package.json` / TS bundle / lint →
     [`punch-performance-test-engineer`](../agents/punch-performance-test-engineer.agent.md)
     (`punch-k6-testing`).
2. Hand engineer the goal, scope, constraints, expected output, required
   evidence (depth-1 — engineer delegates to no one).
3. On return, consolidate result, changed files, evidence, next step.

## Expected output

Per `punch-builder` evidence contract: **Result · Changed Files · Evidence ·
Unresolved Assumptions · Recommended Next Step**. Evidence (paths, commands, run
output, `reports/state/punch-run.json`) verbatim.

## Validation gate

Verify (`./bin/punch run <test>`) — no success claim here. Change done
when `reports/state/punch-run.json` records `passed: true`.

## Scope expansion rule

Any edit outside task allowed paths → **stop**, return to Plan.

## Mandatory engineer tools + skills scope (absorbed)

Both engineers are **leaf** agents (`agents: []`, depth-1, spawn nothing). When
dispatcher picks one, MUST hand over that engineer's **full mandatory
tools and skills scope** below. These mirror canonical agent files — still source
of truth — absorbed here so Build contract self-contained, non-negotiable.

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

Plan may **narrow** these lists; may not widen past Forbidden set
without re-planning.

## Operating comms (enforced)

Caveman enforced for Build. Activate `caveman` Agent Skill **once** on
entering phase (per `using-agent-skills`), then rely on persistence:

- **Governance tier** (this prompt + `punch-builder` dispatcher): **`ultra`**.
- **Execution tier** (engineer sub-agents): **`wenyan`** — max efficiency.
- **Evidence never compressed** — code, commands, paths, k6/Compose output,
  JSON/YAML/CSV, `reports/state/punch-run.json` quoted verbatim any mode.

Full policy (tiers, modes, evidence list, Auto-Clarity, priority order) lives in
[`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md) +
[ADR 0003](../../docs/ai/decisions/0003-caveman-build-comms.md) — not restated here.
