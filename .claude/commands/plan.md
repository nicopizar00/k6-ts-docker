---
description: Punch Plan (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <approved spec or topic>
---

Activate the `guard` skill, then run Punch's **Plan** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-plan.prompt.md`
- Persona + scope: `.github/agents/punch-planner.agent.md`
- Caveman: `full` (canon: `.github/skills/punch-build-caveman/SKILL.md`)

Follow that prompt exactly. Input: $ARGUMENTS
