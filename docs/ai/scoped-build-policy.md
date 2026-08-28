# Scoped Build Policy

Build only phase that edit product code. Keep Build safe inside multi-layer system (Python orchestrator + Compose + k6 + reporting): every Build task declare scope as **three path lists**, applied by `punch-builder` per the subsystem (runtime vs. performance-test) it classifies the task into.

## The three lists

1. **Allowed edit paths** — Build may create, modify, delete files here.
2. **Read-only context paths** — Build may read for context, must not edit.
3. **Forbidden paths** — Build must refuse to touch. Touching one = *scope expansion*, triggers [stop-and-replan rule](#scope-expansion-process).

`punch-builder` ships defaults for these lists per subsystem (see
[`punch-builder.agent.md`](../../.github/agents/punch-builder.agent.md)'s
"Paths by subsystem"). Approved Plan can narrow or widen, never beyond the
subsystem's *forbidden* set.

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

Each domain below is classified by `punch-builder` into a subsystem, which carries the scope table.

### Python orchestration task

Runtime subsystem.

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

Runtime subsystem.

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

Performance-test subsystem.

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

Performance-test subsystem.

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

Runtime subsystem.

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

Reporting changes = *contract* changes. Plan must spell out artifact path, schema, downstream consumers (see [`artifacts-reporting.instructions.md`](../../.github/instructions/artifacts-reporting.instructions.md) and [`docs/ai/maintenance-matrix.md`](maintenance-matrix.md)).

## Service-change route (narrow exception)

`src/services/**` defaults to **read-only** for every Build task above — no
domain example lists it as Allowed. A future Plan may route a `src/services/**`
change to the runtime subsystem when the task is driven by an approved
performance, observability, or security finding, by naming the exact service
path in that task's own Allowed edit paths (see
[`punch-builder.agent.md`](../../.github/agents/punch-builder.agent.md)'s
"Service-change route" note). This is a per-task grant, not a standing widening
— every other task's default stays read-only.

## Cross-layer tasks

Some real tasks legit cross layers (e.g. "add new test, wire into compose, expose via `bin/punch run X`"). These = **integration tasks**, require:

- Single Plan that explicitly authorize cross-layer edit.
- One `punch-build` invocation per subsystem, fixed order (k6 → compose → orchestrator typically) — `punch-builder` works each subsystem's paths in turn, respecting each one's own scope before moving to the next.
- Verify runs full suite, not just the new test.

Never collapse an integration task into one undifferentiated edit across both subsystems' paths at once — the split exists to keep each layer's diff reviewable.
