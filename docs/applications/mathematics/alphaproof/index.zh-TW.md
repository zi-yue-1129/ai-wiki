---
translation_reviewed: 2026-10-28
---

# AlphaProof（Hubert 等人，2025）

AlphaProof 是一個代理人，它以 AlphaZero 式的強化學習，學習在 Lean 證明助理中撰寫形式證明。它在大量經自動翻譯為形式陳述的問題上訓練，並在最困難的題目上於推論時進行調適。Hubert 等人於 2025 年在 Nature 發表此系統。它是父頁面[數學與形式證明](../index.md)介紹的三種里程碑式方法之一。

## 概述

形式證明具有一項有用的性質：證明檢查器會逐步接受或拒絕每一步。這使證明寫作成為強化學習的環境：每個動作是一個證明步驟，而當檢查器接受整個證明時，便給予獎勵。Hubert 等人把形式語言描述為一個能讓推理有所根據的環境，因此學習可以來自經驗，而不只來自人類寫的證明。

難點在於資料。形式證明相較於非形式的數學十分稀少，而且以手工撰寫既慢又費力。AlphaProof 的做法是：以語言模型把大量自然語言問題翻譯為 Lean 陳述，再保留可用於訓練的翻譯結果。以搜尋進行自我對弈來學習的想法，源自 AlphaZero（Silver 等人，2018），它在沒有人類棋譜的情況下學會了下棋。

## 關鍵概念

- **證明狀態與戰術。** Lean 證明會經過一系列狀態，每個狀態由一個目標及其假設組成。戰術把一個狀態轉換為另一個狀態，檢查器會確認每一次轉換。
- **自動形式化。** 把自然語言的問題翻譯為形式陳述。Wu 等人（2022）顯示，語言模型能部分地做到這一點。
- **帶有學習式引導的樹狀搜尋。** 代理人把可能的戰術視為搜尋樹來探索，並由對各步驟是否有前景的學習式估計來引導，精神上與 AlphaZero 相同。
- **測試時強化學習。** 對一道困難題目，代理人在推論時生成許多相關變體，並從中學習，在嘗試原題之前先適應該題。

## 運作方式

訓練與求解過程分為四個階段：

1. **建立問題集。** 以語言模型把自然語言問題翻譯為 Lean 陳述，並保留可用的陳述。
2. **搜尋證明。** 對每個陳述，樹狀搜尋提出戰術。Lean 檢查器逐一接受或拒絕，被接受的狀態則繼續展開。
3. **從結果中學習。** 成功與失敗的嘗試都會更新引導搜尋的網路。
4. **在困難題目上調適。** 對最困難的題目，於推論時生成並從許多題目變體中學習（測試時強化學習），然後再次嘗試原題。

輸出的是一個 Lean 已接受的證明；其正確性取決於檢查器與陳述，而不取決於學習得到的元件。

## 結果

在 2024 年國際數學奧林匹亞中，AlphaProof 解出五道非幾何題中的三題，包括該次競賽最難的一題。結合 AlphaGeometry 2 處理幾何題後，系統達到銀牌得主等價的分數。作者表示，就他們所知，這是 AI 系統首次在 IMO 取得任何獎牌水準的表現。

## 限制

- **運算量。** IMO 的結果動用了多日的運算。
- **翻譯風險。** 通過檢查的證明，證明的是形式陳述。若從自然語言題目到形式陳述的翻譯改變了原意，檢查器仍會接受一個對錯誤結果的證明。
- **部分涵蓋。** 五道非幾何題中解出三題，而幾何題則交由另一個系統處理。
- **可讀性。** 形式證明精確，但冗長，人類讀起來很困難。

## 開放問題

- 測試時強化學習能否用於研究問題？這些問題沒有已知的非形式解答，變體必須自行構造。檢查形式陳述是否符合原題，是另一個尚未解決的問題。
- 哪些要素最關鍵？Ren 等人（2025）採用不同的做法，把問題分解為子目標，並以由此得到的冷啟動資料進行訓練，同樣取得了強勁的結果。

## 相關連結

- AlphaProof 屬於[數學與形式證明](../index.md)的形式路線，也屬於符號 AI 中[自動推理與定理證明](../../../theory/paradigms/symbolic-ai/index.md)的理論範疇。
- 其訓練方法屬於 [AlphaZero](../../../theory/paradigms/reinforcement-learning/mcts-and-self-play/alphazero/index.md)頁面所述的自我對弈家族，而其測試時調適則與[推理模型](../../../theory/models/reasoning/index.md)相關。

## 應用

AlphaProof 是論文中描述的研究系統。它的想法也延伸到更大的流程中：Georgiev 等人（2025）把演化式程式代理人與 AlphaProof 及其他推理系統結合，用於自動證明生成。

## 參考文獻

### 開創性論文

- Hubert, T. 等人（2025）。*Olympiad-level formal mathematical reasoning with reinforcement learning*。Nature。https://doi.org/10.1038/s41586-025-09833-y — 介紹 AlphaProof，並報告其 2024 年 IMO 的結果。
- Silver, D. 等人（2018）。*A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*。Science。https://doi.org/10.1126/science.aar6404 — 介紹 AlphaZero，以自我對弈加上樹狀搜尋來學習棋類遊戲。
- de Moura, L. & Ullrich, S.（2021）。*The Lean 4 Theorem Prover and Programming Language*。CADE-28, Lecture Notes in Computer Science。https://doi.org/10.1007/978-3-030-79876-5_37 — 說明 Lean 4，即 AlphaProof 撰寫證明所用的證明助理。
- Wu, Y. 等人（2022）。*Autoformalization with Large Language Models*。arXiv。https://arxiv.org/abs/2205.12615 — 展示語言模型把競賽題目翻譯為形式陳述。

### 綜述與教科書

- Yang, K. 等人（2024）。*Formal Mathematical Reasoning: A New Frontier in AI*。arXiv。https://arxiv.org/abs/2412.16075 — 綜述形式定理證明，以及自動檢查的價值。

### 文章與文件

- Mathlib Community（2020）。*The Lean Mathematical Library*。CPP 2020, ACM SIGPLAN。https://doi.org/10.1145/3372885.3373824 — 介紹 Mathlib，即形式化數學的函式庫。
- Ren, Z. Z. 等人（2025）。*DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition*。arXiv。https://arxiv.org/abs/2504.21801 — 以子目標分解為基礎的開放權重 Lean 證明器，是另一種不同的做法。
- Georgiev, B. 等人（2025）。*Mathematical exploration and discovery at scale*。arXiv。https://arxiv.org/abs/2511.02864 — 把演化式程式代理人與 AlphaProof 結合，用於證明生成。
- Chervonyi, Y. 等人（2025）。*Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2*。arXiv。https://arxiv.org/abs/2502.03544 — 介紹 AlphaGeometry 2，它在 2024 年 IMO 與 AlphaProof 結合。
