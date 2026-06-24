# ADR 0004 — Claude Code `guard` bridge reuses the GitHub-Copilot-First config

**Status:** Accepted (2026-06-18)
**Deciders:** repository owner + Punch AI Governance

## Context

Punch AI config = **GitHub Copilot First**: single source of truth =
`.github/` (instructions, prompts, agents, skills) plus `docs/ai/`. Repo also
opened in **Claude Code**, own asset layout (`.claude/skills/`,
`.claude/commands/`). No deliberate bridge → Claude Code usage either
ignore Punch config or — worse — grow **second, divergent copy** of
lifecycle rules, break Copilot-First single-source guarantee.

## Decision

Add **project-scoped Claude Code `guard` skill** plus thin per-command wraps that
**reuse** canonical `.github/` assets, not re-author them.

- **`.claude/skills/guard/SKILL.md`** — bridge policy. On any lifecycle /
  governance / doc request in Claude Code, resolve to matching
  `.github/prompts/punch-*.prompt.md`, adopt that prompt's declared
  `.github/agents/*.agent.md` persona + scope + guards, apply Caveman canon
  (`punch-build-caveman`), obey it. Golden rule: **reuse, never re-author.**
- **`.claude/commands/{spec,plan,build,test,review,ship,document,init}.md`** —
  one-line delegations to canonical prompt + persona + Caveman level. No
  behavior of own; wiring map in `guard/SKILL.md` = contract.
  `/verify` + `@punch-ai-governance` audits reachable same way.

## No-break invariants (Copilot First preserved)

- `.github/` stays read-authoritative; `.claude/` wraps only point into it.
- No duplication — wrap = delegation, not paraphrase (mirrors
  no-duplication-of-AI-guidance rule).
- Same Critical Rules bind both hosts: Docker-First, stdlib-only, depth-1
  delegation, approval-before-write, evidence never compressed.
- Caveman = output style only — never widens tools, access, delegation.
- `punch-ai-governance` (admin over `.github/` + `docs/`) owns wiring map; any
  change to reuse behavior = governance edit in `.github/`, never Claude-only
  patch.

## Consequences

- **Positive:** one source of truth serves both hosts; Claude Code gets full
  Punch lifecycle, zero policy drift; VS Code GitHub Copilot stays primary.
- **Negative / watch:** wiring map must track prompt/agent renames — renamed
  `.github/` asset requires updating `guard/SKILL.md` + affected wrap. Any
  rule existing **only** in `.claude/` = drift + Review failure.
