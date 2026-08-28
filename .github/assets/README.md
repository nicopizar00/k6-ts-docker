# `.github/assets` — GitHub Copilot Chat export template (VS Code · Hub-Spoke)

Minimal template that makes the `.github` GitHub Copilot assets exportable as a
VS Code GitHub Copilot Chat template. Export = copy-paste `.github/` +
`docs/ai/`. Sole target = **GitHub Copilot VS Code**.

## ⚠ Warnings

> ⚠ TEMPLATE only. Human adapts before use. Never ship as-is.
> ⚠ Target = GitHub Copilot VS Code Chat ONLY. Other tools (Claude/Codex/agents) NOT in scope.
> ⚠ `resolve/` stubs = link-fix only, NOT real content. Human fills on adopt.
> ⚠ `resolve/` stub prose = wenyan snapshots. Copilot may misread classical Chinese. Team review before adopting.

## Contents (essentials)

### Copilot Chat native assets

| Template | Real location (after adopt) |
|------|------------------|
| `copilot-instructions.md` | `.github/copilot-instructions.md` (the hub) |
| `instructions/governance.instructions.md` | `.github/instructions/` (spoke, `applyTo: '**'`) |

### `resolve/` — snapshot mirrors of out-of-bundle repo docs (self-resolutive)

On export, repo docs referenced from outside `.github/` + `docs/ai/` break.
`resolve/` mirrors those paths so the bundle stays **self-resolutive and
resilient**: the bundle needs only `.github/` · `docs/ai/` · `.ai-upstream/` ·
`resolve/`, nothing external. Mirrors are **minimal terse snapshots**
(not real content; humans fill / replace on adopt). Coverage of the
`resolve/` table against every out-of-bundle link is a **manual check on
export** — human confirms the table below before adopting the bundle.

| Out-of-bundle target (ref count) | resolve/ snapshot |
|--------------------|------------------------|
| `docs/architecture/punch-boundaries.md` (7) | `resolve/docs/architecture/punch-boundaries.md` |
| `docs/workflows/validation.md` (2) | `resolve/docs/workflows/validation.md` |

## Hub-Spoke

Hub = `.github/copilot-instructions.md`; carries only rules + links. Spokes
carry detail. Change the spoke, never restate.

## Out of scope (not in template · not certified)

Template covers only **VS Code GitHub Copilot** assets in settled state. These
classes are **excluded from the template, not certified**:

- **WIP / draft docs** — unsettled plans and drafts. Not mirrored, not
  resolved, not fixed.
- **Other-tool docs** — LLM-specific files that are not Copilot-native.
- **External-tool snapshots** — upstream provenance under `.ai-upstream/`;
  external, official guides apply, humans install locally.

> ⚠ Broken links in these classes stay unresolved on export **by design** — not
> a template defect. Coverage of the `resolve/` table above is a manual human
> check on export, not automated.
