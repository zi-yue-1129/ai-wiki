---
translation_reviewed: 2026-10-28
---

# 二階與擬牛頓方法

二階方法利用曲率來決定步長。曲率是損失的二階導數矩陣（或其近似）。牛頓法是典型的例子，但它的成本對大型網路太高，因此實用的方法會近似曲率，例如 L-BFGS 這類擬牛頓法；或近似其結構，例如 K-FAC 與 Shampoo。

## 概述

梯度下降只使用損失的斜率。在點 \(\theta\) 附近，二階泰勒展開為 \(L(\theta+\delta)\approx L(\theta)+\nabla L^\top\delta+\tfrac12\delta^\top H\delta\)，其中 \(H=\nabla^2 L\) 為 Hessian。最小化這個二次模型，就得到牛頓步 \(\delta=-H^{-1}\nabla L\)。這一步考慮了每個方向的曲率，因此在平坦方向上可以走得很遠，在陡峭方向上則走得很短。當二次模型準確時，牛頓法所需的迭代次數遠少於梯度下降。

## 核心概念

- **Hessian**：\(d\times d\) 的二階導數矩陣。儲存它需要 \(O(d^2)\) 記憶體，求逆需要 \(O(d^3)\) 時間，當 \(d\) 達到數百萬時就不切實際。
- **擬牛頓近似**：由連續的梯度差所建構的矩陣，在不直接計算的情況下近似 Hessian 的逆。
- **費雪資訊**：梯度的期望外積。對許多模型而言，它是 Hessian 的半正定替代。自然梯度下降以其逆來預處理梯度（Amari，1998）。
- **克羅內克分解**：把某一層的曲率區塊寫成兩個較小矩陣的克羅內克積，使其能廉價地求逆。
- **預條件子**：在步進前用來重新縮放梯度的任何矩陣。自適應方法使用對角預條件子，二階方法則使用完整或有結構的預條件子。

## 運作方式

此家族可以用三個步驟概括：

1. 以梯度資訊（有時也包含曲率）對目前點附近的損失建立模型。
2. 計算使該模型最小的步長，必要時先以近似的逆曲率做預處理。
3. 移動，並以新的梯度更新近似。

各種近似的差別在於如何讓第 2 步保持可負擔。擬牛頓法保存低秩的歷史資訊，K-FAC 保存費雪矩陣的克羅內克分解估計，Shampoo 則為每個張量維度保存一個矩陣。

## 關鍵方法

三個方法各有獨立頁面。它們的差別在於近似的曲率為何，以及如何儲存它。

| 方法 | 使用的曲率 | 區別所在 |
|---|---|---|
| [L-BFGS](lbfgs.md)（Liu 與 Nocedal，1989） | 最近 \(m\) 步的梯度差 | 有限記憶的擬牛頓法。它儲存 \(m\) 對向量而非矩陣，設計上用於全批次問題 |
| [K-FAC](kfac.md)（Martens 與 Grosse，2015） | 費雪矩陣，逐層近似為克羅內克積 | 自然梯度的近似，對小矩陣求逆，用於以小批次訓練的神經網路 |
| [Shampoo](shampoo.md)（Gupta 等人，2018） | 每個張量維度一個預條件矩陣，由梯度統計量建構 | 針對張量的結構感知預條件，依摘要所述，每步成本與一階方法相近 |

## 關聯

- [自適應方法](adaptive/index.md)使用對角預條件子。Shampoo 是其矩陣值的推廣，其頁面已在該處連結。
- [SGD 與動量](sgd-and-momentum/index.md)是這些方法比較時所用的一階基準。
- [數學](../math/index.md)涵蓋此處使用的泰勒展開、半正定矩陣與克羅內克積。
- [學習率排程](learning-rate-schedules.md)在此也很重要，因為牛頓型的步長已包含一個尺度，排程可以縮小或放大它。

## 應用

- L-BFGS 用於較小的問題，例如擬合邏輯迴歸與部分科學模型，這些問題的全批次梯度負擔得起。
- K-FAC 與相關的自然梯度方法已用於大規模神經網路訓練。
- Shampoo 等矩陣預條件子已被研究用於訓練大型模型，作為加速收斂的途徑。

## 開放問題

- 二階方法能否在每一步的成本上與 SGD 相當，同時在各種模型規模下不損失實際的牆鐘時間？
- 在隨機訓練中，曲率近似要多準確，才能保留收斂上的優勢？
- 在梯度雜訊會改變的超大批次下，這些近似是否仍保有優勢？

## 參考文獻

### 開創性論文

- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — 提出 L-BFGS，一種適用於大型問題的有限記憶擬牛頓法。
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — 提出自然梯度下降，以費雪資訊的逆來預處理梯度。
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — 提出 K-FAC，為神經網路的自然梯度提供克羅內克分解近似。
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — 針對張量隨機最佳化的矩陣結構預條件子。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機梯度方法的綜述，包括擬牛頓與自然梯度的變體及其取捨。
