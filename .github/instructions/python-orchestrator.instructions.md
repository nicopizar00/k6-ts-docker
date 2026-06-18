---
applyTo: "src/punch/**,bin/punch"
description: Behavior rules for the Python orchestrator (bin/punch and src/punch).
---

# Python Orchestrator — Path Instructions

Scope: `bin/punch` and everything under `src/punch/`.

## Rules

- **Stdlib only.** No `requirements.txt`, no `pip install`, no
  `pyproject.toml` dependencies. `argparse`, `subprocess`, `pathlib`,
  `json`, `os`, `sys`, `datetime`, `time`, `shutil` are enough.
- **Single responsibility — orchestration.** The orchestrator owns control
  flow: argument parsing, subprocess invocation, exit-code propagation,
  evidence writing. It does **not** own Docker semantics, k6 thresholds,
  or report HTML — those belong to compose, k6 scripts, and
  `src/tests/support/`.
- **Stream subprocess output, do not buffer.** Every `Popen` reads
  `stdout`/`stderr` line by line. Native command output (Docker, k6) must
  reach the terminal as it happens **and** be captured to a log file when
  `--collect-logs` (or equivalent) is set.
- **Exit codes propagate.** The CLI's exit code is the child process exit
  code (or the first non-zero in a sequence). Never swallow non-zero codes.
- **Evidence artifact is mandatory.** Every `run` writes
  `reports/state/punch-run.json` with: tests run, per-test exit codes, an
  overall `passed: true|false`. Write it even on failure.
- **Artifact paths are explicit.** Use `pathlib.Path` and anchor every path
  to `REPO_ROOT`. No relative `./reports/`; no `os.getcwd()` surprises.
- **Docker Compose invocations are consistent.** Always
  `docker compose run --rm <service>` (not `docker run`), always from
  `REPO_ROOT`, always with the compose file picked up implicitly. Do not
  hand-construct container commands.
- **Bash thin-wrapper principle.** `bin/punch` execs the Python module —
  no logic, no path massaging, no env defaulting. If logic appears in
  `bin/`, move it into `src/punch/`.
- **No interactive prompts.** The CLI must work non-interactively in CI.
  No TTY assumptions; no terminal-colour gating.
- **No new subcommands without a Plan.** Adding a command is a lifecycle
  change; do not extend the parser inline during Build.

## Tests

`python3 -m punch --help` and a dry `doctor` are the smoke tests. Heavier
tests are deferred until the CLI grows beyond a small command set.

## Build prompt

Use [`punch-build`](../prompts/punch-build.prompt.md) — the dispatcher routes orchestrator tasks to `punch-runtime-engineer`.
