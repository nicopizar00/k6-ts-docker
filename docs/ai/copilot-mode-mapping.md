# Copilot Mode Mapping

How the seven lifecycle phases map to GitHub Copilot's three modes.

## Reference

GitHub Copilot Chat exposes three execution modes:

- **Ask Mode** — conversation; reads the workspace; does not edit files.
- **Edit Mode** — targeted file edits over a small set of files; less
  autonomous than Agent.
- **Agent Mode** — autonomous task execution; reads, edits, runs commands.

Punch uses **Ask** and **Agent** as the primary modes and treats
**Plan** as an Ask-Mode discipline (no `plan` mode exists in Copilot;
"Plan" here means "Ask Mode whose output is a plan document").

## Mapping

| Lifecycle phase | Copilot mode | Agent persona | Why |
|---|---|---|---|
| Define | Ask | `punch-architect-readonly` | Pure investigation. Edits would skip Spec. |
| Spec   | Ask | `punch-architect-readonly` | The output is a spec doc, not edits. |
| Plan   | Ask (Plan discipline) | `punch-planner` | The output is a plan, not edits. |
| Build  | Agent | `punch-builder-scoped` | One scoped task with autonomous edit. |
| Verify | Agent (run) or Ask (interpret) | `punch-verifier` | Running `./bin/punch` needs Agent; reading the result is Ask. |
| Review | Ask | `punch-reviewer` | Read-only critique. |
| Ship   | Agent (mechanical) | `punch-reviewer` | git + gh commands only — no logic edits. |

## Prompt → mode contract

Each prompt file under `.github/prompts/` declares its mode in
frontmatter:

```yaml
---
mode: ask     # or "edit" / "agent"
description: ...
---
```

If the prompt says `mode: ask`, do not invoke it in Agent Mode.

## Mode discipline rules

1. **Never run a `mode: ask` prompt in Agent Mode.** It bypasses the
   read-only guarantee.
2. **Never run a `mode: agent` prompt without an approved Plan task.**
   The Plan is the scope; without it, Agent edits are unbounded.
3. **Build calls are one-task.** Each Build invocation executes **one**
   task ID from the Plan. Bundle multiple tasks only when the Plan
   explicitly authorizes the integration and the Build is one of
   several layer-specific calls.
4. **Ship is the only Agent Mode prompt that may touch the working
   tree without a per-task allowed-paths list.** Its scope is strictly
   mechanical: git, gh, no logic edits.

## What the human controls

- Toggling between Ask and Agent in the Copilot UI.
- Confirming Plans before Build.
- Approving the PR opened by Ship.
- Authorizing exceptions (e.g. a Build that must cross scope) by
  amending the Plan first.

## What the human does NOT do

- Hand-edit `dist/` bundles (Docker rebuilds them).
- Run k6 outside Docker.
- Add a skill, agent, or prompt outside a Plan.
