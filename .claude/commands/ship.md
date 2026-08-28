---
description: Punch Ship (Claude Code wrap → canonical GitHub Copilot asset)
argument-hint: <approved review; branch>
---

Activate the `guard` skill, then run Punch's **Ship** phase by loading and obeying
the canonical Copilot asset — do not re-author or paraphrase it:

- Prompt: `.github/prompts/punch-ship.prompt.md`
- Persona + scope: none — the prompt's own fan-out + mechanical git/gh under
  generic Agent mode (no dedicated coordinator persona)

Mechanical only (git/gh). Never merges, tags, or pushes to `main` — a human
approves the merge. Follow that prompt exactly. Input: $ARGUMENTS
