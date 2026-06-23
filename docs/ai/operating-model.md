# AI Operating Model

This file define **how** AI changes flow through Punch.
For **rules** about what code may look like, see `CLAUDE.md` and
path-specific instructions under `.github/instructions/`.

(Was `operating-protocol.md`. Rename part of redesigned
lifecycle: Spec → Plan → Build → Test → Review → Ship — Spec absorb
former Define clarify step.)

## Foundational principle

> AI may explore broadly to understand. AI may plan structurally to
> delimit. AI may only build inside explicit scoped boundary. AI
> must verify through Punch's official runtime contract. AI must not
> expand implementation scope without returning to planning.

Single sentence whole operating model shaped around.

## The six phases

| Phase | Purpose | Mode | Edits allowed |
|---|---|---|---|
| Spec     | Clarify/refine request (former Define), then translate into goals, non-goals, constraints | Ask | Only spec doc, if requested |
| Plan     | Produce scoped tasks with allowed / read-only / forbidden paths | Ask (Plan discipline) | Only plan doc, if requested |
| Build    | Implement one approved task within declared scope | Agent (scoped) | Yes — only allowed paths |
| Test     | Run official Punch commands, confirm evidence (`punch-test` RED→GREEN) | Agent / Ask | Only if patching change |
| Review   | Read-only critique of diff against plan | Ask | No |
| Ship     | Commit, push, open PR; **human merges** | Agent (mechanical only) | Yes (git/gh only) |

Each phase has matching prompt under `.github/prompts/`. See
[`prompt-registry.md`](prompt-registry.md) for what each does and
[`workflow.md`](workflow.md) for walkthrough.

## Four kinds of AI asset

Punch's AI config use four distinct artifact types. Not
interchangeable.

| Kind | Lives in | Answers | Lifetime |
|---|---|---|---|
| **Instructions** | `.github/instructions/` (path-scoped) and `CLAUDE.md` (global) | "What rules apply when I touch this code?" | Long — change rarely. |
| **Prompts** | `.github/prompts/` | "How do I run *this phase* of the lifecycle?" | Long — one per phase/domain. |
| **Skills** | `.github/skills/<skill>/SKILL.md` | "What does an expert in *this domain or method* always do?" | Long — domain skills (one per subsystem) + lifecycle skills (one per method). |
| **Agents** | `.github/agents/` | "Which behavioral profile fits *this phase*?" | Long — one per persona. |

Rule of thumb: **instructions** passive (loaded whenever file
touched). **Prompts** active (human runs them). **Skills**
behavioral (prompt or agent activates them). **Agents** persona
constraints (which tools, which mode, which handoff rules) — bounded at runtime
by shared [`agent-guards.md`](agent-guards.md) discipline.

## Permission boundaries

- **No edits in Ask Mode.** If phase say Ask, agent reads and writes
  prose — not files.
- **Plan output is the plan, not edits.** Plan doc itself is
  artifact. Build refuse to edit files outside plan's allowed list.
- **Build is scoped.** Each Build prompt declares allowed / read-only /
  forbidden paths. Scope expansion → stop, return to Plan.
- **Test uses official Punch commands.** No ad-hoc `docker run`. No host
  `k6` or `npm`. See [`docs/architecture/punch-boundaries.md`](../architecture/punch-boundaries.md).
- **Ship is mechanical only.** Commits, push, `gh pr create`. No merges, no
  tags, no force pushes, no skipping hooks.

## Validation gates

Change cannot advance until gate met.

| Transition | Gate |
|---|---|
| Spec → Plan | Clear, narrowed problem statement (former Define gate), then goals, non-goals, acceptance criteria documented. |
| Plan → Build | Plan approved by human; allowed paths listed. |
| Build → Test | Focused diff inside plan's allowed paths. |
| Test → Review | `reports/state/punch-run.json` with `passed: true` (or equivalent named artifact for non-test changes). |
| Review → Ship | Review verdict = Approve. |
| Ship → done | Human-merged PR. |

Mechanical steps: see [`../workflows/validation.md`](../workflows/validation.md).

## Adopting this in a team

1. **Start with one phase.** Most teams under-do Plan, over-do Build.
   Begin by enforcing "no Build without Plan" for one sprint.
2. **One persona per role, not one agent per ticket.** Agents in
   `.github/agents/` (core personas, `punch-builder` dispatcher + its two
   engineers, on-demand specialists like `punch-security-auditor`, `punch-code-reviewer` and
   `punch-ai-governance` maintainer) reusable across all work. Resist adding
   new core persona without killing one.
3. **Promote prompts, not prose.** When you paste same
   guidance into chat repeatedly, that's missing prompt — file small PR.
4. **Audit before adding.** New skill / new agent / new prompt should answer:
   *which existing one could not absorb this?* If answer fuzzy, don't add.

## Avoiding agent sprawl

This redesign deliberately moved from 3-skill cap to six-domain-skill setup
with small agent roster (core personas + `punch-builder` dispatcher and its
two engineers + `punch-security-auditor` and `punch-ai-governance` specialists). Ceiling
enforced by *function*, not *count*:

- **Domain skills** must each name unique Punch subsystem (context,
  orchestration, runtime, performance, artifacts, governance). Six is
  full domain set; adding more should require killing one.
- **Lifecycle skills** separate axis — engineering methods adapted from
  upstream `agent-skills` set (idea-refine, spec-driven-development, …).
  Not subject to domain cap, but each must name unique method, avoid
  duplicating domain skill or path-instruction, and be registered when added.
  Phase prompt *activates* lifecycle skill; phase does not become one.
- Each **agent** is **core persona** (`punch-architect` Spec+Plan,
  `punch-test-engineer` Test, `punch-code-reviewer` Review, `punch-release-captain`
  Ship), **`punch-builder` dispatcher** or one of its two **engineers**
  (`punch-runtime-engineer`, `punch-performance-test-engineer` — split by Build
  domain), an on-demand **specialist persona** (`punch-security-auditor`,
  `punch-ai-governance`), or a bounded **`cavecrew-*` leaf worker**. New core
  persona should require killing one; specialists each name unique on-demand lens.
- Each **prompt** is single lifecycle phase (Build's per-domain scope lives in
  engineers, not extra prompts). New prompts must show why existing one
  cannot stretch.

`punch-ai-governance` skill checks new additions against this rule
during Review. Skill axes and absorption process detailed in
[`skill-registry.md`](skill-registry.md) and
[`agent-skills-absorption-plan.md`](history/agent-skills-absorption-plan.md).

## Where this differs from a generic agent setup

- Orchestrator is **Python stdlib only**. No agent should suggest adding
  Python dependency.
- Execution chain **strictly linear**: TS → bundle (in Docker) →
  k6 image → run → reports. Do not branch it.
- CI/CD is **external** to Punch. Punch provides reusable local/CI-compatible
  container contracts; does not own GitHub Actions workflows.

## Drift control

- Run `punch-ai-governance` (via Review phase) before merging any PR
  touching `.github/` or `docs/ai/`.
- Update `skill-registry.md` and `prompt-registry.md` in same PR that
  adds or removes asset.
- `CLAUDE.md` is constitution. If rule moves, moves there; this
  file only describes lifecycle.
