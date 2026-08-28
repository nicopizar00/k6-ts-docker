# `.github/.ai-upstream/` — optional vendor skill manifest

Staging + provenance for **optional vendor** skills Punch may reuse **as-is** for
VS Code GitHub Copilot. Neither is a Punch prerequisite — Punch runs the full
lifecycle without them. Punch does **not** fork these — if installed, keep them
verbatim. This README (the manifest) is tracked; the installed vendor skill
folders are gitignored (see `.gitignore`).

> **User manual action, optional.** Punch cannot run the network installer for
> you, and does not require you to. If you want these capabilities, install
> only the assets listed below, scoped to GitHub Copilot.

## Optional capabilities (install only if you want them)

| Asset | What it adds |
|---|---|
| `caveman` | Concise assistant-prose comms, VS Code GitHub Copilot Chat only; default `lite` rule lives in [`copilot-instructions.md`](../copilot-instructions.md) |

`cavecrew` was evaluated and **retired**: its worker pattern added coordination
overhead — an incomplete vendor skill package, an `agents:` allowlist gap on
its two Copilot adaptations — without a demonstrated benefit at this repo's
scale. Review/Test/Security coordinators perform reference search and diff
pre-scan inline instead (`agents: []`); do not reinstall it.

The installer places `caveman` in the Copilot skills dir (`.agents/skills/caveman/`)
— it has no notion of `.github/skills/`. Immediately after install, relocate it:
move `.agents/skills/caveman/` to `.github/skills/caveman/` (the Copilot
project-skill location Punch registers) and add `user-invocable: true` +
`disable-model-invocation: true` to its frontmatter — no other change to the
upstream body. Keep an optional verbatim provenance snapshot under
`.github/.ai-upstream/<skill>/` for drift diffing (untracked).

**Do not install** the rest of the upstream pack (`caveman-compress` ships host
Python scripts vs Punch Docker-First; `caveman-commit`/`-help`/`-review`/`-stats`
are unused).

## Install (manual, Copilot-scoped)

Upstream: <https://github.com/JuliusBrussee/caveman>

```
# add only the skill Punch needs, for GitHub Copilot
npx -y skills add JuliusBrussee/caveman --skill caveman --agent github-copilot --yes
```

Do **not** run `install.sh --with-init` — it appends always-on rules to
`.github/copilot-instructions.md` (Punch Critical Rules file) and writes parallel
`.cursor`/`.windsurf`/`.clinerules`/`.opencode` files the layout forbids. Remove
any such artifacts if the installer created them.

## Sub-agent setting

`chat.subagents.allowInvocationsFromSubagents` stays at its default (`false`) —
no Punch agent spawns a sub-agent that itself spawns further sub-agents. Only
`punch-builder` (Build, its two engineers) and `punch-release-captain` (Ship,
report-only fan-out) list sub-agents at all; every other agent carries
`agents: []`. Canon: [`agent-guards.md`](../../docs/ai/agent-guards.md).

## Rules

- **Keep vendor files verbatim.** The one-time `caveman` relocate step (above)
  adds only two frontmatter fields — no other hand-edit, ever.
- `punch-ai-governance` excludes the installed/relocated vendor folder
  (`.github/skills/caveman/`) from naming / duplication / stale-asset checks.
