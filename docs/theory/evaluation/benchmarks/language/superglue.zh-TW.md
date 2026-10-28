---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# SuperGLUE

SuperGLUE 是 [GLUE](glue.md) 的後繼基準。它保留「在多個語言理解任務上取一個分數」的做法，但使用更困難的任務、一套軟體工具包與公開排行榜（Wang et al., 2019）。

## 任務與資料

SuperGLUE 包含八個任務，涵蓋閱讀理解、問答、詞義消歧、指代消解與文本蘊涵。有些任務需要超越句子間表面重疊的推理（Wang et al., 2019）。

## 協定與指標

每個任務有各自的指標，整體分數是它們的平均。作者報告了人類基準，因此可以說明模型在同一任務上距離人類多遠。測試標籤不公開，結果透過排行榜提交。

## 它能說明什麼

這個基準是在模型已超越 GLUE 上非專家人類分數之後建立的，目的是恢復進步的空間（Wang et al., 2019）。預訓練的文字到文字模型報告了它的結果（Raffel et al., 2019），它因此成為英文遷移學習的標準測試。

## 限制

- **污染。** 由網路文字建立的預訓練語料，可能含有任務資料或近似重複的內容，因此高分可能部分反映記憶。
- **飽和。** 頂尖系統已接近人類基準，因此這個基準現在能區分的系統比發表時少。
- **只有英文。** 這些任務不測試其他語言。
- **排行榜的使用。** 反覆提交到隱藏的測試集，可能是在擬合排行榜，而非任務本身。比較分數前應先閱讀提交規則。

## 相關

- [GLUE](glue.md) 是這個基準所取代的基準。
- [MMLU](mmlu.md) 與 [GPQA](gpqa.md) 測試的是知識與專家推理，而非句子層級的理解。
- [語言家族概述](index.md) 比較各語言基準。

## 參考文獻

### 開創性論文

- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — 介紹這個基準、其任務、工具包與人類基準。
- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — SuperGLUE 所要取代的基準。

### 文章與文件

- Raffel, C. et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv. https://arxiv.org/abs/1910.10683 — 報告文字到文字模型在 SuperGLUE 任務上的結果。
- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL. https://arxiv.org/abs/1810.04805 — 預訓練編碼器，其遷移結果促成了更困難的基準。

### 補充來源

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 以上下文範例評估大型模型，這類基準即屬此類。
