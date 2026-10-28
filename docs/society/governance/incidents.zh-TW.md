---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/governance
  - society/safety-alignment
  - society/ethics
tags:
  - incidents
  - AI failures
  - reporting
aliases:
  - AI 事故
  - 事件資料庫
  - AI 事件
  - Incident database
---

# AI 事件資料庫與案例研究

AI 事件資料庫是記錄 AI 系統實際造成傷害或險些造成傷害案例的結構化紀錄。這些紀錄可以幫助研究者、監管機構與企業看出反覆出現的失敗模式，而零散的個案新聞報導無法呈現這些模式。本頁說明主要的資料庫、事件如何分類、案例研究的教訓，以及法規如何開始要求事件通報。

## 概述

航空與醫療領域很早就學會記錄事故與險些發生的事件，以免同樣的失敗在不同場景重複發生。AI 缺少相似的慣例。McGregor 描述 AI 事件資料庫是由產業與非營利合作組織發起的事件彙整，目的是透過編目真實世界的 AI 失敗，防止它們重複發生 [(McGregor, 2020)](https://arxiv.org/abs/2011.08512)。

## 關鍵概念

- **事件（incident）**：AI 系統促成傷害或險些促成傷害的真實事件。
- **危害（hazard）**：可能合理地導致事件、但尚未發生的情況。
- **分類架構（taxonomy）**：對事件的共同分類方式，例如依傷害類型、受影響對象、領域與成因。分類架構讓紀錄可以相互比較。
- **功能落差**：系統被宣稱的功能與其實際表現之間的差距。

## 運作方式

資料庫從新聞、公開文件與投稿收集報告，並以分類架構為每筆紀錄加上標籤。好的紀錄會記載系統、部署情境、造成的傷害，以及採取了哪些回應。不完整的紀錄很常見，因此多數資料庫會列出來源並標示不確定的欄位。例如，OECD AI 事件與危害監測器是一個自動化的媒體監測工具，它會標示摘要與分類為 AI 生成，並聲明其結果不代表 OECD 或其會員國的官方立場 [(OECD AI Incidents Monitor)](https://oecd.ai/en/incidents)。

OECD 也發布了對 AI 事件及相關用語的定義，讓資料庫與監管機構能就何者算事件、何者算危害取得共識 [(OECD, 2024)](https://doi.org/10.1787/d1a8d965-en)。

## 案例研究

案例研究能揭露單一測試看不出的失敗模式。Raji 等人主張，許多已部署的 AI 系統並未達到其宣稱的功能，而這種功能落差是反覆出現的傷害來源。他們呼籲進行直接檢驗這些宣稱本身的稽核 [(Raji et al., 2022)](https://doi.org/10.1145/3531146.3533158)。部署後才出現的失敗，例如在基準測試表現良好、但在新族群中表現不佳的系統，也是事件彙整中常見的主題。

## 與其他頁面的關聯

事件會提供 [AI 安全與對齊](../safety-alignment/index.md)中討論的安全議題的材料，包括規格博弈與獎勵駭客。許多事件涉及[倫理與公平](../ethics/index.md)中的公平性失敗。部署前對 AI 系統的評估，則見[評估](../../theory/evaluation/index.md)。

## 應用

企業在風險管理與產品審查中使用事件紀錄。監管機構與標準組織用它們來決定優先處理哪些危害。研究者則用它們建立分類架構，並檢驗某種新風險是否已經發生過。

## 通報義務

歐盟 AI 法規要求高風險 AI 系統的提供者，向事件發生所在會員國的市場監督機關通報嚴重事件，並規定通報的期限 [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)。通報義務能讓事件資料更完整，但它們可能只適用於受該法規範的提供者，因此公開資料庫仍將依賴新聞與自願通報。

## 開放問題

- 事件資料庫應如何處理不確定或有爭議的事實？新聞報導與企業揭露之間應如何權衡？
- 應採用哪一種跨管轄區的分類架構？隨著系統變化，它能否保持穩定？
- 事件紀錄能減少重複的失敗，還是主要用於風險評估？
- 如何在不洩露敏感商業資訊的前提下，納入險些發生的事件與危害？

## 參考文獻

### 重要論文

- McGregor，*Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident Database*（2020）。https://arxiv.org/abs/2011.08512 — 說明 AI 事件資料庫的設計與目的。
- Raji、Kumar、Horowitz 與 Selbst，*The Fallacy of AI Functionality*，ACM Conference on Fairness, Accountability, and Transparency（2022）。https://doi.org/10.1145/3531146.3533158 — 主張未能達到宣稱功能是 AI 傷害的反覆來源，並呼籲稽核。

### 綜述與教科書

- OECD，*Defining AI incidents and related terms*，OECD Artificial Intelligence Papers（2024）。https://doi.org/10.1787/d1a8d965-en — 提出 AI 事件與危害的共同定義。

### 文章與文件

- OECD，*AI Incidents and Hazards Monitor (AIM)*，OECD.AI。https://oecd.ai/en/incidents — AI 事件與危害的自動化監測工具，並附有其資料地位的聲明。
- 歐盟，*Regulation (EU) 2024/1689 (Artificial Intelligence Act)*，歐盟官方公報（2024）。https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 為高風險 AI 系統的提供者設定嚴重事件通報義務。
