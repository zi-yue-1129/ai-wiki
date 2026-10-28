---
translation_reviewed: 2026-10-28
---

# 演化策略

演化策略（ES）透過取樣一組擾動後的參數，並依各樣本的分數加權，來估計期望獎勵的梯度。Salimans 等人（2017）顯示，這個簡單方法能擴展到大量平行工作者，並能訓練出與強化學習競爭的策略。上層概述見[零階與演化最佳化](zeroth-order-and-evolutionary.md)。

## 概述

ES 是零階方法。它只需要每個取樣策略的獎勵，不需要其梯度，因此適用於模擬器與黑箱環境。

## 問題

最大化期望獎勵 \(F(\theta)\)，其中 \(F\) 可能不可微，或無法透過環境做反向傳播。政策梯度需要獎勵沿策略路徑可微，但這不一定成立。

## 核心想法

在參數上加入高斯雜訊，以平滑化目標：

\[
F_\sigma(\theta) = \mathbb{E}_{\varepsilon \sim \mathcal{N}(0, I)}\big[F(\theta + \sigma\varepsilon)\big].
\]

平滑目標的梯度可以在不對 \(F\) 求導的情況下寫出：

\[
\nabla_\theta F_\sigma(\theta) = \frac{1}{\sigma}\,\mathbb{E}_{\varepsilon}\big[F(\theta + \sigma\varepsilon)\,\varepsilon\big].
\]

## 演算法

從 \(\mathcal{N}(0, I)\) 取出 \(n\) 個雜訊向量 \(\varepsilon_1,\dots,\varepsilon_n\)，對每個計算獎勵 \(F_i = F(\theta + \sigma\varepsilon_i)\)，並形成估計

\[
g = \frac{1}{n\sigma}\sum_{i=1}^{n} F_i\,\varepsilon_i.
\]

再以 \(\theta \leftarrow \theta + \alpha g\) 更新，其中 \(\alpha\) 是學習率。每個工作者評估部分樣本，因此工作者之間只需分享純量獎勵與隨機種子。

## 主要結果

摘要報告，ES 能擴展到超過一千個平行工作者，只需傳送純量，並在 10 分鐘內解決三維人形機器人行走的問題。它也報告在 Atari 大多數遊戲上，訓練一小時後能取得有競爭力的結果。摘要未給出各遊戲的分數，因此本頁不引用。

## 限制

- 每次更新都需要一整個族群的展開，因此與每步只用一條軌跡的梯度方法相比，ES 需要的樣本較多。
- 估計的變異數隨參數數量增加，因此大型網路需要大的族群。
- 平滑尺度 \(\sigma\) 與學習率 \(\alpha\) 必須調校，結果對它們高度敏感。
- 論文中的優勢仰賴大規模平行化，因此與單機上的比較並非同條件的比較。

## 關聯

- [零階與演化最佳化](zeroth-order-and-evolutionary.md)是上層概述，ES 與 SPSA、CMA-ES 並列於其中。
- [SPSA](spsa.md)以兩次擾動估計梯度，而不是以族群。
- [CMA-ES](cma-es.md)使用同類的族群取樣，但不以相同方式調整完整的協方差矩陣。
- [強化學習](../paradigms/reinforcement-learning/index.md)提供 ES 所比較的政策梯度方法。

## 應用

- 在物理模擬器中訓練移動策略，如人形機器人行走的結果。
- 從像素訓練 Atari 代理人，此時獎勵可取得但不可微。

## 開放問題

- 在相同的環境互動次數下，ES 與政策梯度方法相比如何？
- 對大型網路，能否在不損失梯度估計品質的情況下減少族群大小？

## 參考文獻

### 開創性論文

- Salimans, T., Ho, J., Chen, X., Sidor, S. & Sutskever, I.（2017）。*Evolution Strategies as a Scalable Alternative to Reinforcement Learning*。arXiv。https://arxiv.org/abs/1703.03864 — 顯示 ES 能擴展到超過一千個平行工作者，並在 MuJoCo 與 Atari 上與強化學習競爭。
- Spall, J. C.（1992）。Multivariate stochastic approximation using a simultaneous perturbation gradient approximation。*IEEE Transactions on Automatic Control*，37(3)，332–341。https://doi.org/10.1109/9.119632 — ES 作為黑箱目標替代方案時，所對照的無梯度估計器。
- Malladi, S., 等人（2023）。*Fine-Tuning Language Models with Just Forward Passes*。arXiv。https://arxiv.org/abs/2305.17333 — 後來用於語言模型微調的零階方法，與 ES 作比較。

### 綜述與教科書

- Hansen, N.（2016）。*The CMA Evolution Strategy: A Tutorial*。arXiv。https://arxiv.org/abs/1604.00772 — 演化策略家族中調整協方差之成員的教學文件。
- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 基於梯度的隨機方法綜述，是 ES 比較時的基準。
