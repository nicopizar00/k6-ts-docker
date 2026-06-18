---
name: guard
description: >
  Project-scoped Claude Code bridge to Punch's GitHub-Copilot-First AI config.
  Use whenever working this repo in Claude Code and a lifecycle, governance, or
  doc action is requested (spec, plan, build, test, verify, review, ship,
  document, audit). Guard REUSES the canonical assets under `.github/` (prompts,
  agents, skills, instructions) + `docs/ai/` — it never forks, duplicates, or
  overrides them. It keeps GitHub Copilot VS Code the primary target and stops
  Claude Code reuse from breaking that.
---

# Guard — Claude Code ↔ GitHub Copilot bridge

Punch is **GitHub Copilot First**. The single source of truth for AI behavior is
`.github/` (instructions, prompts, agents, skills) plus `docs/ai/`. Guard lets
**Claude Code** reuse that exact configuration without maintaining a second copy.

> Golden rule: **Reuse, never re-author.** Claude Code reads `.github/` and obeys
> it. If a rule needs to change, change it in `.github/` (the Copilot source) —
> never patch behavior only into `.claude/`.

## What Guard does

When a lifecycle / governance / documentation request arrives in Claude Code:

1. **Resolve** the request to its canonical Copilot asset (table below).
2. **Load + obey** that `.github/prompts/punch-*.prompt.md`, adopting the persona,
   scope, and guards of its declared `.github/agents/*.agent.md`, and activating
   the skills that prompt names.
3. **Apply the Caveman canon** (`.github/skills/punch-build-caveman/SKILL.md`) and
   the runtime guards (`docs/ai/agent-guards.md`) exactly as Copilot would.
4. **Report** back; for delegated work, sub-agent reports stay `wenyan`-compatible
   with evidence verbatim.

## Wiring map (Claude Code command → canonical Copilot asset)

The `.claude/commands/*` wraps are **thin pointers**; this table is the contract.

| Claude command | Canonical prompt | Persona (agent) | Caveman level |
|---|---|---|---|
| `/spec`     | `.github/prompts/punch-spec.prompt.md`     | `punch-architect-readonly` | `lite` |
| `/plan`     | `.github/prompts/punch-plan.prompt.md`     | `punch-planner`            | `full` |
| `/build`    | `.github/prompts/punch-build.prompt.md`    | `punch-builder` → engineer | `ultra` (sub: `wenyan`) |
| `/test`     | `.github/prompts/punch-test.prompt.md`     | `punch-verifier`           | `ultra` (sub: `wenyan`) |
| `/review`   | `.github/prompts/punch-review.prompt.md`   | `punch-reviewer`           | `full` |
| `/ship`     | `.github/prompts/punch-ship.prompt.md`     | `punch-reviewer`           | `full` |
| `/document` | `.github/prompts/punch-document.prompt.md` | `punch-ai-governance`      | `lite` (`ultra` status only) |

`/verify` (`.github/prompts/punch-verify.prompt.md`, `punch-verifier`) and
`@punch-ai-governance` audits are reachable the same way — load the prompt/agent
and obey it; a dedicated command wrap is optional.

## No-break rules (preserve Copilot First)

- **`.github/` is read-authoritative.** Guard and the `.claude/commands/*` wraps
  point into `.github/`; they carry **no behavior of their own** beyond "go read X
  and obey it." Any divergence is a bug in the wrap, not new policy.
- **No duplication.** Do not copy a prompt/agent/skill's rules into `.claude/`.
  A wrap is a one-line delegation, not a paraphrase. (Mirrors Punch's
  no-duplication-of-AI-guidance rule.)
- **No host-tool drift.** Reuse does not relax Docker-First or stdlib-only. The
  same Critical Rules in `.github/copilot-instructions.md` and `CLAUDE.md` bind
  Claude Code here.
- **Respect agent boundaries.** Adopt the target agent's allowed/read-only/
  forbidden scope, tool surface, depth-1 delegation, and approval-before-write.
  Caveman is output style only — it never widens tools or access.
- **Governance owns this bridge.** `punch-ai-governance` (which holds admin over
  `.github/` and `docs/`) maintains the wiring map; changes to it are a governance
  edit. Claude Code never edits `.github/` to "make reuse work" without that.

## When NOT to use

- Don't use Guard to invent a Claude-only workflow that has no `.github/` source —
  add it to `.github/` first (Copilot First), then wire it here.
- Don't use it to bypass the lifecycle (no Build without an approved Plan, etc.).
