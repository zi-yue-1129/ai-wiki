---
translation_reviewed: 2026-10-28
---

# 穩定彩票

穩定彩票的研究把[彩票假說](../lottery-ticket-hypothesis/index.zh-TW.md)延伸到較深的網路。Frankle 等人發現，把剩餘權重重設到初始化對較大的模型會失敗，但若倒回到訓練中一個早期點（在最初的不穩定步驟之後），就能找到獲勝彩票。

## 問題

對於較深的網路，重設到初始化無法產生獲勝彩票，因此假說似乎在小型模型之外失效。

## 核心想法

把剩餘權重倒回到訓練的一個早期迭代，而不是初始化。這個早期點選在訓練最初的不穩定階段之後，使倒回的權重是穩定的。作者也尋找能在訓練早期辨識出的子網路。

## 公式或演算法

修改迭代程序：遮罩取自早期迭代 \(k\)，剩餘權重倒回到迭代 \(k\) 的權重。然後從那裡繼續訓練，並以相同方式重複剪枝。

## 結果

摘要描述這個修改後的程序是在尋找那些可以在訓練早期剪枝得到的子網路，並把彩票延伸到較深的網路。

## 限制

找到彩票仍需要完整的稠密訓練，直到倒回點，因此這個方法本身不會節省訓練計算量。

## 開放問題與相關變體

- **倒回點。** 合適的倒回點取決於網路與資料集，只能靠實驗找到。
- **相關**：[漸進剪枝](../../magnitude-pruning/gradual-pruning/index.zh-TW.md)在單次訓練中剪枝，因此不需要重複訓練。

## 相關連結

穩定的程序是把彩票概念擴展到[訓練](../../../../../engineering/training/index.zh-TW.md)實務中所用網路的版本。哪些稀疏子網路能良好訓練，也是[深度學習理論](../../../../../theory/deep-learning/index.zh-TW.md)的問題。

## 參考文獻

### 開創性論文

- Frankle, J., Dziugaite, G. K., Roy, D. M., Carbin, M. (2019). *Stabilizing the Lottery Ticket Hypothesis*. arXiv:1903.01611. https://arxiv.org/abs/1903.01611 — 倒回到早期訓練點，在較深網路中找到獲勝彩票。
- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — 本研究所修改的原始重設到初始化程序。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 彩票程序所延伸的迭代剪枝加重新訓練流程。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述透過倒回找到的彩票。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 將彩票產生的稀疏網路與其他方法做基準比較。
