---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
aliases:
  - Reasoning and agent benchmarks
  - 推理與代理基準
---

# 推理與代理基準

這個家族要問的是：系統能否從少數範例中習得一條新規則並加以應用，而不只是回想事實或遵循既定程序。代理基準則加上另一個問題：系統能否在工具或網頁環境中完成多步驟任務。這些基準的設計使得單靠記憶的知識無法解決它們。

## 概述

Chollet（2019）主張，在某一固定任務上的技能是衡量智力的弱指標，因為技能高度依賴先備知識與經驗。依此觀點，他提出了抽象與推理語料庫（ARC），每個任務給出幾組輸入與輸出的網格配對，要求解題者推斷規則並套用到新的輸入上。ARC-AGI-2（Chollet et al., 2025）保留相同的輸入輸出格式，但加入一組新整理、較困難的任務，並以人類測試來校準難度。

代理基準在不同的情境中提出相關的問題。GAIA 包含 466 個需要推理、瀏覽網頁與使用工具的真實世界問題。作者報告，人類答對其中 92%，而附帶外掛程式的 GPT-4 只答對 15%（Mialon et al., 2023）。WebArena 將代理放入四個自架網站的複本中，涵蓋電子商務、社群論壇討論、協作軟體開發與內容管理，並依任務是否正確完成來計分（Zhou et al., 2023）。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [ARC-AGI](arc-agi.md) | 從範例推斷網格轉換 | 輸出網格的完全符合 |
| [GAIA](gaia.md) | 需要瀏覽與工具的真實世界問題 | 完全符合的準確率 |
| [WebArena](webarena.md) | 自架網站上的任務 | 依功能正確性判定的任務成功率 |

ARC 類任務採嚴格計分：輸出網格不是完全正確就是錯誤。代理任務則依環境的最終狀態或最終答案計分，因此一次執行可能在許多正確步驟之後失敗。兩種計分規則衡量的東西不同，單一數字無法直接比較。

## 關鍵概念

- **少樣本規則歸納**：從少量示範推斷規則，並套用到未見過的輸入。
- **功能正確性**：以動作的結果來判定，例如訂單是否成立，而不是拿動作序列與參考答案比對。
- **鷹架（scaffold）**：模型周圍的提示、搜尋與工具迴圈。在代理基準中，鷹架是被衡量的系統的一部分。

## 運作方式

一次典型的執行會給系統任務描述，對代理基準還會提供工具或瀏覽器的存取權。分數只計算最終結果。提示方法會大幅改變結果：要求模型寫出中間推理的思維鏈提示，改善了推理任務的表現（Wei et al., 2022）。少樣本提示則是在輸入中給予示範、不做梯度更新，是大型模型嘗試這些任務的常見做法（Brown et al., 2020）。

## 常見問題

- **測試集小。** 少數幾個任務就可能大幅改變分數，因此信賴區間很重要。
- **鷹架與搜尋。** 提示與搜尋方法會改變結果，因此除非報告鷹架，否則系統很難比較。
- **排行榜壓力。** 公開的範例可能被針對調校。隱藏的測試集與保留的任務可以降低這種風險。
- **環境漂移。** 線上網站會隨時間改變。像 WebArena 這樣的自架複本則能讓執行可重現。

## 相關連結

- [數學與程式](../math-and-code/index.md) 涵蓋答案可以檢查的推理基準。
- [代理](../../../models/agents/index.md) 說明這些基準所評估的系統。
- [少樣本](../few-shot/index.md) 在分類情境中測試從少數範例學習的能力。

## 開放問題

- 能否設計出對以搜尋為基礎的系統很難、但對人類仍然容易的固定規則歸納基準。
- 當部分進展很重要、而一個失敗步驟就會結束執行時，如何為長程代理任務計分。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [多模態](../multimodal/index.md) 涵蓋結合影像與推理的任務。

## 參考文獻

### 開創性論文

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張任務上的技能是衡量智力的弱指標，並介紹 ARC 的任務格式。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 介紹以 GPT-3 進行的上下文少樣本提示，是嘗試這些任務的常見做法。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示中間推理步驟能改善算術、常識與符號推理的結果。

### 文章與文件

- Chollet, F., Knoop, M., Kamradt, G., Landers, B. & Pinkard, H. (2025). *ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems*. arXiv. https://arxiv.org/abs/2505.11831 — 介紹較難的 ARC-AGI-2 任務，保留輸入輸出格式，並附人類測試結果。
- Mialon, G. et al. (2023). *GAIA: a benchmark for General AI Assistants*. arXiv. https://arxiv.org/abs/2311.12983 — 介紹 466 個真實世界問題，並報告人類與 GPT-4 的結果。
- Zhou, S. et al. (2023). *WebArena: A Realistic Web Environment for Building Autonomous Agents*. arXiv. https://arxiv.org/abs/2307.13854 — 介紹自架網站環境與功能正確性任務。
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 介紹 BIG-bench，共 204 項任務，由 450 位作者、132 個機構提供，主題涵蓋語言學到物理學。
