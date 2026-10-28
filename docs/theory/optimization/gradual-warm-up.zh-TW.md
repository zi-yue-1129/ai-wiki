---
translation_reviewed: 2026-10-28
---

# 漸進式預熱與線性縮放

漸進式預熱是一種學習率排程，開頭從小值出發，並在訓練的前段逐步上升。Goyal 等人（2017）把它與線性縮放規則結合：批次大小乘以 \(k\) 時，學習率也乘以 \(k\)。如此，ResNet 得以在極大的小批次上訓練而不損失準確率。上層概述見[學習率排程與預熱](learning-rate-schedules.md)。

## 概述

若批次大小乘以 \(k\)，梯度就是對 \(k\) 倍的樣本取平均，雜訊因此較少。線性縮放規則主張學習率也應以同樣的 \(k\) 倍成長，使每個 epoch 的進展大致不變。但在實務中，若從第一步就套用大的學習率，隨機初始化網路的早期梯度並不可靠，權重可能被推入不佳的區域。預熱就是針對這個問題的做法。

## 問題

大批次訓練的吸引力在於能以許多加速器並行運算。然而，若排程不改變，批次越大，準確率就越低。Goyal 等人想知道，是否有一條簡單的規則，能在不做調校的情況下，於大批次下維持準確率。

## 核心想法

兩項改變。第一，學習率依小批次大小線性縮放。第二，學習率從小的基礎值開始，在前幾個 epoch 內升到縮放後的目標值，而不是一步跳上去。

## 演算法

令 \(\eta\) 為批次大小 \(n\) 時的基礎學習率，而實際批次為 \(kn\)。

1. 大批次的學習率設為 \(k\eta\)（線性縮放規則）。
2. 在預熱期間，從 \(\eta\) 出發，每次迭代增加固定的量。論文的排程在 5 個 epoch 後達到 \(\hat\eta = k\eta\)。
3. 預熱結束後，改用一般的衰減排程。

論文指出，結果對預熱的確切長度並不敏感。

對於 Transformer，Vaswani 等人（2017）使用相關的預熱，之後接反平方根衰減：

\[
\mathrm{lrate} = d_{\mathrm{model}}^{-0.5}\cdot \min\!\left(\mathrm{step}^{-0.5},\ \mathrm{step}\cdot \mathrm{warmup\_steps}^{-1.5}\right)
\]

在 \(\mathrm{warmup\_steps} = 4000\) 時，學習率在前 4000 步線性上升，之後與步數的平方根倒數成比例下降。

## 結果

- Goyal 等人（2017）報告，在 ImageNet 上，批次大小達 8192 張圖片時「沒有準確率損失」。
- 他們報告，在所述硬體上，以 256 張 GPU、批次 8192 訓練 ResNet-50 只需一小時，從 8 張擴展到 256 張 GPU 時約有 90% 的擴展效率。
- Vaswani 等人（2017）的 Transformer 排程使用 warmup_steps = 4000，此數值為論文所述。

## 限制

- 線性縮放規則不需要額外的超參數，但它只在論文研究的大批次範圍內測試過，其他設定可能需要不同的縮放方式。
- 5 個 epoch 的預熱，在 ImageNet 上的 ResNet-50 已證實穩健，但這並非通用的規定，其他任務可能需要更長或更短的上升段。
- Transformer 排程透過 \(d_{\mathrm{model}}\) 把學習率與模型寬度綁在一起，因此相同的數字換到不同寬度時，需要重新檢查。

## 關聯

- [學習率排程與預熱](learning-rate-schedules.md)是比較本方法與餘弦重啟、循環學習率的上層概述。
- [大批次與分散式訓練](large-batch-and-distributed.md)是線性縮放與預熱最重要的場景。
- [餘弦退火與暖重啟](cosine-annealing-warm-restarts.md)是預熱之後常接的衰減。
- [Transformer](../models/transformer/index.md)幾乎所有訓練流程都使用預熱。

## 開放問題

- 預熱是在解決訓練初期的最佳化問題，還是主要在穩定正規化統計量？
- 線性縮放規則在其他架構、遠超過 8192 的批次大小下是否仍成立？

## 參考文獻

### 開創性論文

- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 線性縮放規則與漸進式預熱，以及批次大小 8192 的 ResNet-50 結果。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 附線性預熱與反平方根衰減的 Transformer 排程。
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — 較晚的排程，同樣在重啟後以較高的學習率開始每一輪。
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — 另一種在界限之間變化學習率的排程，供比較之用。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機梯度方法的綜述，包含預熱背後的步長選擇。
