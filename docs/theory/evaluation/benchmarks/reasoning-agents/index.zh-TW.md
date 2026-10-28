---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# 推理與代理基準

這個家族要問的是，系統能否從少數範例中獲得新規則並加以應用，而不是回想事實或遵循既定程序。這些基準的設計使得記憶的知識無法解決它們。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [ARC-AGI](arc-agi.md) | 從範例推斷格子的轉換 | 輸出格子的完全相符 |

## 常見問題

- **測試集小。** 少數任務就可能大幅改變分數。
- **框架與搜尋。** 提示與搜尋方法會改變結果，因此系統難以比較。
- **排行榜壓力。** 當公開範例可被用來調整時，隱藏測試集就很重要。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [少樣本](../few-shot/index.md) 在分類情境中測試從少數範例學習的能力。

## 參考文獻

### 開創性論文

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 提出以技能獲取效率定義智力，並介紹 ARC。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 介紹上下文少樣本提示，是這類任務的常見嘗試方式。

### 文章與文件

- Chollet, F. & Knoop, M. et al. (2025). *ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems*. arXiv. https://arxiv.org/abs/2505.11831 — 介紹設計來挑戰前沿系統的較困難版本。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示中間推理步驟如何改變推理任務的結果。
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 描述推理基準應如何設計與報告。
