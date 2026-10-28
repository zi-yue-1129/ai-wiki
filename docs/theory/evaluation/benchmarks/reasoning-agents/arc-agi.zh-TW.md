---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# ARC-AGI

抽象與推理語料庫（ARC）由 François Chollet 提出，作為衡量流動智力而非技能的基準。每個任務提供數組輸入與輸出的格子對，解題者必須推斷其轉換規則，並將它套用到新的輸入上（Chollet, 2019）。ARC-AGI 是此基準家族的名稱，ARC-AGI-2 是之後更困難的版本（Chollet et al., 2025）。

## 任務與資料

每個任務是一個小型的彩色格子謎題，附有幾組示範配對與一或多個測試輸入。任務依賴物件、計數與對稱等核心先驗知識，論文將其設計得接近人類的天生先驗（Chollet, 2019）。

## 協定與指標

只有當輸出格子與答案完全相同時，預測才算正確。測試在每個任務有限的嘗試次數下進行。隱藏測試集由主辦者保管，因此解題者能針對它調整的次數有限。

## 它能說明什麼

Chollet（2019）主張，衡量某項任務上的技能對智力說明有限，因為技能取決於先備知識與訓練資料。這個基準的設計要求系統從少數範例中學會規則，它衡量的是技能獲取的效率，而非可被記憶之任務上的表現。

## 限制

- **測試集小。** 任務數少，代表少數解出的謎題就會大幅改變分數。
- **對框架敏感。** 結果高度取決於提示與搜尋方法，因此分數難以跨系統比較。
- **排行榜壓力。** 公開的結果可能鼓勵針對可見範例調整，這也是隱藏測試集重要的原因。

## 相關

- [GPQA](../language/gpqa.md) 與 [MMLU](../language/mmlu.md) 測試的是知識，而非技能獲取。
- [推理與代理家族概述](index.md) 說明此領域。

## 參考文獻

### 開創性論文

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 把智力定義為技能獲取效率，並介紹 ARC。
- Chollet, F. & Knoop, M. et al. (2025). *ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems*. arXiv. https://arxiv.org/abs/2505.11831 — 較困難的後繼版本，設計為前沿系統的新挑戰。

### 文章與文件

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 上下文少樣本提示，是嘗試 ARC 類任務的常見方式。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 中間推理步驟，常用於嘗試格子推理任務。

### 補充來源

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 討論基準應如何區分模型學到的內容與它能做到的事。
