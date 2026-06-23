---
description: Punch Test / Prove-It (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <check/threshold or change under test>
---

Activate the `guard` skill, then run Punch's **Test** (TDD/Prove-It) phase by
loading and obeying the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-test.prompt.md`
- Persona + scope: `.github/agents/punch-test-engineer.agent.md`
- Caveman: `ultra` (governance) / `wenyan` (execution); canon:
  `.github/skills/punch-build-caveman/SKILL.md`

Runs via `./bin/punch` only — never host k6 or raw docker. Follow that prompt
exactly. Input: $ARGUMENTS
