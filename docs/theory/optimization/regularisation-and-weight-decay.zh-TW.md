---
translation_reviewed: 2026-10-28
---

# 最佳化中的正則化與權重衰減

正則化是任何使訓練偏好某些解、而非其他解的改動，通常是為了改善泛化能力。在最佳化中，它有三種形式：加在損失上的懲罰項、每一步施加在參數上的收縮，以及最佳化器本身的隱含偏好，後者來自步長、批次大小與梯度中的雜訊。損失面的觀點見[損失函數與最佳化](../paradigms/supervised/loss-functions-and-optimization/index.md)，本頁討論最佳化器如何與之互動。

## 概述

對於普通的梯度下降，在損失中加入 L2 懲罰 \(\frac{\lambda}{2}\|\theta\|^2\)，然後做一步梯度下降，等同於每一步把參數乘以 \(1-\eta\lambda\) 進行收縮。在 SGD 下兩種觀點一致；在自適應最佳化器下則會分開。懲罰項的梯度會進入自適應分母，因此梯度大的參數得到的衰減較少。Loshchilov 與 Hutter（2017）指出了這一點，而 [AdamW](adaptive/adamw.md) 則把衰減移到自適應步驟之外。

除了顯式的懲罰項，最佳化器本身也具有正則化作用。小批次與大步長會注入梯度雜訊，而這些雜訊傾向於偏好寬的極小值，而非窄的極小值。這種隱含偏好在[尖銳極小值](sharp-minima.md)與[SGD 雜訊尺度](sgd-noise-scale.md)兩頁中討論。

## 核心概念

- **L2 懲罰**：加在損失上的項 \(\frac{\lambda}{2}\|\theta\|^2\)，其梯度為 \(\lambda\theta\)。
- **權重衰減**：每一步施加的收縮 \(\theta \leftarrow (1-\eta\lambda)\theta\)，與梯度分開。
- **解耦**：以獨立的係數施加權重衰減，不受自適應縮放影響。
- **隱含正則化**：最佳化器動態帶來的、對特定解的偏好，不需要損失中有任何懲罰項。
- **雜訊注入**：刻意在梯度或參數上加入隨機擾動。

## 運作方式

依顯式程度由強到弱，有三種機制：

| 機制 | 作用位置 | 典型形式 |
|---|---|---|
| 損失中的懲罰項 | 梯度，由最佳化器縮放 | 加在 \(L(\theta)\) 上的 L2 |
| 解耦的衰減 | 參數，位於梯度之外 | \(\theta \leftarrow \theta - \eta(\nabla \hat L + \lambda\theta)\) |
| 隱含偏好 | 步長、批次大小、梯度雜訊 | 偏好寬的極小值，以及較小的有效學習率 \(\eta/B\) |

在 SGD 下，前兩者一致，因此要解釋不同批次大小之間的泛化差距，剩下的就是第三種。

## 關鍵方法

三個條目，各有頁面或連結。第一個是指向既有頁面的連結，因為該方法已在那裡說明。

| 方法 | 機制 | 區別所在 |
|---|---|---|
| [解耦權重衰減（AdamW）](adaptive/adamw.md)（Loshchilov 與 Hutter，2017） | 解耦的衰減 | 把懲罰移到自適應步驟之外，使衰減不會被二階矩重新縮放 |
| [尖銳極小值與大批次泛化](sharp-minima.md)（Keskar 等人，2017） | 批次大小的隱含偏好 | 在作者的實驗中，大批次收斂到的尖銳極小值泛化較差 |
| [SGD 雜訊尺度](sgd-noise-scale.md)（Smith 與 Le，2018） | 學習率與批次大小的隱含偏好 | 雜訊尺度 \(\epsilon N/B\) 決定泛化達到最佳時的批次大小 |

## 關聯

- [損失函數與最佳化](../paradigms/supervised/loss-functions-and-optimization/index.md)把懲罰項解釋為目標函數的一部分。
- [SGD 與動量](sgd-and-momentum/index.md)是 L2 與權重衰減一致的設定。
- [自適應方法](adaptive/index.md)是兩者分歧之處，而 [AdamW](adaptive/adamw.md) 是其修正。
- [學習率排程](learning-rate-schedules.md)與衰減互相影響，因為有效的收縮量取決於當前的學習率。
- [大批次與分散式訓練](large-batch-and-distributed.md)是隱含偏好結果最重要的場景。
- [權重範數動態](weight-norm-dynamics/index.md) 說明在正規化層中，衰減如何設定平衡範數。

## 應用

- 在 Transformer 與視覺訓練的配方中，設定權重衰減係數，通常與 AdamW 一起使用。
- 同時選擇批次大小與學習率，並以雜訊尺度規則作為指引。

## 開放問題

- 小批次的泛化優勢，是來自雜訊本身，還是來自較小的有效學習率？
- 當學習率與衰減係數在訓練中同時改變時，應如何一起調校？
- 最佳化器的隱含偏好，在加入顯式正則化項後是否仍然存在？

## 參考文獻

### 開創性論文

- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. ICLR. https://arxiv.org/abs/1711.05101 — 指出 L2 正則化與權重衰減在自適應方法下不同，並提出 AdamW。
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR. https://arxiv.org/abs/1609.04836 — 報告大批次訓練收斂到的尖銳極小值，泛化較差。
- Smith, S. L. & Le, Q. V. (2018). *A Bayesian Perspective on Generalization and Stochastic Gradient Descent*. ICLR. https://arxiv.org/abs/1710.06451 — 主張最佳批次大小隨學習率與訓練集大小而成長，以雜訊尺度解釋。
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 顯示以線性縮放與預熱，大批次可達到小批次的準確率。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機梯度方法的綜述，討論梯度雜訊與批次大小的角色。
