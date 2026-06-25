#!/usr/bin/env python3
"""Adopt Adapt — read-only `compare`.

Loads ai.ingest/adopt.lock.json + the named adapter, probes/hashes the live
skill assets, and prints a three-axis drift report:

  1. version      — pinned package_version vs live CLI probe
  2. upstream      — live snapshot files vs lock upstream_snapshot.asset_hashes
  3. adaptation    — live adapted files vs lock adaptation.asset_hashes

Strictly read-only: it writes nothing, mutates nothing, proposes no edits.
stdlib-only (Critical Rule #3). Off the Docker execution chain — host tooling.

Spec: docs/architecture/specs/adopt-adapt-compare.md
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # ai.ingest/
REPO = HERE.parent                               # repo root
LOCK = HERE / "adopt.lock.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return "sha256:" + h.hexdigest()


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: {path} not found")
    except json.JSONDecodeError as e:
        sys.exit(f"error: {path} is not valid JSON: {e}")


def live_assets(root: Path, track_globs, exclude_root: Path, skip_names=()):
    """Map relative-path -> sha256 for files under root matching track_globs.

    `exclude_root` (the generated outputs dir, e.g. graphify-out/) is never
    hashed even if it sits under root. `skip_names` (e.g. the version-marker
    file, compared once in axis 1) are excluded from the content asset axes.
    """
    found = {}
    for pattern in track_globs:
        for p in sorted(root.glob(pattern)):
            if not p.is_file():
                continue
            rel = p.relative_to(root).as_posix()
            if rel in skip_names:
                continue  # version marker — axis 1's concern, not a content asset
            try:
                p.relative_to(exclude_root)
                continue  # inside the excluded outputs dir — skip
            except ValueError:
                pass
            found[rel] = sha256_file(p)
    return found


def diff_axis(recorded: dict, live: dict, suppress_absent=(), skip_names=()):
    """Per-asset verdicts comparing recorded baseline hashes to live hashes.

    recorded value None  -> baseline-not-recorded (no false drift)
    recorded == live     -> unchanged
    recorded != live     -> changed
    in recorded only     -> removed (suppressed if in `suppress_absent`)
    in live only         -> added

    `skip_names` (e.g. the version marker) are dropped from both sides so the
    marker is never double-counted against axis 1.
    """
    recorded = {k: v for k, v in recorded.items() if k not in skip_names}
    live = {k: v for k, v in live.items() if k not in skip_names}
    rows = []
    for name in sorted(set(recorded) | set(live)):
        rec, liv = recorded.get(name, "__absent__"), live.get(name)
        if rec == "__absent__":
            rows.append((name, "added"))
        elif liv is None:
            if name in suppress_absent:
                rows.append((name, "intentional-absent"))
            else:
                rows.append((name, "removed"))
        elif rec is None:
            rows.append((name, "baseline-not-recorded"))
        elif rec == liv:
            rows.append((name, "unchanged"))
        else:
            rows.append((name, "changed"))
    return rows


def probe_version(version_probe):
    # version_probe is a command *list* read from the (repo-controlled, trusted)
    # adapter descriptor — no shell=True, so no shell injection.
    try:
        out = subprocess.run(
            version_probe, capture_output=True, text=True, timeout=15
        )
    except (FileNotFoundError, OSError):
        return None  # not installed
    if out.returncode != 0:
        return None  # present but errored — treat as unusable, not a version
    blob = (out.stdout + " " + out.stderr).strip()
    m = re.search(r"\d+\.\d+\.\d+", blob)
    return m.group(0) if m else (blob or None)


def axis_version(skill, desc):
    pinned = skill["adopted_version"]["package_version"]
    probe = desc.get("verify", {}).get("version_probe")
    live = probe_version(probe) if probe else None
    if live is None:
        return ("not-installed", pinned, None)
    return ("match" if live == pinned else "version-drift", pinned, live)


def render_asset_rows(rows):
    if not rows:
        return ["    (no assets)"]
    width = max(len(n) for n, _ in rows)
    return [f"    {n.ljust(width)}  {verdict}" for n, verdict in rows]


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="compare", description="Adopt Adapt read-only drift report."
    )
    ap.add_argument("skill", nargs="?", help="skill name (default: lone lock entry)")
    args = ap.parse_args(argv)

    lock = load_json(LOCK)
    skills = lock.get("skills", {})
    if not skills:
        sys.exit("error: no skills recorded in adopt.lock.json")

    name = args.skill
    if name is None:
        if len(skills) == 1:
            name = next(iter(skills))
        else:
            sys.exit(f"error: multiple skills; name one of: {', '.join(skills)}")
    if name not in skills:
        sys.exit(f"error: skill '{name}' not in lock (have: {', '.join(skills)})")

    skill = skills[name]
    desc = load_json(HERE / skill["adapter"])

    out = [f"Adopt Adapt — compare: {name}", "=" * 40]

    # graphify-out/ (outputs.root) is never hashed.
    outputs_root = (REPO / desc.get("outputs", {}).get("root", "graphify-out/")).resolve()
    track = desc.get("assets", {}).get("track_globs", [])
    # version marker is compared once (axis 1) — keep it out of the content axes.
    marker = desc.get("verify", {}).get("version_marker_file")
    skip = {marker} if marker else set()
    suppress = {
        "references/" + f
        for f in desc.get("adaptation", {}).get("expected_absent_references", [])
    }

    drift_flags = []

    # Axis 1 — version
    verdict, pinned, live = axis_version(skill, desc)
    out += ["", "[1] version drift", f"    pinned : {pinned}",
            f"    live   : {live if live else '(graphify not installed)'}",
            f"    verdict: {verdict}"]
    if verdict == "version-drift":
        drift_flags.append("version")

    # Axis 2 — upstream-asset
    out += ["", "[2] upstream-asset drift"]
    up_root = (REPO / skill["upstream_snapshot"]["path"]).resolve()
    if not up_root.exists():
        out.append("    missing-baseline (snapshot absent — re-adopt)")
    else:
        rows = diff_axis(
            skill["upstream_snapshot"]["asset_hashes"],
            live_assets(up_root, track, outputs_root, skip),
            skip_names=skip,
        )
        out += render_asset_rows(rows)
        if any(v in ("changed", "added", "removed") for _, v in rows):
            drift_flags.append("upstream")

    # Axis 3 — adaptation
    out += ["", "[3] adaptation drift"]
    ad_root = (REPO / skill["adaptation"]["path"]).resolve()
    if not ad_root.exists():
        out.append("    missing-baseline (adaptation absent)")
    else:
        rows = diff_axis(
            skill["adaptation"]["asset_hashes"],
            live_assets(ad_root, track, outputs_root, skip),
            suppress_absent=suppress,
            skip_names=skip,
        )
        out += render_asset_rows(rows)
        if any(v in ("changed", "added", "removed") for _, v in rows):
            drift_flags.append("adaptation")

    # Summary
    null_baseline = any(
        v is None
        for axis in ("upstream_snapshot", "adaptation")
        for v in skill[axis]["asset_hashes"].values()
    )
    out += ["", "-" * 40]
    if drift_flags:
        summary = "drift detected: " + ", ".join(drift_flags)
    elif null_baseline:
        summary = "baseline incomplete (hash slots not recorded — run adopt)"
    else:
        summary = "clean"
    out.append("summary: " + summary)

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
