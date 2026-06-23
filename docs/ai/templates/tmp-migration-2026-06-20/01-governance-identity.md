# 01 · 治理鑰 · Punch 身份 · rebind（governance key / identity）

> ⚠ IDEA scratch。Punch = template origin, NEVER active identity in target。

採範本,身份事易漏：

- **治理鑰(governance key)**：Punch 乃範本源,非本倉活身份。`/punch-init` 解一**本地鑰**。考：target 倉鑰名為何？`<repo-key>`？一處定,處處引。
- **`punch-*` 命名**：`punch-ai-governance`、`punch-runtime-engineer`、`punch-builder`…全帶 `punch` 前綴。考：rebind 至本倉鑰(`<key>-ai-governance`)？或留 Punch 為框架名、唯鑰異？決一,勿半。
- **graphify-adapter 名**：init_scan 生 `<key>-graphify-adapter` 等派生名。考：與本倉命名規一致否。
- **身份漂移險**：若留 `punch-*` 又設本鑰,二身份並存 → 代理混。考：單一身份源。
- **框架 vs 倉**：Punch = 操作系統(lifecycle);倉 = 特化。考：文中分清「框架戒律」與「本倉戒律」,勿混。
- **多倉採用**：長期目標 = 可復用 perf gate,他隊採。考：鑰命名須避撞;範本須真 agnostic(無硬寫 k6-ts-docker)。
- **ADR 繼承**：ADR 0001-0004 屬源倉決策。考：target 倉繼承否？或重立本倉 ADR 序？provenance 鏈。
- **README 警留否**：範本帶「TEMPLATE only / human adapt」警。考：採後除警(已成活配置),勿留誤導。

> ⚠ Miss → 代理自稱 Punch 而非本倉,或鑰未解 → `/punch-init` governance gate WARN。
