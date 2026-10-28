---
translation_reviewed: 2026-10-28
---

# 漸進剪枝

漸進剪枝在訓練期間平滑地提高網路的稀疏度，而不是一次剪到底。Zhu 與 Gupta 用它來比較大型稀疏網路與相同參數量的小型稠密網路，結果發現稀疏網路持續表現較好。它是疊加在[量值剪枝](../index.zh-TW.md)之上的排程。

## 問題

剪枝論文通常把剪枝後的網路與其原始稠密網路比較。在固定參數預算下，剪枝是否比從頭訓練一個較小的稠密網路更好，並不清楚。

## 核心想法

在相同參數數量下比較大型稀疏模型與小型稠密模型，並在訓練期間逐步剪枝大型模型。網路能適應每次小幅度的剪除，因此漸進排程能比一次剪到同樣稀疏度恢復更多準確度。

## 公式或演算法

稀疏度依平滑的三次排程，從零隨訓練步數升到目標值。每一步都遮蔽量值最小的權重，直到達到當前稀疏度，然後在剩餘權重上繼續訓練。排程以許多小幅剪除取代一次大剪除。

## 結果

作者發現，在他們測試的各種架構中，相同參數數量下大型稀疏模型都持續優於小型稠密模型。

## 限制

漸進排程需要額外的訓練步數。比較的基準是固定參數數量，這不等於固定計算量，因為稀疏層在稠密硬體上不一定跑得更快。

## 開放問題與相關變體

- **排程轉移。** 為一種架構調整的排程，能否不重新調參就轉移到另一種架構，目前沒有定論。
- **相關**：[彩票假說](../../lottery-ticket/lottery-ticket-hypothesis/index.zh-TW.md)的程序也是逐步剪枝，但它會把剩餘權重倒回到訓練的早期點。

## 相關連結

漸進排程是[同時學習權重與連接](../../learning-weights-and-connections/index.zh-TW.md)中迭代剪枝的一種形式。把量值剪枝放在其他方法之中做比較的基準，見[神經網路中稀疏性的現況](../state-of-sparsity/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — 提出漸進排程，並顯示大型稀疏模型優於小型稠密模型。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 漸進排程所改進的迭代剪枝加重新訓練流程。
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 將漸進量值剪枝與其他稀疏化方法做基準比較。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述訓練期間稀疏度的排程。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — 倒回並重新訓練，是漸進排程的替代方案。
