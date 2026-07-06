#!/usr/bin/env python3
"""Validate committed Graphify shared artifacts.

This guard is intentionally stdlib-only and read-only. It enforces ADR 0002:
only the canonical root shared artifacts may be committed, and those artifacts
must not contain local paths, interpreter paths, hostnames, or raw cost keys.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

ALLOWED_TRACKED = {
    "graphify-out/graph.json",
    "graphify-out/GRAPH_REPORT.md",
}

LEAK_PATTERNS = (
    ("absolute path", re.compile(r"/(Users|home)/[^/]+/")),
    (
        "venv/interpreter path",
        re.compile(r"(\.venv|\.pyenv|\.local/lib|site-packages|python3\.[0-9]+)"),
    ),
    ("hostname/machine string", re.compile(r"(MacBook|\.local$)", re.MULTILINE)),
)
RAW_COST_KEYS = re.compile(r"input_tokens|output_tokens|total_cost")


def display_path(path: Path, repo: Path = REPO) -> str:
    try:
        return path.relative_to(repo).as_posix()
    except ValueError:
        return path.as_posix()


def tracked_files(repo: Path) -> list[str]:
    """Return git-tracked files as POSIX paths relative to repo root."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=repo,
            capture_output=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot list git-tracked files: {exc}") from exc
    return [p for p in out.stdout.decode("utf-8").split("\0") if p]


def graphify_path_violations(paths: list[str]) -> list[str]:
    """Find tracked rogue Graphify output paths.

    The only allowed tracked output files are:
    - graphify-out/graph.json
    - graphify-out/GRAPH_REPORT.md

    Any other tracked file under a graphify-out directory, plus directories that
    look like renamed Graphify output folders such as graphify-out-copy/, fails.
    """
    bad = []
    for rel in paths:
        parts = rel.split("/")
        dirs = parts[:-1]
        in_graphify_out = "graphify-out" in parts
        in_renamed_output = any(
            part.startswith("graphify-out-") or part.startswith("graphify-out_")
            for part in dirs
        )
        if (in_graphify_out or in_renamed_output) and rel not in ALLOWED_TRACKED:
            bad.append(rel)
    return sorted(bad)


def check_text_patterns(path: Path, text: str, repo: Path = REPO) -> list[str]:
    errors = []
    for label, pattern in LEAK_PATTERNS:
        if pattern.search(text):
            errors.append(f"{display_path(path, repo)}: contains {label}")
    if RAW_COST_KEYS.search(text):
        errors.append(f"{display_path(path, repo)}: contains raw cost/token key")
    return errors


def check_graph_json(path: Path, repo: Path = REPO) -> list[str]:
    errors = []
    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        return [f"{display_path(path, repo)}: invalid JSON: {exc}"]

    bad_ids = [
        node.get("id")
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str) and node["id"].startswith("/")
    ]
    if bad_ids:
        sample = ", ".join(bad_ids[:5])
        suffix = "" if len(bad_ids) <= 5 else f" (+{len(bad_ids) - 5} more)"
        errors.append(f"{display_path(path, repo)}: absolute node IDs: {sample}{suffix}")
    return errors


def validate(repo: Path) -> list[str]:
    errors = []

    bad_paths = graphify_path_violations(tracked_files(repo))
    errors.extend(f"tracked rogue Graphify output: {path}" for path in bad_paths)

    for rel in sorted(ALLOWED_TRACKED):
        path = repo / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(check_text_patterns(path, text, repo))

    errors.extend(check_graph_json(repo / "graphify-out/graph.json", repo))
    return errors


def main(argv=None) -> int:
    repo = Path(argv[0]).resolve() if argv else REPO
    errors = validate(repo)
    if errors:
        print("Graphify share validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print("Graphify share validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
