---
applyTo: "**"
description: Cross-cutting architectural boundaries that apply to every change in Punch.
---

# Punch Architecture — Path Instructions

Scope: **every file**. This is the always-on architectural contract. For
the visual layer map, see [`docs/architecture/punch-boundaries.md`](../../docs/architecture/punch-boundaries.md).

## Ownership

| Layer | Owns | Lives in |
|---|---|---|
| Bash wrapper | route shell calls to Python | `bin/punch`, `bin/*` |
| Python orchestrator | argparse, subprocess streaming, exit codes, evidence file | `src/punch/**` |
| Docker Compose | services as runtime boundaries, image names, ports, env, healthchecks, volumes | `docker-compose.yml` |
| Dockerfiles | how each service is built | `docker/*.Dockerfile` |
| Service code | per-service behavior (gateway / catalog / orders) | `src/services/**` |
| k6 tests | scenarios, thresholds, `handleSummary`, checks | `src/tests/**` |
| Artifacts / reports | the contract between runtime and downstream consumers | `reports/**` |

## Rules

- **Python owns orchestration.** Anything that decides *what to run, in what
  order, with what evidence* lives in `src/punch/`. Bash and k6 do not.
- **Docker Compose owns runtime boundaries.** Service names, ports, env
  vars, dependencies, volumes are contracts. Renames cascade.
- **k6 owns test behavior only.** k6 does not start containers, poll
  state, or write outside `/reports/`.
- **Bash is a thin wrapper.** A bin script that branches on output or
  computes pass/fail belongs in Python instead.
- **Reporting is a product contract.** Artifact paths (`reports/state/punch-run.json`,
  HTML reports, JSON summaries, `reports/logs/`) are stable. Renames or
  schema changes require a Plan that names every consumer.
- **CI/CD is external.** `.github/workflows/` consumes Punch; Punch does
  not extend its own ownership into CI. Workflow edits are out of scope
  for Build prompts unless the Plan explicitly authorizes them.

## Anti-patterns to flag in Review

1. k6 test code that starts containers or shells out.
2. Bash that parses subprocess output to decide control flow.
3. A compose service rename without a dependents grep.
4. A subprocess call from Python that runs k6 directly (skipping compose).
5. A Build that touches Python + compose + k6 in one diff without a Plan
   that authorized the integration.
6. A reporting file path or schema change without a maintenance-matrix
   update.

## When this file activates

Always. It is the global contract every other instruction file refines.
