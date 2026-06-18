---
applyTo: "docs/**,README.md,CLAUDE.md"
description: Behavior rules for repository documentation.
---

# Documentation — Path Instructions

Scope: `README.md`, `CLAUDE.md`, and everything under `docs/`.

## Rules

- **README is a doorway, not a manual.** It explains what Punch is, the
  shortest local run, and links into `docs/`. Detail goes elsewhere.
- **`CLAUDE.md` is the project constitution.** Changes to it require a Plan
  and a one-line note in `docs/ai/operating-model.md` if a rule moves.
- **No duplication.**
  - Architecture lives in `docs/architecture.md` (folder map + execution
    chain) and `docs/architecture/punch-boundaries.md` (ownership layers).
  - Lifecycle walkthrough lives in `docs/ai/workflow.md`.
  - Operating model lives in `docs/ai/operating-model.md`.
  - Scoped build policy lives in `docs/ai/scoped-build-policy.md`.
  - Model selection guidance lives in `docs/ai/model-selection.md`.
  - AI mode mapping lives in `docs/ai/copilot-mode-mapping.md`.
  - Skill catalogue lives in `docs/ai/skill-registry.md`.
  - Prompt catalogue lives in `docs/ai/prompt-registry.md`.
  If you'd repeat content, link instead.
- **AI-friendly structure.** Use tables for catalogs, headings for navigation,
  and explicit file paths so an LLM can resolve references without guessing.
- **No essays.** Prefer terse lists over paragraphs. If a section grows past
  ~40 lines, consider whether it should split.
- **No marketing language.** Describe what the project does, not how great
  it is.

## When adding a new doc

- Place it under the right subtree (`architecture/`, `ai/`, `workflows/`,
  `validation/`).
- Add one line to the relevant registry (skill, prompt) or to `README.md`'s
  pointer section.
- Delete or merge the doc it is replacing in the same change.

## Build prompt

Doc-only changes typically use [`punch-build`](../prompts/punch-build.prompt.md)
(routed to `punch-runtime-engineer`) when they change an artifact contract,
otherwise no Build prompt is
needed — a doc edit can go straight from Plan to PR if it does not affect
runtime behavior.
