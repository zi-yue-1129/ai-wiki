---
translation_reviewed: 2026-10-28
---

# 前向模式自動微分

前向模式自動微分在程式執行時，為每個中間值附帶一個切線，藉此計算程式沿指定輸入方向的導數。它是[自動微分](../index.md)的兩種基本模式之一，當函數的輸入很少時特別有效率。

## 概述

前向模式依照程式計算數值的順序套用連鎖律。每個值 $v$ 都配對一個切線 $\dot v$，即它沿指定輸入方向的變化率。每個運算依其局部規則更新切線，因此輸出的切線就是雅可比-向量乘積 $J\dot{x}$。Hoffmann（2014）指出，前向模式的幾種描述方式，包括矩陣-向量乘積、對偶數與對偶數上的泰勒級數，實際上執行的是相同的運算鏈。Baydin 等人（2015/2018）則把前向模式與反向模式並列為兩種基本技術。

## 核心概念

- **切線** $\dot v$：中間值沿輸入方向的導數。
- **種子**：輸入上的初始切線。取 $\dot x = e_i$ 即可選出對輸入 $i$ 的導數。
- **對偶數**：形如 $a + b\varepsilon$ 的數對，其中 $\varepsilon^2 = 0$，$a$ 為數值，$b$ 為其切線。對偶數的運算同時計算數值與導數。
- **局部規則**：對 $z = \varphi(x, y)$，$\dot z = \frac{\partial \varphi}{\partial x}\dot x + \frac{\partial \varphi}{\partial y}\dot y$。

## 運作方式

演算法有三個步驟：

1. 依種子方向 $\dot x$ 設定每個輸入的切線。
2. 依程式順序處理每個運算：照常計算其數值，再計算其切線 $\dot v_k = \sum_j \frac{\partial v_k}{\partial v_j}\dot v_j$，對其所有父節點 $j$ 求和。
3. 讀出輸出的切線，它等於 $J\dot{x}$。

對偶數的運算把局部規則寫得很清楚：$(a + b\varepsilon)(c + d\varepsilon) = ac + (ad + bc)\varepsilon$（因為 $\varepsilon^2 = 0$），且 $\sin(a + b\varepsilon) = \sin a + b\cos a\,\varepsilon$。對 $(2, 3)$ 處的 $f(x, y) = xy + \sin x$，取種子 $\dot x = 1$，一次計算即得 $\partial f/\partial x = 3 + \cos 2 \approx 2.584$，與[概述](../index.md)中的值相同。

每次計算得到雅可比矩陣的一欄，因此有 $n$ 個輸入的函數其完整梯度需要 $n$ 次計算。前向模式不需要磁帶，因為每個切線在其輸入準備好時就能立即得到。把前向模式套在反向模式內，可以得到二階導數，例如海森-向量乘積（Pearlmutter，1994）。

## 結果

前向模式並沒有單一的基準測試來定義其表現，其證據主要來自分析。正如 Baydin 等人（2015/2018）的綜述所說明，其成本隨輸入數量增加。Baydin 等人（2022）以前向模式的方向導數作為「前向梯度」的核心，只需一次前向計算即可完成。他們的摘要報告，在所測試的問題上，這種方法在部分情況下的訓練速度可達兩倍。Pearlmutter（1994）展示了精確的海森-向量乘積，其成本與一次梯度計算相當。這裡除了摘要中的數字外，不引用其他數值。

## 限制

- **成本隨輸入增加。** 對於以數百萬個參數為變數的純量損失，每個參數各計算一次的成本太高，這也是反向模式主導訓練的原因。
- **隨機化估計有雜訊。** 前向梯度使用隨機的切線方向。其估計量是無偏的，但變異數可能很大。
- **仍需局部規則。** 前向模式的品質取決於每個基本運算的導數規則，而不可微分的運算需要另外處理。

## 開放問題

- 對於輸入與輸出都很多的函數，如何有效地把前向模式的方向導數與反向模式結合。
- 前向梯度能否擴展到最大的模型上，而反向模式目前是那裡的標準做法。

## 參考文獻

### 開創性論文

- Baydin, A. G., Pearlmutter, B. A., Syme, D., Wood, F. & Torr, P. (2022). Gradients without Backpropagation. https://arxiv.org/abs/2202.08587 — 在單次前向計算中，由前向模式的方向導數估計梯度，並報告部分情況下訓練較快。
- Pearlmutter, B. A. (1994). Fast Exact Multiplication by the Hessian. *Neural Computation*. https://doi.org/10.1162/neco.1994.6.1.147 — 說明如何藉由微分得到精確的海森-向量乘積，這是前向模式套在反向模式內的主要用途。

### 綜述與教科書

- Baydin, A. G., Pearlmutter, B. A., Radul, A. A. & Siskind, J. M. (2015/2018). Automatic differentiation in machine learning: a survey. *Journal of Machine Learning Research*. https://arxiv.org/abs/1502.05767 — 綜述，定義前向與反向模式並說明兩者的關係。
- Griewank, A. & Walther, A. (2008). *Evaluating Derivatives*. SIAM. https://doi.org/10.1137/1.9780898717761 — 演算法微分的標準參考書，對前向模式的實作有詳細討論。
- Hoffmann, P. H. W. (2014). A Hitchhiker's Guide to Automatic Differentiation. arXiv. https://arxiv.org/abs/1411.0583 — 教學文件，比較前向模式的矩陣、對偶數與泰勒級數三種描述。
