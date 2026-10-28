---
translation_reviewed: 2026-10-28
---

# LAMB

LAMB（用於批次訓練的逐層自適應動量）把 LARS 的逐層信任比套用到類似 Adam 的更新上。You 等人（2019）以它以極大批次訓練 BERT，把訓練時間從三天縮短到 76 分鐘（在 TPU Pod 上）。上層概述見[梯度裁剪與正規化更新](gradient-clipping-and-normalisation.md)，它所延伸的逐座標方法是 [Adam](adaptive/adam.md)。

## 概述

LARS 以信任比縮放每一層的步長，但它只適用於 SGD 類的更新。Transformer 通常以 Adam 訓練，而 Adam 的逐座標正規化對它們很重要。LAMB 保留 Adam 的更新（包含經偏差校正的一階與二階矩），然後以信任比縮放整層的更新量。其結果是一個自適應的最佳化器，每一層更新的大小與該層的權重範數（經 \(\phi\) 裁剪）成正比。

## 問題

摘要把目標陳述為：在大批次下訓練而不損失效能。對 BERT 而言，作者希望使用足夠大的批次，以大幅縮短訓練時間，並想知道基於 Adam 的方法能否在不損失準確率的情況下做到這一點。

## 核心想法

為每一層計算 Adam 方向，然後乘上信任比。信任比等於經 \(\phi\) 裁剪後的該層權重範數，除以更新的範數。如同 LARS，這使每一層的變化與自身權重成正比，同時保留 Adam 的逐座標行為。

## 演算法

對於第 \(\ell\) 層，參數為 \(x_t\)。令 \(r_t = \dfrac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}\) 為經偏差校正的 Adam 方向（不含權重衰減），\(\lambda\) 為權重衰減係數。令 \(\phi(z)=\min\{\max\{z,\gamma_l\},\gamma_u\}\) 為上下界為 \(\gamma_l\)、\(\gamma_u\) 的裁剪函數，\(\phi(z)=z\) 為其特例。

1. 計算信任比 \(\dfrac{\phi(\|x_t\|)}{\|r_t+\lambda x_t\|}\)。
2. 更新 \(x_{t+1} = x_t - \eta_t\,\dfrac{\phi(\|x_t\|)}{\|r_t+\lambda x_t\|}\,(r_t+\lambda x_t)\)。

此更新式已對照論文全文核對。

## 結果

- 摘要報告以 32,868 的極大批次訓練，且「沒有任何效能退步」。
- 摘要報告 BERT 的訓練時間可以「從三天縮短到只需 76 分鐘」，較短的時間來自把批次大小提高到 TPUv3 Pod 的記憶體上限。
- 摘要提及 BERT 與 ResNet-50 的訓練，並述及 LAMB 與 LARS 的收斂分析。

## 限制

- 所報告的加速依賴大型硬體，並非在單一機器上對演算法做的同條件比較。
- 裁剪函數 \(\phi\) 含有上下界 \(\gamma_l\) 與 \(\gamma_u\)，它們是另外需要選擇的設定。
- 收斂分析是一般性的結果，無法取代對目標模型的實證檢驗。

## 關聯

- [LARS](lars.md)是基於 SGD 的方法，LAMB 採用了它的信任比。
- [Adam](adaptive/adam.md)提供 LAMB 所縮放的更新。
- [AdamW](adaptive/adamw.md)把權重衰減與自適應步驟分開，LAMB 的更新也需要處理這一點。
- [漸進式預熱與線性縮放](gradual-warm-up.md)是大批次預訓練中與它一起使用的排程做法。
- [大批次與分散式訓練](large-batch-and-distributed.md)是此方法在實務中使用的場景。

## 開放問題

- 信任比在不同大小的 Transformer 上是否都有幫助，還是只在所研究的批次大小下有效？
- 在兩者都調校良好的情況下，LAMB 與沒有逐層縮放的自適應方法相比如何？

## 參考文獻

### 開創性論文

- You, Y., et al. (2019). *Large Batch Optimization for Deep Learning: Training BERT in 76 Minutes*. ICLR. https://arxiv.org/abs/1904.00962 — 提出 LAMB，一種基於 Adam 的逐層最佳化器，用於極大批次的 BERT 預訓練。
- You, Y., Gitman, I. & Ginsburg, B. (2017). *Large Batch Training of Convolutional Networks*. arXiv. https://arxiv.org/abs/1708.03888 — LAMB 延伸到 Adam 的 SGD 版信任比想法。
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — LAMB 逐層縮放的逐座標更新。
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. arXiv:1711.05101（ICLR 2019）. https://arxiv.org/abs/1711.05101 — 解耦的權重衰減，與信任比一同用於自適應更新。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 大規模訓練中自適應隨機方法及其取捨的綜述。
