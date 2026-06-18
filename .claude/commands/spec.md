---
description: Punch Spec (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <request, issue, or symptom>
---

Activate the `guard` skill, then run Punch's **Spec** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-spec.prompt.md`
- Persona + scope: `.github/agents/punch-architect-readonly.agent.md`
- Caveman: `lite` (canon: `.github/skills/punch-build-caveman/SKILL.md`)

Follow that prompt exactly. Input: $ARGUMENTS
