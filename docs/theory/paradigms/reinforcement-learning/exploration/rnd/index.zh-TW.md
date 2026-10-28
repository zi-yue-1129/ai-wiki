---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
---

# 隨機網路蒸餾（Burda 等人，2018）

一種探索方法，獎勵智能體造訪其自身預測器尚未學會的狀態。預測器被訓練去模仿一個固定、隨機初始化的網路，因此在新穎狀態上誤差很高，並隨著狀態變得熟悉而下降。

## 問題

在稀疏獎勵的環境中，智能體在找到罕見獎勵之前幾乎得不到學習訊號。有些遊戲（例如《蒙特祖瑪的復仇》）需要一長串特定的動作，之後才會出現獎勵。先前以計數或學習得到的動力學模型為基礎的獎勵，難以擴展到這類高維觀測上。Burda 等人探討：在這些情境中，一個簡單的預測誤差能否驅動探索。

## 核心想法

RND 有兩個以相同觀測為輸入的網路。**目標網路**具有隨機權重，固定不訓練。**預測器網路**以梯度下降訓練，使其在智能體造訪的狀態上匹配目標網路的輸出。兩者輸出之差的平方即為探索獎勵，並加到外在獎勵上。

由於預測器在常被造訪的狀態上已經訓練過，那裡的誤差很小。新的狀態會產生較大的誤差，從而把智能體推向那裡。此方法不需要環境動力學的模型，也避開了預測原始未來觀測的困難。

論文也使用了修改過的 PPO。兩個價值頭（value heads）分別估計外在與內在獎勵的回報，因此兩個串流可以使用不同的折扣率。

## 方程式與演算法

對觀測 \(s\)，固定的隨機目標為 \(f\)，訓練中的預測器為 \(\hat f_\theta\)，內在獎勵為

\[
r^{\text{int}}_t = \lVert \hat f_\theta(s_t) - f(s_t) \rVert^2 .
\]

預測器參數 \(\theta\) 被更新，以最小化在已造訪狀態上的誤差；智能體則最大化外在與內在回報的總和。

## 結果

論文指出，若只最大化 RND 獎勵、不使用外在獎勵，智能體能穩定地找到《蒙特祖瑪的復仇》中超過一半的房間。完整方法搭配雙頭 PPO，通常能在第一關找到 24 個房間中的 22 個，並偶爾（但不常）通過第一關。摘要報告，此方法在 Venture、Gravitar 與《蒙特祖瑪的復仇》上達到當時最先進的效能。對於 Gravitar，論文指出 RND 並非每次都勝過 PPO，但它超越了先前的最先進結果。

## 限制

- **衡量的是新穎性，而非進展。** 獎勵偏好新穎性，因此智能體可能被難以預測但不重要的狀態吸引。
- **隨機觀測。** 對看似新穎但其實不是的狀態，預測器可能持續產生誤差，這可能會阻礙探索。
- **調校。** 結果取決於獎勵標準化的方式與兩個折扣率的選擇。

## 關聯

- 上層主題：[探索](../index.zh-TW.md)。
- 它是一種預測誤差獎勵，與[內在好奇心模組](../icm/index.zh-TW.md)相似，但不需要前向模型。
- Bellemare 等人（2016）的計數式獎勵是 RND 所比較的較早方法；修改後的 PPO 則建立在 [PPO](../../proximal-policy-optimisation/index.zh-TW.md) 之上。

## 應用

- **困難探索遊戲**，獎勵罕見，需要很長的動作序列。
- **稀疏獎勵的機器人**，獎勵只在任務完成時才出現。

## 未解問題

- 如何區分由智能體自身選擇所造成的新穎性，與環境隨機性所造成的新穎性。
- 如何把新穎性獎勵與任務所需的目標導向行為結合。

## 參考文獻

### 開創性論文

- Burda、Edwards、Storkey 與 Klimov（2018），"Exploration by random network distillation"，[arXiv:1810.12894](https://arxiv.org/abs/1810.12894) — RND 原始論文，包含目標與預測器獎勵、雙頭 PPO，以及《蒙特祖瑪的復仇》結果。
- Bellemare 等人（2016），"Unifying count-based exploration and intrinsic motivation"，[arXiv:1606.01868](https://arxiv.org/abs/1606.01868) — 偽計數獎勵，是 RND 所比較的計數式方法。
- Pathak、Agrawal、Efros 與 Darrell（2017），"Curiosity-driven exploration by self-supervised prediction"，[arXiv:1705.05363](https://arxiv.org/abs/1705.05363) — 內在好奇心模組，另一種預測誤差獎勵。
- Stadie、Levine 與 Abbeel（2015），"Incentivizing exploration in reinforcement learning with deep predictive models"，[arXiv:1507.00814](https://arxiv.org/abs/1507.00814) — 以學到的預測模型為基礎的早期預測誤差獎勵。
- Houthooft 等人（2016），"VIME: Variational information maximizing exploration"，[arXiv:1605.09674](https://arxiv.org/abs/1605.09674) — 以資訊增益進行探索，是預測誤差獎勵的替代方案。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — RND 以兩個價值頭修改的策略梯度方法。
