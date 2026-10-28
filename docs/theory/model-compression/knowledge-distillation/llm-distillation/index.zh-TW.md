---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
- theory/models/llm
- engineering/training
tags:
- model compression
- knowledge distillation
- large language models
aliases:
  - 大型語言模型蒸餾
  - LLM distillation
  - On-policy distillation
  - Reasoning distillation
---

# 大型語言模型的蒸餾

語言模型的蒸餾，是透過在大型模型生成的文字（通常包括其推理過程）上訓練，把大型模型的行為轉移到較小的模型上。它是目前實務中最常用的[知識蒸餾](../index.zh-TW.md)形式，因為教師可以低成本地產生大量訓練資料。

## 概觀

常見的做法有兩類。在**序列層級（sequence-level）**蒸餾中，教師對一組提示生成回應，學生再以一般的監督式學習在這些回應上訓練。在**同策略（on-policy）**蒸餾中，學生自己生成回應，教師為其打分，因此學生是在它實際產生的分布上訓練。第三種做法是蒸餾推理軌跡（reasoning traces），也就是強大模型寫出的逐步解題過程，把它們轉移到較小的模型上，使其學會產生類似的軌跡。

## 關鍵概念

- **教師生成的資料。** 由大型模型產生的回應，作為小型模型的訓練目標。
- **同策略訓練。** 在學生自己的樣本上訓練，並由教師評分，從而減少訓練與生成之間的不一致。
- **推理軌跡。** 模型在給出答案前寫下的中間步驟。蒸餾它們，轉移的是解題的方式，而不只是最後答案。
- **模型家族。** 學生通常是同一家族中的較小模型，因此分詞器與輸出空間相符。

## 主要方法

以下三個代表性方法都是用大型模型的輸出訓練小型模型，但資料由誰生成、訓練目標為何，各有不同。

- [序列層級知識蒸餾（Kim 與 Rush，2016）](sequence-level/index.zh-TW.md)：由教師產生序列，學生以一般的最大概似估計學習。這是最簡單的做法，也是語言模型蒸餾最早的形式。
- [MiniLLM（Gu 等人，2023）](minillm/index.zh-TW.md)：學生自己產生樣本，訓練使用反向 KL 目標與同策略最佳化方法，針對訓練與生成之間的不一致。
- [DeepSeek-R1 蒸餾（DeepSeek-AI，2025）](deepseek-r1/index.zh-TW.md)：以大型推理模型的推理模式訓練較小的模型；論文報告這些模式可以提升小模型的推理能力。

序列層級蒸餾最便宜，因為教師的輸出只需生成一次。MiniLLM 成本較高，因為訓練時教師要為學生的樣本打分，但它處理了訓練與生成之間的不一致。推理蒸餾把序列層級的做法套用到很長的軌跡上，此時軌跡的品質最為關鍵。

## 取捨

- **品質與生成成本。** 教師生成的資料與人工標註相比成本低，但很長的推理軌跡生成起來很昂貴。
- **教師的使用條款。** 以專有模型的輸出訓練學生，可能受供應商規定限制。
- **多樣性。** 只用教師輸出訓練的學生，可能承襲教師的風格，也可能漏掉教師的失敗模式。

## 更多變體與未解問題

- **變體：**[無資料蒸餾](../data-free/index.zh-TW.md)，合成資料由教師在沒有提示的情況下產生。
- **未解問題：**學生從推理軌跡中學到什麼，以及這種能力能否超出訓練資料中的任務。
- **未解問題：**如何衡量蒸餾後的模型是否忠實於教師的推理，而不只是最後答案。

## 關聯

大型語言模型的蒸餾位於[訓練](../../../../engineering/training/index.zh-TW.md)流程與[大型語言模型](../../../models/llm/index.zh-TW.md)頁面之間，後者把蒸餾列為降低成本的方法之一。用大型模型為小型模型產生訓練資料，類似人從範例中學習的方式，相關討論見[認知科學](../../../../brain-mind/cognitive-science/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Kim, Y. & Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — 在教師自身的序列輸出上訓練；摘要報告學生速度約為教師的 10 倍，品質損失很小。
- Gu, Y., Dong, L., Wei, F. & Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — 以反向 KL 取代標準蒸餾的前向 KL，並以同策略方式最佳化；摘要報告此方法可套用於 1.2 億至 130 億參數的模型。
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — 報告大型模型以強化學習訓練出的推理能力，並指出大型模型的推理模式可用來提升小型模型。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 最初的蒸餾目標，上述語言模型方法都建立在它之上。

### 綜述與教科書

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — 回顧蒸餾，是上述語言模型方法的背景。

### 講座與影片

（本頁未查核）

### 文章與文件

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 將 BERT 蒸餾為約小 40% 的模型，同時保留 97% 的語言理解能力；是蒸餾預訓練語言模型的早期範例。
