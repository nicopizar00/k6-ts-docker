---
description: Punch Build (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <approved Plan task ID>
---

Activate the `guard` skill, then run Punch's **Build** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-build.prompt.md`
- Agent: `.github/agents/punch-builder.agent.md` — classifies the task into a
  subsystem (runtime or performance-test) and implements it directly, no
  delegation

Requires an approved Plan task ID with allowed/read-only/forbidden paths. Follow
that prompt exactly. Input: $ARGUMENTS
