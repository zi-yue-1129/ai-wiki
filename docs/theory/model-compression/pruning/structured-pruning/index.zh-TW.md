---
translation_reviewed: 2026-10-28
---

# 結構化與通道剪枝

結構化剪枝移除整個單位，例如濾波器、通道、神經元、注意力頭或區塊，而不是個別權重。結果是較小的稠密網路，一般硬體不需特殊稀疏核心就能跑得更快。因此，當標準加速器上的速度比最高稀疏度更重要時，結構化剪枝通常是首選。

## 概述

有 \(C\) 個輸出通道的卷積層，可以連同其濾波器一起失去一個通道，並移除下一層對應的輸入通道。Transformer 也能以相同方式移除注意力頭或前饋神經元。這個方法有兩個部分：依重要性對單位排序的分數，以及移除排序最低的單位，同時保持網路一致的規則。

## 關鍵概念

- **濾波器與通道剪枝**：移除卷積的一個輸出通道，同時移除下一層對應的輸入通道。
- **重要性分數**：常見選擇包括濾波器的範數、批次正規化的縮放因子，或移除該單位後損失的變化。
- **加速與壓縮**：移除通道同時減少參數與計算量，但兩者的比例取決於移除的位置。
- **一致性**：移除後網路仍須定義良好，這限制了哪些通道可以一起移除，例如殘差連接的情形。

## 各重要方法比較

| 方法 | 重要性分數 | 頁面 |
| --- | --- | --- |
| 濾波器剪枝 | 每個濾波器權重的 \(\ell_1\) 範數 | [濾波器剪枝](filter-pruning/index.zh-TW.md) |
| 網路瘦身 | 批次正規化的縮放因子，並以 \(\ell_1\) 懲罰壓低 | [網路瘦身](network-slimming/index.zh-TW.md) |

濾波器剪枝不需改動訓練，但它只看濾波器本身的權重來評分。網路瘦身則在訓練時加入懲罰，使分數更直接反映訓練後網路的狀況；它也需要架構中有批次正規化。

## 取捨

- **標準硬體上的速度與稀疏度**：結構化剪枝能在稠密加速器上帶來真正的加速，但它移除的單位較粗，在相同準確度下通常達到的稀疏度低於非結構化剪枝。
- **評分成本**：像範數這類便宜的分數，比衡量損失影響的分數較不準確。
- **架構依賴**：殘差連接與注意力頭需要保持網路有效的規則，因此方法在不同架構間有所不同。

## 更多變體與開放問題

- **變體**：[N:M 稀疏](../n-m-sparsity/index.zh-TW.md)，一種介於非結構化與結構化之間的細緻模式。
- **開放問題**：如何在大型 Transformer 中剪除注意力頭與前饋神經元，而不需要完整成本的重新訓練。
- **開放問題**：批次正規化因子對沒有批次正規化的架構是否仍然有意義。

## 相關連結

結構化剪枝符合 [AI 加速器](../../../../engineering/hardware/index.zh-TW.md)的稠密矩陣單元，因此在部署中很常見。它與生物界消除整條路徑的現象之間的連結，在[神經科學](../../../../brain-mind/neuroscience/index.zh-TW.md)中討論。

## 參考文獻

### 開創性論文

- Li, H., Kadav, A., Durdanovic, I., Samet, H., Graf, H. P. (2016). *Pruning Filters for Efficient ConvNets*. arXiv:1608.08710. https://arxiv.org/abs/1608.08710 — 濾波器剪枝，在 CIFAR-10 上使 VGG-16 的推論成本最多降低 34%。
- Liu, Z., 等人 (2017). *Learning Efficient Convolutional Networks through Network Slimming*. arXiv:1708.06519. https://arxiv.org/abs/1708.06519 — 以批次正規化縮放因子加 \(\ell_1\) 懲罰來選擇要移除的通道。
- He, Y., Zhang, X., Sun, J. (2017). *Channel Pruning for Accelerating Very Deep Neural Networks*. arXiv:1707.06168. https://arxiv.org/abs/1707.06168 — 以 LASSO 迴歸選擇通道，再以最小平方法重建該層輸出，使 VGG-16 加速 5 倍，誤差只增加 0.3%。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 非結構化剪枝，是結構化方法所對照的基準。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 比較訓練與推論中的結構化與非結構化稀疏。
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 比較各種稀疏化方法，包括結構化方法。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

（本頁尚未查核任何項目）
