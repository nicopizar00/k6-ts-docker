# Upstream provenance — caveman

This directory is a **pristine, do-not-edit snapshot** of the upstream Caveman
Skill, kept for drift detection. Punch reuses only the *style* of this skill,
scoped to Build, through the authored adapter
[`punch-build-caveman`](../../.github/skills/punch-build-caveman/SKILL.md). This
copy is the reference we diff against when upstream changes.

| Field | Value |
|---|---|
| Upstream project | https://github.com/JuliusBrussee/caveman |
| Install guide | https://github.com/JuliusBrussee/caveman/blob/main/INSTALL.md |
| Skill source | https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md |
| Distribution | `install.sh` / `npx -y github:JuliusBrussee/caveman` (package `caveman-installer`) |
| Snapshot version | **0.1.0** (see `.caveman_version`) |
| Snapshot date | 2026-06-18 |
| Skill entrypoint | `SKILL.md` (invoked as `/caveman` with modes `lite` / `full` / `ultra`) |
| Purpose in Punch | concise **assistant-prose** communication for the **Build** phase only — see [ADR 0003](../../docs/ai/decisions/0003-caveman-build-comms.md) |

## How it was adopted (and why NOT via the official installer)

The task asked for the official Copilot install path. A `--dry-run` was executed
on 2026-06-18:

```
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash -s -- --only copilot --with-init --dry-run
```

The dry run revealed two actions that are **unsafe for Punch**:

1. `npx -y skills add JuliusBrussee/caveman --skill * -a github-copilot --yes`
   — installs **all** Caveman skills globally for the `github-copilot` agent.
   Punch wants **one** Build-scoped adapter, not a global multi-skill install.
2. `caveman-init.js --with-init` — **appends** an always-on activation rule to
   the existing `.github/copilot-instructions.md` (verified: `mode: 'append'`,
   `fs.writeFileSync(existing + sep + ruleBody)`), and writes a parallel
   multi-agent rule structure (`.cursor/`, `.windsurf/`, `.clinerules/`,
   `.opencode/AGENTS.md`, root `AGENTS.md`). That would make Caveman **global**
   across every Copilot session (violating Build-only scoping), mutate Punch's
   authored Critical Rules file (weakening governance precedence), and add a
   parallel structure Punch's project layout forbids.

Per the task's fallback clause ("Do not use a custom manual copy … unless the
official installer … is unsafe. If fallback is needed, document exactly why"),
the official installer was **not** run. Instead this pristine snapshot + the
authored Punch adapter reproduce the skill *style* under Punch governance. No
global hooks, no `$CLAUDE_CONFIG_DIR` writes, no parallel rule files.

## Rules

- **Do not edit these files.** They are upstream verbatim. Punch's adaptation
  lives in `.github/skills/punch-build-caveman/` and the Build prompt, never here.
- `.ai-upstream/**` is **frozen provenance**: `punch-ai-governance` excludes it
  from cross-reference, naming, duplication, and stale-asset checks.
- **Reuse the style, don't fork the tooling.** Punch consumes only Caveman's
  prose-compression convention. It does **not** install Caveman's hooks,
  statusline, MCP shrink, or per-agent rule files.

## Updating

1. Re-run the upstream installer dry run (or fetch `skills/caveman/SKILL.md`) and
   compare its version against `.caveman_version`.
2. `git diff` the fetched `SKILL.md` against this snapshot to see what changed.
3. If a changed rule or mode affects the Punch adapter, open a governance issue —
   do **not** silently apply. Only `punch-ai-governance` commits the bump after
   review.
