---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# WebArena

WebArena 是一個可重現的環境，供以語言指令在網站上執行任務的代理使用。它提供四種常見領域的完整運作網站：電子商務、社群論壇討論、協作式軟體開發與內容管理。網站附有地圖等工具與外部知識來源（Zhou et al., 2023）。

## 任務與資料

代理收到一段自然語言指令，例如購買商品、發文或修改儲存庫，並必須透過瀏覽器在這些網站上操作。由於環境是自行架設的，每次執行都從相同的狀態開始，因此不同系統的結果可以比較（Zhou et al., 2023）。

## 協定與指標

成功與否是依網站最終狀態是否達到目標來判定，而非依代理的文字輸出。指標是**任務成功率**。結果取決於觀察的格式、動作空間與步數上限，因此這些設定都必須連同分數一起報告。

## 它能說明什麼

實際的網頁任務對以現有模型建構的代理而言仍然困難，最佳代理與人類之間的差距很大。這個基準的建立，是因為在簡化的合成環境中測試的代理，無法轉移到真實網站上（Zhou et al., 2023）。

## 限制

- **模擬網站。** 這些網站是逼真的複製品，而非即時的網路，因此在開放網際網路上的表現可能不同。
- **只有四個領域。** 涵蓋範圍限於四種網站類型。
- **觀察設計。** 網頁如何呈現給模型（文字、截圖或無障礙樹）會大幅改變結果。
- **步數限制。** 長任務對預算敏感，因此不同預算下的分數不能比較。

## 相關

- [GAIA](gaia.md) 以開放網路上的問題測試助理。
- [SWE-bench](../math-and-code/swe-bench.md) 在軟體儲存庫中以測試判定代理的表現。
- [推理與代理家族概述](index.md) 比較此領域的基準。

## 參考文獻

### 開創性論文

- Zhou, S. et al. (2023). *WebArena: A Realistic Web Environment for Building Autonomous Agents*. arXiv. https://arxiv.org/abs/2307.13854 — 介紹自行架設的網站、任務與以成功為準的評估。
- Mialon, G. et al. (2023). *GAIA: a benchmark for General AI Assistants*. arXiv. https://arxiv.org/abs/2311.12983 — 針對會使用網頁瀏覽與其他工具的助理的基準。

### 文章與文件

- Yang, J. et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. arXiv. https://arxiv.org/abs/2405.15793 — 顯示代理所使用的介面如何改變它完成的任務數。
- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — 在軟體環境中行動的代理的平行基準。

### 補充來源

- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 代理在觀察與動作之間常使用的推理步驟。
