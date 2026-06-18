# ADR 0001 — punch-performance-test-engineer may use host npm

**Status:** Accepted (2026-06-17)
**Deciders:** repository owner + Punch Builder architecture work

## Context

Punch's Rule #1 is **Docker First**: the host needs only Docker and a stdlib
Python 3 runtime — "no Node, no k6". `npm`/esbuild run **inside** the
`docker/k6.Dockerfile` builder stage, never as user-facing host commands.

The new `punch-performance-test-engineer` agent owns k6 test scripting **and** the
TypeScript/esbuild bundle toolchain — `package.json`, `tsconfig.json`, the esbuild
config, and lint. It is invoked heavily during `/punch-build`. Authoring and
maintaining that toolchain (dependency bumps, type-checking, lint, local bundle
iteration) is materially slower if every `npm` action must go through a container
round-trip.

## Decision

`punch-performance-test-engineer` is the **single sanctioned surface** allowed to
run host `npm`/`pnpm`/`esbuild`/lint — **and host `k6` for the smoke pre-check**
(`npm run smoke:local`) — while authoring and maintaining the k6 test toolchain.
This is a **scoped exception** to Docker First, not a repeal:

- The exception applies **only** to this agent, **only** for the TS/k6 test
  toolchain (`package.json`, `tsconfig.json`, esbuild/lint config, `src/tests/**`)
  and the **`smoke:local` host-k6 gate** — a fast *does-the-script-run* check
  before orchestration. It runs **smoke only** and writes **no** canonical
  `punch-run.json`.
- **No other agent, command, or contributor workflow** gains host-Node
  dependence. `bin/punch`, orchestration, and the end-user contract stay
  Docker-only + stdlib Python.
- The **shipped execution chain is unchanged**: source → esbuild **in
  `docker/k6.Dockerfile`** → k6 image → run → reports. Host `npm` is an
  *authoring* convenience; it never becomes a runtime dependency.

## Consequences

- **Positive:** faster, more maintainable k6 test-script authoring; the bundle
  toolchain has a clear owner.
- **Negative / watch:** a contributor running this agent's authoring loop locally
  needs Node installed. This is acceptable because it is opt-in (only when working
  the test toolchain) and does not touch the Docker-First *runtime* guarantee.
- **Guardrail:** `CLAUDE.md` Rule #1 links here; `punch-ai-governance` treats any
  *other* host-`npm` usage as drift.
