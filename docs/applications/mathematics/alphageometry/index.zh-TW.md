---
translation_reviewed: 2026-10-28
---

# AlphaGeometry（Trinh 等人，2024）

AlphaGeometry 是一個神經符號系統，能證明奧林匹亞水準的歐氏平面幾何題。語言模型提出輔助構造，例如一個額外的點或線，符號推導引擎則推算由此得出的結論。Trinh 及其同事於 2024 年在 Nature 發表此系統。它是父頁面[數學與形式證明](../index.md)介紹的三種里程碑式方法之一。

## 概述

許多奧林匹亞幾何題都需要輔助構造：題目沒有提及、但能讓證明變得明顯的一個點或一條線。選擇這個構造是困難的一步；畫出之後，其餘推論大多只是例行的推導。學習型證明器在這裡缺乏訓練資料，因為人類證明必須被翻譯成機器可檢查的形式，而幾何的翻譯特別困難（Trinh 等人，2024）。

AlphaGeometry 避開了對人類示範的依賴。它生成數百萬個合成定理及其證明，在其上訓練語言模型，並且只讓模型負責提出構造。推導由符號引擎完成，因此每一步都仍可檢查。

## 關鍵概念

- **歐氏平面幾何**：點、線、圓與角，以一套小型的幾何述詞形式語言來描述。
- **推導引擎**：一個符號元件，會把幾何規則向前套用，直到不再產生新的事實為止。
- **輔助構造**：在圖形上新增的一個點或一條線，由語言模型提出。
- **分支搜尋**：每一次構造的選擇都會開啟一個新分支，因此搜尋樹非常寬。
- **合成資料**：透過抽樣圖形並記錄引擎能推導出什麼而生成的定理。

## 運作方式

系統以推導與提案交替的迴圈運作：

1. 把問題翻譯為形式前提與目標陳述。
2. 執行推導引擎，推導出前提的所有後果。若目標出現，即停止。
3. 否則，依據目前狀態，請語言模型提出數個候選輔助構造。
4. 把每個候選加入圖形，回到第 2 步，並保持對各分支的搜尋。
5. 達到目標時，輸出證明。Trinh 等人指出，證明是人類可讀的。

語言模型是唯一的學習元件。它的建議本身從不被信任：只有當引擎能由該構造推導出目標時，這個構造才有用。

## 結果

在 30 道近期的奧林匹亞幾何題上，AlphaGeometry 解出 25 題，而先前最好的方法只解出十題。作者稱此結果已接近平均水準的 IMO 金牌得主（Trinh 等人，2024）。在專家評估下，它解出了 IMO 2000 與 2015 年的所有幾何題。摘要給出這些數字；本頁不再引用其他數字。

## 限制

- **範圍。** 此系統僅處理歐氏平面幾何。其形式語言並未涵蓋所有題型：後續系統報告，在擴充語言之後，IMO 2000 至 2024 幾何題的涵蓋率由 66% 提高到 88%（Chervonyi 等人，2025）。
- **翻譯。** 題目必須先轉換為形式語言，系統才能運作。忠實翻譯自然語言陳述，正是自動形式化研究所要處理的難題（Wu 等人，2022）。後續系統被描述為邁向從自然語言出發的全自動流程的進展，而非完成品（Chervonyi 等人，2025）。
- **合成資料。** 訓練依賴於能產生引擎可解定理的生成器，這在幾何以外的領域很難重現。
- **搜尋成本。** 搜尋樹很寬，因此單一題目可能需要大量運算。

## 開放問題

- 語言模型與符號引擎的分工，能否擴展到幾何以外、形式語言不同的代數與數論？[AlphaProof](../alphaproof/index.md)走的是另一條路，使用 Lean。
- 語言模型是否學到了可重用的幾何直覺，還是主要學到合成資料的統計規律？Yang 等人（2024）主張，形式檢查提供了衡量真正進展所需的自動回饋。
- 效能有多少來自引擎，有多少來自學習得到的提案？Petrov 等人（2025）以人工批改完整證明，顯示在沒有檢查器的情況下評判證明品質的成本有多高。

## 相關連結

- 推導引擎是經典的[符號 AI](../../../theory/paradigms/symbolic-ai/index.md)元件，這裡與學習得到的提案模型結合，是該領域反覆出現的模式。
- AlphaGeometry 2 與 AlphaProof 結合，在 2024 年 IMO 達到銀牌水準（Hubert 等人，2025）。
- 人類幾何學家是憑眼睛畫出輔助線的，這使該任務與空間視覺相關，相關內容見[視覺感知](../../../brain-mind/visual-perception/index.md)頁面。

## 應用

此系統曾作為 2024 年 IMO 銀牌等價成績系統的一部分（Hubert 等人，2025）；其後繼系統則是全自動幾何流程研究的基礎（Chervonyi 等人，2025）。

## 參考文獻

### 開創性論文

- Trinh, T. H. 等人（2024）。*Solving olympiad geometry without human demonstrations*。Nature。https://doi.org/10.1038/s41586-023-06747-5 — 介紹 AlphaGeometry，它在 30 道測試奧林匹亞幾何題中解出 25 題。
- Wu, Y. 等人（2022）。*Autoformalization with Large Language Models*。arXiv。https://arxiv.org/abs/2205.12615 — 研究把自然語言數學翻譯為形式陳述的方法。
- de Moura, L. & Ullrich, S.（2021）。*The Lean 4 Theorem Prover and Programming Language*。CADE-28, Lecture Notes in Computer Science。https://doi.org/10.1007/978-3-030-79876-5_37 — 說明 Lean 4，即另一種路線所使用的形式系統。

### 綜述與教科書

- Yang, K. 等人（2024）。*Formal Mathematical Reasoning: A New Frontier in AI*。arXiv。https://arxiv.org/abs/2412.16075 — 立場論文，主張 AI 數學應採用形式檢查。

### 文章與文件

- Chervonyi, Y. 等人（2025）。*Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2*。arXiv。https://arxiv.org/abs/2502.03544 — 報告後續系統及其擴充後的形式語言。
- Petrov, I. 等人（2025）。*Proof or Bluff? Evaluating LLMs on 2025 USA Math Olympiad*。arXiv。https://arxiv.org/abs/2503.21934 — 專家批改完整證明，顯示評判證明品質有多困難。
- Hubert, T. 等人（2025）。*Olympiad-level formal mathematical reasoning with reinforcement learning*。Nature。https://doi.org/10.1038/s41586-025-09833-y — 說明結合 AlphaGeometry 2 與 AlphaProof 的 2024 年 IMO 系統。
