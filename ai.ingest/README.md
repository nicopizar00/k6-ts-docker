# `ai.ingest/` — Adopt Adapt index + adapter descriptors

Local, auditable record of external Agent Skills / tool-backed skills this repo has **adopted** and
**adapted**. Host tooling that *operates on* `.github/` and `.ai-upstream/` — it is **not** a GitHub
Copilot asset and does not belong inside `.github/` (which stays Copilot-canon single source of truth).

**Default behavior is report-only.** Nothing here mutates a skill. Fetching, inspecting, and drift
comparison are read-only; any change to an adapted skill is a separate, explicitly-flagged step gated on
governance review (see [ADR 0002](../docs/ai/decisions/0002-graphify-host-tool.md)).

MVP scope = **graphify only**. Punch integration, VS Code Copilot wiring, a generic adapter registry, and
auto-apply are deferred.

## Three artifact categories (kept strictly separate)

| Category | Meaning | Tracked? | graphify example |
|---|---|---|---|
| **upstream** | pristine, do-not-edit snapshot | gitignored snapshot; identity tracked here | `.ai-upstream/graphify/` |
| **adapted** | this repo's authored (leaned) version | tracked canon | `.github/skills/punch-graphify/` |
| **generated / cache** | tool runtime output | gitignored, never hashed for drift | `graphify-out/` |

## Files

- `adopt.lock.json` — the **lock / index**. One entry per adopted skill: pinned version, upstream snapshot
  path + per-asset hashes, adaptation path + per-asset hashes. Hashes are `null` until populated by the
  `adopt` command (future) — never hand-typed; `compare` reads them.
- `adapters/<skill>.json` — the **adapter descriptor**. Skill-specific, declarative knowledge the generic
  core consumes: install method, version probe, which paths are upstream vs adapted vs generated/cache, and
  which divergences from upstream are *intentional* (so they are not reported as drift).
- `compare.py` — the read-only drift reporter (stdlib only). See **Using `compare`** below.
- `tests/test_compare.py` — stdlib `unittest` regression suite for `compare.py`.

Both are **strict JSON** (no comments) so any stdlib `json.load` consumer works with zero special-casing.
Field meanings are documented here rather than inline.

### Lock field reference (`adopt.lock.json`)

- `schema_version` — lock format version.
- `skills.<name>.adapter` — path (relative to this dir) to the skill's descriptor.
- `adopted_version` — `package_version` / `commit` / `tag` of what was adopted, plus `install_method` and
  `adopted_at`. For PyPI-only skills (graphify), `commit` and `tag` are `null` by design.
- `upstream_snapshot` — `path` to the pristine baseline, `present` (false on a fresh clone, since
  `.ai-upstream/` is gitignored → compare reports "missing baseline, re-adopt" instead of false drift), and
  `asset_hashes` (sha256 per pristine file, enumerated so removed/added upstream files are also detectable).
- `adaptation` — `path` to the adapted canon, `kind` (`verbatim` / `leaned-fork` / `wrapper`), and
  `asset_hashes` of the adapted files.
- `last_compared_at` — timestamp of the last drift comparison.

### Descriptor field reference (`adapters/<skill>.json`)

- `identity` — upstream repo, distribution, CLI names, entrypoint, `version_kind`.
- `install` / `verify` — recommended install commands and usability probes (import check, version probe,
  version-marker file).
- `assets` — snapshot root, adaptation root, and `track_globs` (which files count as the skill's content).
- `outputs` — generated `root`, which outputs are `evidence` vs `cache`, and `exclude_from_drift` (the
  output dir churns every run and must never be hashed).
- `adaptation` — `kind`, `removed_upstream_features`, and `expected_absent_references` (upstream files the
  lean intentionally drops, so their absence is suppressed as a false positive during compare).
- `governance` — linked ADR and whether applying an adaptation requires review.

## Drift, in brief

Comparison reports three independent axes, never collapsed into one yes/no:

1. **Version drift** — pinned `package_version` vs a freshly-installed/queried version.
2. **Upstream asset drift** — re-fetched upstream files vs `upstream_snapshot.asset_hashes`.
3. **Adaptation drift** — current adapted files vs `adaptation.asset_hashes`.

A report ends with a *proposed* adaptation plan — it does **not** auto-apply anything.

## Using `compare`

Read-only drift report for one adopted skill. Writes nothing, mutates nothing.

```sh
python3 ai.ingest/compare.py            # default: the lone lock entry (graphify)
python3 ai.ingest/compare.py graphify   # name a skill explicitly
```

Prints the three axes above, each with a per-asset verdict, then a one-line summary.

**Per-asset verdicts**

| Verdict | Meaning |
|---|---|
| `unchanged` | live hash matches the recorded baseline |
| `changed` | live hash differs from the baseline |
| `added` | live file present, no baseline entry |
| `removed` | baseline entry present, live file gone |
| `intentional-absent` | absent **and** listed in `expected_absent_references` — suppressed, not drift |
| `baseline-not-recorded` | baseline hash is `null` (seed state) — run `adopt` to populate |

**Degrade paths (no false drift)**

- Lock hash slot `null` → `baseline-not-recorded` (not `changed`).
- Snapshot/adaptation root absent (e.g. gitignored `.ai-upstream/` on a fresh clone) → `missing-baseline`.
- Skill not installed → version axis reports `not-installed`.

**Summary line** — `clean` · `drift detected: <axes>` · `baseline incomplete (…)`.

**Notes**

- The version-marker file (`verify.version_marker_file`, e.g. `.graphify_version`) is compared once in the
  version axis — never double-counted as a content asset.
- `outputs.root` (`graphify-out/`) is never hashed (`exclude_from_drift`).
- Exit code is `0` on a successful report (drift is reported in output, not via exit code); non-zero only on
  a usage/load error (missing or invalid lock/descriptor).
- Until `adopt` populates baseline hashes, only the **version axis** does a live comparison; the asset axes
  report `baseline-not-recorded`.

Run the regression suite with: `python3 -m unittest discover -s ai.ingest/tests`.
