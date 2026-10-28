---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/math/automatic-differentiation
  - theory/math
tags:
  - forward-mode differentiation
  - dual numbers
  - Jacobian-vector product
aliases:
  - 前向模式自動微分
  - Forward-mode automatic differentiation
  - Forward mode
---

# 前向模式微分

前向模式微分把導數從程式的輸入傳播到輸出，與數值本身一同計算。對於選定的輸入方向，它在一次掃描中就能得到每個輸出的方向導數。當函數的輸入很少時，它的計算成本低；它也是[反向模式](reverse-mode.zh-TW.md)的對偶，後者在函數輸出很少時較為便宜。

## 概觀

[自動微分章節](index.zh-TW.md)介紹了兩種模式。本頁說明前向模式：它如何計算、回傳什麼，以及何時是較好的選擇。

## 問題

許多科學與機器學習任務需要的是輸出對少數輸入的敏感度，或雅可比矩陣作用於向量的結果，而不是純量的完整梯度。反向模式在這些任務上很浪費，因為它對每個輸出計算雅可比的一列，而不是對每個輸入計算一行。問題在於如何直接、便宜地取得方向導數。

## 核心想法

為每個中間值附上一個切向量（tangent）。若輸入沿方向 $\dot{x}$ 被微擾，每個中間值 $v$ 都會得到切向量 $\dot{v}$，而每個基本運算則依其自身的微分規則傳播切向量。一次前向掃描會回傳雅可比向量積 $J\dot{x}$，即輸出沿該方向的導數。對偶數（dual numbers）提供了一種簡潔的表述方式：數值與其切向量成對攜帶，對這些配對做算術時會自動套用鏈式法則。

## 方程式

對於基本運算 $v = \phi(u)$，切向規則為

$$\dot{v} = \phi'(u)\, \dot{u}$$

對於一個合成的程式，切向量沿圖相乘，順序與程式執行的順序相同。完整的雅可比則透過每個輸入方向一次掃描來恢復，取標準基向量作為 $\dot{x}$，因此其成本隨輸入數量線性成長。

## 結果

前向模式給出精確的導數，且不需要儲存圖，因此其記憶體用量接近原程式本身。Baydin 等人的綜述比較了前向與反向模式，並說明各自適用的情況 [(Baydin et al., 2018)](https://arxiv.org/abs/1502.05767)。具體的計時取決於實作，並在綜述所引用的工作中報告。

## 限制

- 完整雅可比的成本隨輸入數量線性成長，因此對於參數很多、輸出很少的函數（例如神經網路的損失），前向模式效率很低。
- 前向模式一次只計算一個方向。高階的乘積可以由它組合而成，但組合方式需要謹慎，才能保持效率。
- 與反向模式一樣，導數只沿程式實際執行的路徑是正確的，而且在非平滑點上可能不存在。

## 關聯

對於敏感度分析與雅可比向量積，前向模式是有效率的選擇，並且可與反向模式組合，計算 Hessian 向量積。上層[章節](index.zh-TW.md)說明了兩種模式的關係。訓練[反向傳播](../../deep-learning/index.zh-TW.md)則改用反向模式。背後的微積分見[微積分](../index.zh-TW.md)。

## 應用

參數很少的模擬的敏感度分析、以少量輸入進行的不確定性傳播，以及為二階最佳化計算 Hessian 向量積。

## 開放問題

- 在大型程式中，前向模式應如何與反向模式結合，使每個部分都使用較便宜的模式？
- 前向模式的切向量應如何有效率地穿過控制流與數值求解器傳播？

## 參考文獻

### 奠基性論文

- Wengert，*A simple automatic derivative evaluation program*，Communications of the ACM（1964）。https://doi.org/10.1145/355586.364791 — 早期描述沿程式前向傳播以計算導數的方法。
- Pearlmutter 與 Siskind，*Reverse-mode AD in a functional framework: Lambda the ultimate backpropagator*，ACM Transactions on Programming Languages and Systems（2008）。https://doi.org/10.1145/1330017.1330018 — 在函數式設定中，連結前向與反向模式。

### 綜述與教科書

- Griewank 與 Walther，*Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*，SIAM（2008）。https://doi.org/10.1137/1.9780898717761 — 涵蓋切線性模型與各模式成本的標準教科書。
- Baydin、Pearlmutter、Radul 與 Siskind，*Automatic differentiation in machine learning: a survey*，Journal of Machine Learning Research（2018）。https://arxiv.org/abs/1502.05767 — 比較前向與反向模式的綜述。

### 文章與文件

- Paszke 等人，*PyTorch: An Imperative Style, High-Performance Deep Learning Library*（2019）。https://arxiv.org/abs/1912.01703 — 說明一個透過記錄運算來計算導數的框架，前向模式也在此設定中使用。
