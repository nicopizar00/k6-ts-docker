---
applyTo: "docs/**,README.md,CLAUDE.md"
description: Behavior rules for repository documentation.
---
# Documentation — Path Instructions

Scope: `README.md`, `CLAUDE.md`, everything under `docs/`.

## Rules

- **README is a doorway, not a manual.** Explain what Punch is, shortest local
  run, link into `docs/`. Detail go elsewhere.
- **`CLAUDE.md` is the project constitution.** Changes need Plan + one-line note
  in `docs/ai/operating-model.md` if rule moves.
- **No duplication.**
  - Architecture: `docs/architecture.md` (folder map + execution chain) +
    `docs/architecture/punch-boundaries.md` (ownership layers).
  - Lifecycle walkthrough: `docs/ai/workflow.md`.
  - Operating model: `docs/ai/operating-model.md`.
  - Scoped build policy: `docs/ai/scoped-build-policy.md`.
  - Model selection guidance: `docs/ai/model-selection.md`.
  - AI mode mapping: `docs/ai/copilot-mode-mapping.md`.
  - Skill catalogue: `docs/ai/skill-registry.md`.
  - Prompt catalogue: `docs/ai/prompt-registry.md`.
  If you'd repeat content, link instead.
- **AI-friendly structure.** Tables for catalogs, headings for navigation,
  explicit file paths so LLM resolve references without guessing.
- **No essays.** Terse lists over paragraphs. Section past ~40 lines, consider
  split.
- **No marketing language.** Describe what project does, not how great it is.

## When adding a new doc

- Place under right subtree (`architecture/`, `ai/`, `workflows/`,
  `validation/`).
- Add one line to relevant registry (skill, prompt) or `README.md` pointer
  section.
- Delete or merge replaced doc in same change.

## Build prompt

Doc-only changes typically use [`punch-build`](../prompts/punch-build.prompt.md)
(routed to `punch-runtime-engineer`) when they change artifact contract.
Otherwise no Build prompt needed — doc edit go straight Plan to PR if no runtime
behavior change.
