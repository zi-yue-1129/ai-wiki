---
translation_reviewed: 2026-10-28
---

# DeepSeek-R1 蒸餾

DeepSeek-R1 蒸餾，是透過在大型模型的推理軌跡上訓練小模型，把大型模型的推理能力轉移到較小的模型中。DeepSeek-AI 的報告顯示，大型模型中發現的推理模式可以用來增強小型模型；並報告，蒸餾這些模式的效果優於直接對小模型進行強化學習。它是[語言模型蒸餾](../index.zh-TW.md)的一種方法，對很長的推理輸出而言，也是一種[序列層級蒸餾](../sequence-level/index.zh-TW.md)。

## 問題

強的多步推理一直被認為需要非常大的模型。小型模型若從頭以強化學習訓練，推理能力不如大型模型；而小模型能否以更低的成本學會同樣的行為，尚不清楚。

## 核心想法

先以強化學習訓練大型模型，直到它推理得很好，然後把它的推理軌跡當作較小模型的監督式訓練資料。小模型學會寫出同類的逐步解答，而不需要自己執行強化學習。

## 公式或演算法

大型模型針對一組提示生成推理軌跡與答案，並經過品質篩選。接著，從 Qwen 與 Llama 等開放基礎模型家族取得的小模型，以一般的下一個 token 目標在這些軌跡上微調。這一步是監督式學習，因此在小模型規模上不需要獎勵模型。

## 結果

摘要表示，大型模型發現的推理模式，可以被系統性地用來引導並增強小型模型的推理能力。論文報告，蒸餾後的模型表現優於直接對小模型套用強化學習。基準數字見論文。

## 限制

學生的推理受限於教師的推理，而訓練資料是很長的推理軌跡，生成成本高。論文並未隔離比較中的每個因素，因此差距取決於所選的基準。

## 開放問題與相關變體

- **忠實度。** 學生的推理是遵循教師的步驟，還是只模仿其形式，仍是開放問題。
- **推廣性。** 在數學與程式碼上學到的推理，可能無法轉移到其他領域。
- **相關：** [MiniLLM](../minillm/index.zh-TW.md)在學生自己的樣本上訓練，而不是固定的軌跡，從而減少訓練與生成之間的不一致。

## 相關連結

「推理可以透過模仿來教」的想法，與[大型語言模型](../../../../../theory/models/llm/index.zh-TW.md)頁中思維鏈行為的討論相關。生成軌跡的成本，則是[訓練](../../../../../engineering/training/index.zh-TW.md)的考量。

## 參考文獻

### 開創性論文

- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — 顯示大型模型的推理模式能用來增強小型模型。
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — 較早的教師輸出方法，在教師的最佳序列上訓練。
- Gu, Y., Dong, L., Wei, F., Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — 同策略蒸餾，是改在學生自己樣本上訓練的替代方案。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾，作為用教師輸出訓練小模型的背景。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 原始的蒸餾目標，推理蒸餾將它延伸到文字。
