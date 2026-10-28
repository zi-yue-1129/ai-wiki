---
translation_reviewed: 2026-10-28
---

# 反向模式自動微分

反向模式自動微分計算純量輸出對程式所有輸入的梯度。它先做一次保存中間值的前向計算，再做一次反向掃描。套用於神經網路時，就是稱為反向傳播的演算法。它是[自動微分](../index.md)的第二種基本模式。

## 概述

反向模式把連鎖律倒過來執行。它不是把某個輸入的變化向前推，而是把輸出的敏感度逐個運算向後拉回，每一步計算一個伴隨值 $\bar v_j = \partial f / \partial v_j$。它計算的乘積是向量-雅可比乘積。一次反向掃描即可服務所有輸入，因此反向模式適合多輸入、單輸出的函數，例如訓練損失。Baydin 等人（2022）把反向傳播描述為 AD 的一個特例，與前向模式並列。

## 核心概念

- **伴隨值** $\bar v$：輸出對某個中間值的導數。
- **磁帶**：前向計算中運算與其輸入的紀錄，反向讀取。
- **VJP 規則**：對每個運算，把輸出的伴隨值映射到輸入伴隨值的規則。例如對 $z = Wx$，$\bar x = W^{\top}\bar z$，且 $\bar W = \bar z\,x^{\top}$。
- **累加**：被多個運算使用的值，會收到這些運算各自貢獻的總和。

## 運作方式

每個值的伴隨值，等於所有消費該值的運算貢獻之和：

$$\bar v_j = \sum_{k \,:\, v_j \text{ 是 } v_k \text{ 的輸入}} \bar v_k \,\frac{\partial v_k}{\partial v_j}$$

演算法有四個步驟：

1. **前向計算**：依順序執行程式，保存每個中間值及產生它的運算。
2. **設定種子**：對純量損失，把輸出的伴隨值設為 $\bar y = 1$，其餘伴隨值設為零。
3. **反向掃描**：從最後一個運算到第一個，對每個運算的每個輸入 $v_j$，把 $\bar v_k\,\partial v_k/\partial v_j$ 加到 $\bar v_j$ 上。
4. **讀出**：輸入或參數的伴隨值即為梯度。

以[概述](../index.md)中的例子來說，反向掃描一次即得 $\bar x = 2.584$ 與 $\bar y = 2$。對純量輸出，無論有多少輸入，梯度的成本都只是前向計算的小常數倍。Griewank 與 Walther（2008）把這稱為廉價梯度原理。

保存的數值是代價：記憶體隨前向計算的長度增長，而原地（in-place）運算可能覆寫反向計算需要的值。

## 結果

反向模式的證據來自三類結果，這裡不引用基準測試表格中的數字：

- Rumelhart 等人（1986）在小型任務上展示，梯度反向傳播能讓隱藏單元學到內部表徵。
- Chen 等人（2016）顯示，記憶體可以用重新計算來交換。他們的摘要報告，將一個 1,000 層殘差網路的記憶體從 48 GB 降到 7 GB，運行時間約增加 30%。
- Chen 等人（2018）顯示，伴隨方法可以在固定記憶體成本下，透過 ODE 求解器反向傳播。

## 限制

- **記憶體**隨前向計算增長，因此深度模型需要檢查點。
- **多輸出的成本高。** 一個有許多輸出的函數其完整雅可比矩陣，需要每個輸出一次反向計算，此時前向模式可能更便宜。
- **不可微分的運算**，例如脈衝門檻或取樣，需要代理或估計量處理，見[代理梯度](../../../../brain-mind/snn-neuromorphic/surrogate-gradients/index.md)。
- **生物合理性。** 精確的反向模式需要在反向過程中使用前向權重的轉置。Lillicrap 等人（2016）指出，隨機、固定的回饋權重可以避開這個需求，但問題仍未解決。

## 開放問題

- 在極大規模下，檢查點、重新計算與記憶體之間的最佳取捨為何？
- Elliott（2018）那類不使用圖的函數式表述，能否在平行執行上帶來實際好處？
- 局部學習規則能否在不傳遞權重的情況下近似反向模式？

## 參考文獻

### 開創性論文

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*. https://doi.org/10.1038/323533a0 — 推廣多層網路的反向傳播，即訓練深度網路所用的反向模式方法。
- Pearlmutter, B. A. & Siskind, J. M. (2008). Reverse-mode AD in a functional framework. *ACM Transactions on Programming Languages and Systems*. https://doi.org/10.1145/1330017.1330018 — 以函數式語言表達反向模式 AD，包括高階函數。
- Elliott, C. (2018). The simple essence of automatic differentiation. ICFP 2018. https://arxiv.org/abs/1804.00746 — 從簡短的規格推導出不使用圖、磁帶的反向模式 AD 演算法。
- Chen, T., Xu, B., Zhang, C. & Guestrin, C. (2016). Training Deep Nets with Sublinear Memory Cost. https://arxiv.org/abs/1604.06174 — 梯度檢查點，以重新計算換取記憶體，用於訓練極深的網路。
- Lillicrap, T. P., Cownden, D., Tweed, D. B. & Akerman, C. J. (2016). Random synaptic feedback weights support error backpropagation for deep learning. *Nature Communications*. https://doi.org/10.1038/ncomms13276 — 主張隨機、固定的回饋權重可以取代誤差反向傳播中前向權重的轉置。

### 綜述與教科書

- Baydin, A. G., Pearlmutter, B. A., Radul, A. A. & Siskind, J. M. (2015/2018). Automatic differentiation in machine learning: a survey. *Journal of Machine Learning Research*. https://arxiv.org/abs/1502.05767 — 綜述，定義主要的微分技術及其關係，並以反向傳播作為反向模式的例子。
- Griewank, A. & Walther, A. (2008). *Evaluating Derivatives*. SIAM. https://doi.org/10.1137/1.9780898717761 — 反向模式、檢查點與廉價梯度原理的標準參考書。
- Baydin, A. G., Pearlmutter, B. A., Syme, D., Wood, F. & Torr, P. (2022). Gradients without Backpropagation. https://arxiv.org/abs/2202.08587 — 說明反向傳播是 AD 與前向模式並列下的一個特例，並提出前向梯度作為替代方案。

### 文章與文件

- Paszke, A. 等人（2019）。PyTorch: An Imperative Style, High-Performance Deep Learning Library. NeurIPS. https://arxiv.org/abs/1912.01703 — 描述 PyTorch 的設計，這是一個以 Python 為核心的框架，其執行環境中的 autograd 引擎即實作反向模式。
