# Scoped Build Policy

Build is the only phase that edits product code. To keep Build safe inside
a multi-layer system (Python orchestrator + Compose + k6 + reporting), every
Build prompt declares its scope as **three path lists**.

## The three lists

1. **Allowed edit paths** — Build may create, modify, or delete files here.
2. **Read-only context paths** — Build may read these for context but must
   not edit them.
3. **Forbidden paths** — Build must refuse to touch these. Touching one is
   a *scope expansion* and triggers the [stop-and-replan rule](#scope-expansion-process).

Each Build prompt under `.github/prompts/punch-build-*.prompt.md` ships with
defaults for these lists. The approved Plan can narrow or widen them, but
never beyond the prompt's *forbidden* set.

## Human checkpoint

Before any Build prompt runs:

1. The Plan must list the task's allowed / read-only / forbidden paths
   explicitly.
2. A human must confirm the plan (chat OK, or PR description).
3. The Build prompt re-states the scope at the top of its work and aborts
   if it cannot match the plan.

## Scope expansion process

If, mid-Build, the agent discovers it cannot complete the task within the
allowed paths:

1. **Stop.** Do not edit a forbidden or read-only file as a "small fix".
2. Capture the new fact (which file, which constraint).
3. Return to **Plan**. Update the task or split it.
4. Get human re-approval.
5. Resume Build on the updated plan.

This is the single most-violated rule in agentic coding. Stopping is cheap.
Unauthorized cross-layer edits cause the most regressions.

## Examples by build domain

### Python orchestration task

Use [`punch-build-orchestrator`](../../.github/prompts/punch-build-orchestrator.prompt.md).

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

Use [`punch-build-compose`](../../.github/prompts/punch-build-compose.prompt.md).

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

Use [`punch-build-k6-http`](../../.github/prompts/punch-build-k6-http.prompt.md).

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

Use [`punch-build-k6-browser`](../../.github/prompts/punch-build-k6-browser.prompt.md).

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

> The Browser image is currently deferred (see
> `src/tests/browser-smoke.ts.example`). Any task that *enables* it must
> first land a Plan that accepts the cost (image size, build time, CI).

### Data harvest / reporting task

Use [`punch-build-data-harvest`](../../.github/prompts/punch-build-data-harvest.prompt.md).

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

Reporting changes are *contract* changes. The plan must spell out the
artifact path, schema, and downstream consumers (see
[`punch-data-harvest` skill](../../.github/skills/punch-data-harvest/SKILL.md)
and [`docs/ai/maintenance-matrix.md`](maintenance-matrix.md)).

## Cross-layer tasks

Some real tasks legitimately cross layers (e.g. "add a new test, wire it
into compose, expose it via `bin/punch run X`"). These are **integration
tasks** and require:

- A single Plan that explicitly authorizes the cross-layer edit.
- One Build prompt invocation per layer, in a fixed order (k6 → compose →
  orchestrator typically), each respecting its own scope.
- Verify runs the full suite, not just the new test.

Never collapse an integration task into a single broad Build. The point of
the per-layer prompts is keeping each layer's reviewer focused.
