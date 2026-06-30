# ADR 0002 — graphify as a scoped host-tool for documentation mapping

**Status:** Accepted (2026-06-18)
**Deciders:** repository owner + Punch AI Governance work

## Context

Punch Rule #1 = **Docker First**: host need only Docker + stdlib Python 3 runtime. One prior exception: [ADR 0001](0001-perf-engineer-host-npm.md) (host `npm` for perf-test engineer).

Want way to manage **documentation debt** — duplicated, stale, partial, orphaned docs across `docs/`, `docs/ai/`, `.github/`, `README.md`, `AGENTS.md`. [Graphify](https://github.com/safishamsi/graphify) (PyPI `graphifyy`, host CLI `graphify`) maps corpus into knowledge graph with community detection + `query` / `path` / `explain` / `affected` traversal — useful **evidence** for spotting drift. Host CLI installed via `uv tool install graphifyy`; **not** Dockerized, not part of source → bundle → image → run → report chain.

Pristine upstream snapshot (v0.8.41) may live in `.ai-upstream/graphify/` with provenance in its `UPSTREAM.md`. Note: `.ai-upstream/` = **gitignored local staging area** (see `.ai-upstream/.gitkeep`), not version-controlled — canonical Punch adaptation lives in `.github/` (`punch-document` prompt + `punch-ai-governance` Documentation mode). Snapshot = local drift baseline; re-fetch (`uv tool install graphifyy`, re-copy installed skill) when absent.

**Leaned for Copilot plug-in (2026-06-18).** In-repo `.github/skills/punch-graphify/` skill trimmed to Punch **in-IDE subset** (build / `--update` / `--cluster-only` / query / path / explain / add+watch / hooks). Removed: remote-repo clone & cross-repo merge, media transcription (Whisper), external-DB push (Neo4j/FalkorDB, incl. credential examples), MCP server, wiki/SVG/GraphML/obsidian exports — none used by Punch. Skill therefore **authored Punch-leaned adaptation** (subject to governance checks), not verbatim upstream copy; pristine upstream stays drift baseline in `.ai-upstream/graphify/`.

## Decision

Graphify adopted as **scoped host-tool exception** to Docker First, used **only** by documentation-reconciliation workflow. Exception, not repeal:

- **Reuse, don't fork.** Punch invokes existing `/graphify` skill, consumes its **native outputs** (`graphify-out/graph.json`, `GRAPH_REPORT.md`). No custom AST/indexing skill created.
- **One governed workflow.** `/punch-document` prompt drives existing [`punch-ai-governance`](../../../.github/agents/punch-ai-governance.agent.md) agent, which reconciles docs in **waves** (keep / merge / rewrite / archive / delete / promote). Graphify gives map; `punch-ai-governance` makes every decision.
- **VS Code-native delegation.** Agent forks `/graphify` as **single subagent** for structural map, relying on VS Code subagent **tool inheritance**, kept **1-deep** (`chat.subagents.allowInvocationsFromSubagents` stays default — subagents cannot spawn subagents). For this, agent gains `runSubagent` + scoped run-tool surface. *(Implemented with `punch-document` workflow; see that prompt + agent Documentation mode.)*
- **Guard reworded, not removed.** `punch-ai-governance` still **never runs Punch Docker/k6 runtime or `bin/punch` suite**. Only command surface = forking `/graphify` map subagent.
- **Outputs evidence, not canonical.** Everything under `graphify-out/` = audit **evidence** — never canonical docs. `CLAUDE.md`, `docs/`, registries stay authoritative; nothing promoted to canonical without governance decision. `graph.json` and `GRAPH_REPORT.md` may be committed as shared team artifacts after passing the leakage validation checklist (see **Team Sharing** below); all other `graphify-out/` contents remain gitignored.
- **No other surface.** No other agent, command, contributor workflow gains host-graphify dependence; execution chain unchanged.

## Consequences

- **Positive:** documentation debt gets lean, wave-based reconciliation phase backed by graph evidence — **no new skill, no new agent** (logic folds into existing `punch-ai-governance` agent + one prompt).
- **Negative / watch:** contributor running `/punch-document` locally need graphify host-installed (`uv tool install graphifyy`). Acceptable: opt-in, off evidence/execution path, doesn't touch Docker-First *runtime* guarantee.
- **Watch:** `punch-ai-governance` now holds terminal surface (scoped to graphify map subagent). Any *other* command execution by this agent — or host-graphify use outside `/punch-document` — = **drift**.
- **Guardrail:** `CLAUDE.md` Rule #1 links here; `punch-ai-governance` treats above as only sanctioned host-graphify surface.

## Team Sharing

**Status:** Accepted (2026-06-25) — extends the original Decision above.
**Deciders:** repository owner + Punch AI Governance.

### Decision

Punch opts into a **two-tier `graphify-out/` policy**: local-only state (the original
default) plus a narrow committed-artifact allowlist for team context sharing.

**Allowlist (`.gitignore` allowlist pattern `!graphify-out/<file>`):**

| File | Status | Rationale |
|---|---|---|
| `graphify-out/graph.json` | **Committed** (after validation) | Shared team query baseline |
| `graphify-out/GRAPH_REPORT.md` | **Committed** (after validation) | Human-readable audit trail |
| All other `graphify-out/` contents | Gitignored (local only) | Machine-specific or noisy |

`.gitignore` uses `graphify-out/*` (wildcard) + `!` un-ignore lines rather than the
former `graphify-out/` directory rule, which would have blocked negation.

### Validation gate (required before every commit)

`punch-ai-governance` runs all six checks and confirms before committing:

1. No absolute paths (`/(Users|home)/`) in `graph.json` or `GRAPH_REPORT.md`.
2. No venv / interpreter paths (`.venv`, `.pyenv`, `site-packages`) in either file.
3. No hostname / machine-specific strings (`MacBook`, `.local`) in either file.
4. `graph.json` parses as valid JSON.
5. All node IDs in `graph.json` are relative paths (none start with `/`).
6. No cost / token data (`input_tokens`, `output_tokens`) in shared files.

Full checklist text lives in `.github/skills/punch-graphify/SKILL.md` (Team Share section).

### Forbidden by default

These commands are **never invoked autonomously** and require an explicit team decision
plus `punch-ai-governance` sign-off: `graphify *install` (vscode / claude / copilot /
agents / hook), `--watch`, `--mcp`, `graphify add <url>`, cloud semantic backends
(`GEMINI_API_KEY`), Neo4j / FalkorDB push, cross-repo / remote-repo clone.

### Consequences

- **Positive:** team members on a fresh clone can run `graphify query` without
  rebuilding — shared baseline reduces orientation cost.
- **Negative / watch:** committed graph can go stale after major codebase shape
  changes. The designated updater for a structural change is responsible for
  updating and validating the shared graph before merging.
- **Guardrail:** `punch-ai-governance` owns the validation gate on every shared-graph
  commit. No graph update merges without the six-check sign-off.
