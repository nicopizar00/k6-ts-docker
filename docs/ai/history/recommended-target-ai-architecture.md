# Recommended Target AI Architecture

> **Reconciled 2026-06-17 (post-restructure).** Skills-home decision
> (`.github/skills/`) and two-axis model below hold. Since written, prompt/agent
> layer executed different than phased plan implied: prompts command-mapped,
> lifecycle now **6 phases** (Spec absorbs Define), Build persona became
> **5-member builder family** (9 agents), prompt frontmatter is
> **`agent:`**, not `mode:`. Treat `mode:` / "7-phase" mentions below as
> historical. Canonical record:
> [`agent-skills-absorption-plan.md` § Execution status](agent-skills-absorption-plan.md).

> **Status:** Review artifact (no runtime AI config changed). Made
> 2026-06-16 on branch `feat/agent-skills`. Proposed end state +
> safest path to it. Nothing built yet.

## Design goals (in priority order)

1. **Copilot-first.** Primary runtime = GitHub Copilot Chat in VS Code.
2. **Skill-first execution, prompt-thin.** Procedure lives in skills; prompts
   thin entry points; instructions always-on rules.
3. **One home per concept.** No rule restated across layers
   (`copilot-instructions.md:74-76`).
4. **Punch constraints win on stack; upstream wins on method.**
5. **Claude Code + Codex stay compatible** without contaminating Copilot layer.

## Decisions ratified (2026-06-16)

- **Skills home: `.github/skills/`** (current location — **no migration**).
  Already Copilot-valid (`copilot-setup.md:7`); lifecycle skills added here
  beside existing domain skills. `.agents/skills/` **not** adopted as runtime
  home; if Codex-native discovery ever needed, can be thin mirror, but out of
  scope. Read every `.agents/skills/` reference in other review docs as
  **`.github/skills/`**.
- **Scope of next work: full absorption planned** in
  [`agent-skills-absorption-plan.md`](agent-skills-absorption-plan.md) (its 7
  *implementation* phases — distinct from 6 *lifecycle* phases).

## Target folder structure

```
.
├── CLAUDE.md                         # Constitution (canonical architecture + rules)
├── AGENTS.md                         # Minimal cross-agent contract → points at skills
├── .github/
│   ├── copilot-instructions.md       # Always-on global rules (short)
│   ├── instructions/                 # Path-scoped Punch rules (the override layer)
│   │   └── *.instructions.md         # (7 existing — keep)
│   ├── prompts/                      # Thin lifecycle entry points (agent: + delegate)
│   │   └── *.prompt.md
│   ├── agents/                       # Copilot custom personas (*.agent.md)
│   │   └── *.agent.md
│   └── skills/                       # CANONICAL skill core (decided — stays here)
│       ├── <domain skills>/          # Punch subsystems (6 existing — keep)
│       └── <lifecycle skills>/       # Adapted upstream methodology skills (new)
├── .claude/                          # Claude-only harness/config (optional skills mirror)
├── docs/ai/                          # Governance, registries, migration rationale (this folder)
└── .ai-upstream/agent-skills/        # Provenance — never edited, never the runtime
```

### Why `.github/skills/` (decided)
- **Zero migration churn:** 6 domain skills, every prompt/agent reference,
  `skill-registry.md`, `maintenance-matrix.md` row 12, `punch-context` keep
  pointing at same paths. Lifecycle skills just added here.
- Already **Copilot-valid** (`copilot-setup.md:7`), matches Punch's existing
  governance, which audits `.github/skills/*/SKILL.md`
  (`punch-governance-review/SKILL.md:65-67`).
- **Considered and not taken:** `.agents/skills/` (tool-neutral, Codex-native)
  adds portability but needs cascade-heavy relocation PR for zero Copilot
  benefit. If Codex-native discovery ever needed, mirror — don't move.

## Role of each layer

| Layer | Answers | Owns | Does NOT own |
|---|---|---|---|
| `CLAUDE.md` | "What is the architecture and the law?" | Constitution; canonical rules; execution chain. Keep current role. | Lifecycle procedure (links to `docs/ai/`). |
| `.github/copilot-instructions.md` | "What rules apply to every Copilot session?" | Short critical rules, ownership table, entry-point table, universal core behaviors. | Procedural workflows (those skills). |
| `.github/instructions/` | "What rules apply when I touch *this path*?" | Punch stack constraints — the **override layer** beating generic skill examples. | Methodology (that skills). |
| `.github/prompts/` | "How do I run *this phase*?" | Thin wrappers: `agent:` (binds custom agent), phase, scope, **activate skill**, Punch overrides. | The procedure itself (delegated to skills). |
| `.github/agents/` | "Which persona/tooling fits *this phase*?" | 5 Punch personas + adapted `security-auditor`; scope + handoff rules. | Cross-persona orchestration (prompts do that). |
| `.github/skills/` | "What does an expert in *this domain/method* always do?" | **Domain skills** (Punch subsystems) + **lifecycle skills** (adapted upstream). The *how*. | Stack rules (link to instructions) or phase gating (prompts/agents). |
| `AGENTS.md` | "Minimal contract for any coding agent (Codex…)?" | Pointers to CLAUDE.md, operating-model, `.github/skills/`. | Restated lifecycle/agent tables. |
| `docs/ai/` | "Why shaped this way? How does it change?" | Governance, registries, model selection, migration ADRs, these review docs. | Runtime behavior. |
| validation script | "Is config internally consistent?" | Frontmatter/registry/cross-ref checks — **stdlib Python or folded into `punch-governance-review`** (no host Node). | — |

## The two-axis skill model (the key reconciliation)

```
Skills
├── Domain skills  → "what an expert in this Punch SUBSYSTEM does"
│   punch-context · punch-python-orchestration · punch-docker-compose
│   punch-k6-performance · punch-data-harvest · punch-governance-review
└── Lifecycle skills → "what an expert in this METHOD does"  (adapted upstream)
    idea-refine · spec-driven-development · planning-and-task-breakdown
    incremental-implementation · test-driven-development(k6) ·
    debugging-and-error-recovery · code-review-and-quality ·
    code-simplification · git-workflow-and-versioning · …
```
A **prompt** (phase) activates **one lifecycle skill** (method) **+ relevant
domain skill** (Punch specifics). This how skill-first execution coexists with
Punch's phase/scope governance.

Governance update needed: reframe `skill-registry.md` cap from "6" to
"6 domain + N lifecycle", refine `operating-model.md`'s "phases are not
skills" into "phases are prompts+agents that *activate* lifecycle skills."

## Implementation order

> **Expanded into per-phase scoped tasks in
> [`agent-skills-absorption-plan.md`](agent-skills-absorption-plan.md).**
> Summary below stays high-level map.

Dogfood Punch's own lifecycle (Spec → Plan → Build → Verify → Review → Ship) for
each step. Each step small, reviewable PR.

### Phase 0 — Review (this pass) ✅
- These six `docs/ai/*` documents. No runtime change.

### Phase 1 — Fix existing drift + ratify governance *(P1, unblocks everything)*
1. Register `idea-refine` in `skill-registry.md`; add `applies-to:`; remove
   `/mnt/skills/...` path. (`punch-refine.prompt.md` later **deleted** —
   idea-refine runs inside `punch-spec`; prompt frontmatter `agent:`, not `mode:`.)
2. Edit `operating-model.md` + `skill-registry.md` to introduce **two-axis
   skill model** and reframe cap (C1 resolution).
3. Run `punch-governance-review` → clean baseline.
> Rationale: copying more skills before this only multiplies `idea-refine`
> drift. **Do not skip.**

### Phase 2 — Skills home *(decided — no work)*
4. **Decided 2026-06-16: keep `.github/skills/`.** No migration. Lifecycle skills
   added here in Phase 3. (`.agents/skills/` considered and not taken.)

### Phase 3 — Absorb Tier-A lifecycle skills (adapted) *(P2)*
5. In small batches, adapt + register: `spec-driven-development`,
   `planning-and-task-breakdown`, `incremental-implementation`,
   `test-driven-development` (k6/evidence), `debugging-and-error-recovery`,
   `code-review-and-quality`, `code-simplification`,
   `git-workflow-and-versioning`. Add `documentation-and-adrs`,
   `security-and-hardening`, `doubt-driven-development`, `source-driven-development`
   as P3.

### Phase 4 — Slim prompts to delegate *(P2)*
6. Rewrite `punch-spec/plan/review` (+ Build prompts) as thin wrappers that
   activate matching lifecycle skill + domain skill (Track 2). Add new
   thin `punch-simplify` prompt.

### Phase 5 — Agents *(P3)*
7. Add adapted `security-auditor.agent.md`. Fold upstream `code-reviewer` into
   `punch-reviewer`. Exclude `test-engineer`, `web-performance-auditor`.

### Phase 6 — Fold overlaps, exclude non-fits *(P3)*
8. Merge `context-engineering`→`punch-context`,
   `observability-and-instrumentation`→`punch-data-harvest`, salvage
   `performance-optimization`→`punch-k6-performance`. **Exclude**
   `ci-cd-and-automation`, `frontend-ui-engineering`,
   `browser-testing-with-devtools`, `webperf`.

### Phase 7 — Contracts, index, validator *(P3)*
9. Slim `AGENTS.md` to pointer contract; add skill-discovery pointer to
   `CLAUDE.md`; build Punch skill index (adapted `using-agent-skills`);
   reimplement `validate-skills.js` as stdlib Python or fold into
   `punch-governance-review`. Final governance pass.

## Acceptance for the absorption as a whole
- [ ] `punch-governance-review` reports **clean** (every skill/prompt/agent
      registered; frontmatter complete; no duplicated rule; cross-refs resolve).
- [ ] No host `npm`/`k6`/`pip` introduced; `.github/skills/` has no `/mnt/...`
      or `subagent_type` leakage into Copilot layer.
- [ ] Each absorbed skill names its `applies-to` and defers stack specifics to
      `.github/instructions/`.
- [ ] `punch-ship` still mechanical; CI/CD stays external.
- [ ] Worked task (e.g. "add a k6 threshold") flows Spec→Ship using lifecycle
      skill + domain skill, producing `reports/state/punch-run.json`.
