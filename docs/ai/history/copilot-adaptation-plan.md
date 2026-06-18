# Copilot Adaptation Plan

> **Reconciled 2026-06-17 (post-restructure).** Key correction: VS Code prompt
> files use the **`agent:`** frontmatter field (`ask`/`agent`/`plan`/custom-agent),
> **not `mode:`** — verified against the VS Code docs. Track 2's `mode:` examples
> below are corrected to `agent:`. The agent layer was also executed: 5 per-domain
> builder agents replaced `punch-builder-scoped`, and `punch-define`/`punch-refine`
> were deleted (`idea-refine` runs inside `punch-spec`). Canonical record:
> [`agent-skills-absorption-plan.md` § Execution status](agent-skills-absorption-plan.md).

> **Status:** Review artifact (no runtime AI config changed). Produced
> 2026-06-16 on branch `feat/agent-skills`. All code blocks below are
> **draft examples for review**, not files to create in this pass.

Goal: absorb upstream Core B **optimized first for GitHub Copilot Chat in VS
Code**, while keeping Claude Code and Codex compatible. Six adaptation tracks,
each with mechanical transformation rules grounded in files inspected this pass.

## Compatibility facts that drive every rule

From upstream `docs/copilot-setup.md` (verified):
- Copilot reads skills from **`.github/skills`, `.claude/skills`, or
  `.agents/skills`** (`copilot-setup.md:7`). Punch already uses `.github/skills`.
- Copilot custom agents **must be `*.agent.md`**; plain `*.md` is silently
  ignored (`copilot-setup.md:22-25`). Upstream agents are plain `.md`.
- Copilot project instructions live in `.github/copilot-instructions.md` and
  should stay **concise** (`copilot-setup.md:84`). Punch's already is.
- Copilot invokes agents with `@agent-name` (`copilot-setup.md:35-38`) — there
  is **no programmatic subagent fan-out** like Claude Code's `subagent_type`.

## Track 1 — Upstream agents → `.github/agents/*.agent.md`

**Transform rules**
1. Rename `agents/<role>.md` → `.github/agents/<role>.agent.md` (Copilot rule).
2. Keep `name:` + `description:` frontmatter (already Copilot-compatible; matches
   Punch agent contract in `agentic-workflow.instructions.md:53`).
3. Replace the Claude "Composition" block's `subagent_type`/Agent-tool language
   with Copilot `@mention` + "invoked via `<punch-prompt>`" language.
4. Insert a **Punch scope block** (allowed/forbidden behavior) — every Punch
   agent declares this; upstream personas don't.
5. Apply the absorption decisions: **add** `security-auditor`; **merge**
   `code-reviewer` into `punch-reviewer`; **exclude** `test-engineer` and
   `web-performance-auditor`.

**Draft example — `security-auditor.agent.md` (new):**
```markdown
---
name: security-auditor
description: Security reviewer for Punch. Read-only audit of input handling,
  secrets/env, container surface, and the gateway/catalog/orders boundary.
---
# Security Auditor (Punch-scoped)
Read-only persona. Audits the diff for: untrusted input at the gateway,
secrets/URLs in source, docs, tests, or artifacts (Critical Rule #5), container
and Postgres exposure. Does NOT cover web auth/session (Punch has none).

## Scope
- Allowed: read any file; produce a findings report.
- Forbidden: edits, `docker run`, host `k6`/`npm`, deploys.

## Output
Severity-ranked findings (Critical/High/Medium/Low) with file:line + fix.
Defer code-style/architecture findings to `punch-reviewer`.

## Composition
- Invoke via `@security-auditor` or the Review phase when the diff touches
  `src/services/**`, env, or `docker/**`.
- Does not invoke other agents.
```

## Track 2 — Upstream commands → `.github/prompts/*.prompt.md`

**Transform rules**
1. Frontmatter: replace Claude `description:`-only / `argument-hint:` with
   **Punch's `agent:` field + `description:`** — VS Code prompt files use
   `agent:` (`ask`/`agent`/`plan`/custom-agent), not `mode:` (`prompt-registry.md`).
2. Replace `Invoke the agent-skills:<skill> skill` with
   `Activate the **<skill>** skill at `.github/skills/<skill>/SKILL.md``.
3. Keep prompts **thin** (the upstream commands are 15–22 lines — good). Move
   procedure into the skill, not the prompt (rule #9/#10 in the brief).
4. Preserve every Punch-specific gate the upstream command lacks: phase, owner
   skill, agent, pre-conditions, scope, validation gate (`prompt-registry.md:46-61`).
5. **Drop `/build auto`** (autonomous whole-plan) — conflicts with "one task,
   human approves" (`copilot-mode-mapping.md:48-53`).
6. **Do not** point `punch-ship` at upstream `shipping-and-launch` fan-out; that
   maps to Review.

**Draft example — slimmed `punch-spec.prompt.md`:**
```markdown
---
agent: punch-architect-readonly
description: Spec — clarify (former Define), then specify goals, non-goals, acceptance criteria.
---
Phase: Spec · Agent: punch-architect-readonly (read-only + spec-doc edit)
Owner skill: spec-driven-development (.github/skills/spec-driven-development)

Activate the **spec-driven-development** skill and follow it, with these Punch
overrides:
- Punch is Docker-first + Python stdlib + k6 (NOT a web app). Use Punch commands
  (`./bin/punch …`), never `npm`.
- "Affected layers" uses the ownership map in punch-architecture.instructions.md.
- "Acceptance criteria" must name the evidence artifact (reports/state/punch-run.json).
Output: Goal · Non-goals · Constraints · Affected layers · Artifact implications ·
Acceptance criteria. No code edits.
```

## Track 3 — Upstream skills → `.github/skills/*`

**Canonical home:** `.github/skills/` (decided 2026-06-16 — no migration; already
Copilot-valid and matches existing Punch governance; see
[target architecture](recommended-target-ai-architecture.md)).

**Transform rules**
1. Copy `SKILL.md` (+ needed supporting files) into
   `.github/skills/<name>/`.
2. **Add Punch frontmatter:** Punch requires `applies-to:`
   (`agentic-workflow.instructions.md:50`). Upstream skills have only
   `name`/`description`. Add `applies-to:` so they pass `punch-governance-review`.
3. **Strip stack-specific examples** that contradict Punch and replace the
   "Commands" sections with Punch commands. Keep the *workflow*, drop web/Node
   idioms (jest/vitest/React/`npm`). The path-instructions remain the
   authority on stack (Decision policy #1).
4. **Remove Claude runtime paths** like `/mnt/skills/user/...`
   (`idea-refine/SKILL.md:22`).
5. **Cross-link, don't duplicate:** where a skill restates a Punch rule, link to
   the instruction file instead.
6. Register every absorbed skill in `skill-registry.md` **in the same PR**
   (this is the rule the `idea-refine` precedent violated).

**Draft frontmatter (adapted):**
```yaml
---
name: test-driven-development
description: Drives Punch changes with evidence. Use when changing k6 test
  behavior or orchestrator logic. Adapts the Prove-It pattern to k6 checks,
  thresholds, and reports/state/punch-run.json.
applies-to: src/tests/**, src/punch/**
---
```

## Track 4 — Punch constraints → instructions (the override layer)

Punch-specific logic that upstream skills would otherwise contradict stays in
the **instruction layer**, which always wins on stack:

| Constraint | Already lives in | Action |
|---|---|---|
| Docker-first / no host npm·k6·pip | `copilot-instructions.md:13-14`, `python-orchestrator.instructions.md:12` | keep — skills must defer |
| k6 HTTP vs Browser separation | `k6-performance.instructions.md` | keep — overrides upstream "test" idioms |
| Evidence = `punch-run.json` | `artifacts-reporting.instructions.md:40-42` | keep — overrides upstream "build passes" |
| CI/CD is external | `punch-architecture.instructions.md:36` | keep — basis for excluding `ci-cd-and-automation` |
| Low-noise console / full file logs | `artifacts-reporting.instructions.md:30-34` | keep — overrides upstream observability defaults |

**Rule:** do **not** move these into skills, and do **not** restate them inside
absorbed skills. Skills *reference* them.

## Track 5 — Cross-agent guidance → `AGENTS.md`

Slim `AGENTS.md` from a 123-line near-duplicate into a **minimal contract** that
points Codex/other agents at the skill core:

**Draft skeleton:**
```markdown
# AGENTS.md — cross-agent contract
- Architecture + rules: CLAUDE.md (canonical).
- Lifecycle + asset model: docs/ai/operating-model.md.
- Skills (the *how*): .github/skills/<name>/SKILL.md — if a task matches a
  skill, use it. Domain skills (Punch subsystems) + lifecycle skills (method).
- Verify only through `./bin/punch`. Humans merge.
(no lifecycle/agent tables here — link, don't duplicate)
```
This honors Decision policy #5 (Codex compat via `AGENTS.md` + `.github/skills/`).

## Track 6 — Claude-specific compatibility → `CLAUDE.md`

Punch deliberately uses `CLAUDE.md` as the **constitution** (canonical, linked
by `copilot-instructions.md:13`). Keep that role — do **not** reduce it to a
stub. Add only a short Claude-facing pointer to skill discovery:

```markdown
## Skill discovery (Claude Code)
Skills live in `.github/skills/`. Claude Code also auto-discovers
`.claude/skills/` — if you want Claude-native discovery, symlink or copy there.
Domain skills + lifecycle skills are indexed in docs/ai/skill-registry.md.
```
Claude-only constructs (`subagent_type`, Agent Teams, `/mnt/skills/...`,
`allowed-tools`, `.zip` packaging) stay out of the Copilot layer and, where
useful, are documented here or in `.claude/` only (Decision policy #4).

## What stays Claude-only (do not port to Copilot layer)

Evidence-backed Claude-isms that must NOT leak into `.github/prompts` or
`.github/agents`:

| Claude-ism | Source | Copilot equivalent |
|---|---|---|
| `subagent_type` parallel fan-out | `commands/ship.md:13-26` | `@agent` mentions; no programmatic fan-out — Review runs personas sequentially |
| `name:` on a prompt file (wrong field) | `punch-refine` (since deleted) | drop it; bind via `agent:` (`argument-hint:` is itself valid Copilot) |
| `/mnt/skills/user/...` script paths | `idea-refine/SKILL.md:22` | repo-relative paths run via Docker/`bin/` |
| `allowed-tools:` frontmatter | `punch-governance-review/SKILL.md:5` | informational only in Copilot |
| `.zip` skill packaging, `cp … ~/.claude/skills` | upstream `AGENTS.md:168-187` | not used; skills are in-repo |
