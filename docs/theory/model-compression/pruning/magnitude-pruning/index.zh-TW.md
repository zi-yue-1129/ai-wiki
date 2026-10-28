---
translation_reviewed: 2026-10-28
---

# 量值剪枝

量值剪枝移除絕對值最小的權重，保留其餘權重。它是最古老也最簡單的[剪枝](../index.zh-TW.md)準則，至今仍是新方法必須超越的基準。它的優點是不需要額外的統計量、二階資訊，也不需要特殊硬體就能計算分數。

## 概述

給定權重張量 \(W\) 與稀疏度目標 \(s\)，量值剪枝建立遮罩 \(M\)，保留絕對值高於 \(|W|\) 之 \(s\) 分位數的權重，其餘設為零。一次完成就是單次剪枝；若重複進行並在其間重新訓練，或使用在訓練過程中逐步提高稀疏度的排程，則能恢復更多準確度。排程的選擇，以及門檻是全域還是逐層的，與評分規則同樣重要。

## 關鍵概念

- **分數**：權重的絕對值。它忽略權重與輸入之間的交互作用，這是後來的分數（例如 [Wanda](../one-shot-llm-pruning/wanda/index.zh-TW.md)）所要解決的弱點。
- **全域與逐層門檻**：全域門檻允許某些層剪得比其他層多；逐層門檻則使每層的稀疏度相同。
- **漸進排程**：稀疏度在訓練過程中從零逐步升到目標值，使網路能在剪枝的同時調整。
- **重新訓練**：每次剪枝後，剩餘權重繼續訓練以恢復準確度。

## 各重要方法比較

| 方法 | 相對於量值剪枝新增的內容 | 頁面 |
| --- | --- | --- |
| 漸進剪枝 | 訓練過程中的平滑稀疏度排程，證明優於小型稠密網路 | [漸進剪枝](gradual-pruning/index.zh-TW.md) |
| 基準研究 | 直接比較，顯示量值剪枝是強基準 | [神經網路中稀疏性的現況](state-of-sparsity/index.zh-TW.md) |

漸進剪枝改變的是遮罩何時被剪下。基準研究則問：更複雜的遮罩選擇是否值得，並發現對許多任務而言並不值得。

## 取捨

- **簡單性與高稀疏度下的準確度**：量值剪枝便宜，在中等稀疏度時很強。在非常高的稀疏度下，會修正剩餘權重的方法表現較好。
- **非結構化與結構化**：量值分數也可以用來剪除整個結構，但通常得到不規則的遮罩，需要稀疏核心才能加速。
- **排程成本**：漸進剪枝需要訓練時間，而計算量的節省取決於硬體。

## 更多變體與開放問題

- **開放問題**：為何在訓練好的網路中，權重的量值是重要性的良好代理。[彩票假說](../lottery-ticket/index.zh-TW.md)的研究從另一個角度探討這個問題。
- **變體**：量值乘以輸入範數，這是 [Wanda](../one-shot-llm-pruning/wanda/index.zh-TW.md) 的基礎。
- **開放問題**：漸進排程能否在不同架構間轉移而不需調參。

## 相關連結

量值剪枝得到非結構化遮罩，其加速取決於 [AI 硬體](../../../../engineering/hardware/index.zh-TW.md)中討論的稀疏核心。大腦在發育期間消除弱連接，與量值剪枝相似，此議題在[神經科學](../../../../brain-mind/neuroscience/index.zh-TW.md)中討論。

## 參考文獻

### 開創性論文

- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — 在相同參數數量下，大型稀疏模型優於小型稠密模型。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 量值剪枝加重新訓練，使 AlexNet 的參數減少為九分之一。
- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — 以量值剪枝找到的子網路，能從初始權重開始良好訓練。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 涵蓋訓練與推論稀疏化方法的廣泛綜述。
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 比較稀疏化方法，發現量值剪枝是強基準。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

（本頁尚未查核任何項目）
