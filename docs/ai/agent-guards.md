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
| `punch-builder` (coordinator) | via delegation only | n/a (delegates) | per sub-task | **may call its registered leaves (engineers + cavecrew workers); each leaf may NOT spawn another** |
| `punch-runtime-engineer` | **yes** — `./bin/punch`, `docker compose` for evidence | before product-code writes | yes | leaf — `agents: []` |
| `punch-performance-test-engineer` | **yes** — k6 smoke/dry-run, containerized bundle | before product-code writes | yes | leaf — `agents: []` |
| `punch-code-reviewer` (Review coordinator) | no — read-only | n/a (read-only) | n/a | **read-only cavecrew** (`cavecrew-investigator`, `cavecrew-reviewer`); not `cavecrew-builder` (no edit ⊄); verdict never delegated |
| `punch-security-auditor` (Review security axis) | no — read-only | n/a (read-only) | n/a | **`cavecrew-investigator` only**; verdict never delegated |
| `punch-test-engineer` (Test coordinator) | **yes** — `./bin/punch` | n/a (no edit) | n/a | **`cavecrew-investigator` only** (read-only locate); verdict never delegated |
| `punch-release-captain` (Ship coordinator) | **yes** — git/gh (commit/push/PR) | n/a (no logic edits) | n/a | fan-out **report-only leaves**: `punch-code-reviewer` + `punch-security-auditor` + `punch-test-engineer` (parallel; they don't nest further here); GO/NO-GO never delegated |
| `cavecrew-investigator` (worker) | no — read-only | n/a | bounded locate packet | leaf — no `agents:` |
| `cavecrew-builder` (worker) | no | before edit | **1-2 files; refuse 3+** | leaf — no `agents:` |
| `cavecrew-reviewer` (worker) | no — read-only | n/a | bounded diff check | leaf — no `agents:` |
| `punch-ai-governance` (maintainer) | **scoped** — `./bin/punch init` (read-only scan) + host `graphify` map (ADR 0002); never the Punch runtime | **mandatory** before any `.github`/`docs` write | yes | forks only the `/graphify` map (1-deep); never a sub-agent |

## Depth-1 / no recursion

Depth-1 guarantee = **native VS Code behaviour**: subagents cannot spawn
more subagents unless `chat.subagents.allowInvocationsFromSubagents` enabled
(keep **off**). Only a **phase coordinator** spawns, depth-1: `punch-builder`
(Build), `punch-code-reviewer` (Review), `punch-test-engineer` (Test),
`punch-release-captain` (Ship). Punch reinforce — both engineers carry `agents: []`;
cavecrew workers carry no `agents:`; so every leaf is non-spawning and the setting
stays off. `punch-builder` lists its two engineers **plus** the three `cavecrew-*`
workers in `agents:`; `punch-code-reviewer` lists `cavecrew-investigator` +
`cavecrew-reviewer` (read-only); `punch-security-auditor` + `punch-test-engineer`
list `cavecrew-investigator` only; `punch-release-captain` lists the three Review/Test
specialists as report-only leaves (which therefore do not spawn cavecrew under
Ship). The
`punch-ai-governance` maintainer **never** listed in any `agents:` allowlist
(`disable-model-invocation: true`), so user-direct only; in Documentation
mode its single sanctioned delegation = `/graphify` map (1-deep), spawn no
other sub-agent.

## Worker capability bound (cavecrew ⊆ coordinator)

A coordinator may dispatch a cavecrew worker **only when the worker's `tools` are
a subset of the coordinator's `tools`** — workers never exceed the persona that
spawns them. So `cavecrew-builder` (`edit/editFiles`) is Build-only; the
read-only `punch-code-reviewer` / `punch-test-engineer` / `punch-security-auditor`
may dispatch read-only workers only. cavecrew inherits the owning persona's **skills + allowed paths by injected
brief** (VS Code custom agents have no skills frontmatter field — no static
inheritance). `punch-ai-governance` verifies the subset relation and that each
leaf carries an empty / absent `agents:` roster.
