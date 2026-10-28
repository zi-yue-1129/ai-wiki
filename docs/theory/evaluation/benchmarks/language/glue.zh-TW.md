---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# GLUE

GLUE（General Language Understanding Evaluation）把數個自然語言理解任務合併為一個分數，並附有用於分析的診斷測試集（Wang et al., 2018）。它的設計目標是讓某一任務上的進步能轉移到其他任務。

## 任務與資料

GLUE 包含九個任務，涵蓋句子可接受性、情感、改寫、文字相似度與自然語言推論。各任務的規模不同，部分任務的訓練資料很少，因此會獎勵能在任務之間共享知識的模型（Wang et al., 2018）。

## 協定與指標

每個任務有各自的指標，例如準確率、F1 或相關係數。整體分數是各任務分數的平均。測試標籤不公開，因此提交結果要透過公開排行榜。診斷測試集是人工建立的範例，用來分析語言現象。

## 它能說明什麼

發表時，多任務與遷移的基準並沒有比最佳的單任務模型帶來大幅進步（Wang et al., 2018）。預訓練編碼器改變了這個情況：BERT 報告了它在 GLUE 上的結果（Devlin et al., 2019），GLUE 因此成為預訓練語言模型的主要測試平台。

## 限制

- **飽和。** SuperGLUE 的作者指出，模型在 GLUE 上已超過非專家人類，剩餘的進步空間很小（Wang et al., 2019）。
- **捷徑。** 部分任務可以靠利用資料中的模式解出。診斷測試集就是為了揭露這類失敗而設計。
- **只有英文。** 這個基準不測試其他語言。

## 後繼基準

[SuperGLUE](superglue.md) 以更困難的任務取代了它。之後的基準，例如 [MMLU](mmlu.md)，測試的是知識與推理，而非句子層級的理解。

## 相關

- [語言家族概述](index.md) 比較各語言基準。
- [準確率](../../metrics/classification/accuracy.md) 與 [F1](../../metrics/classification/f1.md) 是多數 GLUE 任務使用的指標。

## 參考文獻

### 開創性論文

- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — 介紹多任務基準、其整體分數與診斷測試集。
- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL. https://arxiv.org/abs/1810.04805 — 報告預訓練編碼器在 GLUE 上的結果，改變了它作為測試平台的角色。

### 文章與文件

- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — 較困難的後繼基準，附有自己的工具包與排行榜。
- Raffel, C. et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv. https://arxiv.org/abs/1910.10683 — 在 GLUE 與 SuperGLUE 任務上評估統一的文字到文字模型。

### 補充來源

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — 之後的多任務測試，目標是知識而非句子理解。
