---
name: punch-orchestration
description: Owns local control flow for the Punch orchestrator — argument parsing, docker compose invocation, subprocess streaming, log collection, report directories, exit codes, and developer experience for `bin/punch`.
applies-to: src/punch/**, bin/punch
---

# Skill: punch-orchestration

## Responsibility

This skill is the authority on **how the orchestrator runs**.

It owns:

- The `bin/punch` CLI surface and argparse layout.
- `subprocess` invocation patterns (streamed, non-buffered, cwd-anchored to
  `REPO_ROOT`).
- Exit-code propagation from `docker compose` back to the shell.
- The evidence artifact contract (`reports/state/punch-run.json`).
- Report and log directory creation under `reports/`.
- Developer experience: `--help` text, `doctor` checks, error messages.

It does **not** own:

- Docker / container internals (see `docker-compose.yml`,
  `docker/*.Dockerfile`, and `docker-compose` instructions).
- k6 thresholds, test logic, or `handleSummary` outputs (see
  `punch-performance-k6`).
- HTML or JSON report shape (see `src/tests/support/report.ts`).

## Behavioral rules

1. **Stdlib only.** No new dependencies. Ever.
2. **Stream, don't buffer.** Every `Popen` reads `stdout` line by line and
   writes to both terminal and (optionally) a log file.
3. **Fail loudly.** Non-zero child exits propagate; never swallow.
4. **Evidence first.** A `run` is not complete until
   `reports/state/punch-run.json` is written, even on failure.
5. **No interactive prompts.** The CLI must work non-interactively in CI.
6. **No premature subcommands.** Wait for a Shape plan before adding one.

## When this skill activates

- Editing `src/punch/__main__.py` or `bin/punch`.
- Adding or renaming a Punch subcommand.
- Changing how subprocess output is captured.
- Changing the evidence artifact shape.

## Why this is a separate skill

Without it, control-flow concerns (subprocess plumbing, exit codes) would
leak into docker-compose YAML or k6 TypeScript. Keeping them isolated lets
each layer evolve independently.
