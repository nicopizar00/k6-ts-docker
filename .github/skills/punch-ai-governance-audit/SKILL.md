---
name: punch-ai-governance-audit
description: Audits the repository's AI configuration — instructions, prompts, skills, lifecycle docs — for duplication, conflicts, drift, missing frontmatter, and lifecycle alignment.
applies-to: .github/**, docs/ai/**, CLAUDE.md
---

# Skill: punch-ai-governance-audit

## Responsibility

This skill is the authority on **whether the AI operating model is healthy**.

It owns:

- The frontmatter contract for instructions, prompts, and skills.
- The cap of three skills (`punch-orchestration`, `punch-performance-k6`,
  `punch-ai-governance-audit`).
- The one-prompt-per-lifecycle-phase rule.
- Duplication and conflict detection across `.github/` and `docs/ai/`.
- The link from `.github/instructions/ai-governance.instructions.md` and
  the `punch-governance-audit` prompt into a concrete audit pass.

It does **not** own:

- Repository code (Python, TS, Docker) — that is the other two skills'
  domain.
- The architecture itself — that lives in `CLAUDE.md` and
  `docs/architecture.md`.

## Behavioral rules

1. **No silent additions.** New skills, prompts, or instructions need a
   Shape plan and a registry entry.
2. **Cap enforced.** Anyone proposing a fourth skill must justify why
   `punch-orchestration` or `punch-performance-k6` cannot absorb it.
3. **Lifecycle is canonical.** Skills are not named after phases. Phases are
   prompts, not skills.
4. **Read-only audits.** This skill flags drift; it does not edit. Fixes go
   through a normal Build slice.
5. **Cross-link, do not duplicate.** Any rule that already exists in
   `CLAUDE.md` or `copilot-instructions.md` is referenced, not restated.

## When this skill activates

- A PR touches `.github/` or `docs/ai/`.
- The `punch-governance-audit` prompt is invoked.
- Periodic governance review (quarterly cadence recommended).

## Why this is a separate skill

Governance drift is a distinct failure mode from "the code doesn't work".
Without a dedicated skill, governance regressions accumulate silently as
each PR adds "just one more" instruction or prompt. Isolating governance
makes the cost of new AI assets visible.
