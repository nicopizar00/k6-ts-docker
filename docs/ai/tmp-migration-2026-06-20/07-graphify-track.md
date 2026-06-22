# 07 · Graphify 全倉軌 · ignore · 首繪本（graphify track）

> ⚠ IDEA scratch。Graphify = precondition external。Evidence, never canonical。

Graphify 軌,易漏：

- **首繪成本**:`/graphify .` 繪全倉首圖 —— 大倉慢、耗。考:首次 build 時長?CI 跑否(無,in-IDE only)。
- **`.graphifyignore`**:無則圖含 `node_modules`、`dist`、`reports`、`.git` —— 雜、慢、洩。考:採前置 `.graphifyignore` scope 之。init 薦之。
- **graphify-out gitignore**:`graphify-out/` never commit(ADR 0002)。考:採者 `.gitignore` 加否?漏 → 圖入版控,洩碼結構 + 脹倉。
- **in-IDE vs headless**:in-IDE 用 active model 無 key;headless `graphify extract --backend` 需 key 且範本**不用**。考:採者誤跑 headless → throw 或耗 key。
- **圖鮮度(stale)**:`/graphify . --update` 維新。考:誰跑 update?寫文後須手 update 使新文入圖。漂移 → 誤 stale 信號。
- **版本鎖**:`graphifyy` v0.8.41 baseline(ADR 0002)。考:採者裝新版,行為漂?pin 否。
- **`.ai-upstream/graphify/`**:pristine snapshot 於 gitignored staging。考:採者有此 baseline 否?無則無 drift 基準。
- **model 質**:in-IDE semantic extract 倚 active model。考:弱 model → 弱圖 → 弱 evidence。Gemini extra(`graphifyy[gemini]`)需 key。
- **graphify ≠ 決策**:圖唯 evidence,`punch-ai-governance` 決。考:採者勿將 `graphify-out/` 直升 canonical。boundary 守。
- **video extra**:`graphifyy[video]` + yt-dlp 重依賴。考:不需則不裝。

> ⚠ Miss `.graphifyignore` → 首圖含垃圾、洩、慢。第一 graphify 陷。
