---
applyTo: "src/punch/**,bin/punch"
description: Behavior rules for the Python orchestrator (bin/punch and src/punch).
---
# Python Orchestrator — Path Instructions

Scope: `bin/punch` and all under `src/punch/`.

## Rules

- **Stdlib only.** No `requirements.txt`, no `pip install`, no
  `pyproject.toml` deps. `argparse`, `subprocess`, `pathlib`,
  `json`, `os`, `sys`, `datetime`, `time`, `shutil` enough.
- **Single responsibility — orchestration.** Orchestrator own control
  flow: arg parse, subprocess invoke, exit-code propagate,
  evidence write. Not own Docker semantics, k6 thresholds,
  or report HTML — those belong to compose, k6 scripts,
  `src/tests/support/`.
- **Stream subprocess output, no buffer.** Every `Popen` read
  `stdout`/`stderr` line by line. Native command output (Docker, k6) must
  reach terminal live **and** capture to log file when
  `--collect-logs` (or equivalent) set.
- **Exit codes propagate.** CLI exit code = child process exit
  code (or first non-zero in sequence). Never swallow non-zero.
- **Evidence artifact mandatory.** Every `run` write
  `reports/state/punch-run.json` with: tests run, per-test exit codes,
  overall `passed: true|false`. Write even on failure.
- **Artifact paths explicit.** Use `pathlib.Path`, anchor every path
  to `REPO_ROOT`. No relative `./reports/`; no `os.getcwd()` surprise.
- **Docker Compose invocations consistent.** Always
  `docker compose run --rm <service>` (not `docker run`), always from
  `REPO_ROOT`, always compose file picked up implicit. No
  hand-built container commands.
- **Bash thin-wrapper principle.** `bin/punch` exec Python module —
  no logic, no path massage, no env default. Logic in
  `bin/` → move to `src/punch/`.
- **No interactive prompts.** CLI must work non-interactive in CI.
  No TTY assumption; no terminal-colour gating.
- **No new subcommands without Plan.** Adding command = lifecycle
  change; no inline parser extend during Build.

## Tests

`python3 -m punch --help` and dry `doctor` = smoke tests. Heavier
tests deferred till CLI grow beyond small command set.

## Streaming subprocess pattern

The canonical implementation lives in `src/punch/__main__.py`; read it before
extending. The shape:

```python
import subprocess
from pathlib import Path

def stream(cmd: list[str], cwd: Path, log_path: Path | None = None) -> int:
    """Run `cmd`, stream stdout+stderr to terminal and (optionally) a log.
    Returns the child exit code. Never buffers. Never swallows non-zero."""
    log_fp = log_path.open("w") if log_path else None
    try:
        with subprocess.Popen(
            cmd, cwd=str(cwd), stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, bufsize=1, text=True,
        ) as proc:
            for line in proc.stdout:
                print(line, end="")
                if log_fp:
                    log_fp.write(line)
            return proc.wait()
    finally:
        if log_fp:
            log_fp.close()
```

- `stderr=subprocess.STDOUT` keeps line order matching what a human running
  the command directly would see.
- `bufsize=1` + `text=True` is the line-buffered contract; raw byte streams
  break Unicode in k6 output.
- `for line in proc.stdout` is the only correct streaming loop —
  `proc.communicate()` buffers, `proc.stdout.read()` blocks until EOF.
- Extending: a `--quiet` mode makes the `print()` conditional but the log
  write stays unconditional; `--collect-logs` always sets `log_path`.
  Parallel runs are **not** a within-contract extension — sequential is the
  contract; parallel breaks exit-code propagation semantics, needs a Plan.
- Does not parse output for control flow, does not retry (retries belong in
  `doctor`, not `run`), never `docker run`s directly (`docker compose run
  --rm` is the contract).

## Build prompt

Use [`punch-build`](../prompts/punch-build.prompt.md) — `punch-builder` classifies orchestrator tasks into its runtime subsystem.
