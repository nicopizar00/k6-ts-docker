# Spec — Adopt Adapt: adopt `caveman` + `cavecrew` (increment)

> Increment on approved Spec [`adopt-adapt.md`](adopt-adapt.md). Adds the second
> and third adopted skills, validating that the index is generic beyond graphify.
> Pattern source: `.github/prompts/punch-spec.prompt.md` (Caveman `lite`).

**Status:** Spec — awaiting approval. Plan = next phase.

## Problem (clarify)

Adopt Adapt's index was built and proven against **one** skill (graphify). The
"generic enough for other skills" claim is untested. `caveman` and `cavecrew`
(vendor skills from `github.com/JuliusBrussee/caveman`, already snapshotted in
`.ai-upstream/` and listed in `.github/.ai-upstream/README.md`) are the natural
next adoptions — and they deliberately **break graphify's assumptions**, so
adopting them is the real genericity test:

| Trait | graphify | caveman | cavecrew |
|---|---|---|---|
| Distribution | PyPI `graphifyy` | `npx github:JuliusBrussee/caveman` | `npx skills add … --skill cavecrew` |
| Version probe | `graphify --version` CLI | **no CLI** — marker `.caveman_version` (0.1.0) | **no CLI** — tied to caveman 0.1.0 |
| Adaptation kind | leaned-fork | **authored style-adapter** | **verbatim vendor** |
| Adaptation shape | one dir tree | one dir (`punch-build-caveman/`) | **file-set** (3 agent files) |
| Install safety | plain install | official `--with-init` **unsafe** (documented) | same unsafe path |

If the lock + descriptor schema absorbs all three without contortion, the design
holds. Where it cannot, this Spec names the minimal extension.

- **Goal** — Add `caveman` and `cavecrew` as adopted entries (one descriptor +
  one lock entry each) in the existing `ai.ingest/` index, extending the schema
  only as far as those two skills' real shape requires, with no mutation of the
  skills, the snapshots, or `.github/`.

- **Non-goals** — this increment will NOT:
  - Run the upstream official installer (`install.sh --with-init` /
    `npx … skills add`). Both UPSTREAM.md files document it as **unsafe** (global
    install, appends to `.github/copilot-instructions.md`, writes parallel
    `.cursor`/`.windsurf`/… rule files). Adopt Adapt records the safe
    snapshot-based adoption; it does not re-run the unsafe path.
  - Re-implement, fork, or edit `caveman`/`cavecrew` or their Punch adaptations
    (`punch-build-caveman/`, `punch-cavecrew-*.agent.md`).
  - Build the `adopt --write` / hash-population tooling (still future).
  - Generalize into a plugin registry. Three hardcoded adapters is the evidence
    that the shape is reusable — not yet a framework.
  - Fix the two pre-existing discrepancies found during clarify (see Risks) —
    they are flagged for a separate governance task, not repaired here.

- **Functional requirements** — observable shape:
  - `ai.ingest/adapters/caveman.json` + `ai.ingest/adapters/cavecrew.json`
    (schema-faithful descriptors), and matching `caveman` / `cavecrew` entries in
    `ai.ingest/adopt.lock.json`.
  - **Schema extension — version source.** Descriptor `identity.version_kind`
    gains non-CLI values (`github`, `vendored`). When there is no version CLI,
    `verify.version_probe` is `null` and version is read from
    `verify.version_marker_file` (e.g. `.caveman_version`) or pinned only. The
    version axis must degrade to a marker/manifest comparison, never crash on the
    missing CLI.
  - **Schema extension — adaptation shape.** `adaptation` accepts either a single
    `path` (dir, as today: caveman → `.github/skills/punch-build-caveman/`) **or**
    an explicit `paths` file-set (cavecrew → the three
    `.github/agents/punch-cavecrew-*.agent.md`). `asset_hashes` keys are relative
    to a stated base.
  - **Schema — kind vocabulary.** `kind` covers `leaned-fork` (graphify),
    `authored-adapter` (caveman — reuses *style* only, scoped to Build), and
    `verbatim` (cavecrew — vendor kept as-is; adaptation is the bounding worker
    agents, not a skill fork).
  - **Install / safety fields.** Descriptor records the real `install` method
    (npx) **and** an `install_unsafe` note pointing at the documented reason the
    official installer is not used.
  - **Vendor install location.** cavecrew's installed canon is
    `.agents/skills/cavecrew/`; the descriptor records it as the vendor root.
    Absent install → `missing-baseline` (same degrade as graphify's gitignored
    snapshot).
  - Hash slots seeded `null` (populated later by `adopt`, never hand-typed).
  - The two new entries coexist with `graphify` under one `skills` map; `compare`
    can target any by name.

- **Technical constraints** —
  - **Strict JSON**, **stdlib-only**, **read-only by default** — unchanged from
    base Spec.
  - **Reuse, not fork**; preserve upstream identity + version verbatim
    (`.caveman_version` 0.1.0; cavecrew version-matched to caveman).
  - `.ai-upstream/**` stays **frozen provenance** — read, never written.
  - **Do not duplicate** `.github/.ai-upstream/README.md`. That human manifest and
    the Adopt Adapt lock describe the same vendor skills; the Spec must state their
    relationship (lock = machine index; README = prose manifest) — not fork it.
  - Schema change is **additive/optional**: existing `graphify` entry stays valid.
    If the adaptation-shape change is not cleanly additive, bump `schema_version`
    to 2 and state the migration (graphify re-expressed under v2).
  - **Off the execution chain / Docker-First intact.**

- **Affected layers** ([punch-boundaries.md](../punch-boundaries.md)) — extends the
  host-tooling `ai.ingest/` set only. Reads `.ai-upstream/{caveman,cavecrew}/`,
  `.github/skills/punch-build-caveman/`, `.github/agents/punch-cavecrew-*.agent.md`,
  `.agents/skills/cavecrew/` — **writes none of them**. Governance
  (`punch-ai-governance`) owns the `.github/` canon these entries point at.

- **Artifact / log / reporting implications** —
  - New tracked files: two descriptors + two lock entries under `ai.ingest/`.
    Not Punch run evidence; `reports/` unaffected.
  - No terminal-noise change.
  - `.gitignore` unchanged by this increment. (Note the `.agents/` discrepancy
    under Risks — not changed here.)

- **Acceptance criteria** — what Test asserts:
  1. `ai.ingest/adapters/caveman.json` + `cavecrew.json` parse as strict JSON.
  2. `adopt.lock.json` parses and now has `graphify`, `caveman`, `cavecrew`
     entries; the existing `graphify` entry is byte-unchanged (or, if
     `schema_version` bumped to 2, re-expressed and re-validated).
  3. caveman: `version_kind=github`, `version_probe=null`,
     `version_marker_file=.caveman_version`, pinned `0.1.0`, `kind=authored-adapter`,
     adaptation `path=.github/skills/punch-build-caveman/`.
  4. cavecrew: `kind=verbatim`, adaptation expressed as a **file-set** of the three
     `.github/agents/punch-cavecrew-*.agent.md`, vendor root `.agents/skills/cavecrew/`.
  5. Every descriptor path resolves to a real repo location (snapshot roots,
     adaptation roots/files, vendor root).
  6. All hash slots `null`.
  7. Each descriptor records the npx `install` method and an `install_unsafe` note
     referencing the documented reason the official installer is skipped.
  8. `git status` shows only new/edited `ai.ingest/` files (+ this spec doc).
  9. If `compare` is run against `caveman`/`cavecrew` in this increment's scope, it
     does not crash on the absent version CLI — version axis reports a
     marker/pinned verdict or `not-installed`, asset axes report
     `baseline-not-recorded`/`missing-baseline`.

## Risks / pre-existing findings (flagged, not fixed here)

- **Dangling ADR.** `.ai-upstream/caveman/UPSTREAM.md` cites
  `docs/ai/decisions/0003-caveman-build-comms.md` — **the file does not exist**.
  caveman's descriptor `governance.adr` would point at a missing ADR. Flag for a
  governance task (write ADR 0003 or correct the reference).
- **`.agents/` not gitignored.** `.github/.ai-upstream/README.md` says installed
  vendor folders are gitignored, but `git check-ignore .agents/` reports it is
  **not** ignored — the vendor skills may be committed. Governance discrepancy;
  out of scope here, flagged for follow-up.
- **`compare` does not yet handle no-CLI version or file-set adaptation.** AC9
  bounds the minimum (no crash); full marker/file-set support is a likely
  follow-up `compare` increment, mirroring how graphify's `compare` was staged.

**Gate:** approved when Goal, Non-goals, Acceptance criteria agreed → Plan
decomposes the descriptor + lock-entry tasks (and any `compare` extension).
