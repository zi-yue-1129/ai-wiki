---
translation_reviewed: 2026-10-28
---

# L-BFGS

L-BFGS 是一種有限記憶的擬牛頓法。它由最近幾對參數差與梯度差近似 Hessian 的逆，且從不儲存完整的矩陣。Liu 與 Nocedal（1989）為大型最佳化提出了此方法。上層概述見[二階與擬牛頓方法](second-order.md)。

## 概述

BFGS 方法依據觀察到的梯度變化，建構 Hessian 逆的近似。完整的 BFGS 需要儲存 $d\times d$ 的矩陣，每步需要 $O(d^2)$ 的記憶體與時間，當 $d$ 達到數百萬時就太大了。L-BFGS 只保留最近 $m$ 對 $(s_k, y_k)$，其中 $s_k = \theta_{k+1} - \theta_k$，$y_k = \nabla L_{k+1} - \nabla L_k$。近似逆與梯度的乘積，可以用兩迴圈遞迴在 $O(md)$ 時間內算出。

## 問題

梯度下降在病態問題上很慢，因為不同方向的曲率差異很大。牛頓法能處理這個問題，但需要 Hessian。Liu 與 Nocedal 想知道：一段短的梯度歷史所含的曲率資訊，是否足以獲得 BFGS 的大部分好處，而且記憶體成本只隨變數數量線性成長。

## 核心想法

保留一段短的 $(s_k, y_k)$ 歷史，並用它定義隱含的 Hessian 逆近似。這個近似從不以矩陣的形式算出。每一步的搜尋方向，是把遞迴套用到目前的梯度上而得到；接著以線搜尋選擇步長。

## 演算法

1. 在目前點計算梯度 $g_k$。
2. 使用儲存的各對，以兩迴圈遞迴算出方向 $d_k = -H_k g_k$，其中 $H_k$ 為隱含的 Hessian 逆近似。
3. 以滿足 Wolfe 條件的線搜尋，選擇步長 $\alpha_k$。
4. 令 $\theta_{k+1} = \theta_k + \alpha_k d_k$，計算 $s_k$ 與 $y_k$，並只保留最近的 $m$ 對。

記憶參數 $m$ 通常很小，它在近似品質與儲存空間之間做取捨。

## 結果

Liu 與 Nocedal 報告了大型測試問題上的數值實驗。本頁未引用其圖表或計時數字，因為未能核對該論文的全文。測試問題與計時結果應參考原論文。

## 限制

- 此方法假設目標函數是確定性的，梯度是精確的。當梯度來自小批次時，曲率對 $(s_k, y_k)$ 會變得不可靠，這也是 L-BFGS 多用於全批次設定的原因。
- 每一步都需要線搜尋，每個試探點都需要一次梯度計算。
- 記憶體 $m$ 限制了保留的曲率歷史。曲率變化快速的問題可能需要較大的 $m$，或需要重新啟動。

## 關聯

- [二階與擬牛頓方法](second-order.md)是上層概述，L-BFGS 與 K-FAC、Shampoo 並列於其中。
- [附克羅內克分解的曲率（K-FAC）](kfac/index.md)是針對神經網路、隨機設定的替代方法。
- [SGD 與動量](sgd-and-momentum/index.md)是 L-BFGS 通常比較的一階方法。
- [數學](../math/index.md)涵蓋推導中使用的 Wolfe 條件與 Hessian。

## 應用

- 以邏輯迴歸、條件隨機場等損失平滑且確定性的模型做擬合。
- 梯度精確且負擔得起的科學與工程最佳化問題。

## 開放問題

- 在梯度有雜訊時，應如何建構曲率對，才能讓 L-BFGS 用於隨機訓練？
- 對某一類問題，$m$ 的最佳選擇是什麼？

## 參考文獻

### 開創性論文

- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — 提出 L-BFGS，並報告其在大型問題上的數值表現。
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — 針對神經網路的隨機曲率方法，與全批次的擬牛頓法形成對比。
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — 自然梯度的想法，擬牛頓法以另一種方式近似它。

### 綜述與教科書

- Nocedal, J. & Wright, S. J. (2006). *Numerical Optimization*. 第 2 版. Springer. https://doi.org/10.1007/978-0-387-40065-5 — 擬牛頓法的教科書式介紹，包括有限記憶更新與 Wolfe 線搜尋。
- Nocedal, J. & Wright, S. J. (2006). *Numerical Optimization*，第 7 章：Large-Scale Unconstrained Optimization。Springer. https://doi.org/10.1007/978-0-387-40065-5_7 — 教科書中關於大型無約束最佳化的章節，有限記憶方法通常是在此情境下介紹的。
- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — 綜述擬牛頓法及其在隨機梯度下的使用。
