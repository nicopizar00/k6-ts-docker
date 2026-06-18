# ADR 0002 — graphify as a scoped host-tool for documentation mapping

**Status:** Accepted (2026-06-18)
**Deciders:** repository owner + Punch AI Governance work

## Context

Punch's Rule #1 is **Docker First**: the host needs only Docker and a stdlib
Python 3 runtime. The one prior exception is [ADR 0001](0001-perf-engineer-host-npm.md)
(host `npm` for the perf-test engineer).

We want a way to manage **documentation debt** — duplicated, stale, partial, or
orphaned docs across `docs/`, `docs/ai/`, `.github/`, `README.md`, and
`AGENTS.md`. [Graphify](https://github.com/safishamsi/graphify) (PyPI `graphifyy`,
host CLI `graphify`) maps a corpus into a knowledge graph with community
detection and `query` / `path` / `explain` / `affected` traversal — useful
**evidence** for spotting that drift. It is a host CLI installed via
`uv tool install graphifyy`; it is **not** Dockerized and is not part of the
source → bundle → image → run → report execution chain.

A pristine upstream snapshot (v0.8.41) may be kept in `.ai-upstream/graphify/`
with provenance in its `UPSTREAM.md`. Note: `.ai-upstream/` is a **gitignored
local staging area** (see `.ai-upstream/.gitkeep`), not version-controlled — the
canonical Punch adaptation lives in `.github/` (the `punch-document` prompt + the
`punch-ai-governance` Documentation mode). The snapshot is a local drift baseline;
re-fetch it (`uv tool install graphifyy`, re-copy the installed skill) when absent.

## Decision

Graphify is adopted as a **scoped host-tool exception** to Docker First, used
**only** by the documentation-reconciliation workflow. This is an exception, not
a repeal:

- **Reuse, don't fork.** Punch invokes the existing `/graphify` skill and
  consumes its **native outputs** (`graphify-out/graph.json`,
  `GRAPH_REPORT.md`). No custom AST/indexing skill is created.
- **One governed workflow.** A `/punch-document` prompt drives the existing
  [`punch-ai-governance`](../../../.github/agents/punch-ai-governance.agent.md)
  agent, which reconciles documentation in **waves** (keep / merge / rewrite /
  archive / delete / promote). Graphify provides the map; `punch-ai-governance`
  makes every decision.
- **VS Code-native delegation.** The agent forks `/graphify` as a **single
  subagent** for the structural map, relying on VS Code subagent **tool
  inheritance**, kept **1-deep** (`chat.subagents.allowInvocationsFromSubagents`
  stays at its default — subagents cannot spawn subagents). For this, the agent
  gains `runSubagent` and a scoped run-tool surface. *(Implemented with the
  `punch-document` workflow; see that prompt and the agent's Documentation
  mode.)*
- **Guard reworded, not removed.** `punch-ai-governance` still **never runs the
  Punch Docker/k6 runtime or the `bin/punch` suite**. Its only command surface
  is forking the `/graphify` map subagent.
- **Outputs are throwaway.** Everything under `graphify-out/` is gitignored
  audit **evidence** — never canonical documentation. `CLAUDE.md`, `docs/`, and
  the registries remain authoritative; nothing is promoted to canonical without
  a governance decision.
- **No other surface.** No other agent, command, or contributor workflow gains
  host-graphify dependence, and the execution chain is unchanged.

## Consequences

- **Positive:** documentation debt gets a lean, wave-based reconciliation phase
  backed by graph evidence — with **no new skill and no new agent** (logic folds
  into the existing `punch-ai-governance` agent + one prompt).
- **Negative / watch:** a contributor running `/punch-document` locally needs
  graphify host-installed (`uv tool install graphifyy`). This is acceptable: it
  is opt-in, off the evidence/execution path, and does not touch the Docker-First
  *runtime* guarantee.
- **Watch:** `punch-ai-governance` now holds a terminal surface (scoped to the
  graphify map subagent). Any *other* command execution by this agent — or
  host-graphify use outside `/punch-document` — is **drift**.
- **Guardrail:** `CLAUDE.md` Rule #1 links here; `punch-ai-governance` treats the
  above as the only sanctioned host-graphify surface.
