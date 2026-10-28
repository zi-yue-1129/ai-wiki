---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - REINFORCE
  - 策略梯度 REINFORCE
---

# REINFORCE（Williams，1992）

一種蒙地卡羅策略梯度方法：每個被取樣的動作，其對數機率會依其後所得的回報成比例地提高。

## 問題

隨機策略應該被直接調整，以增加它所獲得的期望強化，而不需要環境模型或價值函數。Williams 探討：對於具有隨機輸出單元的網路，哪一種更新規則能做到這點，以及它是否會使參數沿著期望強化的梯度方向移動。

## 核心想法

對於權重為 \(w_{ij}\) 的隨機單元，Williams 定義更新 \(\Delta w_{ij} = \alpha_{ij}\,(r - b_{ij})\,e_{ij}\)。其中 \(r\) 是強化訊號，\(b_{ij}\) 是基線，\(e_{ij}\) 是資格項（eligibility term），即被取樣輸出的對數機率對該權重的導數。論文的定理 1 指出，平均更新向量位於期望強化會增加的方向上。該定理對任何強化基線都成立，但論文推測，基線的選擇會使演算法收斂到局部最大值的可能性有所不同。

## 方程式與演算法

依本維基使用的記號，REINFORCE 以取樣的回合估計期望回報 \(J(\theta)\) 的梯度：

\[
\nabla_\theta J(\theta) \approx \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\,\big(G_t - b\big)
\]

其中 \(G_t\) 是從第 \(t\) 步起的回報，\(b\) 是基線。流程如下：

1. 初始化策略參數 \(\theta\)。
2. 依 \(\pi_\theta\) 行動，取樣一個完整的回合。
3. 對每一步 \(t\)，計算回報 \(G_t\)。
4. 更新 \(\theta \leftarrow \theta + \alpha \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\,(G_t - b)\)。
5. 回到第 2 步重複。

## 結果

Williams 的論文提供的是推導與定理，而非基準測試。它的貢獻在於一般化的更新規則類別，後來的策略梯度方法都建立在這個基礎上。

## 限制

- **高變異。** 以完整回報作為權重，得到的是不偏但雜訊很大的梯度。基線與評論家（即[演員–評論家方法](../a3c/index.zh-TW.md)的基礎）能降低變異。
- **同策略且以回合為單位。** 每個回合只用於一次更新，因此方法很耗樣本。
- **局部最大值。** 論文並未證明收斂。它推測基線會影響演算法最終到達哪一個局部最大值，而定理只保證期望更新指向上坡方向。

## 關聯

- 上層主題：[策略梯度與演員–評論家](../index.md)，以及更廣的[強化學習](../../index.zh-TW.md)概觀。
- 其帶優勢的形式是 [A3C](../a3c/index.zh-TW.md)、[TRPO](../trpo/index.zh-TW.md) 與[近端策略最佳化](../../proximal-policy-optimisation/index.zh-TW.md)的出發點。
- [GRPO](../grpo/index.zh-TW.md) 保留 REINFORCE 式的更新，但其基線取自一組被取樣輸出的平均獎勵。

## 應用

- **語言模型微調。** 以取樣獎勵作為基線的策略梯度更新，是用來對齊語言模型的強化學習基礎（Ouyang 等人，2022；Shao 等人，2024）。

## 未解問題

- 在長時程任務中，哪些基線能在不引入偏差的情況下降低變異。
- 如何保留 REINFORCE 的簡單性，同時重用資料；後來的方法正朝此方向努力。

## 參考文獻

### 開創性論文

- Williams（1992），"Simple statistical gradient-following algorithms for connectionist reinforcement learning"，*Machine Learning* 8(3–4), 229–256。https://doi.org/10.1007/bf00992696 — 提出 REINFORCE 更新並證明梯度方向定理的論文。
- Schulman 等人（2016），"High-dimensional continuous control using generalized advantage estimation"，[arXiv:1506.02438](https://arxiv.org/abs/1506.02438) — 用於降低策略梯度更新變異的優勢估計。
- Mnih 等人（2016），"Asynchronous methods for deep reinforcement learning"，[arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — 以優勢作為基線的演員–評論家策略梯度。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — 建立在相同對數機率梯度上的截斷式策略梯度方法。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*，第 2 版。MIT Press, 2018。http://incompleteideas.net/book/the-book-2nd.html — 標準教科書中的策略梯度方法與基線的角色。

### 文章與文件

- Ouyang 等人（2022），"Training language models to follow instructions with human feedback"，[arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT，以來自人類回饋的強化學習微調語言模型。
- Shao 等人（2024），"DeepSeekMath: Pushing the limits of mathematical reasoning in open language models"，[arXiv:2402.03300](https://arxiv.org/abs/2402.03300) — 提出 GRPO，以群組平均取代學習得到的評論家。
