---
translation_reviewed: 2026-10-28
---

# MiniLLM

MiniLLM 透過讓學生在自己生成的文字上訓練（由教師評分），來蒸餾大型語言模型，而不是只在教師的文字上訓練。Gu 等人以反向 KL 取代常用的前向 KL 散度，使學生不會把機率放在教師認為不太可能的區域。論文報告此方法可以擴展到 1.2 億至 130 億參數的不同模型家族。它是[語言模型蒸餾](../index.zh-TW.md)中的[同策略](../index.zh-TW.md)方法，也是[序列層級蒸餾](../sequence-level/index.zh-TW.md)最接近的親戚。

## 問題

標準的語言模型蒸餾，是在教師產生的序列或教師對這些序列的分布上訓練學生。然而在生成時，學生產生的是它自己的序列。早期的錯誤因此會累積，因為學生會進入訓練時從未見過的狀態。標準蒸餾所用的前向 KL 也會促使學生把機率分散到教師的每一個模式上，包括它難以匹配的模式。

## 核心想法

從學生取樣回應，並請教師評估學生的每個回應有多可能。在學生自己的樣本上，以反向 KL 訓練學生。反向 KL 是模式尋求的：學生集中在教師認為可能的輸出上，而不是覆蓋教師分布的全部。

## 公式或演算法

令 \(p\) 為教師的分布，\(q_\theta\) 為學生的分布。標準蒸餾最小化前向 KL \(\mathrm{KL}(p \Vert q_\theta)\)。MiniLLM 則最小化反向 KL \(\mathrm{KL}(q_\theta \Vert p)\)，並在學生自己的樣本上進行最佳化。由於抽樣本身不可微分，梯度以策略梯度式的方法估計；論文另外加入降低變異的技巧，並使長序列生成的訓練更穩定。

## 結果

摘要報告，此方法可擴展到 1.2 億至 130 億參數的不同模型家族。與基準的比較，包括指令遵循等任務，見論文。

## 限制

策略梯度式的更新比監督式蒸餾更複雜、成本更高，而且需要教師在訓練期間為學生的樣本評分。長序列生成時的最佳化穩定性，是實務上的一個疑慮。

## 開放問題與相關變體

- **散度的選擇。** 反向 KL 是模式尋求的，前向 KL 則是模式覆蓋的。哪一種散度適合特定任務，或兩者混合是否更好，尚無定論。
- **同策略抽樣的成本。** 每一步都從學生生成樣本，成本很高；重複使用樣本的較便宜方案，是開放的研究領域。
- **相關：** [序列層級蒸餾](../sequence-level/index.zh-TW.md)在教師的輸出上訓練，避開了同策略的成本，但也承受了 MiniLLM 所處理的不一致。

## 相關連結

同策略訓練是強化學習的概念，因此此方法與[訓練](../../../../../engineering/training/index.zh-TW.md)流程相連，也與[大型語言模型](../../../../../theory/models/llm/index.zh-TW.md)頁中以回饋進行後訓練的討論相關。

## 參考文獻

### 開創性論文

- Gu, Y., Dong, L., Wei, F., Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — 在學生自己的樣本上以反向 KL 訓練，可擴展到 1.2 億至 130 億參數。
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — MiniLLM 所改進的教師輸出方法，學生速度快 10 倍。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 以前向 KL 為基礎的軟目標，此方法以反向 KL 取代它。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾，以及用來匹配教師的各種散度。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — 後來大規模使用教師生成的推理來訓練小模型的例子。
