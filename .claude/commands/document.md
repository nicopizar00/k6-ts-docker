---
description: Punch Document (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <wave scope, e.g. docs/ai or README>
---

Activate the `guard` skill, then run Punch's **Document** phase by loading and
obeying the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-document.prompt.md`
- Persona + scope: `.github/agents/punch-ai-governance.agent.md` (admin over
  `.github/` + all `docs/`)
- Caveman: `full` for wave working comms (diagnose / classify / plan); `lite` for
  persisted docs and reports; Wenyan forbidden in docs. Emojis / ASCII emoticons
  allowed in docs. Canon: `.github/skills/punch-build-caveman/SKILL.md`
- Map with the **Global Graphify repository track** (`/graphify .` then
  `--update`); evidence only, never canonical.

Documentation-debt remediation + AI-artifact lifecycle — inherited docs and prior
AI artifacts untrusted until verified. Maintain lean, AI-First,
minimal-human-readable docs. Follow that prompt exactly.
Input: $ARGUMENTS
