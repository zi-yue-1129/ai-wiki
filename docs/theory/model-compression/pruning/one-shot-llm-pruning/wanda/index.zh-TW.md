---
translation_reviewed: 2026-10-28
---

# Wanda

Wanda（依權重與激活值剪枝）是大型語言模型的單次剪枝方法。它以權重量值乘以對應輸入激活值的範數來為每個權重評分，並在每個輸出列中移除分數最低的權重。它不需要重新訓練，也不更新權重，因此比 [SparseGPT](../sparsegpt/index.zh-TW.md) 便宜得多。

## 問題

SparseGPT 準確，但每層都需要二階計算。一個更簡單、能擴展到大型模型的方法，會更容易被採用，特別是在校準時間有限的情況下。

## 核心想法

一個權重重要，當它本身量值大，且它所乘的輸入也大。以兩者的乘積為每個權重評分，並在每個輸出列中剪除分數最低的權重。其他權重都不改變。

## 公式或演算法

權重 \(W_{ij}\) 的分數為 \(|W_{ij}| \cdot \lVert X_j \rVert_2\)，在校準輸入上計算。分數最低的權重在每個輸出列中被移除，因此每一列的稀疏度相同。

## 結果

作者報告，在大型語言模型上，Wanda 顯著優於量值剪枝這個既有基準。

## 限制

此方法移除權重時不修正剩餘權重，因此在非常高的稀疏度下，準確度損失比會更新權重的方法（例如 SparseGPT）大。

## 開放問題與相關變體

- **高稀疏度。** 如何把便宜的分數與輕量的修正步驟結合，以縮小與 SparseGPT 在高稀疏度時的差距，仍是開放問題。
- **相關**：[SparseGPT](../sparsegpt/index.zh-TW.md)增加了權重更新，而這個方法沒有。

## 相關連結

Wanda 的分數是量值乘以激活值的規則，把簡單的[量值剪枝](../../magnitude-pruning/index.zh-TW.md)基準擴展為使用輸入。這種非結構化結果需要 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)討論的稀疏核心才能加速推論。

## 參考文獻

### 開創性論文

- Sun, M., 等人 (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — Wanda，一種量值乘以激活值的分數，逐輸出列剪枝且不需重新訓練。
- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — 會更新權重的單次方法，Wanda 與它比較。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 搭配重新訓練的量值剪枝，是 Wanda 所改進的基準。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述稀疏化分數及其取捨。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Wanda 所擴展的量值基準。
