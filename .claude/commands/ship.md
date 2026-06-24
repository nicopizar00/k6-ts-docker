---
description: Punch Ship (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <approved review; branch>
---

Activate the `guard` skill, then run Punch's **Ship** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-ship.prompt.md`
- Persona + scope: `.github/agents/punch-reviewer.agent.md`
- Caveman: `full` (canon: `.github/skills/punch-build-caveman/SKILL.md`)

Mechanical only (git/gh). Never merges, tags, or pushes to `main` — a human
approves the merge. Follow that prompt exactly. Input: $ARGUMENTS
