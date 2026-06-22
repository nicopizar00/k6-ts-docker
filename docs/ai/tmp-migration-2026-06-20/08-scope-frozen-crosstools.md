# 08 · 範圍外 · 凍區 · 他工具（scope / frozen / cross-tool）

> ⚠ IDEA scratch。Template = Copilot VS Code ONLY。Others out of scope。

範圍與他工具,易漏：

- **唯 Copilot VS Code**:範本唯標 GitHub Copilot VS Code Chat。考:target 隊用 Claude Code / Codex / Cursor / JetBrains 否?則範本不覆 —— 須各自橋。
- **Claude Code 橋**:源倉有 `.claude/skills/guard` + `.claude/commands/*` 復用 `.github/`(ADR 0004)。考:**此橋不在 `.github/assets` 範本**!採者用 Claude Code 須另採橋。文之。
- **CODEX.md / 他 LLM 檔**:範圍外,匯出留懸 by design。考:target 用 Codex 則須自建。
- **root CLAUDE.md/AGENTS.md**:範本以 caveman-wenyan resolve 鏡照覆鏈(self-resolutive)。考:採者欲真用 Claude Code/agents 須填實鏡照 → 真根檔。
- **凍區(frozen zones)**:`docs/ai/history/**`、`.ai-upstream/**`、adopted-upstream skills —— refresh/append,勿重寫。考:`/punch-document` Handle-with-care 範圍。採者誤改凍區?
- **history off-by-one**:`docs/ai/history/...:59` 斷鏈 —— history,範圍外,**不入範本、不 certify**(Group C dismissed)。考:源頭維護自理,非遷移阻。
- **`.ai-upstream` 外部**:caveman / graphify pristine snapshot,gitignored staging,非版控。考:採者無此 → 無 drift baseline;re-fetch 法文否。
- **多工具並存**:一倉 Copilot + Claude + Codex?考:三配置源衝突否?單一 `.github/` 真源 + 各橋復用(勿 fork)。
- **org/多隊復用**:長期 = 可復用 perf gate。考:範本須真 agnostic;org-level 治理 vs repo-level。

> ⚠ Miss → 採 Claude Code 隊得 Copilot-only 範本,橋缺,半治理。
