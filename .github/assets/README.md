# `.github/assets` — GitHub Copilot Chat 匯出範本（VS Code · Hub-Spoke）

最小範本,使 `.github` GitHub Copilot 資產可作 VS Code GitHub Copilot Chat 範本匯出。匯出 = copy-paste `.github/` + `docs/ai/`。唯一標的 = **GitHub Copilot VS Code**。

## ⚠ 警（caveman ultra）

> ⚠ TEMPLATE only. Human adapt before use. No ship as-is.
> ⚠ Target = GitHub Copilot VS Code Chat ONLY. Other tool (Claude/Codex/agent) NOT in scope.
> ⚠ resolve/ stub = link-fix only, NOT real content. Human fill on adopt.
> ⚠ Prose = wenyan. Copilot may misread classical Chinese. Team review first.

## 內容（essentials）

### Copilot Chat native 資產

| 範本 | 真位（adopt 後） |
|------|------------------|
| `copilot-instructions.md` | `.github/copilot-instructions.md`（中樞 hub） |
| `instructions/governance.instructions.md` | `.github/instructions/`（輻,`applyTo: '**'`） |
| `prompts/punch-init.prompt.md` | `.github/prompts/`（AI 治理代理） |

### `resolve/` — 倉內出域文鏈鏡照 snapshot（self-resolutive）

匯出時,`.github/` + `docs/ai/` 之外被引之倉內文 → 斷。`resolve/` 鏡真路、補之,使 bundle **自解(self-resolutive)、韌(resilient)**:bundle 唯需 `.github/` · `docs/ai/` · `.ai-upstream/` · `resolve/`,不外伸。鏡照乃 **caveman-wenyan 最小 snapshot**(非真文,人於 adopt 時填 / 換)。`/punch-init` certify 此鏡照覆全出域鏈(見 `prompts/punch-init.prompt.md` 之 resolve gate)。

| 出域標的（引處數） | resolve/ 鏡照 snapshot |
|--------------------|------------------------|
| `docs/architecture/punch-boundaries.md`（7） | `resolve/docs/architecture/punch-boundaries.md` |
| `docs/workflows/validation.md`（2） | `resolve/docs/workflows/validation.md` |
| `CLAUDE.md`（2 · 倉根戒律源） | `resolve/CLAUDE.md` |
| `AGENTS.md`（1 · AI 代理導覽） | `resolve/AGENTS.md` |

## Hub-Spoke

中樞(hub)= `.github/copilot-instructions.md`,唯載戒律與連。輻載細則。改則改輻,勿復述。

## 範圍外（out of scope · 不入範本 · 不 certify）

範本唯涵 **VS Code GitHub Copilot** 相關、已定之資產。下類**不入範本、`/punch-init` 不計、不 certify**:

- **WIP / 草稿 / history 文**：如 `docs/ai/history/**`、未定 plan / draft。凍區,不鏡、不解、不修。(故 `docs/ai/history/agent-skills-absorption-plan.md:59` 之 off-by-one 斷鏈 **不入範本範圍** —— history 文,源頭維護自理。)
- **他工具文**：root `CODEX.md` 及他 LLM 專屬(非 Copilot)。
- **外部工具 snapshot**：`.ai-upstream/` 之 caveman / graphify —— 外部,官方指南,人自裝於本機。

> ⚠ 此三類之斷鏈於匯出時留懸,**by design**,非範本缺陷。`/punch-init` resolve gate 唯 certify 上方 `resolve/` 表之出域鏈。
