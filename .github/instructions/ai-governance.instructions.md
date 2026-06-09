---
applyTo: ".github/**,docs/ai/**"
description: Rules for changes to AI configuration, skills, prompts, and governance docs.
---

# AI Governance — Path Instructions

Scope: `.github/copilot-instructions.md`, `.github/instructions/`,
`.github/prompts/`, `.github/skills/`, and `docs/ai/`.

## Rules

- **Three skills, period.** The MVP supports exactly three skills:
  `punch-orchestration`, `punch-performance-k6`, `punch-ai-governance-audit`.
  Do not add a fourth without a Shape plan that explains why an existing
  skill cannot absorb the responsibility.
- **One prompt per lifecycle phase.** Understand, Shape, Build, Verify,
  Review, Ship, plus the dedicated `punch-governance-audit`. No phase-specific
  variants ("understand-fast", "shape-deep") in the MVP.
- **Frontmatter is mandatory.**
  - Instructions: `applyTo:` glob, `description:` one-liner.
  - Prompts: `mode: ask|edit|agent`, `description:` one-liner.
  - Skills: `name:`, `description:`, `applies-to:` (free-form scope).
- **No duplication across files.** Each behavioral rule lives in exactly one
  instruction file. Prompts reference instructions; they do not restate them.
- **Lifecycle ≠ skill.** The lifecycle is the operating protocol. Do not
  create a skill named after a phase (no `punch-build`, `punch-verify`).
- **Read-only is enforced by mode.** Audits and reviews use Ask Mode.
  Shape uses Plan Mode. Build uses Agent Mode within a named scope.
- **Governance audits run via the `punch-governance-audit` prompt.** That
  prompt's contract is the only place that drives the
  `punch-ai-governance-audit` skill.

## When adding new AI assets

Run `punch-governance-audit` against the change before merging. It checks
for duplication, drift, missing frontmatter, and unjustified new skills.
