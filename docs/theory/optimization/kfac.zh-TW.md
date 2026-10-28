---
translation_reviewed: 2026-10-28
---

# K-FAC

K-FAC（Kronecker 分解近似曲率）是神經網路自然梯度的實用近似。它逐層近似費雪資訊矩陣，把每個區塊寫成兩個小矩陣的克羅內克積，然後對這兩個小矩陣求逆。Martens 與 Grosse（2015）提出了此方法。上層概述見[二階與擬牛頓方法](second-order.md)。

## 概述

自然梯度下降以費雪資訊矩陣的逆來預處理梯度。這使得更新與參數的寫法無關，對許多模型而言，它也是比原始梯度更有意義的方向。困難在於，神經網路的費雪矩陣有數百萬列，無法形成也無法求逆。K-FAC 利用全連接層的結構，讓求逆變得可負擔。

## 問題

自然梯度法有原則性的基礎，但對神經網路而言，費雪矩陣太大，無法形成或求逆。Martens 與 Grosse 想知道，能否以有結構的近似，使求逆的成本低到能保有自然梯度的進展，同時每步成本接近 SGD。

## 核心想法

對於輸入激活為 \(a\)、輸出梯度為 \(g\) 的全連接層，其權重矩陣的梯度為 \(\nabla W = g a^\top\)。作者以克羅內克積 \(A \otimes G\) 近似每層的費雪區塊，其中 \(A\) 為激活的二階矩，\(G\) 為反向傳播得到的輸出梯度的二階矩。克羅內克積的逆是各因子的逆之克羅內克積，因此只需對兩個小因子求逆。

## 演算法

對每一層 \(\ell\)：

1. 累積激活共變異數 \(A_\ell\) 與輸出梯度共變異數 \(G_\ell\) 的滾動估計。
2. 對兩個因子求逆，通常會為每個因子加上阻尼項以維持穩定。
3. 以 \(\Delta W_\ell = G_\ell^{-1}\,\nabla W_\ell\,A_\ell^{-1}\) 預處理該層的梯度，因子如上加上阻尼。
4. 以學習率套用更新，並每隔固定間隔更新因子及其逆，以節省運算。

因子的逆比梯度更新得少，因為統計量相對於參數變化得慢。

## 結果

- 摘要指出，K-FAC 是費雪矩陣「可有效求逆的近似」，其更新能比帶動量的隨機梯度下降取得更快的進展。
- 摘要描述其計算成本「只比普通的隨機梯度高出數倍」。摘要未給出數值上的加速比，因此增益大小應參考論文的實驗。

## 限制

- 克羅內克積是一種近似。摘要指出它既非對角也非低秩，但仍忽略了層與層之間的相關性。
- 此方法針對全連接層設計，要擴展到卷積與循環層，需要進一步的近似。
- 因子必須每隔一段時間更新並求逆，阻尼也需要調校，因此它比 SGD 有更多超參數。

## 關聯

- [二階與擬牛頓方法](second-order.md)是上層概述，K-FAC 與 L-BFGS、Shampoo 並列於其中。
- [L-BFGS](lbfgs.md)是確定性的擬牛頓替代方法。
- [Shampoo](shampoo.md)是相關的矩陣結構預條件子，它的建構來自梯度統計量而非費雪矩陣。
- [深度學習](../deep-learning/index.md)描述了為各因子提供輸出梯度的反向傳播。

## 應用

- 訓練大型前饋網路與卷積網路，這些情況下每步成本必須接近 SGD。
- 以策略網路進行強化學習，此時自然梯度是更新的自然選擇。

## 開放問題

- 應如何把近似擴展到卷積與注意力層，同時不失去速度上的優勢？
- K-FAC 的好處有多少來自曲率估計，又有多少來自阻尼與更新的排程？

## 參考文獻

### 開創性論文

- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — 提出 K-FAC，為神經網路的自然梯度提供克羅內克分解近似。
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — K-FAC 所近似的自然梯度方法。
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — 相關的矩陣結構預條件子，與基於費雪矩陣的做法作比較。
- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — 與 K-FAC 形成對比的確定性擬牛頓法。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 將自然梯度與曲率方法與一階方法並列的綜述。
