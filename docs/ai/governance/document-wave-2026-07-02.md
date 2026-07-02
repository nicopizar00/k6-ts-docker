---
wave: document-2026-07-02
scope: F-008 + F-009 — queued governance findings from wave-2026-06-28
status: complete — both findings closed
owner: punch-ai-governance
graph: existing baseline reused — no rebuild (gate rule 2; narrow scope)
---

# Document Wave — 2026-07-02

**Steps complete:** Map & Gather (1) · Classify (2) · Reconcile (3) · Record (4)\
**Evidence source:** governance audit 2026-07-02 (frontmatter / parity / link
sweep script) + direct source re-verification. Graphify gate decision: graph
exists and scope is two enumerated findings → no rebuild, no `--update`; source
files validate (gate rules 2 + 4).

## Findings

| ID | Classification | source_location | Decision | Applied edit |
|---|---|---|---|---|
| F-008 | partial (registry coverage) | `.github/skills/punch-ai-governance/SKILL.md` step 2 · agents `punch-cavecrew-builder` / `-investigator` / `-reviewer` / `punch-security-auditor` | keep + align wording — a phase coordinator's `agents:` roster is a valid agent reference; orphan detection preserved (referenced nowhere → flag) | step-2 bullet extended |
| F-009 | partial (vocabulary variance) | same skill, step 3 · several `.github/agents/*.agent.md` | keep + align wording — boundary declared via literal Allowed/Forbidden sections **or** `Scope`/`Boundary` + `Guards (per agent-guards.md)` | step-3 bullet rewritten, cross-links `agent-guards.md` |

## Decisions

- Rejected for F-008: a sub-agent roster line in `copilot-instructions.md` —
  duplicates roster canon already in coordinator agent files.
- Rejected for F-009: renaming sections in ~8 agent files to literal
  Allowed/Forbidden — restates what `agent-guards.md` centralizes.
- Untrusted-by-default check: both audit claims re-verified against source
  before any edit.
- Registry impact: none — the `punch-ai-governance` row in
  `docs/ai/skill-registry.md` still describes the skill accurately.

## Queue

Documentation debt closed for this scope. Nothing queued for the next wave.
