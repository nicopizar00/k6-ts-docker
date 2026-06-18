---
description: Punch Init / bootstrap-adoption guard (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <optional: --write | --with-graphify | --output DIR>
---

Activate the `guard` skill, then run Punch's **Init** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-init.prompt.md`
- Persona + scope: `.github/agents/punch-ai-governance.agent.md` (**enforced** —
  complete admin over `.github/` + `docs/`; only this agent runs Init)
- Caveman: `lite` (canon: `.github/skills/punch-build-caveman/SKILL.md`)

Runs the read-only `./bin/punch init` scan, guards pending adoption items, and
hands documentation reconciliation to `/document`. Non-destructive; never runs the
Punch runtime. Follow that prompt exactly. Input: $ARGUMENTS
