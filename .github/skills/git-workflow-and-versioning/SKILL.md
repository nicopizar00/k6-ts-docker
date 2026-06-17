---
name: git-workflow-and-versioning
description: Structures git workflow — atomic commits, short-lived branches, descriptive conventional messages. Use when committing or branching. Stack-neutral discipline; Punch's Ship mechanics (mechanical, human-gated) override the commit-loop.
applies-to: lifecycle/Ship — the method behind punch-ship + punch-reviewer; not path-scoped
---

# Git Workflow and Versioning

## In Punch

This is the **method** behind the Ship phase
([`punch-ship`](../../prompts/punch-ship.prompt.md) + the `punch-reviewer` agent).
Punch overrides the generic loop:

- **Ship is mechanical and human-gated.** The agent stages in-scope files, commits
  with a tight message, pushes, and opens a PR — and **never merges, tags,
  force-pushes, amends pushed commits, or uses `--no-verify`**. Humans merge.
- **Build edits, Ship commits.** Builders don't commit; commits happen at Ship,
  referencing the Plan task(s). The "commit each slice" pattern below maps to
  Punch's per-slice Verify plus the single Ship commit(s).
- **Explicit `git add` of in-scope files** — never `git add -A`/`git add .` (guards
  against committing secrets, `reports/`, or `dist/`).
- **Verify via `./bin/punch`**, not host `npm`/lint/`tsc`. CI re-runs Verify on the PR.

## Overview

Git is your safety net: commits are save points, branches are sandboxes, history is
documentation. With agents generating code fast, disciplined version control keeps
changes reviewable and reversible.

## Core Principles

### Short-lived branches

Keep `main` always deployable. Work in short-lived feature branches
(`feat/<topic>`, like `feat/agent-skills`) that merge back within 1-3 days. Long
branches diverge and accumulate merge risk. Punch's deferred-domain pattern (e.g.
the k6 Browser placeholder) is the analog of a feature flag — prefer it over a
long-lived branch.

### Atomic commits

Each commit does one logical thing.

```
# Good
a1b2c3d feat(k6): add cart-gate threshold test
d4e5f6g feat(compose): expose cart route service
# Bad
x1y2z3a add cart test, fix smoke, bump k6 image, refactor report
```

### Descriptive, conventional messages

Explain the *why*, not just the *what*. This repo uses Conventional Commits:

```
<type>(<scope>): <short imperative description>

<body: why, not what — reference the Plan task(s)>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`. Scopes seen in this
repo include `ai`, `orchestrator`, `compose`, `k6`, `punch`. Avoid "fix", "update",
"misc".

### Keep concerns separate

Don't mix formatting with behavior, or a refactor with a feature — each is a
separate commit (in Punch, a separate Plan task). A cross-layer change is an
*integration task* = one commit per layer.

### Size your changes

`~100 lines` easy to review · `~300` acceptable for one logical change · `~1000`
split it (see `code-review-and-quality` splitting strategies).

## Branch Naming

```
feat/<topic>      fix/<topic>      chore/<topic>      refactor/<topic>
```

## Worktrees (parallel work)

For parallel agent work, use git worktrees so each branch lives in its own
directory without switching:

```bash
git worktree add ../k6-ts-docker-feat-x feat/x
# ... work in isolation ...
git worktree remove ../k6-ts-docker-feat-x
```

If an experiment fails, delete the worktree — nothing is lost.

## The Save-Point Pattern

```
Build a slice → Verify (./bin/punch run) → green? keep : revert to last good
... → Ship commits the verified work (human merges)
```

`git reset --hard HEAD` returns you to the last committed state if a Build goes off
the rails. You never lose more than one increment.

## Change Summaries

After a change, give a structured summary — it documents scope discipline:

```
CHANGES MADE:
- src/tests/cart-gate.ts: new gate test + thresholds
THINGS I DIDN'T TOUCH (intentionally):
- docker-compose.yml: a new service would be a separate (compose) task
POTENTIAL CONCERNS:
- threshold p95<300 is a guess — confirm against the SLA
```

The "DIDN'T TOUCH" section proves you didn't go on an unsolicited renovation.

## Pre-Commit Hygiene (Ship)

Before the Ship commit:

```bash
git diff --staged                                   # 1. review exactly what's staged
git diff --staged | grep -iE "password|secret|api_key|token"   # 2. no secrets
./bin/punch run smoke                               # 3. evidence is green (Verify already ran)
```

Never `--no-verify`. Never stage `reports/` or `dist/` (both gitignored). The
evidence is `reports/state/punch-run.json`, produced by Verify, linked in the PR.

## Handling Generated / Ignored Files

- **Don't commit:** `dist/` (esbuild output, rebuilt in Docker), `reports/`
  (run artifacts), `.env`, `node_modules/`.
- **Do commit:** `package-lock.json` when deps change.
- Keep `.gitignore` covering those — a committed `.env` with secrets is the failure
  this prevents (Critical Rule #5).

## Git for Debugging

```bash
git bisect run ./bin/punch run <test>   # find the commit that broke a test
git log --oneline -20                    # recent history
git blame <file>                         # who last changed a line
git log --grep="<keyword>" --oneline     # search messages
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll commit when the feature is done" | One giant commit can't be reviewed, debugged, or reverted. Commit per logical change at Ship. |
| "The message doesn't matter" | Messages are documentation for future you and future agents. |
| "I'll squash it later" | Squashing destroys the development narrative; prefer clean commits from the start. |
| "Branches add overhead" | Short-lived branches are free; long-lived ones are the problem. |
| "I don't need .gitignore" | …until `.env` or `reports/` gets committed. |

## Red Flags

- Large uncommitted changes accumulating.
- Messages like "fix", "update", "misc".
- Formatting mixed with behavior.
- Committing `dist/`, `reports/`, `node_modules/`, or `.env`.
- `git add -A`/`.` at Ship; `--no-verify`, force-push, or amend of pushed commits.
- An agent merging its own PR (humans merge).

## Verification

For every Ship commit:

- [ ] Commit does one logical thing; message follows `type(scope): …` conventions.
- [ ] Only in-scope files staged (explicit `git add`, no `-A`); no `reports/`/`dist/`.
- [ ] No secrets in `git diff --staged`.
- [ ] `reports/state/punch-run.json` is green and linked in the PR.
- [ ] No `--no-verify`/force/amend-pushed; the PR is left for a human to merge.
