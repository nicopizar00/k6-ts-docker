---
description: Punch Build (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <approved Plan task ID>
---

Activate the `guard` skill, then run Punch's **Build** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-build.prompt.md`
- Dispatcher: `.github/agents/punch-builder.agent.md` → delegates (depth-1) to
  `punch-runtime-engineer` or `punch-performance-test-engineer`
- Caveman: `ultra` (governance) / `wenyan` (execution sub-agents); canon:
  `.github/skills/punch-build-caveman/SKILL.md`

Requires an approved Plan task ID with allowed/read-only/forbidden paths. Follow
that prompt exactly. Input: $ARGUMENTS
