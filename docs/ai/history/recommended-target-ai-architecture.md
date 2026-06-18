# Recommended Target AI Architecture

> **Reconciled 2026-06-17 (post-restructure).** The skills-home decision
> (`.github/skills/`) and two-axis model below hold. Since written, the prompt/agent
> layer was executed differently than the phased plan implied: prompts are
> command-mapped, the lifecycle is **6 phases** (Spec absorbs Define), the Build
> persona became a **5-member builder family** (9 agents), and prompt frontmatter
> is **`agent:`**, not `mode:`. Treat `mode:` / "7-phase" mentions below as
> historical. Canonical record:
> [`agent-skills-absorption-plan.md` § Execution status](agent-skills-absorption-plan.md).

> **Status:** Review artifact (no runtime AI config changed). Produced
> 2026-06-16 on branch `feat/agent-skills`. This is the proposed end state and
> the safest path to it. Nothing here is built yet.

## Design goals (in priority order)

1. **Copilot-first.** The primary runtime is GitHub Copilot Chat in VS Code.
2. **Skill-first execution, prompt-thin.** Procedure lives in skills; prompts are
   thin entry points; instructions are always-on rules.
3. **One home per concept.** No rule restated across layers
   (`copilot-instructions.md:74-76`).
4. **Punch constraints win on stack; upstream wins on method.**
5. **Claude Code + Codex stay compatible** without contaminating the Copilot
   layer.

## Decisions ratified (2026-06-16)

- **Skills home: `.github/skills/`** (current location — **no migration**).
  Already Copilot-valid (`copilot-setup.md:7`); lifecycle skills are added here
  alongside the existing domain skills. `.agents/skills/` is **not** adopted as
  the runtime home; if Codex-native discovery is ever needed it can be a thin
  mirror, but it is out of scope. Every `.agents/skills/` reference in the other
  review docs should be read as **`.github/skills/`**.
- **Scope of next work: the full absorption is planned** in
  [`agent-skills-absorption-plan.md`](agent-skills-absorption-plan.md) (its 7
  *implementation* phases — distinct from the 6 *lifecycle* phases).

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
- **Zero migration churn:** the 6 domain skills, every prompt/agent reference,
  `skill-registry.md`, `maintenance-matrix.md` row 12, and `punch-context` keep
  pointing at the same paths. Lifecycle skills are simply added here.
- Already **Copilot-valid** (`copilot-setup.md:7`) and matches Punch's existing
  governance, which audits `.github/skills/*/SKILL.md`
  (`punch-governance-review/SKILL.md:65-67`).
- **Considered and not taken:** `.agents/skills/` (tool-neutral, Codex-native)
  would add portability but requires a cascade-heavy relocation PR for no
  Copilot benefit. If Codex-native discovery is ever needed, mirror — don't move.

## Role of each layer

| Layer | Answers | Owns | Does NOT own |
|---|---|---|---|
| `CLAUDE.md` | "What is the architecture and the law?" | The constitution; canonical rules; execution chain. Keep its current role. | Lifecycle procedure (links to `docs/ai/`). |
| `.github/copilot-instructions.md` | "What rules apply to every Copilot session?" | Short critical rules, ownership table, entry-point table, universal core behaviors. | Procedural workflows (those are skills). |
| `.github/instructions/` | "What rules apply when I touch *this path*?" | Punch stack constraints — the **override layer** that beats generic skill examples. | Methodology (that is skills). |
| `.github/prompts/` | "How do I run *this phase*?" | Thin wrappers: `agent:` (binds a custom agent), phase, scope, **activate a skill**, Punch overrides. | The procedure itself (delegated to skills). |
| `.github/agents/` | "Which persona/tooling fits *this phase*?" | 5 Punch personas + adapted `security-auditor`; scope + handoff rules. | Cross-persona orchestration (prompts do that). |
| `.github/skills/` | "What does an expert in *this domain/method* always do?" | **Domain skills** (Punch subsystems) + **lifecycle skills** (adapted upstream). The *how*. | Stack rules (link to instructions) or phase gating (prompts/agents). |
| `AGENTS.md` | "Minimal contract for any coding agent (Codex…)?" | Pointers to CLAUDE.md, operating-model, and `.github/skills/`. | Restated lifecycle/agent tables. |
| `docs/ai/` | "Why is it shaped this way? How does it change?" | Governance, registries, model selection, migration ADRs, these review docs. | Runtime behavior. |
| validation script | "Is the config internally consistent?" | Frontmatter/registry/cross-ref checks — **stdlib Python or folded into `punch-governance-review`** (no host Node). | — |

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
A **prompt** (phase) activates **one lifecycle skill** (the method) **+ the
relevant domain skill** (the Punch specifics). This is how skill-first execution
coexists with Punch's phase/scope governance.

Governance update required: reframe `skill-registry.md` cap from "6" to
"6 domain + N lifecycle", and refine `operating-model.md`'s "phases are not
skills" into "phases are prompts+agents that *activate* lifecycle skills."

## Implementation order

> **Expanded into per-phase scoped tasks in
> [`agent-skills-absorption-plan.md`](agent-skills-absorption-plan.md).** The
> summary below remains the high-level map.

Dogfood Punch's own lifecycle (Spec → Plan → Build → Verify → Review → Ship) for
each step. Each step is a small, reviewable PR.

### Phase 0 — Review (this pass) ✅
- These six `docs/ai/*` documents. No runtime change.

### Phase 1 — Fix existing drift + ratify governance *(P1, unblocks everything)*
1. Register `idea-refine` in `skill-registry.md`; add `applies-to:`; remove the
   `/mnt/skills/...` path. (`punch-refine.prompt.md` was later **deleted** —
   idea-refine runs inside `punch-spec`; prompt frontmatter is `agent:`, not `mode:`.)
2. Edit `operating-model.md` + `skill-registry.md` to introduce the **two-axis
   skill model** and reframe the cap (C1 resolution).
3. Run `punch-governance-review` → clean baseline.
> Rationale: copying more skills before this only multiplies the `idea-refine`
> drift. **Do not skip.**

### Phase 2 — Skills home *(decided — no work)*
4. **Decided 2026-06-16: keep `.github/skills/`.** No migration. Lifecycle skills
   are added here in Phase 3. (`.agents/skills/` considered and not taken.)

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
   activate the matching lifecycle skill + domain skill (Track 2). Add a new
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
9. Slim `AGENTS.md` to a pointer contract; add the skill-discovery pointer to
   `CLAUDE.md`; build the Punch skill index (adapted `using-agent-skills`);
   reimplement `validate-skills.js` as stdlib Python or fold into
   `punch-governance-review`. Final governance pass.

## Acceptance for the absorption as a whole
- [ ] `punch-governance-review` reports **clean** (every skill/prompt/agent
      registered; frontmatter complete; no duplicated rule; cross-refs resolve).
- [ ] No host `npm`/`k6`/`pip` introduced; `.github/skills/` has no `/mnt/...`
      or `subagent_type` leakage into the Copilot layer.
- [ ] Each absorbed skill names its `applies-to` and defers stack specifics to
      `.github/instructions/`.
- [ ] `punch-ship` is still mechanical; CI/CD remains external.
- [ ] A worked task (e.g. "add a k6 threshold") flows Spec→Ship using a lifecycle
      skill + a domain skill, producing `reports/state/punch-run.json`.
