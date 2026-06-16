# Copilot Mode Mapping

How the six lifecycle phases map to GitHub Copilot's three modes.

## Reference

GitHub Copilot Chat exposes three execution modes:

- **Ask Mode** — conversation; reads the workspace; does not edit files.
- **Edit Mode** — targeted file edits over a small set of files; less
  autonomous than Agent.
- **Agent Mode** — autonomous task execution; reads, edits, runs commands.

This project uses **Ask** and **Agent** as the primary modes and treats
**Plan** as an Ask-Mode discipline (no `plan` mode exists in Copilot;
"Plan" here means "Ask Mode whose output is a plan document").

## Mapping

| Lifecycle phase | Copilot mode | Why |
|---|---|---|
| Understand | Ask | Pure investigation. Edits would skip Shape. |
| Shape      | Ask (Plan discipline) | The output is a scoped plan, not edits. |
| Build      | Agent | Multi-file changes need autonomous edit + run. |
| Verify     | Agent (run) or Ask (interpret) | Running `bin/punch` needs Agent; reading the result is Ask. |
| Review     | Ask | Read-only critique. |
| Ship       | Agent (mechanical) | git + gh commands only. |

## Prompt → mode contract

Each prompt file under `.github/prompts/` declares its mode in frontmatter:

```yaml
---
mode: ask     # or "edit" / "agent"
description: ...
---
```

If the prompt says `mode: ask`, do not invoke it in Agent Mode. The audit
prompt (`punch-governance-audit`) is read-only by contract.

## Mode discipline rules

1. **Never run a `mode: ask` prompt in Agent Mode.** It bypasses the
   read-only guarantee.
2. **Never run a `mode: agent` prompt without a Shape plan.** The plan is
   the scope; without it, Agent edits are unbounded.
3. **Build slices are one-shot.** Each Build slice runs `punch-build-slice`
   in Agent Mode for **one** numbered step. Bundle multiple slices only when
   the Shape plan says so explicitly.
4. **Ship is the only Agent Mode prompt that may touch the working tree
   without a Shape plan.** Its scope is strictly mechanical: git, gh, no
   logic edits.

## What the human controls

- Toggling between Ask and Agent in the Copilot UI.
- Confirming Shape plans before Build.
- Approving the PR opened by Ship.
- Authorizing exceptions (e.g. a Build slice that must cross scope) by
  amending the Shape plan first.

## What the human does NOT do

- Hand-edit `dist/` bundles (Docker rebuilds them).
- Run k6 outside Docker.
- Add a skill or prompt outside a Shape plan.
