---
translation_reviewed: 2026-10-28
---

# 大型語言模型的蒸餾

語言模型的蒸餾，是透過在大型模型生成的文字上訓練，把大型模型的行為轉移到小型模型中，通常也包括它的推理過程。它是今日實務上最常使用的[知識蒸餾](../index.zh-TW.md)形式，因為教師能便宜地產生大量訓練資料。

## 概述

常見的做法有兩種。在**序列層級**蒸餾中，教師對一組提示生成回應，學生以一般的監督式學習訓練。在**同策略**（on-policy）蒸餾中，學生生成自己的回應，由教師評分，使學生在它實際產生的分布上訓練。第三種做法是把推理軌跡（強模型所寫的逐步解法）蒸餾到小模型中，使它學會以類似的方式推理。

## 方法比較

| 方法 | 訓練資料 | 散度或損失 | 典型用途 | 頁面 |
| --- | --- | --- | --- | --- |
| 序列層級 KD | 教師的最佳輸出 | 對教師序列的一般最大似然 | 翻譯與生成 | [序列層級 KD](sequence-level/index.zh-TW.md) |
| MiniLLM | 學生自己的樣本，由教師評分 | 反向 KL，以策略梯度最佳化 | 指令遵循模型 | [MiniLLM](minillm/index.zh-TW.md) |
| DeepSeek-R1 蒸餾 | 大型推理模型的推理軌跡 | 監督式微調 | 小型推理模型 | [DeepSeek-R1 蒸餾](deepseek-r1/index.zh-TW.md) |

序列層級蒸餾最簡單也最便宜，因為教師的輸出只需生成一次。MiniLLM 的成本較高，因為教師要在訓練期間為學生的樣本評分，但它消除了訓練與生成之間的不一致。推理蒸餾把序列層級的做法應用在很長的軌跡上，此時軌跡的品質最為重要。

## 關鍵概念

- **教師生成的資料。** 大型模型產生的回應，作為小型模型的訓練目標。
- **同策略訓練。** 在學生自己的樣本上訓練，由教師評分，減少訓練與生成之間的不一致。
- **推理軌跡。** 模型在給出答案前寫下的中間步驟。蒸餾推理軌跡轉移的是解題方式，而不只是最終答案。
- **模型家族。** 學生通常是同一家族的較小模型，因此分詞器與輸出空間相同。

## 取捨

- **品質與生成成本。** 教師生成的資料與人工標籤相比很便宜，但很長的推理軌跡生成成本高。
- **教師的使用條款。** 用專有模型的輸出訓練學生，可能受供應商的限制。
- **多樣性。** 只在教師輸出上訓練的學生，可能繼承教師的風格，也可能漏掉它的失敗模式。

## 更多變體與開放問題

- **變體。** [無資料蒸餾](../data-free/index.zh-TW.md)，其中合成資料來自教師而不需提示。
- **開放問題。** 學生從推理軌跡中學到什麼，以及它能否推廣到訓練資料之外的任務。
- **開放問題。** 如何衡量蒸餾後的模型是否忠於教師的推理，而不只是最終答案。

## 相關連結

語言模型蒸餾位於[訓練](../../../../engineering/training/index.zh-TW.md)流程與[大型語言模型](../../../models/llm/index.zh-TW.md)頁之間，後者把蒸餾列為降低成本的方法之一。大型模型為小模型生成訓練資料，類似人們從示範範例中學習，這在[認知科學](../../../../brain-mind/cognitive-science/index.zh-TW.md)中討論。

## 參考文獻

### 開創性論文

- Gu, Y., Dong, L., Wei, F., Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — 同策略蒸餾，在學生自己的樣本上訓練，可擴展到 1.2 億至 130 億參數。
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — 顯示大型模型的推理模式能用來增強小型模型。
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — 以教師自己的序列輸出訓練，是早期的語言模型蒸餾形式。
- Sanh, V., 等人 (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 蒸餾出的語言模型，比 BERT 小 40%，保留其 97% 的語言理解能力。

### 綜述與教科書

- Gou, J., 等人 (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾，作為上述語言模型方法的背景。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 原始的蒸餾目標，語言模型方法即以此為基礎。
