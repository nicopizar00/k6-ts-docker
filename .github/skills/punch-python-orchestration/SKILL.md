---
name: punch-python-orchestration
description: Owns local control flow for the Punch orchestrator — argument parsing, docker compose invocation, subprocess streaming, log capture, exit codes, evidence artifact, and developer experience for `bin/punch`.
applies-to: src/punch/**, bin/punch
---

# Skill: punch-python-orchestration

## Responsibility

This skill is the authority on **how the orchestrator runs**.

It owns:

- The `bin/punch` CLI surface and `argparse` layout.
- `subprocess` invocation patterns (streamed, non-buffered, anchored to
  `REPO_ROOT`).
- Native command output preservation — `docker compose` and k6 lines reach
  the terminal as the child process emits them, optionally tee'd to a log
  file with `--collect-logs`.
- Exit-code propagation from `docker compose` back to the shell.
- The evidence artifact contract (`reports/state/punch-run.json`).
- Report and log directory creation under `reports/`.
- Dry-run behavior (when added — must be opt-in, never silent).
- Config parsing (stdlib only — `json`, `os.environ`, `argparse`).
- Artifact path stability (no relative paths; everything anchored).
- Developer experience: `--help` text, `doctor` checks, error messages.
- The Bash thin-wrapper principle (`bin/punch` execs Python; no logic).

It does **not** own:

- Docker / container internals (see `punch-compose-runtime`).
- k6 thresholds or test logic (see `punch-k6-testing`).
- HTML or JSON report shape (see `punch-data-harvest` and
  `src/tests/support/report.ts`).
- Governance of the AI configuration (see `punch-governance-review`).

## When to use

- Editing `src/punch/__main__.py` or `bin/punch`.
- Adding or renaming a Punch subcommand (requires a Plan).
- Changing how subprocess output is captured or streamed.
- Changing the evidence artifact shape.
- Adjusting `doctor` checks.

## Inputs expected

- The approved Plan task with allowed/read-only/forbidden paths.
- The intent: which subcommand or behavior is changing.

## Procedure

1. Re-read `src/punch/__main__.py` to ground in the current control flow.
2. Confirm the change keeps stdlib-only.
3. Implement the minimum patch in the allowed paths.
4. Preserve streaming (`Popen` with line-buffered reads); never `.communicate()`
   if the child can take >1s.
5. Always write `reports/state/punch-run.json` at the end of a `run` — pass
   or fail.
6. Update `--help` text and the `doctor` flow if the change surfaces a new
   prerequisite.

## Output format

A focused diff under `src/punch/**` and possibly `bin/punch`. Report:

- Every file changed.
- The new/modified subcommand signature (if any).
- The evidence file's shape if it changed.

## Safety / boundary rules

- **Stdlib only.** No new dependencies — ever.
- **Stream, don't buffer.**
- **Fail loudly.** Non-zero child exits propagate.
- **No interactive prompts.** CI is the binding constraint.
- **No subcommand sprawl.** Adding a subcommand is a Plan-level change.
- **No bypassing Compose.** Always `docker compose run --rm <service>`.

## Why this is a separate skill

Without it, control-flow concerns (subprocess plumbing, exit codes) would
leak into Docker Compose YAML or k6 TypeScript. Keeping them isolated lets
each layer evolve independently.

## Examples

See [`examples/streaming-subprocess.md`](examples/streaming-subprocess.md)
for a reference walkthrough of the streaming pattern as it already exists
in `src/punch/__main__.py`.
