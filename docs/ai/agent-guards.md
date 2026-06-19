# Agent Guards

Guards = **runtime discipline** Punch custom agents inherit. *Adapted per agent purpose* — only rule that flexes is terminal access, follow from whether agent job produce runtime evidence or edit config. Guards constrain agents **at runtime**; not govern one-off repo bootstrap work.

## The four rules

1. **Restricted tool surface.** Agent use only tools its purpose need.
   Config-maintainer agents do **not** get terminal — one documented
   exception: `punch-ai-governance` may run host `graphify` for
   `/punch-document` map ([ADR 0002](decisions/0002-graphify-host-tool.md)),
   never Punch runtime. Runtime engineers get terminal
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
| `punch-builder` (dispatcher) | via delegation only | n/a (delegates) | per sub-task | **may call 1 sub-agent; that sub-agent may NOT spawn another** |
| `punch-runtime-engineer` | **yes** — `./bin/punch`, `docker compose` for evidence | before product-code writes | yes | leaf — `agents: []` |
| `punch-performance-test-engineer` | **yes** — k6 smoke/dry-run, containerized bundle | before product-code writes | yes | leaf — `agents: []` |
| `punch-ai-governance` (maintainer) | **scoped** — `./bin/punch init` (read-only scan) + host `graphify` map (ADR 0002); never the Punch runtime | **mandatory** before any `.github`/`docs` write | yes | forks only the `/graphify` map (1-deep); never a sub-agent |

## Depth-1 / no recursion

Depth-1 guarantee = **native VS Code behaviour**: subagents cannot spawn
more subagents unless `chat.subagents.allowInvocationsFromSubagents` enabled
(keep **off**). Punch reinforce — two engineers carry `agents: []`,
`punch-builder` list exactly its two engineers in `agents:`. The
`punch-ai-governance` maintainer **never** listed in any `agents:` allowlist
(`disable-model-invocation: true`), so user-direct only; in Documentation
mode its single sanctioned delegation = `/graphify` map (1-deep), spawn no
other sub-agent.
