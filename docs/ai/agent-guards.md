# Agent Guards

Guards = **runtime discipline** Punch custom agents inherit. *Adapted per agent purpose* — the rule that flexes most is terminal access, follow from whether agent job produce runtime evidence or edit config. Guards constrain agents **at runtime**; not govern one-off repo bootstrap work.

## The three rules

1. **Restricted tool surface.** Agent use only tools its purpose need.
   Config-maintainer agent `punch-ai-governance` get terminal, but **read-only
   only** — `git status`/`git diff`, `rg`/grep, parity and link-check scripts;
   never the Punch runtime, never a mutating command (no `git add|commit|push`,
   no `rm`/`mv`, no package installs). `punch-builder` gets terminal
   (Docker/Punch-mediated only — never bare host `k6`, host `npm` only where
   documented exception allow, see [`decisions/`](decisions/)).
2. **Serial phases.** Plan → Implement → Verify, in order. State work plan,
   make change, then show evidence. No parallel jumping.
3. **Approval scoped to what's actually risky.** Ordinary edits inside an
   approved Plan task's allowed paths proceed without a per-write pause — the
   approved Plan is the authorization. Surface intended change and wait for
   go-ahead only before something destructive, hard to reverse, externally
   visible, scope-expanding (a Forbidden or unplanned path), or touching
   sensitive configuration (`.github/**`, `docs/ai/**`, `.vscode/settings.json`)
   — `punch-ai-governance` keeps a standing mandatory-approval rule for that
   last category specifically, since it shapes every future agent's behavior.

## Per-agent adaptation (C1)

| Agent | Terminal | Write approval | Delegation |
|---|---|---|---|
| `punch-builder` | **yes** — `./bin/punch`, `docker compose`, containerized k6/esbuild for evidence; host `npm`/`k6` only inside the documented performance-test-subsystem exception ([ADR 0001](decisions/0001-perf-engineer-host-npm.md)) | before destructive/scope-expanding/sensitive-config writes (Rule 3) | leaf — no `agent` tool, implements directly, no sub-agent |
| `punch-code-reviewer` (Review coordinator) | no — read-only | n/a (read-only) | leaf — no `agent` tool; reference search/pre-scan inline; verdict never delegated |
| `punch-security-auditor` (Review security axis) | no — read-only | n/a (read-only) | leaf — no `agent` tool; locate inline; verdict never delegated |
| `punch-test-engineer` (Test coordinator) | **yes** — `./bin/punch` | n/a (no edit) | leaf — no `agent` tool; coverage-gap locate inline; verdict never delegated |
| `punch-ai-governance` (maintainer) | **read-only only** — `git status`/`diff`, `rg`, parity/link checks; never the Punch runtime, never a mutating command | **mandatory** before any `.github`/`docs`/`.vscode/settings.json` write | spawns no sub-agent |

Ship (`punch-ship` prompt) carries no dedicated persona — it fans out to
`punch-code-reviewer` / `punch-security-auditor` / `punch-test-engineer` as
its own prompt-level procedure under generic Agent mode, then does mechanical
git/`gh` (commit/push/PR — no logic edits, humans merge). See
[`punch-ship.prompt.md`](../../.github/prompts/punch-ship.prompt.md).

## Delegation depth

No Punch agent currently lists sub-agents (`agents:` frontmatter field) — every
agent above is a leaf. This is today's configuration, driven by least-privilege
tool assignment and native VS Code behavior (`chat.subagents.allowInvocationsFromSubagents`
stays at its default **off**, so a sub-agent cannot itself spawn further
sub-agents even where the parent is allowed to spawn one). It is not a
standing law that no agent may ever gain the `agent` tool — VS Code natively
supports subagent delegation for parallel research, alternative solutions, or
focused review, and Punch could adopt that pattern for a specific agent if a
scoped need arose. Any such addition goes through Spec → Plan like any other
change, and is bounded by Rule 1's least-privilege tool surface regardless.

The `punch-ai-governance` maintainer is **never** listed in any `agents:`
allowlist (`disable-model-invocation: true`), so user-direct only; it spawns
no sub-agent at all.
