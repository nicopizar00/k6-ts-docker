# ADR 0001 — punch-performance-test-engineer may use host npm

**Status:** Accepted (2026-06-17)
**Deciders:** repository owner + Punch Builder architecture work

## Context

Punch Rule #1 = **Docker First**: host need only Docker + stdlib Python 3 runtime — "no Node, no k6". `npm`/esbuild run **inside** `docker/k6.Dockerfile` builder stage, never host commands.

New `punch-performance-test-engineer` agent own k6 test scripting **and** TypeScript/esbuild bundle toolchain — `package.json`, `tsconfig.json`, esbuild config, lint. Invoked heavy during `/punch-build`. Authoring + maintaining toolchain (dep bumps, type-check, lint, local bundle iteration) much slower if every `npm` action go through container round-trip.

## Decision

`punch-performance-test-engineer` = **single sanctioned surface** allowed to run host `npm`/`pnpm`/`esbuild`/lint — **and host `k6` for smoke pre-check** (`npm run smoke:local`) — while authoring + maintaining k6 test toolchain. This **scoped exception** to Docker First, not repeal:

- Exception applies **only** this agent, **only** TS/k6 test toolchain (`package.json`, `tsconfig.json`, esbuild/lint config, `src/tests/**`) and **`smoke:local` host-k6 gate** — fast *does-script-run* check before orchestration. Run **smoke only**, write **no** canonical `punch-run.json`.
- **No other agent, command, or contributor workflow** gain host-Node dependence. `bin/punch`, orchestration, end-user contract stay Docker-only + stdlib Python.
- **Shipped execution chain unchanged**: source → esbuild **in `docker/k6.Dockerfile`** → k6 image → run → reports. Host `npm` = *authoring* convenience; never runtime dependency.

## Consequences

- **Positive:** faster, more maintainable k6 test-script authoring; bundle toolchain has clear owner.
- **Negative / watch:** contributor running this agent authoring loop locally need Node installed. Acceptable — opt-in (only when working test toolchain), no touch to Docker-First *runtime* guarantee.
- **Guardrail:** `CLAUDE.md` Rule #1 link here; `punch-ai-governance` treat any *other* host-`npm` usage as drift.
