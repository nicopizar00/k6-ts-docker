# Plan — PRESERVE Updated Context Engineering

> **Status:** **NEXT BIG MILESTONE — PRESERVE**
> **Prerequisite:** Complete and review the current native-Graphify migration
> first.

- **Goal:** Adopt and semantically preserve the latest upstream
  `context-engineering` method inside the correctly named
  `punch-context-engineering` skill.
- **Upstream baseline:** Addy Osmani `agent-skills` commit
  [`fea75b1`](https://github.com/addyosmani/agent-skills/commit/fea75b16472ba87e8c11f13a9e000c3ffdb2d1f5),
  SHA-256
  `ff9d4e5706bdd2eb7de1bfed569f1f42d28e478979ce6fcc32e617e7861b491d`.

Preservation is mandatory: every upstream section must be adapted, linked to
its canonical Punch owner, or explicitly excluded with rationale. Silent
omission blocks Review.

## Preservation contract

- Keep skill identity `punch-context-engineering`; do not introduce the
  misspelled `punch-contexct-engineering`.
- Keep it read-only, non-user-invocable, and activated once per phase by
  existing prompts and agents.
- Preserve all upstream concepts: triggers, five-level hierarchy,
  relevant-file checklist, trust levels, concise errors, conversation
  management, packing strategies, optional context tools, confusion handling,
  anti-patterns, red flags, and verification.
- Adapt generic examples to Punch concepts. Map inline planning to Spec/Plan
  checkpoints; never bypass approved Plan scope.
- Retain Punch lifecycle, architecture, domain-skill routing, and scope
  discipline.
- Keep Graphify fully decoupled: no Graphify gate, command, installation,
  ownership, or automatic routing.
- Add `references/upstream-parity.md` containing the source commit/hash and a
  section-by-section disposition ledger: `adapted-inline`, `linked`, or
  `excluded-with-rationale`.

## Tasks

### CE-01 — Build the preserved Punch adaptation

- **Goal:** Restore semantic parity with upstream while retaining Punch-specific
  lifecycle and architecture routing.
- **Allowed edit paths:**
  - `.github/skills/punch-context-engineering/**`
- **Read-only context paths:**
  - `.ai-upstream/agent-skills/skills/context-engineering/SKILL.md`
  - `.github/copilot-instructions.md`
  - `.github/prompts/**`
  - `.github/agents/**`
  - `docs/architecture/punch-boundaries.md`
  - `docs/ai/operating-model.md`
  - `docs/ai/scoped-build-policy.md`
- **Forbidden paths:**
  - `.ai-upstream/**` except the explicitly listed read-only source
  - `.github/skills/graphify/**`
  - `.github/prompts/**` and `.github/agents/**` except as read-only context
  - `ai.ingest/freeze/**`
  - `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`, `reports/**`
  - `.github/workflows/**`
- **Implementation:** Expand the skill and create the parity ledger. Generic
  React/Node examples may be replaced, but their underlying context-engineering
  concepts must remain. Fix procedure numbering and restore upstream triggers
  for session start, degraded output, task switching, and convention drift.
- **Expected diff size:** Approximately 180–300 lines.
- **Validation:** Compare every upstream section against the parity ledger;
  confirm zero unmapped sections; run `git diff --check`.
- **Rollback notes:** Revert the skill and parity ledger together.
- **Human checkpoint:** Human approval required before Build.
- **Build via:** `punch-ai-governance` documentation maintenance; no product
  engineer.

### CE-02 — Align discovery and registry language

- **Goal:** Make discovery describe the preserved project primer and
  context-recovery method without changing current phase activation.
- **Allowed edit paths:**
  - `.github/skills/punch-using-agent-skills/SKILL.md`
  - `docs/ai/skill-registry.md`
- **Read-only context paths:**
  - `.github/skills/punch-context-engineering/**`
  - `.github/prompts/**`
  - `.github/agents/**`
- **Forbidden paths:**
  - `.github/prompts/**` and `.github/agents/**` except as read-only context
  - `.github/skills/graphify/**`
  - `.ai-upstream/**`
  - `ai.ingest/freeze/**`
  - `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`, `reports/**`
  - `.github/workflows/**`
- **Implementation:** Describe `punch-context-engineering` as both the preserved
  project primer and context-recovery method. Retain phase-boundary activation
  and cross-file routing. Link to the parity ledger instead of duplicating it.
- **Expected diff size:** Approximately 15–40 lines.
- **Validation:** Confirm registry-to-skill parity and resolve every existing
  prompt/agent link; run `git diff --check`.
- **Rollback notes:** Revert CE-02 without reverting CE-01.
- **Human checkpoint:** Human approval required before Build.
- **Build via:** `punch-ai-governance` documentation maintenance; no product
  engineer.

### CE-03 — Enforce future preservation

- **Goal:** Make future upstream refreshes fail Review when preservation is
  incomplete or unauditable.
- **Allowed edit paths:**
  - `.github/skills/punch-ai-governance/SKILL.md`
- **Read-only context paths:**
  - `.github/skills/punch-context-engineering/**`
  - `.ai-upstream/agent-skills/skills/context-engineering/SKILL.md`
  - `docs/ai/skill-registry.md`
- **Forbidden paths:** Every other path.
- **Implementation:** Add a linked governance check requiring the preservation
  ledger for future Context Engineering refreshes. Review fails if the upstream
  commit/hash is missing, an upstream section is unaccounted, or an exclusion
  lacks rationale. Keep the detailed mapping solely in the parity ledger.
- **Expected diff size:** Approximately 10–25 lines.
- **Validation:** Run the read-only `punch-ai-governance` audit and confirm the
  preservation check passes without duplicating ledger content.
- **Rollback notes:** Revert the governance rule independently.
- **Human checkpoint:** Human approval required before Build.
- **Build via:** `punch-ai-governance` documentation maintenance; no product
  engineer.

## Order of execution

1. Complete and review the native-Graphify migration.
2. CE-01 — establish semantic parity and its durable ledger.
3. CE-02 — align discovery and registry language.
4. CE-03 — enforce the preservation invariant in governance.
5. Run the complete validation and governance gates.

## Test and acceptance plan

1. Confirm the Graphify migration is complete and governance-clean before
   CE-01.
2. Verify the local upstream source matches the pinned SHA-256.
3. Compare every upstream H2/H3 section against `upstream-parity.md`; require
   zero unmapped sections.
4. Confirm
   `rg -ni 'graphify|punch-graphify' .github/skills/punch-context-engineering`
   returns no matches.
5. Confirm all existing prompt/agent links resolve and activation remains once
   per phase.
6. Run `git diff --check` and a read-only `punch-ai-governance` audit.
7. Run `./bin/punch doctor` and `./bin/punch run smoke`; require
   `reports/state/punch-run.json` with `passed: true`.
8. Confirm `ai.ingest/freeze/**`, product code, workflows, and runtime contracts
   remain unchanged.

Acceptance requires semantic parity, correct skill identity, no Graphify
coupling, no broken callers, successful Punch evidence, and governance verdict
**clean**.

## Cross-cutting risks

- A lean rewrite may silently drop upstream methods. The parity ledger is the
  blocking preservation gate.
- Copying upstream text wholesale may duplicate Punch canon. Adapt or link
  concepts instead of restating existing rules.
- Generic inline planning could bypass Punch's approved Plan boundary. Map it
  explicitly to Spec/Plan handoff behavior.
- Optional context-tool guidance could accidentally auto-enable external tools.
  Preserve the concept while retaining Punch approval and security boundaries.
- Beginning before the Graphify migration lands would mix milestones and make
  provenance difficult to review.

## Rollback plan

Revert CE-03, CE-02, and CE-01 in reverse order. Keep this Plan as the record of
the deferred milestone. Do not rewrite the frozen upstream staging source or
`ai.ingest/freeze/**` to make a failed adaptation appear compliant.

## Assumptions

- “PRESERVE” means semantic parity with traceability, not near-verbatim
  duplication.
- This milestone follows, rather than overlaps or supersedes, the native-
  Graphify milestone.
- The upstream baseline verified on 2026-07-18 remains the implementation
  source unless a newer commit exists when CE-01 begins. If newer, update the
  pinned commit/hash and parity ledger before editing.

**Gate:** Approved when the human confirms the prerequisite and task scope,
then executed CE-01 → CE-02 → CE-03 through `punch-ai-governance` before Test
and Review.
