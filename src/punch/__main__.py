"""punch CLI entry point.

Stdlib-only orchestrator. Owns control flow; delegates execution to
docker compose. Writes a single evidence file at reports/state/punch-run.json
so automation can confirm a run happened without parsing k6 output.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import socket
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = REPO_ROOT / "reports"
STATE_DIR = REPORTS_DIR / "state"
LOGS_DIR = REPORTS_DIR / "logs"

TESTS = {
    "smoke":   "/scripts/smoke.js",
    "gate":    "/scripts/catalog-gate.js",
    "journey": "/scripts/order-journey.js",
    "bff-checkout-journey": "/scripts/bff-checkout-journey.js",
}

# Tests that target an EXTERNAL host (not the in-network reference app) and so
# require an explicit env var. In a full-suite run (`run all`) they are SKIPPED —
# not failed — when their env is unset, keeping the in-network gate green. Run them
# directly (e.g. `punch run bff-checkout-journey`) with the env set to execute them.
REQUIRES_ENV = {
    "bff-checkout-journey": "TARGET_BASE_URL",
}


def _ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def _stream(cmd: list[str], log_path: Path | None = None) -> int:
    """Run a subprocess streaming stdout+stderr to terminal and optional log."""
    print(f"$ {' '.join(cmd)}", flush=True)
    log_fh = log_path.open("w", encoding="utf-8") if log_path else None
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            if log_fh:
                log_fh.write(line)
        return proc.wait()
    finally:
        if log_fh:
            log_fh.close()


def _write_evidence(record: dict) -> None:
    _ensure_dirs()
    path = STATE_DIR / "punch-run.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"[punch] evidence written: {path.relative_to(REPO_ROOT)}", flush=True)


def cmd_doctor(_args: argparse.Namespace) -> int:
    checks: list[tuple[str, bool, str]] = []

    docker = shutil.which("docker")
    checks.append(("docker on PATH", docker is not None, docker or "missing"))

    compose_ok = False
    compose_version = ""
    if docker:
        try:
            out = subprocess.run(
                [docker, "compose", "version"],
                capture_output=True, text=True, check=False,
            )
            compose_ok = out.returncode == 0
            compose_version = (out.stdout or out.stderr).strip().splitlines()[0] if out.stdout or out.stderr else ""
        except OSError as e:
            compose_version = str(e)
    checks.append(("docker compose available", compose_ok, compose_version))

    compose_file = REPO_ROOT / "docker-compose.yml"
    checks.append(("docker-compose.yml present", compose_file.is_file(), str(compose_file)))

    py_ok = sys.version_info >= (3, 10)
    checks.append(("python >= 3.10", py_ok, sys.version.split()[0]))

    for name, ok, detail in checks:
        mark = "OK  " if ok else "FAIL"
        print(f"  [{mark}] {name}: {detail}")

    return 0 if all(ok for _, ok, _ in checks) else 1


def _compose_build() -> int:
    return _stream(["docker", "compose", "build"])


def _run_one(test: str) -> int:
    script = TESTS[test]
    cmd = ["docker", "compose", "run", "--rm"]
    # forward any TARGET_ prefixed env vars into the container
    for k in sorted(os.environ.keys()):
        if k.startswith("TARGET_"):
            cmd.extend(["-e", k])
    cmd.extend(["k6", "run", script])
    log = LOGS_DIR / f"k6-{test}.log"
    return _stream(cmd, log_path=log)


def _diagnose_target_connectivity() -> None:
    """Attempt a best-effort TCP connect to TARGET_BASE_URL to help diagnosis.

    This runs on the host (not inside the container) and is only advisory; it
    does not change orchestration behavior but helps the operator understand
    why a containerized k6 run might fail to reach a host-provided service.
    """
    target = os.environ.get("TARGET_BASE_URL")
    if not target:
        return
    try:
        p = urlparse(target)
        host = p.hostname
        port = p.port or (443 if p.scheme == "https" else 80)
        print(f"[punch] diagnosing TARGET_BASE_URL reachability: {host}:{port}", flush=True)
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"[punch] host reachable: {host}:{port}", flush=True)
        except OSError as e:
            print(f"[punch] host NOT reachable from host: {host}:{port} ({e})", flush=True)
    except Exception as e:
        print(f"[punch] could not parse TARGET_BASE_URL '{target}': {e}", flush=True)


def _collect_service_logs() -> None:
    for svc in ("gateway-api", "catalog-api", "orders-api", "postgres"):
        log = LOGS_DIR / f"{svc}.log"
        try:
            with log.open("w", encoding="utf-8") as fh:
                subprocess.run(
                    ["docker", "compose", "logs", svc],
                    cwd=REPO_ROOT, stdout=fh, stderr=subprocess.STDOUT, check=False,
                )
        except OSError as e:
            print(f"[punch] could not collect logs for {svc}: {e}", flush=True)


def cmd_run(args: argparse.Namespace) -> int:
    _ensure_dirs()
    requested = args.test
    sequence = list(TESTS.keys()) if requested == "all" else [requested]

    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()

    build_rc = _compose_build()
    if build_rc != 0:
        _write_evidence({
            "command": "run",
            "tests": sequence,
            "phase": "build",
            "exitCode": build_rc,
            "passed": False,
            "startedAt": started,
            "durationSeconds": round(time.monotonic() - t0, 2),
        })
        return build_rc

    results: list[dict] = []
    overall_rc = 0
    for test in sequence:
        required_env = REQUIRES_ENV.get(test)
        if requested == "all" and required_env and not os.environ.get(required_env):
            print(
                f"[punch] SKIP {test}: {required_env} not set "
                f"(external-target test; run it directly with {required_env} set)",
                flush=True,
            )
            results.append({
                "test": test,
                "skipped": True,
                "reason": f"{required_env} not set",
                "passed": True,
            })
            continue
        rc = _run_one(test)
        results.append({"test": test, "exitCode": rc, "passed": rc == 0})
        if rc != 0:
            overall_rc = rc
            if not args.keep_going:
                break

    if args.collect_logs:
        _collect_service_logs()

    _write_evidence({
        "command": "run",
        "tests": sequence,
        "results": results,
        "exitCode": overall_rc,
        "passed": overall_rc == 0,
        "startedAt": started,
        "durationSeconds": round(time.monotonic() - t0, 2),
    })
    return overall_rc


def cmd_clean(_args: argparse.Namespace) -> int:
    return _stream(["docker", "compose", "down", "--volumes", "--remove-orphans"])


def cmd_init(args: argparse.Namespace) -> int:
    # Lazy import: the scanner is only needed for this command and keeps the
    # hot path (doctor/run/clean) free of the extra module.
    from punch import init_scan
    return init_scan.run(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="punch",
        description="Local orchestrator for the k6-ts-docker performance gate.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check host prerequisites (docker, compose, python).")

    run_p = sub.add_parser("run", help="Run a k6 test (or all) via docker compose.")
    run_p.add_argument("test", choices=[*TESTS.keys(), "all"], help="Which test to run.")
    run_p.add_argument("--keep-going", action="store_true",
                       help="With 'all', continue subsequent tests after a failure.")
    run_p.add_argument("--collect-logs", action="store_true",
                       help="After the run, dump service logs to reports/logs/.")

    sub.add_parser("clean", help="Tear down compose stack and volumes.")

    init_p = sub.add_parser(
        "init",
        help="First-wave bootstrap scan: map Copilot assets + docs readiness for Punch adoption.",
    )
    init_p.add_argument("--dry-run", action="store_true",
                        help="Compute and print the scan; write nothing (default behavior).")
    init_p.add_argument("--write", action="store_true",
                        help="Persist the generated bootstrap artifacts to the output dir.")
    init_p.add_argument("--with-graphify", action="store_true",
                        help="Explicit opt-in marker for the lightweight Graphify "
                             "availability check. Init always records Graphify "
                             "file-readiness and never shells out to the CLI "
                             "(dependency-free); this flag only annotates that the "
                             "check was requested. Never required.")
    init_p.add_argument("--output", metavar="DIR", default=None,
                        help="Output dir for generated artifacts (default: docs/ai/governance/init).")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    dispatch = {
        "doctor": cmd_doctor,
        "run": cmd_run,
        "clean": cmd_clean,
        "init": cmd_init,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
