---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - theory/math
tags:
  - automatic differentiation
  - backpropagation
  - gradients
aliases:
  - 自動微分
  - 反向傳播
  - Automatic differentiation
  - Autodiff
---

# 自動微分

自動微分透過對程式執行的每個基本運算套用鏈式法則，計算程式的精確導數。它是反向傳播背後的機制，也讓現代框架無需任何人手工推導，就能計算任意模型的梯度。

## 概觀

程式是一連串基本運算：加法、乘法，以及已知導數的函數呼叫。自動微分記錄這些運算，並依系統化的順序對它們套用鏈式法則。它不同於以有限差分近似導數、因而受捨入誤差影響的數值微分，也不同於會建立單一龐大運算式、可能使其大小急速膨脹的符號微分。

## 關鍵概念

- **計算圖（computational graph）**：一個有向圖，節點是中間值，邊是產生這些值的運算。
- **鏈式法則（chain rule）**：合成函數的導數沿圖中路徑相乘的法則。
- **雅可比向量積（Jacobian-vector product, JVP）**：函數沿給定輸入方向的方向導數。
- **向量雅可比積（vector-Jacobian product, VJP）**：純量輸出對輸入的梯度，並套用於給定的輸出敏感度。反向模式計算的就是 VJP。
- **高階導數（higher-order derivatives）**：導數的導數，例如 Hessian，透過對梯度計算再次微分而得。

## 運作方式

自動微分有兩種模式。**前向模式（forward mode）**從輸入傳播導數到輸出，每次處理一個輸入方向，因此成本隨輸入數量增加。**反向模式（reverse mode）**從輸出把敏感度傳回輸入，因此一次反向傳播就能得到對所有輸入的梯度。對於一個純量損失與數百萬個參數，反向模式遠比前向模式省成本，而它正是實作反向傳播的模式 [(Baydin et al., 2018)](https://arxiv.org/abs/1502.05767)。

Rumelhart、Hinton 與 Williams 推廣了用於訓練多層網路的反向傳播，它就是把反向模式應用於分層網路 [(Rumelhart et al., 1986)](https://doi.org/10.1038/323533a0)。

## 關鍵方法

- [反向模式微分](reverse-mode.zh-TW.md)：一次反向傳播即可得到純量輸出的梯度，這就是反向傳播。
- [前向模式微分](forward-mode.zh-TW.md)：每個輸入方向需要一次前向傳播，在輸入很少時效率較高。

## 實作

框架在前向計算時記錄圖，並以反向方式重播以計算梯度。PyTorch 的命令式設計在運算執行時即時記錄，其效能目標見 [Paszke 等人（2019）](https://arxiv.org/abs/1912.01703)。JAX 等函數式框架把前向與反向模式表示為函數的變換，使高階導數容易組合。

## 關聯

依賴梯度的訓練，見[深度學習](../../deep-learning/index.zh-TW.md)，它仰賴反向模式微分。梯度的記號見[符號與記號表](../../../reference/notation/index.zh-TW.md)。微分計算的一般理論由 Griewank 與 Walther 討論 [(Griewank and Walther, 2008)](https://doi.org/10.1137/1.9780898717761)。鏈式法則所建立的微積分見[微積分](../index.zh-TW.md)。

## 應用

訓練現代所有神經網路、計算物理模擬的敏感度、工程中的敏感度分析，以及為最佳化與不確定性計算 Hessian 資訊。

## 開放問題

- 自動微分應如何處理具有離散選擇、控制流與隨機取樣的程式？
- 對於非常長的計算，反向模式應如何在記憶體與計算之間取得最佳權衡？

## 參考文獻

### 奠基性論文

- Rumelhart、Hinton 與 Williams，*Learning representations by back-propagating errors*，Nature（1986）。https://doi.org/10.1038/323533a0 — 推廣了用於多層網路的反向傳播。
- Pearlmutter 與 Siskind，*Reverse-mode AD in a functional framework: Lambda the ultimate backpropagator*，ACM Transactions on Programming Languages and Systems（2008）。https://doi.org/10.1145/1330017.1330018 — 在函數式設定中，把反向模式視為程式變換。

### 綜述與教科書

- Baydin、Pearlmutter、Radul 與 Siskind，*Automatic differentiation in machine learning: a survey*，Journal of Machine Learning Research（2018）。https://arxiv.org/abs/1502.05767 — 涵蓋兩種模式及其在機器學習中應用的綜述。
- Griewank 與 Walther，*Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*，SIAM（2008）。https://doi.org/10.1137/1.9780898717761 — 演算法微分的標準教科書。
- Goodfellow、Bengio 與 Courville，*Deep Learning*，MIT Press（2016）。https://www.deeplearningbook.org/ — 在訓練神經網路的脈絡下說明反向傳播。

### 文章與文件

- Paszke 等人，*PyTorch: An Imperative Style, High-Performance Deep Learning Library*（2019）。https://arxiv.org/abs/1912.01703 — 說明一個在前向傳播時記錄圖、並以反向方式執行的框架。
