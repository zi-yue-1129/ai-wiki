---
translation_reviewed: 2026-10-28
---

# 同時擾動隨機逼近（SPSA）

SPSA 以兩次評估估計帶雜訊損失的梯度，並同時擾動所有參數。Spall（1992）為梯度不可得或成本過高的隨機逼近問題提出此方法。上層概述見[零階與演化最佳化](zeroth-order-and-evolutionary.md)。

## 概述

SPSA 是零階方法，只使用函數值。它的梯度估計在函數評估次數上很便宜，而使用此估計的更新規則就是一般的隨機梯度下降。

## 問題

在只能取得帶雜訊的損失量測 \(y(\theta)\) 時，最小化 \(f(\theta)\)。對 \(p\) 個參數做有限差分需要 \(2p\) 次評估。對於有數百萬參數的模型，每步評估次數太多。

## 核心想法

沿著一個隨機向量 \(\Delta_k\) 同時擾動每個參數，該向量的各分量以相等機率為 \(\pm 1\)。在 \(\theta_k \pm c_k\Delta_k\) 上做兩次評估，就能同時得到每個座標的梯度估計。

## 演算法

令 \(\Delta_k\) 的各分量獨立且為 \(\pm 1\)，\(c_k > 0\) 為擾動大小。梯度估計為

\[
\hat g_k(\theta_k) = \frac{y(\theta_k + c_k\Delta_k) - y(\theta_k - c_k\Delta_k)}{2c_k}\,\Delta_k^{-1},
\]

其中除法逐座標進行。對 \(\pm 1\) 的分量，\(\Delta_k^{-1} = \Delta_k\)。更新式為

\[
\theta_{k+1} = \theta_k - a_k \hat g_k(\theta_k),
\]

其中增益 \(a_k\) 與擾動 \(c_k\) 都隨迭代次數 \(k\) 遞減。每次迭代使用兩次評估，與維度無關。

## 主要結果

Spall（1992）給出增益與擾動序列的條件，使迭代點在隨機逼近的意義下收斂。本頁不引用論文中的數值結果。

## 限制

- 估計有雜訊，因為所有座標共用同樣的兩次評估。需要許多迭代，且變異數隨參數數量增加。
- 增益與擾動序列必須調校，其選擇會強烈影響收斂速度。
- 每次迭代比使用反向傳播的梯度下降慢，因此適用於評估相對於梯度較便宜，或無法計算梯度的情況。

## 關聯

- [零階與演化最佳化](zeroth-order-and-evolutionary.md)是上層概述，SPSA 與演化策略、CMA-ES 並列於其中。
- [演化策略](evolution-strategies.md)從族群而非兩次擾動估計梯度。
- [CMA-ES](cma-es.md)是無梯度方法，它調整的是協方差，而非梯度估計。
- [SGD 與動量](sgd-and-momentum/index.md)提供 SPSA 梯度估計所結合的更新規則。

## 應用

- 調整只能取得帶雜訊之效能量測的系統參數。
- 如 MeZO（Malladi 等人，2023）所示，以前向傳播微調語言模型；它執行的零階 SGD 方法只用兩次前向傳播估計梯度，與 SPSA 同屬一類。

## 開放問題

- 對於有數百萬參數的網路，擾動大小應如何選擇？
- 結合動量或自適應縮放的 SPSA，在大規模下能否達到以反向傳播為基礎之微調的準確率？

## 參考文獻

### 開創性論文

- Spall, J. C.（1992）。Multivariate stochastic approximation using a simultaneous perturbation gradient approximation。*IEEE Transactions on Automatic Control*，37(3)，332–341。https://doi.org/10.1109/9.119632 — 提出 SPSA，以所有參數的同時擾動建構梯度近似。
- Malladi, S., 等人（2023）。*Fine-Tuning Language Models with Just Forward Passes*。arXiv。https://arxiv.org/abs/2305.17333 — 把零階梯度估計器用於微調，記憶體用量接近推論。
- Salimans, T., 等人（2017）。*Evolution Strategies as a Scalable Alternative to Reinforcement Learning*。arXiv。https://arxiv.org/abs/1703.03864 — 另一種基於族群的無梯度估計器，已顯示能擴展到超過一千個工作者。

### 綜述與教科書

- Hansen, N.（2016）。*The CMA Evolution Strategy: A Tutorial*。arXiv。https://arxiv.org/abs/1604.00772 — 另一種無梯度方法的教學文件，用於與 SPSA 比較。
- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。*SIAM Review*, 60(2), 223–311。https://doi.org/10.1137/16M1080173 — 基於梯度的隨機方法綜述，SPSA 的更新規則屬於這一類。
