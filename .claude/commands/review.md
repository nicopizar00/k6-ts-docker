---
description: Punch Review (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <diff, branch, or PR URL>
---

Activate the `guard` skill, then run Punch's **Review** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-review.prompt.md`
- Persona + scope: `.github/agents/punch-reviewer.agent.md`
- Caveman: `full` (canon: `.github/skills/punch-build-caveman/SKILL.md`)

Read-only critique; no product edits. Follow that prompt exactly. Input: $ARGUMENTS
