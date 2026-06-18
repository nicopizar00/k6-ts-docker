# Spec — <topic>

> **Template.** Copy to `docs/architecture/specs/<topic>.md` and fill in.
> Pattern source: `.github/prompts/punch-spec.prompt.md` (Caveman `lite`).

- **Goal** — <one concrete, testable sentence>
- **Non-goals** — <what this work explicitly will NOT do>
  - <...>
- **Functional requirements** — <observable behavior the change delivers>
  - <...>
- **Technical constraints** — <what the implementation may not do; e.g. Docker-First, stdlib-only, no service renames>
  - <...>
- **Affected layers** — <which `docs/architecture/punch-boundaries.md` layer(s) own this>
- **Artifact / log / reporting implications** — <explicit, even if "none">
- **Acceptance criteria** — <the conditions Verify will assert>
  1. <...>

**Gate:** approved when Goal, Non-goals, and Acceptance criteria are agreed → Plan.
