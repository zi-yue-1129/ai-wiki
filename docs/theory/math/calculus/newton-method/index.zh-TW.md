---
translation_reviewed: 2026-10-28
---

# 牛頓法

牛頓法在每一步最小化損失的二階泰勒模型，並利用海森矩陣選擇步長。在海森矩陣為正定、且接近極小值時，它收斂得非常快。然而，對大型網路而言，儲存並求解海森矩陣的成本過高，這正是[二階方法](../../../optimization/second-order.md)要對它做近似的原因。它是[微積分與最佳化基礎](../index.md)一頁中的二階方法。

## 概述

牛頓法是數值分析中的經典演算法，最初用於求解方程式。用於最小化時，它是把求根的迭代套用到梯度上：

$$
x_{k+1}=x_k-\big[\nabla^2 f(x_k)\big]^{-1}\nabla f(x_k).
$$

Dennis 與 Schnabel（1996）給出標準論述。Pearlmutter（1994）展示了如何精確地計算海森矩陣與向量的乘積，成本大約與一次梯度計算相當，而且不需要形成矩陣。這項結果是許多針對大型模型的曲率感知方法的基礎。

## 核心概念

- **二階模型**：$m(\delta)=f(x)+\nabla f(x)^\top\delta+\tfrac12\delta^\top H\,\delta$，其中 $H=\nabla^2 f(x)$。它就是[概述](../index.md)中的二階泰勒展開。
- **牛頓步**：$\delta=-H^{-1}\nabla f(x)$。當 $H$ 為正定時，這是 $m$ 唯一的極小值點。
- **二次收斂**：在海森矩陣為正定且為 Lipschitz 連續的極小值附近，一步之後的誤差以常數乘上前一步誤差的平方為上界。
- **無鞍點牛頓法**：以 $|H|=(H^2)^{1/2}$ 取代 $H$ 的變體，使步長總是指向下坡方向。Dauphin 等人（2014）提出它以逃離鞍點。

## 運作方式

每次迭代計算 $g_k=\nabla f(x_k)$ 與 $H_k=\nabla^2 f(x_k)$，求解 $H_k d_k=-g_k$，然後更新 $x_{k+1}=x_k+\alpha_k d_k$。當 $H_k$ 為正定時，以 Cholesky 分解求解此方程組。步長 $\alpha_k$ 由線搜尋決定，在極小值附近為 1。

二次函數最能展示此方法的優點。設 $f(x)=\tfrac12 x^\top A x-b^\top x$，其中 $A$ 為正定矩陣。則 $\nabla f(x)=Ax-b$，且 $H=A$。從任何起點 $x_0$ 出發，一步牛頓步就得到 $x_1=A^{-1}b$，即精確的極小值點。若 $A$ 病態，梯度下降則需要很多步。

當 $H$ 不定時，牛頓步可能指向上坡，或指向鞍點。實作上會修正 $H$，或加上信任域。當 $H$ 大到無法分解時，牛頓－共軛梯度法只使用海森向量乘積，近似求解此方程組。

## 結果

以下結果來自理論與少數針對神經網路的研究，都不是基準表。

- **局部收斂。** 在海森矩陣為正定且 Lipschitz 連續時，迭代在接近極小值後會二次收斂。這是教科書定理，證明見 Nocedal 與 Wright（2006）以及 Dennis 與 Schnabel（1996）。
- **無鞍點變體。** Dauphin 等人（2014）報告數值證據，指出此方法比梯度下降與擬牛頓法更快速地逃離高維鞍點，並在深度與循環網路上有更好的最佳化表現。其摘要未給出單一數字。
- **海森譜。** Sagun、Bottou 與 LeCun（2016）發現，海森譜由接近零的大量特徵值，加上偏離零的離群特徵值構成。Ghorbani 等人（2019）指出，在沒有批次正規化的網路中，訓練期間會出現大的孤立特徵值；批次正規化大致可以消除它們。

## 限制

- **成本。** 有 $d$ 個參數的模型，其海森矩陣有 $d^2$ 個元素，以它求解的成本約為 $d^3$ 次運算。兩者對現代網路都不可行。
- **被駐點吸引。** 當海森矩陣不定時，牛頓法可能收斂到鞍點或極大值。無鞍點變體可以解決此問題，但需要額外成本。
- **局部性。** 二次模型只在當前點附近準確，因此遠離極小值時需要線搜尋與信任域。
- **雜訊。** 小批次的海森矩陣是由少量資料估計的，因此每一步使用的曲率本身並不確定。

## 開放問題

- **大規模曲率。** K-FAC 或 Shampoo（見[二階方法](../../../optimization/second-order.md)一頁）等結構化近似，能否以可接受的成本保留深度網路所需的曲率，仍是開放問題。
- **譜結構。** 大量特徵值加離群值的結構暗示，可以利用低秩曲率；但要把它轉化為實用的前處理器，尚無定論。
- **實務中處理鞍點。** 無鞍點變體是否優於依賴梯度雜訊的簡單方法，目前仍不清楚。

## 參考文獻

### 開創性論文

- Dauphin, Y. et al. (2014). Identifying and attacking the saddle point problem in high-dimensional non-convex optimization. arXiv. https://arxiv.org/abs/1406.2572 — 提出無鞍點牛頓法，以海森矩陣的絕對值使步長指向下坡。
- Pearlmutter, B. A. (1994). Fast Exact Multiplication by the Hessian. *Neural Computation*. https://doi.org/10.1162/neco.1994.6.1.147 — 說明如何精確計算海森向量乘積，成本約與一次梯度計算相當。
- Sagun, L., Bottou, L. & LeCun, Y. (2016). Eigenvalues of the Hessian in Deep Learning: Singularity and Beyond. arXiv. https://arxiv.org/abs/1611.07476 — 研究訓練前後損失的海森譜。
- Ghorbani, B., Krishnan, S. & Xiao, Y. (2019). An Investigation into Neural Net Optimization via Hessian Eigenvalue Density. arXiv. https://arxiv.org/abs/1901.10159 — 估計大型網路訓練期間的海森譜。

### 綜述與教科書

- Dennis, J. E. & Schnabel, R. B. (1996). *Numerical Methods for Unconstrained Optimization and Nonlinear Equations*. SIAM. https://doi.org/10.1137/1.9781611971200 — 牛頓法與擬牛頓法的標準論述及其收斂性。
- Nocedal, J. & Wright, S. J. (2006). *Numerical Optimization*. Springer. https://doi.org/10.1007/978-0-387-40065-5 — 牛頓法、線搜尋與信任域方法，以及牛頓－共軛梯度變體。
