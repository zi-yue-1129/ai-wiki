---
translation_reviewed: 2026-10-28
---

# 正則化演化（Real 等人，2019）

正則化演化是一種對架構的演化搜尋，它依年齡順序維持族群，每一步移除最老的成員，而非最差的成員。父代以錦標賽選出，子代則由父代做小幅突變產生。本頁是[神經架構搜尋](index.md)的一部分。

## 概述

Zoph 與 Le（2017）以強化學習搜尋架構，當時普遍認為要有學習式的控制器，搜尋才有效率。Real、Aggarwal、Huang 與 Le（2019）顯示，只要以特定方式管理族群，單純的演化搜尋在相同運算預算下，就能與強化學習相當或更好。關鍵的改變是移除最老的模型，而非最差的模型，這使族群保持多樣性，也避免早期的幸運模型一直佔據族群。

## 關鍵概念

- **族群**：依年齡排序的已訓練架構佇列。
- **錦標賽選擇**：從族群中抽出一個樣本，取樣本中最好者作為父代。
- **突變**：對父代的小幅隨機改動，例如改變一個運算或一條連接。
- **老化**：每一步移除族群中最老的架構，無論其分數如何。

## 問題

在不使用學習式控制器的情況下，架構的演化搜尋如何找到至少與強化學習搜尋相當的模型？

## 運作方式

演算法從隨機產生的一群架構開始，每個架構都經過訓練，並在驗證集上評分。每一步執行以下動作。

1. 從族群中隨機抽出 \(S\) 個成員，並選其中最好者作為父代。
2. 對父代突變產生子代，並訓練子代。
3. 把子代加入族群。
4. 移除族群中最老的成員。

因為移除的是最老的成員，而非最差的成員，早期分數好的模型不會永遠留在族群中，搜尋也持續探索。

## 主要方法

本頁只涵蓋一種方法：搭配錦標賽選擇與單次突變的老化演化。

- **初始族群**：隨機架構，各自訓練至完成。
- **選擇**：以大小為 \(S\) 的錦標賽選出父代。
- **突變**：對父代架構的小幅隨機改動。
- **替換**：子代進入族群，最老的成員離開。

## 變體

- **移除最差成員的演化**改為移除分數最低的成員。Real 等人（2019）在其實驗中顯示，老化的選擇較好。
- **其他突變集合**改變允許的運算與連接，這改變的是搜尋空間，而非演算法。

## 結果與限制

- Real 等人（2019）報告，在他們的影像分類搜尋空間上，在相同運算預算下，正則化演化與強化學習搜尋相當或更好。
- 此方法從頭訓練每個子代，因此每個候選的成本與原本的強化學習搜尋相當。[ENAS](efficient-neural-architecture-search.md) 等權重共享方法可以降低這個成本。
- 突變是針對搜尋空間人工設計的，因此結果取決於突變的選擇。
- 老化會同時移除好的與差的模型，在族群很小時，可能使收斂變慢。

## 應用

- **影像分類器搜尋**，在不想使用強化學習控制器的情況下。
- **多工作者的搜尋**，子代可以平行訓練，族群也不需要同步。
- **新架構搜尋方法的基準**。

## 開放問題

- 對新的搜尋空間，族群大小與錦標賽大小應如何選擇？
- 老化能否與權重共享結合，而不損失其多樣性的好處？

## 與其他頁面的連結

- 上層主題：[神經架構搜尋](index.md)
- 較早的演化研究：[影像分類器的大規模演化](large-scale-evolution.md)
- 與其比較的強化學習搜尋：Zoph 與 Le（2017），見[上層頁面](index.md)

## 參考文獻

### 奠基性論文

- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence* 33, 4780–4789. https://doi.org/10.1609/aaai.v33i01.33014780 — 提出老化演化（每一步移除最老的模型），並與強化學習搜尋比較。
- Real, E., Moore, S., Selle, A., Saxena, S., Suematsu, Y. L., Tan, J., Le, Q. & Kurakin, A. (2017). Large-Scale Evolution of Image Classifiers. In *Proceedings of the 34th ICML*, PMLR 70. https://proceedings.mlr.press/v70/real17a.html — 正則化演化所建立於其上的早期大規模演化研究。
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — 老化演化與之比較的強化學習搜尋。

### 綜述與教科書

- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — 把演化搜尋歸入搜尋策略的綜述。
- Pham, H. et al. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — 降低每個候選訓練成本的權重共享替代方案。
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — 演化搜尋的梯度式替代方案。
