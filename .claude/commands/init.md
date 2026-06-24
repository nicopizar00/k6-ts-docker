---
description: Punch Init / Copilot asset enablement sweep (Claude Code wrap → canonical GitHub Copilot asset)
---

Activate the `guard` skill, then run Punch's **Init** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-init.prompt.md`
- Persona + scope: `.github/agents/punch-ai-governance.agent.md` (**enforced** —
  complete admin over `.github/` + `docs/`; only this agent runs Init)
- Caveman: `lite` (canon: `.github/skills/punch-build-caveman/SKILL.md`)

Runs a read-only sweep of the GitHub Copilot asset set (prompts, agents, skills,
instructions + the AI-Ingest Caveman/cavecrew vendor skills), reports
PASS / WARN / BLOCKED, and hands reconciliation to `/document`. Non-destructive;
no runtime, no Python. Follow that prompt exactly. Input: $ARGUMENTS
