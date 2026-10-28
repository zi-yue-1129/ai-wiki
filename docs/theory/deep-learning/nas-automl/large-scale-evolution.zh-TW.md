---
translation_reviewed: 2026-10-28
---

# 影像分類器的大規模演化（Real 等人，2017）

大規模演化以極大的規模，把簡單的演化演算法用於架構搜尋：從簡單的網路開始，並使用為了在大搜尋空間中移動而設計的突變運算子。本頁是[神經架構搜尋](index.md)的一部分。

## 概述

Real、Moore、Selle、Saxena、Suematsu、Tan、Le 與 Kurakin（2017）想知道，在沒有學習式控制器、只給予大量運算的情況下，單純的演化搜尋能走多遠。他們的目標是盡量減少人工參與，因此方法從簡單的初始網路開始，無需人類進一步輸入，即演化成完全訓練好的分類器。論文也強調結果的可重現性，以及各次執行結果的變異。之後的[正則化演化](regularized-evolution.md)方法即建立於這項工作之上。

## 關鍵概念

- **簡單的初始模型**：演化開始時的最小網路。
- **突變運算子**：改變網路的規則，例如加入一層、改變濾波器大小，或改變一條連接。
- **族群**：演化過程中保留的網路集合，每個網路都訓練至完成。

## 問題

在沒有學習式控制器、從簡單模型開始的情況下，單純的演化搜尋能否達到與人類專家設計的架構相當的準確率？

## 運作方式

演算法保留一群已訓練的網路。每一步選出一個父代，對其套用突變運算子產生子代，訓練子代，並把它加入族群。經過許多步之後，族群逐步改善，最終得到完全訓練好的模型，不需人工介入。

突變運算子是主要的設計選擇。它們的目的是讓搜尋能穿越大的搜尋空間，使族群能從簡單的起點抵達好的架構。

## 主要方法

本頁只涵蓋一種方法：以新穎的突變運算子，從簡單網路開始，在極大規模上執行的簡單演化。

- **初始化**：簡單的網路，沒有複雜的結構。
- **突變**：加入、移除或改變層與連接的運算子，著重於大幅度的移動。
- **選擇與替換**：子代訓練完成時更新族群。

## 變體

- **集成輸出**：論文除了單一模型的準確率外，也報告了演化所得模型集成的準確率。
- **其他搜尋空間**改變突變與其作用的網路，而不改變演化迴圈。

## 結果與限制

- Real 等人（2017）報告，從簡單的初始條件開始，單一模型在 CIFAR-10 上的準確率為 94.6%（集成為 95.6%），在 CIFAR-100 上為 77.0%。
- 論文強調搜尋的運算需求，以當時的標準而言非常龐大，並報告了各次執行結果的變異。
- 結果取決於突變運算子，而這些運算子是針對論文中的搜尋空間設計的。
- 由於每個候選都訓練至完成，此方法需要大量運算，在小預算下很難重現。

## 應用

- **影像分類器搜尋**，在有大量運算、並希望盡量減少人工設計投入的情況下。
- **搜尋可重現性的研究**，論文報告了各次執行結果的變異。
- **[正則化演化](regularized-evolution.md)等後續演化方法**的基準。

## 開放問題

- 結果有多少取決於運算規模，又有多少取決於突變運算子？
- 在小預算下，演化搜尋的結果在不同隨機種子之間有多穩定？

## 與其他頁面的連結

- 上層主題：[神經架構搜尋](index.md)
- 後續的演化方法：[正則化演化](regularized-evolution.md)
- 與其比較的強化學習搜尋：Zoph 與 Le（2017），見[上層頁面](index.md)

## 參考文獻

### 奠基性論文

- Real, E., Moore, S., Selle, A., Saxena, S., Suematsu, Y. L., Tan, J., Le, Q. & Kurakin, A. (2017). Large-Scale Evolution of Image Classifiers. In *Proceedings of the 34th ICML*, PMLR 70. https://proceedings.mlr.press/v70/real17a.html — 顯示從簡單的起始網路開始、在大規模下的簡單演化，能在 CIFAR-10 與 CIFAR-100 上達到與已發表模型相當的準確率。
- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence* 33, 4780–4789. https://doi.org/10.1609/aaai.v33i01.33014780 — 改變替換規則的後續演化方法。
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — 本研究與之比較的強化學習搜尋。

### 綜述與教科書

- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — 把演化搜尋歸入搜尋策略的綜述。
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — 避免訓練每個候選之成本的梯度式搜尋。
- Pham, H. et al. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — 降低每個候選成本的權重共享替代方案。
