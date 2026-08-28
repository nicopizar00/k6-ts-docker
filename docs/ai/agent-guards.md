# Agent Guards

Guards = **runtime discipline** Punch custom agents inherit. *Adapted per agent purpose* — only rule that flexes is terminal access, follow from whether agent job produce runtime evidence or edit config. Guards constrain agents **at runtime**; not govern one-off repo bootstrap work.

## The four rules

1. **Restricted tool surface.** Agent use only tools its purpose need.
   Config-maintainer agent `punch-ai-governance` get terminal, but **read-only
   only** — `git status`/`git diff`, `rg`/grep, parity and link-check scripts;
   never the Punch runtime, never a mutating command (no `git add|commit|push`,
   no `rm`/`mv`, no package installs). Runtime engineers get terminal
   (Docker/Punch-mediated only — never host `k6`, host `npm` only where
   documented exception allow, see [`decisions/`](decisions/)).
2. **Serial phases.** Plan → Implement → Verify, in order. State work plan,
   make change, then show evidence. No parallel jumping.
3. **Explicit approval before disk writes.** Before writing files, surface
   intended change and wait for user go-ahead. Memory = draft space; disk
   committed only on approval.
4. **Bounded budget.** Keep each change small (≈≤3 files per logical step),
   diffs targeted. **Stop after 2 consecutive failures** — return to Plan, ask
   for architectural correction not retry blind.

## Per-agent adaptation (C1)

| Agent | Terminal | Write approval | ≤3-file step | Delegation depth |
|---|---|---|---|---|
| `punch-builder` (coordinator) | none — no terminal tool; delegates only | n/a (delegates) | per sub-task | **may call only its registered leaves — its two engineers**; both engineers `user-invocable: false` (Builder-routed only) |
| `punch-runtime-engineer` | **yes** — `./bin/punch`, `docker compose` for evidence | before product-code writes | yes | leaf — no `agent` tool |
| `punch-performance-test-engineer` | **yes** — k6 smoke/dry-run, containerized bundle | before product-code writes | yes | leaf — no `agent` tool |
| `punch-code-reviewer` (Review coordinator) | no — read-only | n/a (read-only) | n/a | leaf — no `agent` tool; reference search/pre-scan inline; verdict never delegated |
| `punch-security-auditor` (Review security axis) | no — read-only | n/a (read-only) | n/a | leaf — no `agent` tool; locate inline; verdict never delegated |
| `punch-test-engineer` (Test coordinator) | **yes** — `./bin/punch` | n/a (no edit) | n/a | leaf — no `agent` tool; coverage-gap locate inline; verdict never delegated |
| `punch-release-captain` (Ship coordinator) | **yes** — git/gh (commit/push/PR) | n/a (no logic edits) | n/a | fan-out **report-only leaves**: `punch-code-reviewer` + `punch-security-auditor` + `punch-test-engineer` (parallel; they don't nest further here); GO/NO-GO never delegated |
| `punch-ai-governance` (maintainer) | **read-only only** — `git status`/`diff`, `rg`, parity/link checks; never the Punch runtime, never a mutating command | **mandatory** before any `.github`/`docs`/`.vscode/settings.json` write | yes | spawns no sub-agent |

## Depth-1 / no recursion

Depth-1 guarantee = **native VS Code behaviour**: subagents cannot spawn
more subagents unless `chat.subagents.allowInvocationsFromSubagents` enabled
(keep **off**). Only two coordinators spawn sub-agents at all, both depth-1:
`punch-builder` (Build) lists **only its two engineers**, and
`punch-release-captain` (Ship) fans out to the three Review/Test/Security
specialists as report-only leaves that don't nest further. `punch-code-reviewer`,
`punch-security-auditor`, and `punch-test-engineer` all carry no `agent` tool —
reference search and diff pre-scan happen inline, not via a spawned worker. The
`punch-ai-governance` maintainer **never** listed in any `agents:` allowlist
(`disable-model-invocation: true`), so user-direct only; it spawns no
sub-agent at all.
