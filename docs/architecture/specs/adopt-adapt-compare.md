# Spec — Adopt Adapt `compare` command (increment)

> Increment on approved Spec [`adopt-adapt.md`](adopt-adapt.md). Unblocks task
> **A-02** in [`plan-adopt-adapt.md`](plan-adopt-adapt.md).
> Pattern source: `.github/prompts/punch-spec.prompt.md` (Caveman `lite`).

**Status:** Spec — awaiting approval. Re-plan A-02 = next phase.

## Problem

Base Spec delivered the data model (`ai.ingest/` lock + descriptor) but listed the
CLI as a non-goal. That data model is inert without a consumer: nothing yet *reads*
it to tell whether the pinned graphify (0.8.41) has drifted from what's installed,
or whether the leaned canon still tracks the pristine snapshot. This increment adds
the **first and only** executable: a read-only `compare` that turns the lock +
descriptor into a drift report. Strictly report-only — no writes, no auto-apply.

- **Goal** — A stdlib-Python read-only `compare` command that loads
  `ai.ingest/adopt.lock.json` + the named adapter, probes/hashes the live skill
  assets, and prints a three-axis drift report (version / upstream-asset /
  adaptation) without mutating any file.

- **Non-goals** — this increment will NOT:
  - Write or mutate anything — not the lock, not hash slots, not `.github/`, not
    `.ai-upstream/`, not `graphify-out/`. (Populating hash slots is a separate
    future `adopt --write` task, out of scope.)
  - Auto-apply, auto-merge, or propose file edits. It reports; it does not change.
  - Add `verify` / `status` / `adopt` / `adapt` — each is its own later increment.
  - Introduce a generic multi-skill abstraction or plugin loader; graphify is the
    only adapter consumed.
  - Add any pip dependency or touch the Docker execution chain.

- **Functional requirements** — observable behavior:
  - Entry: a stdlib Python module under `ai.ingest/`, invoked
    `python3 ai.ingest/compare.py [skill]` (default skill = the lone lock entry,
    `graphify`). Exact module layout finalized in Plan.
  - Loads `ai.ingest/adopt.lock.json` and the adapter named by the skill's
    `adapter` field; fails with a clear message (not a stack trace) if either is
    missing or unparseable.
  - **Axis 1 — version drift:** compares lock `adopted_version.package_version`
    (0.8.41) to a live probe (`graphify --version` per descriptor `verify`). If
    graphify is not installed, reports `not-installed` — does not crash.
  - **Axis 2 — upstream-asset drift:** hashes the live files under the descriptor
    `assets.upstream_snapshot_root` (per `track_globs`) and compares to lock
    `upstream_snapshot.asset_hashes`. Per-asset verdict:
    `unchanged | changed | added | removed`.
  - **Axis 3 — adaptation drift:** same against `assets.adaptation_root` vs lock
    `adaptation.asset_hashes`.
  - **Degrade paths (no false drift):**
    - Lock baseline hash = `null` (current seed state) → that asset reports
      `baseline-not-recorded`, not `changed`.
    - `upstream_snapshot_root` absent (gitignored, fresh clone) → axis 2 reports
      `missing-baseline`, not error.
  - **Intentional divergence suppressed:** files in descriptor
    `adaptation.expected_absent_references` are never reported as drift when absent
    from the adaptation tree.
  - `graphify-out/` (descriptor `outputs.exclude_from_drift`) is never hashed.
  - Output: a human-readable report with the three axes clearly separated; ends
    with a one-line summary (`clean` / `drift detected: <axes>` /
    `baseline incomplete`). No proposed edits.

- **Technical constraints** —
  - **stdlib-only** (`hashlib`, `json`, `pathlib`, `subprocess`, `argparse`, `sys`)
    — no pip deps (Critical Rule #3; matches `src/punch/`).
  - **Read-only:** zero filesystem writes; `git status` is identical before/after a
    run. No network beyond the optional local `graphify --version` probe.
  - **Reuse, not fork:** version probe + asset roots + exclusions come from the
    descriptor — no hardcoded graphify knowledge in the command logic.
  - **Off the execution chain / Docker-First intact:** host authoring tool, not a
    `bin/punch` runtime command, not Dockerized. Owns only `ai.ingest/`.
  - Hashing is sha256 (matches the `sha256:` convention reserved in the lock).

- **Affected layers** ([punch-boundaries.md](../punch-boundaries.md)) — adds the
  **first executable** to the host-tooling `ai.ingest/` set. Reads (never writes)
  `.ai-upstream/graphify/` and `.github/skills/punch-graphify/`. Owns only
  `ai.ingest/`; touches no orchestrator/compose/k6/data layer and nothing in the
  execution chain.

- **Artifact / log / reporting implications** —
  - New tracked source under `ai.ingest/` (e.g. `compare.py`). Not Punch run
    evidence — `reports/state/punch-run.json` unaffected; no `reports/` schema
    change.
  - Report goes to **stdout** by default. Persisting it under `ai.ingest/reports/`
    is deferred (a `--out` flag is a later increment), so no new tracked report
    artifact in this increment.
  - `.gitignore` unchanged.

- **Acceptance criteria** — what Test asserts:
  1. `python3 ai.ingest/compare.py graphify` exits cleanly and `git status` is
     **byte-identical** before/after (read-only proven).
  2. Output labels all three axes separately and ends with a one-line summary.
  3. Axis 1 compares pinned `0.8.41` to the live probe; with graphify absent it
     prints `not-installed`, exit non-crash.
  4. With the current seed (all hash slots `null`), axes 2 & 3 report
     `baseline-not-recorded` — **not** `changed` (no false drift).
  5. With `.ai-upstream/graphify/` absent, axis 2 reports `missing-baseline`, no
     crash.
  6. `expected_absent_references` (`exports.md`, `github-and-merge.md`,
     `transcribe.md`) are never reported as adaptation drift.
  7. `graphify-out/` is never hashed (verified by code path / no access).
  8. No pip import; `python3 -c "import ast; ast.parse(open('ai.ingest/compare.py').read())"`
     and a stdlib-only import audit pass.

**Gate:** approved when Goal, Non-goals, Acceptance criteria agreed → re-plan A-02
(`punch-plan`) as buildable, then Build.
