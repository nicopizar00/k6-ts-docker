# Upstream provenance — graphify

This directory is a **pristine, do-not-edit snapshot** of the upstream Graphify
Agent Skill, kept for drift detection. Punch reuses the *installed* skill; this
copy is the reference we diff against when upstream changes.

| Field | Value |
|---|---|
| Upstream project | https://github.com/safishamsi/graphify |
| Distribution | PyPI package `graphifyy` (host CLI: `graphify`, `graphify-mcp`) |
| Snapshot version | **0.8.41** (see `.graphify_version`) |
| Snapshot date | 2026-06-18 |
| Install (host) | `uv tool install graphifyy` |
| Skill entrypoint | `SKILL.md` (invoked as `/graphify`) + `references/` (lazy-loaded) |
| Purpose in Punch | documentation-cartography **evidence** for the `/punch-documentate` reconciliation phase — see [ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md) |

## Rules

- **Do not edit these files.** They are upstream verbatim. Punch's adaptation
  lives in `.github/` (the `punch-ai-governance` agent's Documentation mode and
  the `punch-documentate` prompt), never here.
- `.ai-upstream/**` is **frozen provenance**: `punch-ai-governance` excludes it
  from cross-reference, naming, duplication, and stale-asset checks.
- **Reuse, don't fork.** Punch consumes Graphify's native outputs
  (`graphify-out/graph.json`, `GRAPH_REPORT.md`) and read-side commands
  (`query` / `path` / `explain` / `affected`). It does not re-implement
  extraction or indexing.

## Updating

1. `uv tool install --upgrade graphifyy` and compare its `.graphify_version`
   against this snapshot's.
2. Re-copy the installed skill into a scratch dir and `git diff` against this
   directory to see exactly what changed in `SKILL.md` / `references/`.
3. If a changed command or flag affects Punch's adaptation, open a governance
   issue — do **not** silently apply. Only `punch-ai-governance` commits the bump
   after review.
