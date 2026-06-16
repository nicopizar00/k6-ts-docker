---
applyTo: "src/punch/**,bin/punch"
description: Behavior rules for the Python orchestrator.
---

# Python Orchestration — Path Instructions

Scope: `bin/punch` and everything under `src/punch/`.

## Rules

- **Stdlib only.** No `requirements.txt`, no `pip install`, no `pyproject.toml`
  dependencies. `argparse`, `subprocess`, `pathlib`, `json`, `os`, `sys`,
  `datetime`, `time`, `shutil` are enough.
- **Single responsibility.** The orchestrator owns control flow:
  argument parsing, subprocess streaming, exit-code propagation, evidence
  writing. It does **not** own Docker semantics, k6 thresholds, or report
  formatting — those belong to compose, k6 scripts, and `src/tests/support/`.
- **Streaming output.** Always stream subprocess stdout+stderr to the
  terminal as it happens. Never silently buffer.
- **Exit code propagation.** The CLI's exit code is the child process exit code
  (or the first non-zero in a sequence). Never swallow non-zero codes.
- **Evidence artifact.** Each `run` writes `reports/state/punch-run.json` with
  the test list, per-test exit codes, and an overall pass/fail boolean.
- **No print-only logic.** Do not gate behavior on terminal colors, TTYs, or
  interactive prompts. The CLI must work in CI.
- **No new subcommands without a Shape plan.** Adding a command is a
  lifecycle change; do not extend the parser inline during Build.

## Tests

Inline `python3 -m punch --help` and a dry `doctor` are the smoke tests.
Heavier tests are deferred until the CLI grows beyond three commands.
