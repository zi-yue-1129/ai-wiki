---
translation_reviewed: 2026-10-28
---

# 重球動量

重球動量由 Polyak（1964）提出，為梯度下降加上一個速度項。每次更新會保留一部分前一步的位移，因此迭代點在梯度方向一致的地方累積速度，在震盪的地方則會減速。這個方法是今日 SGD 所用動量項的起源。概述見 [SGD 與動量](index.md)頁。

## 概述

在條件數不佳的二次問題上，普通梯度下降會在狹窄的山谷中來回折返，沿山谷的前進很慢。Polyak 問：加上一個與前一步成正比的項能否加速？他證明，在適當的步長與動量係數下，這個二階遞迴在二次問題上比普通梯度下降收斂得更快。名稱來自一顆沉重的球在損失曲面上滾動的想像。

## 核心概念

- **速度** \(v_t\)：過去梯度的累加，以動量係數 \(\beta\) 縮放。
- **動量係數** \(\beta\)：保留多少前一個速度。常見值約為 0.9。
- **震盪抑制**：在速度中，正負翻轉的梯度分量會互相抵消，方向一致的分量則會累積。
- **重球遞迴**：以二階差分方程表示的更新規則，這是 Polyak 分析它的方式。

## 運作方式

更新式使用速度：

\[
\begin{aligned}
v_t &= \beta\, v_{t-1} + g_t \\
\theta_t &= \theta_{t-1} - \eta\, v_t
\end{aligned}
\]

展開後，步長是所有過去梯度的加權和，權重以 \(\beta\) 的速率幾何遞減。這就是它為何是梯度的指數移動平均，也是它為何能抑制震盪。Polyak 在二次目標上的分析顯示，選擇適當的 \(\eta\) 與 \(\beta\) 時，在相同條件數下收斂速率優於普通梯度下降。

## 關鍵方法

### Heavy-ball method（Polyak，1964）

- **問題：** 條件數不佳的問題上，梯度下降會來回折返，收斂緩慢。
- **核心想法：** 加入累積過去位移的速度項，使方向一致的步伐加速，震盪的方向則互相抵消。
- **公式或演算法：** 上述兩行更新式，\(\eta\) 為學習率，\(\beta\) 為動量係數。
- **結果：** 論文分析了二次問題上的加速效果，顯示在適當參數選擇下，收斂比普通梯度下降快。數值常數來自該分析，此處不重複。
- **限制：** 分析針對二次目標。對於一般凸函數，重球法不能達到最佳的最壞情況速率；Nesterov 的變體可以（見 [Nesterov 動量](nesterov.md)）。

## 關聯

- [Nesterov 動量](nesterov.md)是在前瞻點計算梯度的變體。
- [Adam](../adaptive/adam.md) 的一階矩也是同樣的速度概念。
- 上層的 [SGD 與動量](index.md)頁涵蓋普通 SGD 與動量的概述。

## 開放問題

- 批次很大、梯度雜訊很小時，\(\beta\) 與 \(\eta\) 應如何耦合？

## 參考文獻

### 開創性論文

- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:[10.1016/0041-5553(64)90137-5](https://doi.org/10.1016/0041-5553(64)90137-5) — 提出重球動量，並分析其在二次問題上的加速效果。
- Sutskever, I., Martens, J., Dahl, G. & Hinton, G. (2013). On the importance of initialization and momentum in deep learning. ICML. https://proceedings.mlr.press/v28/sutskever13.html — 顯示在適當初始化下，動量可以訓練深層與循環網路。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — 動量與隨機梯度方法的綜述，說明其收斂行為。
- Bubeck, S. (2014). Convex Optimization: Algorithms and Complexity. https://arxiv.org/abs/1405.4980 — 關於梯度方法複雜度的專著，包含加速變體。

### 文章與文件

- Stanford CS231n，*Optimization* 講義。https://cs231n.github.io/optimization-1/ — 動量與其對更新方向影響的附圖筆記。
