---
name: punch-using-agent-skills
description: Discovers and invokes Punch agent skills. Use when starting a session or when you need to discover which skill applies to the current task. Meta-skill that governs how all other Punch skills are discovered and invoked, and how the Build phase delegates to engineers and cavecrew workers.
applies-to: meta — skill discovery + Build delegation across the whole lifecycle; not path-scoped
---

# Using Punch Agent Skills

Adopted-adapted from upstream `agent-skills/using-agent-skills`. Punch-scoped:
references only skills that exist under `.github/skills/`, mapped to the Punch
lifecycle **Spec → Plan → Build → Test → Review → Ship → Document**. Vendor file
stays as-is; this is the Punch adaptation.

## Overview

Punch skills sit on two axes — **domain** skills (one per subsystem, capped at
six) and **lifecycle/method** skills (adapted from upstream). This meta-skill
helps pick the right one for the task at hand. Index + rationale:
[`skill-registry.md`](../../../docs/ai/skill-registry.md).

## Skill discovery

Task arrives → find phase → apply skill. Punch slugs only:

```
Task arrives
    │
    ├── Vague idea, need variants? ───────→ punch-idea-refine
    ├── New feature/change, no spec? ─────→ punch-spec-driven-development
    ├── Have spec, need tasks? ───────────→ punch-planning-and-task-breakdown
    ├── Implementing code? ───────────────→ punch-incremental-implementation
    │   ├── Need repo/cross-file context? → punch-context-engineering
    │   ├── Coding against an API/doc? ───→ punch-source-driven-development
    │   └── High-stakes / unfamiliar? ────→ punch-doubt-driven-development
    │   Subsystem domain skill (pick one):
    │   ├── bin/punch, src/punch ─────────→ punch-python-orchestration
    │   ├── compose / Dockerfiles ────────→ punch-compose-runtime
    │   ├── k6 test (HTTP/Browser) ───────→ punch-k6-testing
    │   ├── artifact / report / state ────→ punch-data-harvest
    │   └── .github/** AI config ─────────→ punch-ai-governance
    ├── Writing/running tests? ───────────→ punch-test-driven-development
    │   └── Browser-based? ───────────────→ punch-browser-testing-with-devtools
    ├── Run broke? ───────────────────────→ punch-debugging-and-error-recovery
    ├── Reviewing a diff? ────────────────→ punch-code-review-and-quality
    │   ├── Too complex? ─────────────────→ punch-code-simplification
    │   ├── Security concern? ────────────→ punch-security-and-hardening
    │   └── Perf regression? ─────────────→ punch-performance-optimization
    ├── Committing / branching? ──────────→ punch-git-workflow-and-versioning
    ├── Logs / metrics / events? ─────────→ punch-observability-and-instrumentation
    ├── Recording a decision (ADR)? ──────→ punch-documentation-and-adrs
    └── Doc map / graph? ─────────────────→ graphify
```

## Build delegation (cavecrew)

In the Build phase, [`punch-builder`](../../agents/punch-builder.agent.md) is the
command-owned coordinator. It delegates the complete build to one engineer
(`punch-runtime-engineer` / `punch-performance-test-engineer`) and may hand
bounded, independently-verifiable packets to vendor cavecrew leaf workers
(`punch-cavecrew-investigator`, `punch-cavecrew-builder`, `punch-cavecrew-reviewer`). cavecrew is
an execution/delegation optimization — **not** a replacement for the skills
above. Workers are one level deep; they do not spawn sub-agents. Canon:
[`orchestration-patterns.md`](../../../docs/ai/punch-references/orchestration-patterns.md),
voice [`punch-build-caveman`](../punch-build-caveman/SKILL.md).

## Core operating behaviors (non-negotiable, all phases)

### 1. Surface assumptions

Before anything non-trivial, state assumptions:

```
ASSUMPTIONS:
1. [requirements] 2. [architecture] 3. [scope]
→ Correct now or I proceed with these.
```

Don't silently fill ambiguous requirements. Wrong-assumption-unchecked = top
failure mode. Surface early — cheaper than rework.

### 2. Manage confusion actively

Inconsistency / conflict / unclear spec → **STOP.** Don't guess. Name the
confusion. Present the tradeoff or ask. Wait for resolution.

**Bad:** silently pick one interpretation, hope. **Good:** "Spec says X, code
says Y — which wins?"

### 3. Push back when warranted

Not a yes-machine. Clear problem → point it out, quantify the downside ("+200ms
latency", not "maybe slower"), propose an alternative, accept an informed
override. Sycophancy = failure mode.

### 4. Enforce simplicity

Natural tendency overcomplicates — resist. Before finishing: fewer lines? do the
abstractions earn it? would a staff engineer say "why didn't you just…"? 1000
lines where 100 suffice = failure. Prefer boring + obvious.

### 5. Maintain scope discipline

Touch only what you're asked. Don't: remove comments you don't understand,
"clean up" orthogonal code, refactor adjacent systems, delete seemingly-unused
code without approval, add unrequested features. Surgical precision, not
renovation.

### 6. Verify, don't assume

Every skill has a verification step. Not complete until it passes. "Seems right"
never sufficient — need evidence (passing tests, build output, runtime data). In
Punch: not done until `reports/state/punch-run.json` records the run.

## Skill rules

1. **Check for an applicable skill before starting.** Skills encode processes
   that prevent common mistakes.
2. **Skills are workflows, not suggestions.** Follow steps in order; don't skip
   verification.
3. **Multiple skills apply.** A k6 change → `punch-k6-testing` +
   `punch-incremental-implementation` + `punch-test-driven-development`.
4. **When in doubt, start with a spec** (`punch-spec-driven-development`).
5. **State activation once** on entering a phase, then let persistence carry it
   — no per-message re-invocation.

## Failure modes to avoid

1. Wrong assumptions, unchecked. 2. Plowing ahead when lost. 3. Not surfacing
inconsistencies. 4. Not presenting tradeoffs. 5. Sycophancy on bad approaches.
6. Overcomplicating. 7. Editing orthogonal code/comments. 8. Removing what you
don't understand. 9. Building with no spec because "obvious". 10. Skipping
verification because "looks right".

## Quick reference

| Phase | Skill | One line |
|---|---|---|
| Spec | punch-idea-refine | Refine vague ideas, diverge then converge |
| Spec | punch-spec-driven-development | Requirements + acceptance criteria before code |
| Plan | punch-planning-and-task-breakdown | Decompose into small verifiable tasks |
| Build | punch-incremental-implementation | Thin vertical slices, verify each |
| Build | punch-context-engineering | Right context at the right time (Graphify gate) |
| Build | punch-source-driven-development | Verify against official docs before coding |
| Build | punch-doubt-driven-development | Adversarial fresh-context review of decisions |
| Build | punch-python-orchestration | `bin/punch` / `src/punch` CLI + subprocess |
| Build | punch-compose-runtime | Compose contracts, healthchecks, image pins |
| Build | punch-k6-testing | k6 HTTP/Browser shape, thresholds, summary |
| Build | punch-data-harvest | Artifact paths/schemas, report builder |
| Build | punch-ai-governance | `.github/**` frontmatter + registry consistency |
| Test | punch-test-driven-development | Failing test first, then make it pass |
| Test | punch-browser-testing-with-devtools | DevTools MCP runtime verification |
| Test | punch-debugging-and-error-recovery | Reproduce → localize → fix → guard |
| Review | punch-code-review-and-quality | Multi-axis review with quality gates |
| Review | punch-code-simplification | Cut complexity, preserve behavior |
| Review | punch-security-and-hardening | Input validation, least privilege |
| Review | punch-performance-optimization | Measure first, optimize what matters |
| Ship | punch-git-workflow-and-versioning | Atomic commits, clean history |
| Ship | punch-documentation-and-adrs | Document the why, not just the what |
| Ship | punch-observability-and-instrumentation | Structured logs, metrics, alerts |
| Document | graphify | Doc/dependency map (host tool, off evidence path) |
