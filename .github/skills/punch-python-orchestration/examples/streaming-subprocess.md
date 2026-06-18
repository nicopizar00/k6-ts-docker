# Example — Streaming subprocess pattern

This is a reference for the streaming-subprocess pattern Punch uses to run
`docker compose` commands. The canonical implementation lives in
`src/punch/__main__.py`; this file explains the shape so an agent can
extend it without reinventing it.

## The shape

```python
import subprocess
from pathlib import Path

def stream(cmd: list[str], cwd: Path, log_path: Path | None = None) -> int:
    """Run `cmd`, stream stdout+stderr to terminal and (optionally) a log.

    Returns the child exit code. Never buffers. Never swallows non-zero.
    """
    log_fp = log_path.open("w") if log_path else None
    try:
        with subprocess.Popen(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,           # line-buffered
            text=True,
        ) as proc:
            assert proc.stdout is not None
            for line in proc.stdout:
                print(line, end="")          # terminal
                if log_fp:
                    log_fp.write(line)       # optional file
            return proc.wait()
    finally:
        if log_fp:
            log_fp.close()
```

## Why this shape

- `stderr=subprocess.STDOUT` keeps the line order intact so the terminal
  shows what a human would see running the command directly.
- `bufsize=1` + `text=True` is the line-buffered text contract Python
  guarantees; raw byte streams break Unicode in k6 output.
- The `for line in proc.stdout` loop is the **only** correct way to
  stream — `proc.communicate()` would buffer and `proc.stdout.read()`
  would block until EOF.
- `proc.wait()` returns the exit code; the caller propagates it as the
  CLI's exit code so CI sees the truth.

## When to extend this pattern

- Adding a `--quiet` mode: the terminal `print()` becomes conditional,
  but the log file write must remain unconditional.
- Adding a `--collect-logs` mode: `log_path` becomes always-set under
  `reports/logs/<test>.log`.
- Adding parallel runs: do not — sequential is the contract today, and
  parallel would break exit-code propagation semantics. Replan first.

## What this pattern does NOT do

- It does not parse output for control flow. (That would put business
  logic inside the orchestrator's plumbing layer — a violation.)
- It does not retry. (Retries belong in `doctor` checks, not `run`.)
- It does not start containers directly. (`docker compose run --rm` is the
  contract; the orchestrator never `docker run`s.)

## Reference

The live implementation is in `src/punch/__main__.py`. Read it before
modifying — the example here is documentation, not source.
