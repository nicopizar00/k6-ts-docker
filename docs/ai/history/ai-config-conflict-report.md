# AI Configuration — Conflict & Duplication Report

> **Reconciled 2026-06-17 (post-restructure).** Part-4 drift items
> (`idea-refine`/`punch-refine` unregistered) now **resolved** — `idea-refine`
> registered, `punch-refine` deleted. Correction to C7/contract claims: VS Code
> prompt frontmatter is **`agent:`**, not `mode:` — so `mode:`-vs-`agent:`
> contradiction reconciled toward `agent:` (prompts right; contract docs were
> drift, now fixed). Canonical record:
> [`agent-skills-absorption-plan.md` § Execution status](agent-skills-absorption-plan.md).

> **Status:** Review artifact (no runtime AI config changed). Made
> 2026-06-16 on branch `feat/agent-skills`. Every item cites files inspected
> this pass. "Winner" applies brief's Decision Policy.

## Part 1 — Contradictions (must be resolved before absorption)

### C1 — Skill-first vs prompt-first / the 6-skill cap *(central conflict)*
- **Upstream:** skill-driven; "If a task matches a skill, you MUST invoke it …
  Never implement directly if a skill applies" (`.ai-upstream/.../AGENTS.md:16-18`).
  24 skills, discovery via `using-agent-skills`.
- **Punch:** prompt-driven; "**Lifecycle phases are prompts and agents, not
  skills.** Creating them would invert operating model"
  (`skill-registry.md:60`); hard cap of **6** domain skills
  (`skill-registry.md:1`, `operating-model.md:94-99`).
- **Why matters:** Absorbing `spec-driven-development`,
  `planning-and-task-breakdown`, `incremental-implementation`, etc. as skills
  forbidden by Punch's current rules, breaches cap.
- **Resolution:** Add **second skill axis**. Punch's 6 are *domain*
  skills ("what expert in this Punch subsystem does"); upstream's are
  *lifecycle/methodology* skills ("what expert in this method does"). Reframe
  cap as **"6 domain skills + N lifecycle skills"**, refine
  "phases are not skills" rule to "*phase* still prompt+agent, but
  *method* it runs is lifecycle skill it activates." Prompts stay thin,
  **delegate** procedure to lifecycle skill (skill-first execution, prompt
  as entry point).
- **Winner:** **Upstream lifecycle methodology** for *how* (Decision policy
  #2), **inside Punch's phase/scope governance** for *when/where* (Decision
  policy #1). Needs editing `skill-registry.md` + `operating-model.md` first
  (P1).

### C2 — "Ship" semantics
- **Upstream:** `/ship` = parallel fan-out to `code-reviewer` +
  `security-auditor` + `test-engineer`, then go/no-go **with deploy/rollback**
  (`commands/ship.md:7-64`; `shipping-and-launch` skill).
- **Punch:** Ship **mechanical only** — "Commits, push, `gh pr create`. No
  merges, no tags … **humans merge**" (`operating-model.md:29,63`;
  `copilot-instructions.md:16`).
- **Resolution:** Map upstream `shipping-and-launch` / `/ship` review fan-out to
  Punch's **Review** phase (critique + go/no-go). Keep `punch-ship`
  mechanical. Deploy/rollback content mostly N/A (CI/CD external; humans
  merge).
- **Winner:** **Punch** for Ship boundary (Decision policy #1); upstream
  review methodology relocated to Review.

### C3 — CI/CD ownership
- **Upstream:** `ci-cd-and-automation` skill authors GitHub Actions, deploy
  pipelines, feature flags, rollback workflows (`SKILL.md:57-269`).
- **Punch:** "**CI/CD is external.** `.github/workflows/` consumes Punch; Punch
  does not extend own ownership into CI"
  (`punch-architecture.instructions.md:36`); Build forbids `.github/workflows/`
  (`copilot-instructions.md:47-48`).
- **Resolution:** **Exclude** `ci-cd-and-automation` from core. If ever needed,
  keep as clearly-marked external reference only.
- **Winner:** **Punch** (Decision policy #1).

### C4 — Meaning of "test" / "verify"
- **Upstream:** `test-driven-development` = unit tests via `npm test`,
  jest/vitest; build "passes" = green tests (`test/SKILL.md`, `commands/test.md`).
- **Punch:** "tests" are **k6** perf tests run container-first; verification is
  `./bin/punch` + `reports/state/punch-run.json` with `passed:true`; "unit tests
  only as complement, not replacement" (`copilot-instructions.md:61-62`,
  `workflow.md:93-112`).
- **Resolution:** Adapt TDD skill: keep **Prove-It / failing-first**
  discipline, but bind "evidence" to k6 checks/thresholds + `punch-run.json`.
- **Winner:** **Punch** evidence model (Decision policy #1); upstream Prove-It
  *pattern* retained.

### C5 — Stack defaults in skill examples
- **Upstream:** assumes web/Node — e.g. spec assumes "This is a web application"
  and `npm run build` (`spec-driven-development/SKILL.md:42,56-61`);
  `performance-optimization` is Core Web Vitals + React.
- **Punch:** Docker-first, Python stdlib, k6; no frontend; no host npm
  (`copilot-instructions.md:13-14`).
- **Resolution:** During adaptation, replace example commands with Punch
  commands; rely on path-instructions as stack authority. Exclude purely
  web skills (Tier C).
- **Winner:** **Punch** (Decision policy #1).

### C6 — `/build auto` autonomy
- **Upstream:** `/build auto` runs **whole plan** after single approval
  (`commands/build.md:27-42`).
- **Punch:** "Each Build invocation executes **one** task ID"; human confirms
  plan before Build (`copilot-mode-mapping.md:50-53`,
  `scoped-build-policy.md:20-27`).
- **Resolution:** Drop `auto` mode when adapting `/build`.
- **Winner:** **Punch** (Decision policy #1).

### C7 — Frontmatter contract for SKILL.md
- **Upstream:** SKILL.md frontmatter is `name` + `description` only
  (`skill-anatomy.md:23-28`).
- **Punch:** governance requires `name`, `description`, **`applies-to`**
  (`agentic-workflow.instructions.md:50`, `punch-governance-review/SKILL.md:62`).
- **Resolution:** Add `applies-to:` to each absorbed skill during adaptation.
- **Winner:** **Punch** contract in Copilot layer (Decision policy #3).

### C8 — Multi-agent fan-out availability
- **Upstream:** assumes programmatic subagent fan-out (`subagent_type`, Agent
  Teams) (`commands/ship.md:13-26`, `docs/agents.md:106-115`).
- **Copilot reality:** custom agents invoked via `@mention`; no equivalent
  programmatic parallel fan-out (`copilot-setup.md:35-38`).
- **Resolution:** In Copilot layer, Review invokes personas sequentially via
  `@mention`. Document Claude's fan-out in `CLAUDE.md`/`.claude/` only.
- **Winner:** **Copilot compatibility** in Copilot layer (Decision policy #3).

## Part 2 — Duplications (consolidate to one home)

### D1 — Universal "core behaviors"
- Upstream `using-agent-skills` core behaviors — surface assumptions, manage
  confusion, push back, enforce simplicity, scope discipline, verify-don't-assume
  (`SKILL.md:44-127`) — overlap Punch's agentic rules
  (`copilot-instructions.md:38-55`) and operating-model principle
  (`operating-model.md:10-17`).
- **Resolution:** Keep canonical statement in `copilot-instructions.md`
  (always-on). Skill index *references* it; absorbed skills do not restate
  it. **Winner:** Punch global instructions (single always-on home).

### D2 — Lifecycle table restated in 3 files
- Define→…→Ship table + agent list + "rules for AI assistants" appear in
  `AGENTS.md:84-102`, `copilot-instructions.md:78-91`, and `operating-model.md`.
- **Resolution:** Canonical in `operating-model.md`; `copilot-instructions.md`
  keeps short entry-point table; `AGENTS.md` links instead of restating.
  **Winner:** `operating-model.md` (canonical), per `copilot-instructions.md:74-76`
  ("No duplication of AI guidance").

### D3 — `idea-refine` duplicated upstream ↔ Punch (verbatim)
- `.github/skills/idea-refine/**` **byte-identical** to
  `.ai-upstream/.../skills/idea-refine/**` (SKILL.md + 4 supporting files; `diff`
  confirmed this pass).
- **Resolution:** Treat `.github/skills/idea-refine` (adapted) as single
  runtime copy; `.ai-upstream/` stays provenance only. Register it.
  **Winner:** one adapted runtime copy.

### D4 — Five-axis review in skill + agent + prompt
- `code-review-and-quality` skill, `code-reviewer` agent, and `commands/review.md`
  all enumerate same five axes; Punch also has `punch-reviewer` +
  `punch-review` prompt.
- **Resolution:** Axes live **once** in `code-review-and-quality` skill;
  agent and prompt reference it. Merge upstream `code-reviewer` into
  `punch-reviewer` rather than add parallel persona.
  **Winner:** skill is single source of *how*.

## Part 3 — Inconsistent guidance across Copilot / Claude Code / Codex

| Topic | Copilot would read | Claude Code would read | Codex would read | Fix |
|---|---|---|---|---|
| Where skills live | `.github/skills/` (current) | `.claude/skills/` (native) or in-repo | `.agents/skills/` (native) | **Keep `.github/skills/`** (decided 2026-06-16); Copilot reads it (`copilot-setup.md:7`); Codex can mirror to `.agents/skills/` only if ever needed |
| Whether skills mandatory | "No duplication" + prompt-driven (`copilot-instructions.md`) | Upstream "MUST invoke" (`.ai-upstream/AGENTS.md:16`) | Upstream `AGENTS.md` skill-driven | Unify on "if task matches skill, use it" in `AGENTS.md`, governed by Punch phases |
| Ship behavior | mechanical (`punch-ship`) | upstream `/ship` fan-out + deploy | upstream `shipping-and-launch` | C2 resolution: fan-out → Review; Ship stays mechanical everywhere |
| Agent invocation | `@agent` (`*.agent.md`) | `subagent_type` / Agent Teams | varies | Copilot layer uses `@mention`; Claude specifics in `CLAUDE.md` |
| `idea-refine` status | unregistered skill + off-contract prompt | Claude command with `argument-hint` + `/mnt` path | unregistered | **Resolved:** registered + `applies-to` added + `/mnt` removed; `punch-refine` deleted (idea-refine runs inside `punch-spec`) |

## Part 4 — Existing internal Punch drift (independent of upstream)

These already violate Punch's **own** governance rules; fix first:

1. **`idea-refine` skill unregistered** — breaks "every `SKILL.md` has registry
   row" (`punch-governance-review/SKILL.md:65-67`). Registry lists 6; disk has 7.
2. **`punch-refine` prompt unregistered + off-contract** — **RESOLVED 2026-06-17:**
   `punch-refine` deleted (idea-refine now runs inside `punch-spec`); and
   verified prompt frontmatter field is `agent:`, not `mode:`.
3. **`AGENTS.md` duplication** of lifecycle/agent/skill content (D2 above).

> **Bottom line:** absorption *philosophically aligned* (same 3-layer
> model, near-isomorphic lifecycle) but *governance-blocked* by three things —
> 6-skill cap + "phases-are-not-skills" rule (C1), Ship/CI/test
> semantic clashes (C2–C4), frontmatter contract (C7). Resolve C1 and
> Part-4 drift **first**; rest is mechanical adaptation.
