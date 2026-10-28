---
translation_reviewed: 2026-10-28
---

# 隨機網路蒸餾（Burda 等人，2018）

一種探索方法，獎勵智能體造訪其自身預測器尚未學會的狀態。預測器被訓練來模仿一個固定、隨機初始化的網路，因此在新穎狀態上誤差很高，並隨著狀態變得熟悉而下降。

## 問題

在稀疏獎勵的環境中，智能體在找到罕見的獎勵之前幾乎得不到學習訊號。有些遊戲（例如蒙特祖瑪的復仇）在出現任何獎勵之前，需要一長串特定的動作。先前以計數或學到的動態模型為基礎的獎勵，很難擴展到這類高維觀測。Burda 等人探討：簡單的預測誤差能否在這些設定中驅動探索。

## 核心想法

RND 有兩個接收相同觀測的網路。**目標**網路擁有隨機權重，固定不動、從不訓練。**預測器**網路以梯度下降訓練，使其在智能體造訪的狀態上符合目標網路的輸出。兩個輸出的平方差就是探索獎勵，會加到外在獎勵上。

由於預測器已在頻繁造訪的狀態上訓練，它在那些狀態上的誤差很小；新的狀態則產生很大的誤差，把智能體推向它們。此方法不需要環境動態的模型，也避開了預測原始未來觀測的困難。

論文還使用了修改過的 PPO：兩個價值頭分別估計外在與內在獎勵的回報，使兩個流可以採用不同的折扣率。

## 方程式或演算法

對於觀測 \(s\)，給定固定的隨機目標 \(f\) 與已訓練的預測器 \(\hat f_\theta\)，內在獎勵為

\[
r^{\text{int}}_t = \lVert \hat f_\theta(s_t) - f(s_t) \rVert^2 .
\]

預測器參數 \(\theta\) 被更新以最小化在造訪狀態上的此誤差，而智能體最大化外在與內在回報的總和。

## 結果

論文報告，只最大化 RND 獎勵、沒有外在獎勵的智能體，能持續找到蒙特祖瑪的復仇中超過一半的房間。完整方法結合兩個價值頭的 PPO，常能找到第一關 24 個房間中的 22 個，並偶爾通過第一關。作者在 Venture 與 Gravitar 兩款遊戲上報告了當時最先進的表現。

## 限制

- **衡量新穎性，而非進展。** 獎勵的是新穎性，因此智能體可能被不可預測但不重要的狀態吸引。
- **隨機觀測。** 對於看起來是新的、實際上並非新的狀態，預測器可能持續產生誤差，從而拖累探索。
- **調整。** 結果取決於獎勵正規化的選擇與兩個折扣率。

## 關聯

- 上層主題：[探索](../index.md)。
- 它與[內在好奇心模組](../icm/index.md)同屬預測誤差獎勵，但不需要前向模型。
- Bellemare 等人（2016）的計數獎勵是 RND 比較的先前方法，而修改過的 PPO 建立在 [PPO](../../proximal-policy-optimisation/index.md) 之上。

## 應用

- **困難探索遊戲**，獎勵稀少，需要一長串動作。
- **稀疏獎勵的機器人學**，獎勵只在任務完成時才出現。

## 未解問題

- 如何區分由智能體自身選擇所造成的新穎性，與環境隨機性造成的新穎性。
- 如何結合新穎性獎勵與任務所需的目標導向行為。

## 參考文獻

### 奠基性論文

- Burda, Edwards, Storkey & Klimov（2018），"Exploration by random network distillation"，[arXiv:1810.12894](https://arxiv.org/abs/1810.12894)——RND 論文，包含目標與預測器獎勵、兩個價值頭的 PPO，以及蒙特祖瑪的復仇結果。
- Bellemare 等人（2016），"Unifying count-based exploration and intrinsic motivation"，[arXiv:1606.01868](https://arxiv.org/abs/1606.01868)——偽計數獎勵，是 RND 比較的計數方法。
- Pathak, Agrawal, Efros & Darrell（2017），"Curiosity-driven exploration by self-supervised prediction"，[arXiv:1705.05363](https://arxiv.org/abs/1705.05363)——內在好奇心模組，另一種預測誤差獎勵。
- Stadie, Levine & Abbeel（2015），"Incentivizing exploration in reinforcement learning with deep predictive models"，[arXiv:1507.00814](https://arxiv.org/abs/1507.00814)——較早的、基於學到的預測模型的預測型探索獎勵。
- Houthooft 等人（2016），"VIME: Variational information maximizing exploration"，[arXiv:1605.09674](https://arxiv.org/abs/1605.09674)——資訊增益探索，是預測誤差獎勵的替代方案。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347)——RND 以兩個價值頭修改的策略梯度方法。
