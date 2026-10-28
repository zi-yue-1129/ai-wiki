---
translation_reviewed: 2026-10-28
---

# REINFORCE（Williams，1992）

一種蒙地卡羅策略梯度方法，依照每個被取樣動作之後的回報，提高該動作的對數機率。

## 問題

在不知道環境模型、也沒有價值函數的情況下，應如何直接調整隨機策略的參數，以提高其期望獎勵？Williams 探討對於具有隨機輸出單元的網路，哪一種更新規則能做到這點，並使參數沿著期望強化的梯度方向移動。

## 核心想法

對權重 \(w_{ij}\) 的隨機單元，Williams 定義更新式 \(\Delta w_{ij} = \alpha_{ij}\,(r - b_{ij})\,e_{ij}\)。其中 \(r\) 是強化訊號，\(b_{ij}\) 是基線，\(e_{ij}\) 是資格項，即被取樣輸出的對數機率對該權重的偏導數。論文的定理 1 指出，平均更新向量位於期望強化會增加的方向。基線不改變該方向，但論文指出基線的選擇會影響演算法可能到達的局部最大值。

## 方程式或演算法

以本維基通用的記號，REINFORCE 從取樣的回合估計期望回報 \(J(\theta)\) 的梯度：

\[
\nabla_\theta J(\theta) \approx \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\,\big(G_t - b\big)
\]

其中 \(G_t\) 是從第 \(t\) 步起的回報，\(b\) 是基線。流程如下：

1. 初始化策略參數 \(\theta\)。
2. 依 \(\pi_\theta\) 取樣一整個回合。
3. 對每一步 \(t\)，計算回報 \(G_t\)。
4. 更新 \(\theta \leftarrow \theta + \alpha \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\,(G_t - b)\)。
5. 從第 2 步重複。

## 結果

Williams 的論文提供的是推導與定理，而非基準測試。它的貢獻是更新規則的一般類別，這是之後策略梯度方法的基礎。

## 限制

- **變異數高。**以完整回報作為權重，得到的梯度無偏但含有雜訊。基線與評論家（即[演員–評論家方法](../a3c/index.md)的基礎）可降低變異數。
- **同策略且依回合。**每個回合只用於一次更新，因此很耗樣本。
- **局部最大值。**論文指出基線會影響演算法可能到達的局部最大值，而定理只保證沿梯度方向移動。

## 連結

- 母頁：[策略梯度與演員–評論家](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 其含優勢函數的形式是 [A3C](../a3c/index.md)、[TRPO](../trpo/index.md) 與[近端策略最佳化](../../proximal-policy-optimisation/index.md)的起點。
- [GRPO](../grpo/index.md) 保留 REINFORCE 式的更新，但基線改由一組取樣輸出的平均獎勵提供。

## 應用

- **語言模型微調。**以取樣獎勵作為基線的策略梯度更新，是用於對齊語言模型的強化學習基礎（Ouyang 等人，2022；Shao 等人，2024）。

## 未解問題

- 哪些基線能在長時程任務中，於不引入偏誤的前提下降低變異數。
- 如何在保留 REINFORCE 簡單性的同時重複利用資料，這是後續方法所追求的目標。

## 參考文獻

### 開創性論文

- Williams (1992), "Simple statistical gradient-following algorithms for connectionist reinforcement learning", *Machine Learning* 8(3–4), 229–256. https://doi.org/10.1007/bf00992696 — The paper that introduces the REINFORCE update and proves the gradient-direction theorem.
- Schulman et al. (2016), "High-dimensional continuous control using generalized advantage estimation", [arXiv:1506.02438](https://arxiv.org/abs/1506.02438) — Advantage estimation for reducing the variance of policy-gradient updates.
- Mnih et al. (2016), "Asynchronous methods for deep reinforcement learning", [arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — Actor-critic policy gradients with an advantage baseline.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — A clipped policy-gradient method built on the same log-probability gradient.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Policy-gradient methods and the role of baselines in the standard textbook.

### 文章與文件

- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT, which fine-tunes a language model with reinforcement learning from human feedback.
- Shao et al. (2024), "DeepSeekMath: Pushing the limits of mathematical reasoning in open language models", [arXiv:2402.03300](https://arxiv.org/abs/2402.03300) — Introduces GRPO, which uses a group-mean baseline in place of a learned critic.
