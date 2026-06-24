# `.github/.ai-upstream/` — required vendor skill manifest

Staging + provenance for the **vendor** skills Punch reuses **as-is** for VS Code
GitHub Copilot. Punch does **not** fork these — install them, keep them verbatim.
This README (the manifest) is tracked; the installed vendor skill folders are
gitignored (see `.gitignore`).

> **User manual action required.** Punch cannot run the network installer for you.
> Install only the assets listed below, scoped to GitHub Copilot.

## Required by Punch (install these only)

| Asset | Why Punch needs it |
|---|---|
| `caveman` | Concise assistant-prose comms (per-phase voice; canon in [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md)) |
| `cavecrew` | Bounded leaf workers spawned by a phase **coordinator** (`punch-builder` / `punch-reviewer` / `punch-test-engineer`) at depth-1, with caveman-compressed output. Punch's Copilot adaptation are the `.github/agents/punch-cavecrew-*.agent.md` personas (vendor skill defines no Copilot `tools`) |

The installer places both in the Copilot skills dir (`.agents/skills/caveman/`,
`.agents/skills/cavecrew/`). Keep an optional verbatim provenance snapshot under
`.github/.ai-upstream/<skill>/` for drift diffing (untracked).

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

cavecrew is spawned **either** by an engineer (nested: `punch-builder` → engineer
→ cavecrew) **or** directly by a phase coordinator (`punch-builder` /
`punch-reviewer` / `punch-test-engineer` → cavecrew). The nested path needs
`chat.subagents.allowInvocationsFromSubagents: true` in VS Code settings (lazy
default); `/punch-init` warns when off. Markdown cannot set it. Depth is
**roster-bounded**, not setting-bounded: cavecrew workers carry no `agents:`, so
they never spawn a further level (max chain `builder → engineer → cavecrew`). A
worker inherits its spawner's scope — by **lineage** when an engineer spawns it,
by **injected brief** when a coordinator does (VS Code custom agents have no
skills field) — and its `tools` are a subset of that spawner. Canon:
[`agent-guards.md`](../../docs/ai/agent-guards.md),
[`orchestration-patterns.md`](../../docs/ai/punch-references/orchestration-patterns.md).

## Rules

- **Keep vendor files verbatim.** Punch's adaptation lives in
  `.github/skills/punch-build-caveman/`, never here.
- `punch-ai-governance` excludes installed vendor folders from naming /
  duplication / stale-asset checks.
