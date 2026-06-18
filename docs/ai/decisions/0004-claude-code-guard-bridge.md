# ADR 0004 — Claude Code `guard` bridge reuses the GitHub-Copilot-First config

**Status:** Accepted (2026-06-18)
**Deciders:** repository owner + Punch AI Governance

## Context

Punch's AI configuration is **GitHub Copilot First**: the single source of truth
is `.github/` (instructions, prompts, agents, skills) plus `docs/ai/`. The repo is
also opened in **Claude Code**, which has its own asset layout (`.claude/skills/`,
`.claude/commands/`). Without a deliberate bridge, Claude Code usage would either
ignore the Punch config or — worse — grow a **second, divergent copy** of the
lifecycle rules, breaking the Copilot-First single-source guarantee.

## Decision

Add a **project-scoped Claude Code `guard` skill** plus thin per-command wraps that
**reuse** the canonical `.github/` assets instead of re-authoring them.

- **`.claude/skills/guard/SKILL.md`** — the bridge policy. On any lifecycle /
  governance / doc request in Claude Code, it resolves to the matching
  `.github/prompts/punch-*.prompt.md`, adopts that prompt's declared
  `.github/agents/*.agent.md` persona + scope + guards, applies the Caveman canon
  (`punch-build-caveman`), and obeys it. Golden rule: **reuse, never re-author.**
- **`.claude/commands/{spec,plan,build,test,review,ship,document}.md`** — one-line
  delegations to the canonical prompt + persona + Caveman level. They carry no
  behavior of their own; the wiring map in `guard/SKILL.md` is the contract.
  `/verify` and `@punch-ai-governance` audits are reachable the same way.

## No-break invariants (Copilot First preserved)

- `.github/` stays read-authoritative; `.claude/` wraps only point into it.
- No duplication — a wrap is a delegation, not a paraphrase (mirrors the
  no-duplication-of-AI-guidance rule).
- Same Critical Rules bind both hosts: Docker-First, stdlib-only, depth-1
  delegation, approval-before-write, evidence never compressed.
- Caveman is output style only — it never widens tools, access, or delegation.
- `punch-ai-governance` (admin over `.github/` + `docs/`) owns the wiring map; any
  change to reuse behavior is a governance edit in `.github/`, never a Claude-only
  patch.

## Consequences

- **Positive:** one source of truth serves both hosts; Claude Code gets the full
  Punch lifecycle with zero policy drift; VS Code GitHub Copilot remains primary.
- **Negative / watch:** the wiring map must track prompt/agent renames — a renamed
  `.github/` asset requires updating `guard/SKILL.md` and the affected wrap. Any
  rule that exists **only** in `.claude/` is drift and a Review failure.
