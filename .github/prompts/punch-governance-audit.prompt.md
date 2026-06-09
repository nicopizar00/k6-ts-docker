---
mode: ask
description: Audit AI instructions, prompts, skills, and docs for drift and duplication.
---

# Punch — Governance Audit

**Lifecycle phase:** cross-cutting (run before any AI-asset change is shipped)
**Mode:** Ask (read-only — produces a report)
**Owner skill:** `punch-ai-governance-audit`

## When to use

- Before merging a PR that touches `.github/copilot-instructions.md`,
  `.github/instructions/`, `.github/prompts/`, `.github/skills/`, or
  `docs/ai/`.
- On a periodic cadence (e.g. quarterly) to catch drift in long-lived
  guidance.

## Inputs

- The current state of `.github/` and `docs/ai/`.
- (Optional) a diff if the audit is PR-scoped.

## Checks

1. **Frontmatter completeness.** Every instruction has `applyTo` +
   `description`. Every prompt has `mode` + `description`. Every skill has
   `name` + `description`.
2. **Skill cap.** At most three skills: `punch-orchestration`,
   `punch-performance-k6`, `punch-ai-governance-audit`. Flag any others.
3. **Lifecycle alignment.** Exactly one prompt per phase (Understand, Shape,
   Build, Verify, Review, Ship) + `punch-governance-audit`. Flag duplicates
   or missing phases.
4. **Duplication.** No two files restate the same rule. Flag verbatim or
   near-verbatim repeats.
5. **Conflicts.** No path instruction contradicts `CLAUDE.md` or
   `copilot-instructions.md`. Flag the conflict line by line.
6. **Mode discipline.** Prompts using `mode: agent` must declare an explicit
   scope (a Shape plan or named "mechanical only" purpose).
7. **No phase-named skills.** Flag any skill matching `punch-(understand|shape|build|verify|review|ship)`.
8. **Doc registry sync.** `docs/ai/skill-registry.md` and
   `docs/ai/prompt-registry.md` list every skill / prompt that exists.

## Expected output

A numbered findings list. For each: file, line range, finding, suggested
fix. Conclude with a single verdict line: "Governance is clean" or
"Governance drift — see findings".

## Validation gate

If drift is found, fix in a follow-up Build slice before Ship.
