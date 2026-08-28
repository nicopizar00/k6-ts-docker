# Copilot Mode Mapping

How six lifecycle phases map to GitHub Copilot three modes.

## Reference

GitHub Copilot Chat expose three execution modes:

- **Ask Mode** — conversation; read workspace; no edit files.
- **Edit Mode** — targeted edits over small file set; less autonomous than Agent.
- **Agent Mode** — autonomous task execution; read, edit, run commands.

Punch use **Ask** and **Agent** as primary modes. VS Code Copilot Chat's prompt-file `agent:` field does support a built-in `plan` value alongside `ask`/`agent`/a named custom agent — Punch deliberately does not use it: `punch-plan.prompt.md` binds the custom, read-only `punch-architect` agent instead, so Plan output stays constrained to Punch's own task-contract shape (allowed/read-only/forbidden paths, validation commands, human checkpoint) rather than the built-in mode's generic plan format. Punch's Plan phase is therefore Ask-Mode discipline under a named custom agent, not the built-in `plan` value.

## Mapping

| Lifecycle phase | Copilot mode | Agent persona | Why |
|---|---|---|---|
| Spec   | Ask | `punch-architect` | Clarify (former Define) + write spec doc. |
| Plan   | Ask (Plan discipline) | `punch-architect` | Output is plan, not product edits. |
| Build  | Agent | `punch-builder` (classifies task into a subsystem, implements directly) | One scoped task, autonomous edit. |
| Test   | Agent (run) or Ask (interpret) | `punch-test-engineer` | Run `./bin/punch` need Agent; read result is Ask. |
| Review | Ask | `punch-code-reviewer` | Read-only five-axis critique. |
| Ship   | Agent (generic — gate + mechanical) | no dedicated persona | Fan-out → GO/NO-GO + rollback, then git + gh — no logic edits, all owned by the prompt itself. |

## Prompt → agent contract

Each prompt file under `.github/prompts/` declare its agent in frontmatter. VS Code prompt files use **`agent:`** field (not `mode:`):

```yaml
---
agent: punch-architect   # or ask | agent | plan | <custom-agent-name>
description: ...
---
```

Bound agent own `tools:` set is real guarantee: read-only personas (`punch-architect`, `punch-code-reviewer`) carry `search` + doc-`edit` only; `punch-builder` carries `edit` **and** terminal (`execute/runInTerminal`) — it may run scoped implementation checks, never the final verdict; `punch-test-engineer` carries `runCommands` as the independent verifier. Read-only persona cannot edit product code regardless how prompt invoked.

## Mode discipline rules

1. **Read-only personas stay read-only.** `punch-architect` (Spec + Plan) and `punch-code-reviewer` (Review) carry no code-`edit` tool, so cannot edit product code — preserve phase read-only guarantee.
2. **Never run builder prompt without approved Plan task.** Plan is scope; without it, Build edits unbounded.
3. **Build calls are one-task.** Each Build invocation execute **one** task ID from Plan. Bundle multiple tasks only when Plan explicitly authorize integration and Build is one of several layer-specific calls.
4. **Ship is only Agent Mode prompt that may touch working tree without per-task allowed-paths list.** Scope strictly mechanical: git, gh, no logic edits.

## What the human controls

- Toggle between Ask and Agent in Copilot UI.
- Confirm Plans before Build.
- Approve PR opened by Ship.
- Authorize exceptions (e.g. Build that must cross scope) by amending Plan first.

## What the human does NOT do

- Hand-edit `dist/` bundles (Docker rebuild them).
- Run k6 outside Docker.
- Add skill, agent, or prompt outside Plan.
