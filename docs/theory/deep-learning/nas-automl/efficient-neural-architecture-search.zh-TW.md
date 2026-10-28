---
translation_reviewed: 2026-10-28
---

# 高效神經架構搜尋（Pham 等人，2018）

ENAS 讓所有候選架構共享同一組權重，使架構搜尋比原本以強化學習進行的搜尋便宜許多。循環控制器在一個大型運算圖的子圖中取樣，控制器則以驗證獎勵的策略梯度訓練。本頁是[神經架構搜尋](index.md)的一部分。

## 概述

Zoph 與 Le（2017）的搜尋會從頭訓練每個取樣的架構，因此非常昂貴。Pham、Guan、Zoph、Le 與 Dean（2018）注意到，所有候選架構都是同一個大圖的子圖，因此它們的運算可以共享參數。訓練一個候選時，也會更新其他候選所用的參數，使評估每個候選的成本大幅降低。

## 關鍵概念

- **超圖**：包含所有候選架構作為子圖的有向無環圖。
- **控制器** \(\pi(m;\theta)\)：以參數 \(\theta\) 取樣架構 \(m\) 的循環網路。
- **共享權重** \(w\)：每個取樣子圖都重複使用的一組運算參數。
- **驗證獎勵** \(R(m,w)\)：取樣架構 \(m\) 在共享權重 \(w\) 下、於驗證集上的準確率。

## 問題

如何讓 Zoph 與 Le（2017）的控制器式搜尋便宜到能在一般硬體上執行，而不必從頭訓練每個取樣的架構？

## 運作方式

搜尋交替進行兩種更新。

1. **共享權重。** 從控制器取樣一個架構 \(m\)，並在訓練集上訓練共享權重 \(w\)，使子圖 \(m\) 的交叉熵損失最小。
2. **控制器。** 取樣數個架構，在驗證集上評估其獎勵，並更新 \(\theta\) 以最大化期望獎勵 \(J(\theta) = \mathbb E_{m\sim\pi(m;\theta)}[R(m,w)]\)。

控制器的梯度使用帶基線 \(b\) 的 REINFORCE 估計量，

\[
\nabla_\theta J(\theta) \approx \frac{1}{M}\sum_{k=1}^{M} \bigl(R(m_k, w) - b\bigr)\,\nabla_\theta \log \pi(m_k;\theta),
\]

其中 \(M\) 為取樣的架構數，\(b\) 通常是過去獎勵的指數移動平均。搜尋結束後，控制器偏好的最佳取樣架構會從頭重新訓練，因為共享權重只是一種估計。

## 主要方法

本頁只涵蓋一種方法：控制器在超圖的子圖上取樣，權重共享，並以驗證獎勵的策略梯度訓練。

- **超圖設計**：一組足夠大、能包含好架構的運算與連接。
- **交替更新**：共享權重與控制器在不同的資料切分上輪流訓練。
- **最終訓練**：控制器偏好的架構會從頭重新訓練，因為共享權重只是估計。

## 變體

- **循環單元搜尋**把 ENAS 應用於語言建模，輸出為循環單元。
- **卷積單元搜尋**把它應用於影像分類，輸出為堆疊成網路的卷積單元。
- **其他取樣規則**以不同的分布取代控制器，改變搜尋探索空間的方式。

## 結果與限制

- Pham 等人（2018）報告，ENAS 以遠少於早期自動模型設計的 GPU 小時取得強勁結果，且成本約為標準 NAS 的 1000 分之一。
- 在 Penn Treebank 上，作者報告 ENAS 找到的架構測試困惑度為 55.8。在 CIFAR-10 上，他們報告測試錯誤率為 2.89%，接近 NASNet 的 2.65%（Pham 等人，2018）。
- 參數共享可能使子圖的排序不可靠，因此搜尋時表現最好的架構，在完整訓練後未必最好。Yu 等人（2020）研究了權重共享方法的這種效應。
- 控制器的獎勵取決於仍在變動的共享權重，因此獎勵有雜訊，策略梯度的變異也很大。

## 應用

- **低預算的架構搜尋**，在強化學習搜尋成本過高的情況下使用。
- **循環單元的發現**，用於序列建模，延續語言建模的結果。
- **後續權重共享方法的基準**，例如以同樣想法、但採用不同搜尋策略的 [DARTS](darts.md)。

## 開放問題

- 當搜尋空間大得多，或目標是大型現代模型時，這種成本節省還能保留多少？
- 能否在搜尋過程中，以低成本檢查共享權重排序的可靠性？

## 與其他頁面的連結

- 上層主題：[神經架構搜尋](index.md)
- 本主題的另一方法：[DARTS](darts.md)，它放寬搜尋空間，而不是取樣它
- 此方法所使之更便宜的搜尋：Zoph 與 Le（2017），見[上層頁面](index.md)

## 參考文獻

### 奠基性論文

- Pham, H., Guan, M., Zoph, B., Le, Q. & Dean, J. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — 提出 ENAS：控制器在共享權重的超圖子圖上取樣，並以驗證獎勵的策略梯度訓練。
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — 每個候選都從頭訓練的強化學習搜尋，ENAS 使其更便宜。
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — 另一種權重共享的搜尋，以梯度下降最佳化架構選擇。

### 綜述與教科書

- Yu, K. et al. (2020). Evaluating the Search Phase of Neural Architecture Search. In *ICLR 2020*. arXiv:1902.08142. https://arxiv.org/abs/1902.08142 — 檢驗搜尋時使用的共享權重排序，能否預測最終準確率。
- Zela, A. et al. (2020). Understanding and Robustifying Differentiable Architecture Search. In *ICLR 2020*. arXiv:1909.09656. https://arxiv.org/abs/1909.09656 — 分析可微分設定中權重共享搜尋的失敗模式。
- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — 把權重共享歸入效能估計策略的綜述。
