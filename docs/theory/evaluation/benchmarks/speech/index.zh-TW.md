---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - speech
---

# 語音基準

語音基準測試自動語音辨識，也就是把音訊轉成文字的能力。分數通常是固定測試集上的詞錯誤率，因此只有在切分、文字正規化與解碼設定相同時，結果才可比較。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [LibriSpeech](librispeech.md) | 轉寫英文有聲書的朗讀語音 | 乾淨與其他測試集上的詞錯誤率 |

## 常見問題

- **正規化。** 詞錯誤率取決於比對前如何正規化標點、大小寫與數字，因此必須報告所用的正規化方式。
- **領域轉移。** 朗讀有聲書與對話、口音和嘈雜錄音不同，因此在一個集合上的低錯誤率不會自動延續到其他集合（Radford et al., 2022）。
- **訓練重疊。** 大規模網路訓練資料可能包含接近測試材料的錄音，因此測試集的來源歷史很重要。

## 相關

- [基準測試概述](../index.md) 列出所有家族。
- [語言](../language/index.md) 涵蓋純文字的對應基準。
- [協定](../../protocols/index.md) 說明切分與報告方式。

## 參考文獻

### 開創性論文

- Graves, A. et al. (2006). *Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks*. ICML 2006. https://doi.org/10.1145/1143844.1143891 — 介紹 CTC 損失函數，許多語音辨識器用它作為訓練目標。
- Hannun, A. et al. (2014). *Deep Speech: Scaling up end-to-end speech recognition*. arXiv. https://arxiv.org/abs/1412.5567 — 展示在大量語音上訓練的端到端辨識。

### 文章與文件

- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv. https://arxiv.org/abs/2212.04356 — 顯示大規模且多樣的訓練資料能提升跨測試集的穩健性。

### 補充來源

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
