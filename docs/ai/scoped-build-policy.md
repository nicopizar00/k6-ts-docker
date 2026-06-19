# Scoped Build Policy

Build only phase that edit product code. Keep Build safe inside multi-layer system (Python orchestrator + Compose + k6 + reporting): every Build task declare scope as **three path lists**, carried by engineer agent the `punch-builder` dispatcher route it to.

## The three lists

1. **Allowed edit paths** — Build may create, modify, delete files here.
2. **Read-only context paths** — Build may read for context, must not edit.
3. **Forbidden paths** — Build must refuse to touch. Touching one = *scope expansion*, triggers [stop-and-replan rule](#scope-expansion-process).

Each **engineer agent** (`punch-runtime-engineer`, `punch-performance-test-engineer`) ship defaults for these lists; single `punch-build` prompt + `punch-builder` dispatcher route task to right one. Approved Plan can narrow or widen, never beyond engineer's *forbidden* set.

## Human checkpoint

Before any Build prompt runs:

1. Plan must list task's allowed / read-only / forbidden paths explicitly.
2. Human must confirm plan (chat OK, or PR description).
3. Build prompt re-state scope at top of work, abort if cannot match plan.

## Scope expansion process

If mid-Build agent finds it cannot finish task within allowed paths:

1. **Stop.** No edit forbidden/read-only file as "small fix".
2. Capture new fact (which file, which constraint).
3. Return to **Plan**. Update task or split it.
4. Get human re-approval.
5. Resume Build on updated plan.

Most-violated rule in agentic coding. Stopping cheap. Unauthorized cross-layer edits cause most regressions.

## Examples by build domain

Each domain below routed by `punch-builder` to named engineer, which carry scope table.

### Python orchestration task

Routed to [`punch-runtime-engineer`](../../.github/agents/punch-runtime-engineer.agent.md).

```
Allowed:
  src/punch/**/*.py
  bin/punch                    (only if the wrapper contract changes)
Read-only:
  docker-compose.yml
  docker/**
  src/tests/**
Forbidden:
  src/services/**
  .github/workflows/**
  package.json, tsconfig.json
```

### Docker Compose / runtime task

Routed to [`punch-runtime-engineer`](../../.github/agents/punch-runtime-engineer.agent.md).

```
Allowed:
  docker-compose.yml
  docker/**
  .env.example                 (if added later)
Read-only:
  src/punch/**
  src/tests/**
Forbidden:
  src/services/**              (unless explicitly planned)
  .github/workflows/**
```

### k6 HTTP test task

Routed to [`punch-performance-test-engineer`](../../.github/agents/punch-performance-test-engineer.agent.md).

```
Allowed:
  src/tests/*.ts               (HTTP tests only — not browser-*)
  src/tests/support/**         (only if the shared helper changes)
Read-only:
  docker-compose.yml
  src/services/**
Forbidden:
  src/punch/**
  docker/**                    (unless thresholds require an image change — replan)
  src/tests/browser-*.ts*
```

### k6 Browser test task

Routed to [`punch-performance-test-engineer`](../../.github/agents/punch-performance-test-engineer.agent.md).

```
Allowed:
  src/tests/browser-*.ts
  src/tests/browser-*.ts.example
  docker/k6-browser.Dockerfile (only when explicitly planned)
Read-only:
  docker-compose.yml
  src/services/**
Forbidden:
  src/punch/**
  src/tests/*.ts               (non-browser tests)
  docker/k6.Dockerfile         (HTTP k6 image)
```

> Browser image currently deferred (see `src/tests/browser-smoke.ts.example`). Any task that *enables* it must first land Plan that accepts cost (image size, build time, CI).

### Data harvest / reporting task

Routed to [`punch-runtime-engineer`](../../.github/agents/punch-runtime-engineer.agent.md).

```
Allowed:
  src/tests/support/**         (HTML/JSON report builder)
  src/punch/**                 (only the reporting/state writer parts; the
                               plan must name the functions)
Read-only:
  src/tests/*.ts
  docker-compose.yml
Forbidden:
  docker/**
  src/services/**
  .github/workflows/**
```

Reporting changes = *contract* changes. Plan must spell out artifact path, schema, downstream consumers (see [`punch-data-harvest` skill](../../.github/skills/punch-data-harvest/SKILL.md) and [`docs/ai/maintenance-matrix.md`](maintenance-matrix.md)).

## Cross-layer tasks

Some real tasks legit cross layers (e.g. "add new test, wire into compose, expose via `bin/punch run X`"). These = **integration tasks**, require:

- Single Plan that explicitly authorize cross-layer edit.
- One `punch-build` invocation per layer, fixed order (k6 → compose → orchestrator typically) — dispatcher route each to its engineer, each respecting own scope.
- Verify runs full suite, not just new test.

Never collapse integration task into single broad Build. Point of per-domain engineers = keep each layer's reviewer focused.
