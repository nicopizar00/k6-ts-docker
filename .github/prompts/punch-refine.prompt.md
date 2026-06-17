---
name: idea-refine
description: Refine a raw idea into a clear, testable direction using the idea-refine skill.
argument-hint: the idea, feature, product direction, or problem to refine
---

Follow the **idea-refine** skill at `.github/skills/idea-refine/SKILL.md` exactly.

Use the user-provided argument as the raw idea to refine. If no idea was provided, ask for it in one concise question.

This command is for **idea refinement only**. Do not implement code, create files, edit files, or generate a build plan unless the skill explicitly requires it and the user confirms.

Ground the refinement in observable evidence:

* Use actual user input, actual repository context, and actual files inspected.
* If you inspect files, name the files or directories you used as evidence.
* If you cannot confirm something from user input or runtime/repository state, say so.
* Do not present assumptions as facts.
* Push back on weak, vague, over-complex, or unsupported ideas.

Follow the skill’s flow for clarifying, expanding, evaluating, converging, and sharpening the idea.

When producing the final result, report what you actually did and observed:

* Raw idea received
* Repository/context evidence inspected, if any
* Key clarifying questions or unresolved unknowns
* Strongest refined direction
* Main assumptions to validate
* Explicit “Not Doing” trade-offs
* Recommended next lifecycle step, usually `/spec`, without executing it

If the skill proposes saving a markdown idea artifact, ask for confirmation first. Only save after explicit user approval.
