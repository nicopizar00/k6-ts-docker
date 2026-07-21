# Plan — Copilot-only Caveman default

Implements `docs/specs/spec-copilot-caveman-default.md`. Saved beside its Spec
in `docs/specs/` (not `docs/architecture/specs/`, which does not exist in this
repo) — same precedent as `plan-decouple-punch-build-from-caveman.md`,
`plan-native-graphify-copilot.md`, `plan-context-engineering-preservation.md`.

- **Goal:** Make upstream Caveman the concise-prose default for VS Code GitHub
  Copilot Chat only, relocate its project skill to the Copilot-documented
  location, retire the portable cross-agent copy and the `punch-comms-policy`
  adapter, and strip every Caveman activation surface outside Copilot Chat —
  without touching Build, product code, or Punch lifecycle authority.

## Invariants and acceptance criteria

(mirrors the Spec's acceptance criteria 1–9 verbatim as this Plan's contract)

1. Exactly one active project skill named `caveman`, at
   `.github/skills/caveman/SKILL.md`; no active copy under
   `.agents/skills/caveman/` or `.claude/skills/`.
2. That skill declares `user-invocable: true` and
   `disable-model-invocation: true`, stays reachable via `/caveman`, and is not
   auto-loaded from prompt relevance alone.
3. `.github/copilot-instructions.md` makes `lite` the VS Code Copilot Chat
   default, honors explicit mode/stop overrides, preserves evidence verbatim,
   excludes Build.
4. `AGENTS.md`, `CLAUDE.md`, `.claude/**` contain no Caveman activation, mode,
   skill-path, or obsolete `punch-build-caveman` instruction.
5. No live reference to `punch-comms-policy` remains after retirement; its
   essential evidence/clarity constraints survive in the Copilot rule.
6. Registries, governance checks, and upstream docs agree on skill name,
   Copilot-only location, invocation controls, and source.
7. Build prompts/agents contain no Caveman dependency; normal prose unchanged.
8. `git diff --check` passes; a Punch AI-governance review reports no broken
   links, duplicate activation blocks, orphaned skills, or stale references.
9. `./bin/punch doctor` / `./bin/punch run smoke` remain available; when run,
   `reports/state/punch-run.json` exists with `passed: true`.

Pinned vendor hashes (must be unchanged after AI-01 relocates the skill body):

| Asset | SHA-256 |
|---|---|
| `.agents/skills/caveman/SKILL.md` (pre-move) | `e38ec671ecbee47ce234190be12615daf60ac667d775b7340d49d07f4f63c7bc` |
| `.agents/skills/caveman/README.md` (pre-move) | `95b62190565e0d5b21ced563cf36c0f549abe1ceceff540914102481c9c5849c` |
| `.agents/skills/cavecrew/SKILL.md` (untouched, out of scope) | `b74f374f6aae6e9a31e78e7d876860406fe5833378e9298536edf176c12f379b` |
| `.agents/skills/cavecrew/README.md` (untouched, out of scope) | `965622be25416e1c59d0f69edf359dceeebdf2fa650c3fd5c254081045f27c12` |

## Non-goals

(same as Spec — repeated for the Build-time contract)

- No rename of the skill/command to `punch-caveman` / `/punch-caveman`.
- No Caveman activation for Claude Code, Codex, Cursor, Windsurf, Copilot CLI,
  Copilot coding agent, or any host but VS Code GitHub Copilot Chat.
- No upstream unified installer / `--with-init` run.
- No change to Punch lifecycle authority, phase ownership, tool access,
  delegation, evidence requirements, or verdicts.
- No Caveman in the `punch-build` chain.
- No product code / Compose / k6 / workflow / report-schema change.
- No decision on Cavecrew removal — `.agents/skills/cavecrew/**` stays exactly
  as-is, untouched by every task below.
- **Explicitly out of scope, flagged not fixed:** `.claude/commands/*.md` and
  `.claude/skills/guard/SKILL.md` also name stale, non-existent agent files
  (`punch-planner.agent.md`, `punch-architect-readonly.agent.md`,
  `punch-reviewer.agent.md` — the real files are `punch-architect.agent.md` and
  `punch-code-reviewer.agent.md`). That drift is unrelated to Caveman and
  predates this Spec (noted as a known residual in
  `plan-decouple-punch-build-from-caveman.md`). AI-03 below touches only the
  Caveman-specific lines in those same files; it must not "fix while there"
  the agent-name drift — that needs its own Spec/Plan.

## Tasks

### AI-01 — Relocate the `caveman` project skill to the Copilot location

- **Goal:** Move the vendor skill body (verbatim) from the portable copy to
  `.github/skills/caveman/SKILL.md`, add the two Copilot access-control
  frontmatter fields, retire the portable copy, and update governance's
  adopted-vendor exemption list so the new location isn't flagged as an
  unregistered authored asset.
- **Allowed edit paths:**
  - `.github/skills/caveman/SKILL.md` (create)
  - `.github/skills/caveman/README.md` (create, optional — companion doc only)
  - `.agents/skills/caveman/SKILL.md` (delete)
  - `.agents/skills/caveman/README.md` (delete)
- **Read-only context paths:**
  - `.ai-upstream/caveman/**` (local upstream provenance snapshot)
  - `.github/skills/graphify/**` (sibling adopted-upstream skill — same
    frontmatter-adaptation pattern: only `user-invocable`/
    `disable-model-invocation` are Punch additions)
- **Forbidden paths:**
  - `.agents/skills/cavecrew/**`, `.ai-upstream/**` (write)
  - Every path not explicitly allowed above
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`, `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - Copy `SKILL.md` body unchanged; add only `user-invocable: true` and
    `disable-model-invocation: true` to frontmatter. Diff against the pinned
    hash above must show only the two added frontmatter lines.
  - `README.md` may move as a companion doc; no content change beyond fixing
    its self-referential relative link if the directory depth changes.
  - Do not touch `.github/skills/punch-ai-governance/SKILL.md`'s adopted-scope
    paragraph here — that edit is bundled into AI-04 (same paragraph also
    drops the `punch-comms-policy` sentence; one task owns the whole
    paragraph to avoid split edits).
- **Acceptance criteria:**
  - `.github/skills/caveman/SKILL.md` exists with both required frontmatter
    fields; upstream body otherwise byte-identical to the pinned pre-move hash
    plus the two added lines.
  - `.agents/skills/caveman/` no longer exists (both files removed).
  - `.agents/skills/cavecrew/**` hashes unchanged.
- **Expected diff size:** ~130–160 lines (mostly move: delete + re-add).
- **Validation commands:**
  - `test ! -e .agents/skills/caveman && echo retired`
  - `test -f .github/skills/caveman/SKILL.md && grep -c 'user-invocable: true\|disable-model-invocation: true' .github/skills/caveman/SKILL.md` → `2`
  - `shasum -a 256 .agents/skills/cavecrew/SKILL.md .agents/skills/cavecrew/README.md` → matches pinned hashes above.
- **Rollback notes:** Restore both `.agents/skills/caveman/` files from git
  history; delete `.github/skills/caveman/`.
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration
  maintenance; never `punch-build`.

### AI-02 — Make Copilot's Caveman rule the self-contained default

- **Goal:** Rewrite the existing Caveman block in
  `.github/copilot-instructions.md` into one short, self-contained rule:
  `lite` default for VS Code Copilot Chat prose, explicit `/caveman <mode>` /
  `stop caveman` overrides, Build excluded, evidence/security/architecture
  content always normal prose — folding in the essential constraints that
  `punch-comms-policy` currently carries, ahead of its retirement in AI-04.
- **Allowed edit paths:**
  - `.github/copilot-instructions.md`
- **Read-only context paths:**
  - `.github/skills/caveman/SKILL.md` (post AI-01)
  - `.github/skills/punch-comms-policy/SKILL.md` (source of the constraints
    being folded in, ahead of its own deletion)
- **Forbidden paths:**
  - Every path not explicitly allowed above (this task does not touch Critical
    Rules elsewhere in the same file — only the Caveman section)
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`, `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - Keep the block short — do not require loading the full `SKILL.md` for the
    default `lite` behavior; explicit slash invocation is the path to heavier
    modes (per Spec Technical constraints).
  - State plainly: never compresses code, commands, paths, logs, errors, exit
    codes, thresholds, JSON/YAML/CSV, acceptance criteria, blockers, next
    actions, or `reports/state/punch-run.json`; drops to normal prose for
    security/irreversible/architecture/ambiguous content; Build is fully
    decoupled (link, don't restate, the existing Build-independence rule).
  - Drop the outbound `punch-comms-policy` link — this file becomes the sole
    remaining canon for Copilot Caveman voice.
- **Acceptance criteria:**
  - Block reads as a single self-contained default-`lite` rule (no
    dependency on loading `SKILL.md` to take effect).
  - No reference to `punch-comms-policy` remains in this file.
  - Explicit mode/stop-override behavior and Build exclusion both stated.
- **Expected diff size:** ~15–35 lines (rewrite in place).
- **Validation commands:**
  - `rg -n 'punch-comms-policy' .github/copilot-instructions.md` → no matches.
  - `rg -n 'lite' .github/copilot-instructions.md` → present in the Caveman section.
  - `git diff --check`
- **Rollback notes:** Revert this file's Caveman section independently; does
  not depend on AI-01/03/04/05 landing first (though AI-04 depends on this one).
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration
  maintenance.

### AI-03 — Strip Caveman activation from non-Copilot surfaces

- **Goal:** Remove every Caveman activation, mode, skill-path, or obsolete
  `punch-build-caveman` instruction from `AGENTS.md` and `.claude/**`, without
  touching any other Guard-bridge or agent-boundary content in those files.
- **Allowed edit paths:**
  - `AGENTS.md`
  - `.claude/commands/spec.md`
  - `.claude/commands/plan.md`
  - `.claude/commands/build.md`
  - `.claude/commands/test.md`
  - `.claude/commands/review.md`
  - `.claude/commands/ship.md`
  - `.claude/commands/document.md`
  - `.claude/commands/init.md`
  - `.claude/skills/guard/SKILL.md`
  - `docs/ai/decisions/0004-claude-code-guard-bridge.md`
- **Read-only context paths:**
  - `CLAUDE.md` (verify only — already has zero Caveman references)
  - `.github/copilot-instructions.md` (post AI-02, for the one permitted
    Copilot-only pointer, if any is kept)
- **Forbidden paths:**
  - Every path not explicitly allowed above
  - Any agent-name correction unrelated to Caveman (see Non-goals — the
    `punch-planner.agent.md` / `punch-architect-readonly.agent.md` /
    `punch-reviewer.agent.md` drift stays untouched)
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`, `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - `AGENTS.md`: delete the "Caveman comms" section entirely (currently one
    paragraph). A bare, non-instructional pointer ("Caveman is a VS Code
    Copilot Chat-only convenience; not active here — see
    `.github/copilot-instructions.md`") is allowed since it carries no
    activation/mode instruction; restating levels or `/caveman` syntax is not.
  - Each `.claude/commands/*.md`: delete its
    `Caveman: <level> (canon: .github/skills/punch-build-caveman/SKILL.md)`
    line. This also removes the dangling `punch-build-caveman` path (deleted
    upstream in `1a7c152`) as a side effect — no separate cleanup needed.
  - `.claude/skills/guard/SKILL.md`: remove the "Caveman level" column from
    the wiring-map table and its header note; remove step 3
    ("Apply the Caveman canon…"); remove/adjust the "Do not hard-overwrite the
    global caveman config" line and the "Caveman is output style only" bullet
    if they become orphaned by the column removal. Leave persona/tool/scope
    resolution logic (columns 1–3 of the table, all No-break rules) untouched.
  - `docs/ai/decisions/0004-claude-code-guard-bridge.md`: update the two spots
    describing the bridge applying "the optional Caveman comms canon
    (`punch-comms-policy`)" and the wiring-map "Caveman level" column to match
    the now-Caveman-free wrap (mirror the guard/SKILL.md edit above; this is a
    historical-decision record of *current* bridge behavior, not a frozen
    point-in-time log, so it must track the live wrap).
- **Acceptance criteria:**
  - Zero case-insensitive `caveman` activation/mode/skill-path matches in
    `AGENTS.md` or any `.claude/**` file, except an optional bare non-activation
    pointer in `AGENTS.md`.
  - Zero matches for `punch-build-caveman` anywhere in `.claude/**` or
    `AGENTS.md`.
  - `CLAUDE.md` confirmed already clean (no edit needed, but validated).
  - Guard's wiring-map table still resolves prompt + persona for all 8
    commands (Caveman column removed, others intact).
- **Expected diff size:** ~45–75 lines, mostly deletions across 11 files.
- **Validation commands:**
  - `rg -ni 'caveman' AGENTS.md CLAUDE.md .claude/` → only the optional bare
    pointer in `AGENTS.md`, if kept; no `.claude/**` matches.
  - `rg -n 'punch-build-caveman' AGENTS.md CLAUDE.md .claude/ docs/ai/decisions/0004-claude-code-guard-bridge.md` → no matches.
  - `git diff --check`
- **Rollback notes:** Revert AI-03 as one commit; independent of AI-04/05.
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration
  maintenance.

### AI-04 — Retire `punch-comms-policy`; reconcile every remaining reference

- **Goal:** Delete the now-redundant `punch-comms-policy` skill (its essential
  content already folded into `copilot-instructions.md` by AI-02) and remove
  every other live reference to it, without restating its rules elsewhere.
  Bundle in the one governance adopted-vendor-scope paragraph update that
  reflects both this retirement and AI-01's relocation.
- **Allowed edit paths:**
  - `.github/skills/punch-comms-policy/` (delete, whole directory)
  - `.github/agents/punch-ai-governance.agent.md`
  - `.github/agents/punch-architect.agent.md`
  - `.github/agents/punch-cavecrew-investigator.agent.md`
  - `.github/agents/punch-cavecrew-reviewer.agent.md`
  - `.github/agents/punch-code-reviewer.agent.md`
  - `.github/agents/punch-release-captain.agent.md`
  - `.github/agents/punch-security-auditor.agent.md`
  - `.github/agents/punch-test-engineer.agent.md`
  - `.github/prompts/punch-document.prompt.md`
  - `.github/prompts/punch-init.prompt.md`
  - `.github/prompts/punch-plan.prompt.md`
  - `.github/prompts/punch-review.prompt.md`
  - `.github/prompts/punch-ship.prompt.md`
  - `.github/prompts/punch-spec.prompt.md`
  - `.github/prompts/punch-test.prompt.md`
  - `.github/skills/punch-ai-governance/SKILL.md`
- **Read-only context paths:**
  - `.github/copilot-instructions.md` (post AI-02 — the new sole voice canon)
  - `.github/skills/caveman/SKILL.md` (post AI-01)
  - `docs/ai/agent-guards.md`
- **Forbidden paths:**
  - `.github/prompts/punch-build.prompt.md`, `.github/agents/punch-builder.agent.md`,
    `.github/agents/punch-runtime-engineer.agent.md`,
    `.github/agents/punch-performance-test-engineer.agent.md` (already
    Caveman-free since `1a7c152`; touching them here would be a regression)
  - `docs/ai/skill-registry.md`, `.github/.ai-upstream/README.md` (owned by AI-05)
  - `AGENTS.md`, `.claude/**` (owned by AI-03)
  - Every other path not explicitly allowed above
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`, `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - Delete `.github/skills/punch-comms-policy/SKILL.md`.
  - In each of the 8 agent files: drop the "Caveman comms" footer's
    `punch-comms-policy` link. Keep any inline per-phase voice note the agent
    already states about itself (e.g., "Plan is per-phase `full`") as a plain
    fact, not a restatement of policy — do not copy the retired skill's rule
    text into these files (no duplication).
  - In each of the 7 prompt files: drop the "Canon: `punch-comms-policy`"
    fragment from the "Operating comms" line; keep the rest of that line
    (phase name, level) if the prompt already states its own level inline.
  - `.github/skills/punch-ai-governance/SKILL.md` "Frozen / adopted scope"
    paragraph: remove the `punch-comms-policy` "authored adaptation, subject
    to all checks" sentence (it no longer exists); narrow the
    `.agents/skills/**` exemption to `.agents/skills/cavecrew/**` (caveman no
    longer lives there); add `.github/skills/caveman/**` to the
    adopted-upstream-exempt set alongside `.github/skills/graphify/**`, noting
    the same "only `user-invocable`/`disable-model-invocation` are Punch
    additions" pattern already documented for graphify.
- **Acceptance criteria:**
  - `.github/skills/punch-comms-policy/` no longer exists.
  - No live reference to `punch-comms-policy` remains in any allowed file.
  - `.github/skills/caveman/**` is explicitly listed as adopted-upstream and
    exempt from authored-canon duplication/frontmatter/stale-asset checks;
    `.agents/skills/cavecrew/**` remains exempt under its own narrowed line.
  - No agent/prompt file restates the retired skill's rule text verbatim.
- **Expected diff size:** ~150–250 lines (one skill-directory deletion + ~16
  small reference edits).
- **Validation commands:**
  - `rg -rn 'punch-comms-policy' .github docs AGENTS.md CLAUDE.md .claude` → no matches (excluding this Plan and the Spec themselves, and the frozen `plan-decouple-punch-build-from-caveman.md` historical record).
  - `test ! -e .github/skills/punch-comms-policy && echo retired`
  - `rg -n 'caveman' .github/skills/punch-ai-governance/SKILL.md` → shows `.github/skills/caveman/**` in the adopted-upstream-exempt line.
  - `git diff --check`
- **Rollback notes:** Restore `.github/skills/punch-comms-policy/` from git
  history and revert the reference edits together as one commit.
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration
  maintenance.

### AI-05 — Update registries and the upstream manifest for the new location

- **Goal:** Make `docs/ai/skill-registry.md` and
  `.github/.ai-upstream/README.md` (plus Init's own description of the
  AI-Skills step) describe `caveman`'s Copilot-only location, the frontmatter
  adaptation, the manual relocate-after-install step, and the absence of any
  cross-host installation — and drop their `punch-comms-policy` rows.
- **Allowed edit paths:**
  - `docs/ai/skill-registry.md`
  - `.github/.ai-upstream/README.md`
  - `.github/prompts/punch-init.prompt.md`
- **Read-only context paths:**
  - `.github/skills/caveman/SKILL.md` (post AI-01)
  - `.github/skills/punch-ai-governance/SKILL.md` (post AI-04, for the
    matching adopted-scope wording)
  - `.ai-upstream/caveman/UPSTREAM.md`
- **Forbidden paths:**
  - Every path not explicitly allowed above
  - `.agents/skills/**`, `.ai-upstream/**` (write)
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`, `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - `skill-registry.md`: change the `caveman` row's path from
    `.agents/skills/caveman/SKILL.md` to `.github/skills/caveman/SKILL.md`;
    update the "Files changed by installer" / install-location prose to state
    that the upstream installer still drops `caveman` at
    `.agents/skills/caveman/` (it has no knowledge of `.github/skills/`) and
    that Punch performs one manual relocate step (move + add the two
    frontmatter fields) immediately after install; keep the `cavecrew` row
    pointing at `.agents/skills/cavecrew/SKILL.md`, unchanged. Delete the
    `punch-comms-policy` row.
  - `.github/.ai-upstream/README.md`: update the `caveman` table row and the
    "Install (manual, Copilot-scoped)" section to include the relocate step;
    state plainly that only VS Code GitHub Copilot Chat is supported and no
    other host config is written. `cavecrew` row/instructions unchanged.
  - `punch-init.prompt.md` AI-Skills step (~lines 52–67): update the stated
    install location for `caveman` to `.github/skills/caveman/` (post-relocate)
    while `cavecrew` stays at `.agents/skills/cavecrew/`; keep the existing
    "adopted verbatim, only frontmatter host-adaptation" framing, now applying
    it the same way it already does for `graphify`.
- **Acceptance criteria:**
  - `skill-registry.md` and `.ai-upstream/README.md` agree on `caveman`'s path,
    describe the relocate step, and carry no `punch-comms-policy` row.
  - `punch-init.prompt.md`'s AI-Skills step names the correct post-relocate
    path for `caveman` and the unchanged path for `cavecrew`.
  - No instruction anywhere implies installing `caveman` for any host besides
    VS Code GitHub Copilot Chat.
- **Expected diff size:** ~40–70 lines across 3 files.
- **Validation commands:**
  - `rg -n '\.agents/skills/caveman' docs/ai/skill-registry.md .github/.ai-upstream/README.md .github/prompts/punch-init.prompt.md` → no matches (cavecrew's own `.agents/skills/cavecrew` references are unaffected and expected).
  - `rg -n 'punch-comms-policy' docs/ai/skill-registry.md .github/.ai-upstream/README.md` → no matches.
  - `git diff --check`
- **Rollback notes:** Revert AI-05 as one commit; independent of AI-01–04
  landing (registry text references files that must already exist at review
  time, so this task runs last).
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration
  maintenance.

## Order of execution

1. **AI-01** — relocate the skill so later tasks can reference its final path.
2. **AI-02** — author the self-contained Copilot default rule (needs AI-01's
   path; must land before AI-04 deletes its source material).
3. **AI-03** — strip non-Copilot activation surfaces (independent of AI-02/04,
   sequenced here for reviewability, one governance-config PR at a time).
4. **AI-04** — retire `punch-comms-policy` now that AI-02 holds its essential
   content; also updates the adopted-vendor exemption paragraph for AI-01's
   new path.
5. **AI-05** — update registries/manifest last, once the final paths and
   governance wording from AI-01/04 are settled.
6. Run the complete validation gate below.

## Complete validation gate

```bash
# 1. Vendor integrity (cavecrew untouched; caveman moved with only frontmatter added)
shasum -a 256 .agents/skills/cavecrew/SKILL.md .agents/skills/cavecrew/README.md
test ! -e .agents/skills/caveman && echo "caveman portable copy retired"
grep -c 'user-invocable: true\|disable-model-invocation: true' .github/skills/caveman/SKILL.md   # expect 2

# 2. No Caveman outside Copilot Chat
rg -ni 'caveman' AGENTS.md CLAUDE.md .claude/
rg -n 'punch-build-caveman' . --glob '!docs/specs/plan-decouple-punch-build-from-caveman.md' --glob '!.git'

# 3. punch-comms-policy fully retired
rg -rn 'punch-comms-policy' .github docs AGENTS.md CLAUDE.md .claude \
  --glob '!docs/specs/spec-copilot-caveman-default.md' \
  --glob '!docs/specs/plan-copilot-caveman-default.md' \
  --glob '!docs/specs/plan-decouple-punch-build-from-caveman.md'

# 4. Build stays vendor-free (regression check on 1a7c152's work)
rg -ni 'caveman|cavecrew|wenyan|punch-comms-policy' \
  .github/prompts/punch-build.prompt.md \
  .github/agents/punch-builder.agent.md \
  .github/agents/punch-runtime-engineer.agent.md \
  .github/agents/punch-performance-test-engineer.agent.md

# 5. Formatting + governance
git diff --check
```

Expected: `rg` calls in steps 2–4 report no matches (exit `1`); step 1's
`grep -c` reports `2`. Then run the read-only `punch-ai-governance` audit —
require clean frontmatter, registry parity, cross-reference, duplication, and
adopted-scope results. Finally:

```bash
./bin/punch doctor
./bin/punch run smoke
```

Require `reports/state/punch-run.json` with `passed: true`.

## Cross-cutting risks

- **Hidden coupling:** Caveman/`punch-comms-policy` references are spread
  across 20+ files (agents, prompts, skills, registries, `.claude/**`,
  `AGENTS.md`, an ADR). The repo-wide `rg` sweeps in the validation gate are
  what actually prevent a partial migration — do not skip them because one
  task "looked complete."
- **Governance self-reference:** AI-04 edits
  `.github/skills/punch-ai-governance/SKILL.md`'s own audit-rule paragraph.
  Get this exactly right — an under-scoped exemption will make every future
  Init/Document pass flag `.github/skills/caveman/` as an unregistered
  authored asset; an over-broad one could silently exempt a real future
  authored skill.
- **Residual `.claude/` drift left untouched on purpose:** AI-03 fixes only
  Caveman lines in `.claude/**`. The pre-existing wrong-agent-filename drift
  (`punch-planner.agent.md` etc., see Non-goals) stays broken after this Plan
  — flag it to the human as a separate follow-up Spec, don't let Build "fix
  it while there."
- **Order dependency between AI-02 and AI-04:** if AI-04 runs before AI-02
  lands, the essential clarity/evidence constraints get deleted with no
  destination — AI-04 must verify AI-02's rewrite is already in
  `copilot-instructions.md` before deleting `punch-comms-policy`.
- **Registry/manifest drift if AI-05 runs early:** registry text describing
  the relocated path would reference a file that doesn't exist yet if AI-05
  runs before AI-01. Keep the stated execution order.

## Rollback plan

Revert AI-05, AI-04, AI-03, AI-02, AI-01 in reverse order — each is one
AI-configuration-only commit touching `.github/`, `docs/ai/`, `AGENTS.md`, or
`.claude/**`. No product or runtime rollback is required. `.agents/skills/
cavecrew/**` is never touched by any task, so it needs no rollback
consideration. If only `.agents/skills/caveman/` needs restoring, `git
checkout` it from the commit before AI-01 and delete
`.github/skills/caveman/`.

## Assumptions

- The human's request to produce this Plan confirms the Spec's direction but
  does not itself authorize implementation — explicit Plan approval is still
  required before any AI-0x task starts (per the Spec's own Gate).
- "`.github/skills/` is the Copilot-documented project-skill location" is
  taken as given from the Spec's Source constraints (VS Code Agent Skills
  docs) — this Plan does not re-verify that claim against the vendor docs;
  Build should if the human wants an extra check before AI-01.
- A bare, non-instructional Caveman pointer left in `AGENTS.md` (stating the
  capability exists but is Copilot-only, with no activation/mode/path detail)
  satisfies AC4's "no activation… instruction" bar; if the human instead wants
  `AGENTS.md` to mention Caveman not at all, that is a one-line narrowing of
  AI-03's acceptance criteria, not a new task.
- "Reconciled into the single Copilot instruction block" (FR9) means the
  *rules* move to `copilot-instructions.md`; it does not require every agent
  file to strip its own inline per-phase voice note (e.g., "Plan is `full`")
  — only the outbound link to the retired skill.

**Gate:** Plan approved when the human confirms the five task contracts,
their allowed/read-only/forbidden paths, and the execution order above.
Implementation then proceeds AI-01 → AI-02 → AI-03 → AI-04 → AI-05 through
`punch-ai-governance`, followed by Test and Review. Humans merge.
