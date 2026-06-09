# GitHub Copilot — Repository Instructions (always-on)

These rules apply to **every** Copilot session in this repository. They are deliberately short. Detailed guidance lives in `docs/ai/operating-protocol.md` and the path-specific files under `.github/instructions/`.

## Non-negotiables

1. **Docker First execution.** Tests, services, and bundling run inside Docker.
   The host needs only Docker and a stdlib Python 3 runtime.
2. **Python orchestration façade.** The user-facing CLI is `bin/punch`
   (stdlib-only Python). Do not introduce host-side Node, npm, k6, or any
   pip-installed package.
3. **k6 is the performance execution engine.** No other load-test tool.
4. **Lifecycle-driven work.** Every change goes through Understand → Shape →
   Build → Verify → Review → Ship. Use the matching prompt in `.github/prompts/`.
5. **Mode discipline.** Read-only requests (audits, reviews, explanations) stay
   in **Ask Mode**. Planning stays in **Plan Mode**. Edits happen only in
   **Agent Mode** within a scoped plan.
6. **Validation evidence is mandatory.** A change is not "done" until
   `reports/state/punch-run.json` (or an equivalent artifact) records the
   verification run. See `docs/workflows/validation.md`.
7. **Human approves Ship.** Agent Mode may stage, commit, and open a PR.
   Merging, releasing, or pushing tags is a human action.
8. **No premature abstraction.** Three similar lines beats a clever helper.
9. **No duplication of AI guidance.** New instructions, prompts, or skills
   must not restate content already in `docs/ai/` or `CLAUDE.md`. Link instead.
10. **No secrets, no private URLs, no internal business context** in source,
    docs, prompts, or test inputs. Use environment variables for any external
    base URL.

## Lifecycle entry points

| Phase | Prompt | Mode |
|---|---|---|
| Understand | `punch-understand.prompt.md` | Ask |
| Shape      | `punch-shape.prompt.md`      | Plan |
| Build      | `punch-build-slice.prompt.md`| Agent |
| Verify     | `punch-verify.prompt.md`     | Agent / Ask |
| Review     | `punch-review.prompt.md`     | Ask |
| Ship       | `punch-ship.prompt.md`       | Agent (mechanical only) |

## When in doubt

Read `CLAUDE.md`, then `docs/ai/operating-protocol.md`. Ask before editing files
outside the scope produced in Shape.
