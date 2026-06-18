# Agent Guards

Guards are a **runtime discipline** that Punch custom agents inherit. They are
*adapted per agent purpose* — the only rule that flexes is terminal access, which
follows from whether the agent's job is to produce runtime evidence or to edit
configuration. Guards constrain agents **at runtime**; they do not govern one-off
repository bootstrap work.

## The four rules

1. **Restricted tool surface.** An agent uses only the tools its purpose needs.
   Config-maintainer agents do **not** get a terminal — with one documented
   exception: `punch-ai-governance` may run host `graphify` for the
   `/punch-documentate` map ([ADR 0002](decisions/0002-graphify-host-tool.md)),
   never the Punch runtime. Runtime engineers get a terminal
   (Docker/Punch-mediated only — never host `k6`, and host `npm` only where a
   documented exception allows it, see [`decisions/`](decisions/)).
2. **Serial phases.** Plan → Implement → Verify, in order. State the work plan,
   make the change, then show evidence. No parallel jumping.
3. **Explicit approval before disk writes.** Before writing files, surface the
   intended change and wait for the user's go-ahead. Memory is draft space; disk
   is committed only on approval.
4. **Bounded budget.** Keep each change small (≈≤3 files per logical step) and
   diffs targeted. **Stop after 2 consecutive failures** — return to Plan and ask
   for an architectural correction rather than retrying blindly.

## Per-agent adaptation (C1)

| Agent | Terminal | Write approval | ≤3-file step | Delegation depth |
|---|---|---|---|---|
| `punch-builder` (dispatcher) | via delegation only | n/a (delegates) | per sub-task | **may call 1 sub-agent; that sub-agent may NOT spawn another** |
| `punch-runtime-engineer` | **yes** — `./bin/punch`, `docker compose` for evidence | before product-code writes | yes | leaf — `agents: []` |
| `punch-performance-test-engineer` | **yes** — k6 smoke/dry-run, containerized bundle | before product-code writes | yes | leaf — `agents: []` |
| `punch-ai-governance` (maintainer) | **scoped** — host `graphify` map only (ADR 0002); never runs Punch | **mandatory** before any `.github` write | yes | forks only the `/graphify` map (1-deep); never a sub-agent |

## Depth-1 / no recursion

The depth-1 guarantee is **native VS Code behaviour**: subagents cannot spawn
further subagents unless `chat.subagents.allowInvocationsFromSubagents` is enabled
(keep it **off**). Punch reinforces this — the two engineers carry `agents: []`,
and `punch-builder` lists exactly its two engineers in `agents:`. The
`punch-ai-governance` maintainer is **never** listed in any `agents:` allowlist
(`disable-model-invocation: true`), so it is user-direct only; in Documentation
mode its single sanctioned delegation is the `/graphify` map (1-deep), and it
spawns no other sub-agent.
