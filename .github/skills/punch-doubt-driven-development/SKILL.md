---
name: punch-doubt-driven-development
description: Subjects every non-trivial or high-stakes decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, in unfamiliar code, or when a change is irreversible (Postgres schema, reporting contract, service rename, exit-code/evidence logic).
applies-to: lifecycle/Plan + Build — invoked on non-trivial/high-stakes decisions; not path-scoped
---

# Doubt-Driven Development

## In Punch

An in-flight posture (distinct from the Review phase, which is a verdict on a
finished diff): non-trivial decisions get cross-examined while course-correction is
still cheap. It reinforces Punch's existing **"stop and return to Plan"** rule on
scope expansion and high-stakes work. The "fresh-context reviewer" in Punch is a
**separate review pass**, not a programmatic subagent:

- a new Copilot Chat session given only ARTIFACT + CONTRACT (no prior reasoning), or
- the `@punch-code-reviewer` / `@punch-security-auditor` custom agent invoked on the artifact, or
- a **user-authorized** cross-model review (paste elsewhere / a CLI the user runs).

High-stakes in Punch: Postgres schema or `init.sql` changes, reporting-contract
(artifact path/schema) changes, Compose service renames, exit-code/evidence logic
in the orchestrator — anything you can't undo with `git revert`.

## Overview

A confident answer is not a correct one. Long sessions turn assumptions into
"facts" unnoticed. Materialize a fresh-context reviewer — biased to **disprove** —
before any non-trivial output stands.

## When to Use

A decision is **non-trivial** when at least one holds: it adds/modifies branching
logic; crosses a layer boundary; asserts a property the compiler can't verify
(ordering, idempotence, an invariant); its correctness depends on context a future
reader can't see; or its blast radius is irreversible.

**When NOT to use:** mechanical ops (rename/format/move), clear unambiguous
instructions, reading/summarizing code, one-line obvious changes, or when the user
asked for speed. If you doubt every keystroke, you ship nothing.

## The Process

```
- [ ] CLAIM      — wrote the claim + why-it-matters
- [ ] EXTRACT    — isolated artifact + contract, stripped reasoning
- [ ] DOUBT      — ran a fresh-context adversarial review
- [ ] RECONCILE  — classified every finding against the artifact text
- [ ] STOP       — trivial findings, 3 cycles, or user override
```

### 1. CLAIM — surface what stands
Name the decision in 2-3 lines + why it matters. Example: *"CLAIM: the new
`handleSummary` schema is backward-compatible with the CI validation job. WHY:
a break silently fails the artifact-transfer gate."* If you can't write it
compactly, you have a vibe, not a decision.

### 2. EXTRACT — smallest reviewable unit
Hand the reviewer the **artifact** (the diff/function) + the **contract** (what it
must satisfy) — not your reasoning. If you hand over conclusions, you get back
validation of your conclusions. Decompose anything too big to hold in one read.

### 3. DOUBT — fresh-context adversarial review
Run the review with an **adversarial** prompt — framing decides the answer:

```
Adversarial review. Find what is wrong with this artifact. Assume the author is
overconfident. Look for: unstated assumptions, unhandled edge cases, hidden
coupling/shared state, ways the contract is violated, Punch conventions it breaks
(layer ownership, evidence contract), failure modes under unexpected input.
Do NOT validate. Do NOT summarize. Find issues, or state you found none after
thorough examination.
ARTIFACT: <paste>   CONTRACT: <paste>
```

**Pass ARTIFACT + CONTRACT only — never the CLAIM** (it biases toward agreement).
Run it in a fresh Copilot session or via `@punch-code-reviewer`/`@punch-security-auditor`.
A **cross-model** second opinion catches blind spots a single model shares with
itself — offer it for high-stakes artifacts, but only the user authorizes running
an external tool, and only with ARTIFACT + CONTRACT (no session context).

### 4. RECONCILE — fold findings back
You are still the orchestrator; re-read the artifact against each finding before
classifying (first match wins): **contract misread** (fix the contract, re-loop) →
**valid + actionable** (change it, re-loop) → **valid trade-off** (document it for
the user) → **noise** (correct under context the reviewer lacked; note it).

### 5. STOP — bounded, not recursive
Stop when the next cycle yields only trivial/known findings, after 3 cycles
(escalate, don't grind a 4th), or when the user says "ship it". If 3 cycles still
surface substantive issues, that's information — surface it; don't keep looping. If
3 feels "obviously insufficient", the artifact is too big — decompose (Step 2).

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'm confident, skip it" | Confidence correlates poorly with correctness on novel problems. Certainty is where blind spots hide. |
| "A review pass is expensive" | Debugging a wrong commit (or a broken reporting contract) is more expensive. The check is bounded; the bug isn't. |
| "I'll doubt at Review instead" | Review is the final gate. Doubt catches wrong directions early, when course-correction is cheap. |
| "The reviewer disagreed, so I was wrong" | The reviewer lacks your context — disagreement is information, not verdict. Re-read, classify, decide. |

## Red Flags

- Running a fresh-context review for a one-line rename or formatting change.
- Treating reviewer output as authoritative without re-reading the artifact.
- Looping >3 cycles without escalating.
- Prompting "is this good?" instead of "find issues".
- Passing the CLAIM (or your reasoning) to the reviewer.
- Running a cross-model CLI without explicit user authorization.

## Interaction with Other Skills

- `punch-code-review-and-quality` (Review) — post-hoc diff verdict; doubt-driven is
  in-flight per-decision. Use both.
- `punch-test-driven-development` — a failing k6 check (the RED step) *is* the doubt step
  for a behavioral claim.
- `punch-source-driven-development` — verifies framework *facts*; doubt-driven verifies
  *your reasoning* about the artifact.
- `punch-debugging-and-error-recovery` — when the reviewer surfaces a real failure mode,
  drop into it to localize and fix.

## Verification

- [ ] Each non-trivial/high-stakes decision was named as a CLAIM before standing.
- [ ] A fresh-context adversarial review ran on ARTIFACT + CONTRACT (not the CLAIM/reasoning).
- [ ] Findings were classified against the artifact (not rubber-stamped).
- [ ] A stop condition was met (trivial / 3 cycles / user override).
- [ ] Any external cross-model tool was run only with explicit user authorization.
