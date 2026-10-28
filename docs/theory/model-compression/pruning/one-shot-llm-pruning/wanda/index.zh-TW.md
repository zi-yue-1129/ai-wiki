---
translation_reviewed: 2026-10-28
---

# Wanda

Wanda（Pruning by Weights and Activations，依權重與激活剪枝）是一種針對大型語言模型的一次性剪枝方法。它以權重幅度乘上對應輸入激活的範數來為每個權重評分，並在每個輸出內移除分數最低的權重。它不需要重新訓練，也不更新權重，因此比 [SparseGPT](../sparsegpt/index.zh-TW.md) 便宜得多。

## 問題

SparseGPT 很準確，但每一層都需要二階計算。若有一種更簡單、能擴展到大型模型的方法，會更容易被採用，特別是在校準時間有限的情況下。

## 核心想法

當權重大、且它所乘的輸入也大時，該權重才重要。以這兩者的乘積為每個權重評分，並在每個輸出中剪除分數最低的權重。其他權重一律不變。

## 公式或演算法

權重 \(W_{ij}\) 的分數為

\[
S_{ij} = |W_{ij}| \cdot \lVert X_j \rVert_2
\]

其中 \(X_j\) 是權重 \(j\) 所乘的輸入特徵，在一小組校準資料上計算。分數最低的權重在每個輸出內被移除，因此每個輸出保持相同的稀疏度。剪枝後的模型直接使用，不需重新訓練，也不更新權重。

## 結果

摘要報告，Wanda 在大型語言模型上明顯優於幅度剪枝這個既有基準。作者也報告，它與需要大量權重更新的 SparseGPT 相比具有競爭力。這些結果是在 LLaMA 與 LLaMA-2 模型系列上取得的。

## 限制

此方法移除權重後不修正剩餘的權重。它相對於 SparseGPT 的優勢在於成本與簡單性，而不是準確率全面領先；且論文的結果是針對 LLaMA 系列。

## 未解問題與相關變體

- **高稀疏度。** 如何把廉價的分數與輕量的修正步驟結合，以縮小與 SparseGPT 在高稀疏度下的剩餘差距，仍是未解問題。
- **相關。** [SparseGPT](../sparsegpt/index.zh-TW.md) 加入了本方法所省略的權重更新。

## 與其他主題的連結

Wanda 的分數是「幅度乘激活」的規則，把簡單的[幅度剪枝](../../magnitude-pruning/index.zh-TW.md)基準擴展為同時使用輸入。非結構化的結果需要 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)中討論的稀疏核心，才能加速推論。

## 參考文獻

### 奠基性論文

- Sun, M., Liu, Z., Bair, A., Kolter, J. Z. (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — Wanda，以「幅度乘激活」的分數按輸出剪枝且不重新訓練；明顯優於幅度剪枝。
- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — Wanda 所對照的、會更新權重的一次性方法。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 含再訓練的幅度剪枝，是 Wanda 所改良的基準。

### 綜述與教科書

- Hoefler, T., Alistarh, D., Ben-Nun, T., Dryden, N., Peste, A. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述稀疏分數及其取捨。

### 講座與影片

（本頁未檢核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Wanda 所擴展的幅度剪枝基準。
