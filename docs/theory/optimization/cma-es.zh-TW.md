---
translation_reviewed: 2026-10-28
---

# CMA-ES

CMA-ES（協方差矩陣自適應演化策略）是一種不需要梯度的實數參數最佳化隨機方法。它從高斯分布取樣候選解，依分數排序，並調整該高斯分布的均值、步長與協方差矩陣。Hansen（2016）提供此方法的教學文件。上層概述見[零階與演化最佳化](zeroth-order-and-evolutionary.md)。

## 概述

CMA-ES 是族群方法。它的目標是無法取得梯度的非線性、非凸問題，並從已評估過的樣本中學習搜尋分布的形狀。

## 問題

最小化可能非凸且病態的黑箱目標 \(f:\mathbb{R}^n \to \mathbb{R}\)。固定的隨機搜尋無法適應狹長或旋轉的山谷，因此需要許多次評估才能沿著山谷前進。

## 核心想法

保有一個高斯搜尋分布，其均值為 \(m\)、步長為 \(\sigma\)、協方差為 \(C\)。分布會被移動與重塑，使好的樣本更有可能被取出。協方差會適應搜尋已經有進展的方向，這正是它能沿著狹長山谷前進的原因。

## 演算法

每次迭代：

1. 取樣 \(\lambda\) 個候選解 \(x_i \sim m + \sigma\,\mathcal{N}(0, C)\)。
2. 評估並依 \(f(x_i)\) 排序。
3. 把均值 \(m\) 移向最好的 \(\mu\) 個候選解的加權平均。
4. 由被選中的步長更新協方差 \(C\)，並由一條追蹤步伐是否一致的演化路徑更新步長 \(\sigma\)。

以排名為基礎的更新，使方法對 \(f\) 的單調變換不變，因為只有分數的順序有影響。

## 主要結果

教學文件把 CMA-ES 描述為一種用於實數參數最佳化的隨機方法，目標是非線性、非凸函數。摘要中沒有基準測試的數字，因此本頁不引用任何數值。

## 限制

- 更新協方差矩陣所需的記憶體與計算量，隨參數數量的平方成長，因此方法適用於數百個參數的問題，而非數百萬個。
- 族群大小 \(\lambda\) 影響方法跳出局部極小值的能力，預設值是折衷，並非適合所有問題的設定。
- 沒有梯度時，每次評估的進展通常慢於在平滑問題上的梯度方法。

## 關聯

- [零階與演化最佳化](zeroth-order-and-evolutionary.md)是上層概述，CMA-ES 與 SPSA、演化策略並列於其中。
- [演化策略](evolution-strategies.md)與 CMA-ES 同樣使用族群取樣，但不以相同方式調整完整的協方差矩陣。
- [SPSA](spsa.md)以兩次擾動估計梯度，不調整分布。
- [二階方法](second-order.md)同樣建模目標的局部形狀，但使用梯度而非樣本。

## 應用

- 調整模擬器或控制器的少數參數，此時評估成本高，且無法取得梯度。
- 工程中的連續設計問題，其目標是黑箱模擬。

## 開放問題

- 對於有數百萬參數的模型，如何讓協方差適應變得負擔得起？
- 何時應增加族群大小以跳出局部極小值，能否自動決定？

## 參考文獻

### 開創性論文

- Hansen, N.（2016）。*The CMA Evolution Strategy: A Tutorial*。arXiv。https://arxiv.org/abs/1604.00772 — CMA-ES 的教學文件，這是一種用於非線性、非凸實數參數最佳化的隨機方法。
- Salimans, T., 等人（2017）。*Evolution Strategies as a Scalable Alternative to Reinforcement Learning*。arXiv。https://arxiv.org/abs/1703.03864 — 以族群為基礎的政策梯度估計器，是大規模設定中 CMA-ES 的主要替代方案。
- Spall, J. C.（1992）。Multivariate stochastic approximation using a simultaneous perturbation gradient approximation。*IEEE Transactions on Automatic Control*，37(3)，332–341。https://doi.org/10.1109/9.119632 — 同一比較另一側的無梯度估計器。
- Malladi, S., 等人（2023）。*Fine-Tuning Language Models with Just Forward Passes*。arXiv。https://arxiv.org/abs/2305.17333 — 用於大型模型的零階方法，其中協方差適應負擔不起。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 基於梯度的隨機方法綜述，是無梯度方法比較時的基準。
