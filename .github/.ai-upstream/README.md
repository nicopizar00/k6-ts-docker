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
| `cavecrew` | Bounded read-only leaf workers spawned by an explicitly authorized non-Build phase **coordinator** (`punch-code-reviewer` / `punch-test-engineer` / `punch-security-auditor`) at depth-1, with caveman-compressed output. Punch's Copilot adaptation is the `.github/agents/punch-cavecrew-{investigator,reviewer}.agent.md` personas (vendor skill defines no Copilot `tools`). Build never spawns cavecrew |

The installer places both in the Copilot skills dir (`.agents/skills/caveman/`,
`.agents/skills/cavecrew/`) — it has no notion of `.github/skills/`. Immediately
after install, relocate `caveman` only: move `.agents/skills/caveman/` to
`.github/skills/caveman/` (the Copilot project-skill location Punch registers)
and add `user-invocable: true` + `disable-model-invocation: true` to its
frontmatter — no other change to the upstream body. Leave `cavecrew` at its
installer-default location; it is not relocated. Keep an optional verbatim
provenance snapshot under `.github/.ai-upstream/<skill>/` for drift diffing
(untracked).

**Do not install** the rest of the upstream pack (`caveman-compress` ships host
Python scripts vs Punch Docker-First; `caveman-commit`/`-help`/`-review`/`-stats`
are unused).

## Install (manual, Copilot-scoped)

Upstream: <https://github.com/JuliusBrussee/caveman>

```
# add only the two skills Punch needs, for GitHub Copilot
npx -y skills add JuliusBrussee/caveman --skill caveman  --agent github-copilot --yes
npx -y skills add JuliusBrussee/caveman --skill cavecrew --agent github-copilot --yes
```

Do **not** run `install.sh --with-init` — it appends always-on rules to
`.github/copilot-instructions.md` (Punch Critical Rules file) and writes parallel
`.cursor`/`.windsurf`/`.clinerules`/`.opencode` files the layout forbids. Remove
any such artifacts if the installer created them.

## Sub-agent setting

cavecrew is spawned directly by an explicitly authorized non-Build phase
coordinator (`punch-code-reviewer` / `punch-test-engineer` /
`punch-security-auditor` → cavecrew). Build never spawns it — no nested path,
no `chat.subagents.allowInvocationsFromSubagents` dependency. Depth is
**roster-bounded**: cavecrew workers carry no `agents:`, so they never spawn a
further level. A worker inherits its coordinator's scope by **injected brief**
(VS Code custom agents have no skills field), and its `tools` are a subset of
that coordinator. Canon: [`agent-guards.md`](../../docs/ai/agent-guards.md).

## Rules

- **Keep vendor files verbatim.** The one-time `caveman` relocate step (above)
  adds only two frontmatter fields — no other hand-edit, ever.
- `punch-ai-governance` excludes installed/relocated vendor folders
  (`.agents/skills/cavecrew/`, `.github/skills/caveman/`) from naming /
  duplication / stale-asset checks.
