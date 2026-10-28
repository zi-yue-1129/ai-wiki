---
translation_reviewed: 2026-10-28
---

# 從頭學習 N:M 稀疏網路

從頭學習 N:M 稀疏網路，是從第一步開始就在訓練中施加 N:M 限制，而不是先訓練稠密網路、之後再剪成該模式。Zhou 等人顯示，模式可以在整個訓練過程中維持而不損失準確度，並報告 2:4 稀疏網路在 NVIDIA A100 GPU 上有 2 倍加速。它是 [N:M 稀疏](../index.zh-TW.md)中的一種方法。

## 問題

N:M 稀疏對硬體友善，但不清楚能否從頭以這個模式訓練網路而不損失準確度。訓練後再剪成模式是一種選擇，但被剪掉的權重在能調整之前就已移除。

## 核心想法

在訓練期間施加 N:M 限制，使權重與它們的選擇一起在模式下演變。網路從不需要從一次性剪到模式的衝擊中恢復。

## 公式或演算法

在每 \(M\) 個權重的區塊中，最多 \(N\) 個可以是非零。非零的選擇會隨權重改變而更新。確切的更新規則見論文。

## 結果

摘要表示，2:4 稀疏網路在 NVIDIA A100 GPU 上可以達到 2 倍加速，且沒有效能下降。

## 限制

報告的加速只適用於硬體加速的矩陣乘法，不是整個模型。實驗使用當時的網路。

## 開放問題與相關變體

- **較大的區塊。** 從頭訓練在較大區塊的模式（例如 4:8）上是否可行，研究較少。
- **相關**：[稀疏張量核心](../sparse-tensor-cores/index.zh-TW.md)說明硬體與 2:4 模式的剪枝流程。

## 相關連結

這個模式是硬體設計塑造方法的例子，其效益取決於目標裝置的[記憶體層級](../../../../../engineering/hardware/index.zh-TW.md)與矩陣單元。

## 參考文獻

### 開創性論文

- Zhou, A., 等人 (2021). *Learning N:M Fine-grained Structured Sparse Neural Networks From Scratch*. arXiv:2102.04010. https://arxiv.org/abs/2102.04010 — 從頭以 2:4 模式訓練網路，在 A100 GPU 上有 2 倍加速。
- Mishra, A., 等人 (2021). *Accelerating Sparse Deep Neural Networks*. arXiv:2104.08378. https://arxiv.org/abs/2104.08378 — 說明稀疏張量核心執行的 2:4 模式。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 非結構化剪枝，是 N:M 稀疏所權衡的對象。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述稀疏模式與其硬體實作。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 比較稀疏性的準確度成本，這是 2:4 模式必須維持低成本的標準。
