---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - TRPO
  - 信賴域策略最佳化
---

# 信賴域策略最佳化（Schulman 等人，2015）

一種策略梯度方法：在舊策略與新策略之間的平均 KL 散度受限的條件下，最大化一個替代目標。

## 問題

過大的策略梯度步伐可能使策略崩潰，而用來估計增益的替代目標只在目前策略附近有效。Schulman 等人探討：如何選擇一個更新，既能保證策略的改進與替代目標所預測的一致，又能讓新策略與舊策略保持接近。

## 核心想法

TRPO 最佳化期望回報的局部替代目標，它使用舊策略的狀態訪問頻率，以及新舊策略的機率比。替代目標只有在兩個策略接近時才是好的估計，因此更新被限制在一個信賴域內。此限制是平均 KL 散度的約束，而非更嚴格的最大 KL 約束；論文指出後者因約束過多而不切實際。

## 方程式與演算法

實際要解的問題為

\[
\max_\theta\ L_{\theta_{\text{old}}}(\theta) \quad \text{subject to} \quad \bar{D}_{\text{KL}}(\theta_{\text{old}}, \theta) \le \delta
\]

其中 \(L\) 是替代目標，\(\bar{D}_{\text{KL}}\) 是在被訪問狀態上的平均 KL 散度。論文以重要性抽樣從樣本估計這兩個量，並提供兩種抽樣方式：單一路徑（single-path）與藤蔓（vine）方法。流程如下：

1. 以目前策略 \(\pi_{\theta_{\text{old}}}\) 收集軌跡。
2. 由這些樣本估計優勢或動作價值項。
3. 解出受約束的問題，得到不超出 KL 界限 \(\delta\) 的更新。
4. 令 \(\theta_{\text{old}} \leftarrow \theta\)，然後重複。

論文所有實驗都使用 \(\delta = 0.01\)。

## 結果

- **模擬移動。** 論文在三個 MuJoCo 任務 Swimmer、Hopper 與 Walker 上訓練單一路徑與藤蔓 TRPO。學習曲線是每種演算法五次執行（隨機初始化）的平均。
- **Atari。** 在七款遊戲（Beam Rider、Breakout、Enduro、Pong、Q\*bert、Seaquest 與 Space Invaders）上，論文寫道：「雖然我們的方法只在部分遊戲上超越了先前方法，但它一致地取得了合理的分數。」以 Q\*bert 為例，TRPO-vine 得分 7732.5，深度 Q 學習為 1952，UCC-I 為 20025，顯示此方法並非在每款遊戲都最好。每款遊戲的 TRPO 執行都只進行一次，因此 Atari 結果沒有誤差統計。

## 限制

- **實作複雜。** 受約束的最佳化與取樣得到的 KL 估計，使此方法比截斷式目標更難實作與調整。
- **並非每款 Atari 遊戲都最佳。** 論文自身的結果顯示，此方法不是在每款遊戲上都最好。
- **實務上已被取代。** [近端策略最佳化](../../proximal-policy-optimisation/index.zh-TW.md)保留了「限制每一步幅度」的目標，但以截斷式目標取代硬約束，實作較簡單。PPO 論文的實驗中與 TRPO 進行了比較。

## 關聯

- 上層主題：[策略梯度與演員–評論家](../index.zh-TW.md)，以及更廣的[強化學習](../../index.zh-TW.md)概觀。
- 它使用的優勢估計與 [A3C](../a3c/index.zh-TW.md) 中的相同。
- 後繼方法是 [PPO](../../proximal-policy-optimisation/index.zh-TW.md)；在 Atari 上與之比較的基於價值方法是[深度 Q 網路](../../deep-q-networks/index.zh-TW.md)。

## 應用

- **模擬機器人移動。** MuJoCo 實驗是論文主要的連續控制證據。
- **從像素進行的 Atari 控制。** 七款遊戲的 Atari 研究展示了此方法在原始畫面輸入上的表現。

## 未解問題

- 在實作細節受控之後，是否真的需要硬性的信賴域，還是較軟的懲罰項就已足夠。
- 對於論文以外的任務，KL 界限 \(\delta\) 應如何設定。

## 參考文獻

### 開創性論文

- Schulman、Levine、Moritz、Jordan 與 Abbeel（2015），"Trust region policy optimization"，*Proceedings of the 31st International Conference on Machine Learning (ICML)*，[arXiv:1502.05477](https://arxiv.org/abs/1502.05477) — TRPO 原始論文，包含替代目標、KL 約束以及上述 MuJoCo 與 Atari 結果。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — 以較簡單的截斷式方法取代約束的後續方法。
- Schulman 等人（2016），"High-dimensional continuous control using generalized advantage estimation"，[arXiv:1506.02438](https://arxiv.org/abs/1506.02438) — 信賴域方法所依賴的策略梯度更新中的優勢估計。
- Engstrom 等人（2020），"Implementation matters in deep policy gradients: a case study on PPO and TRPO"，[arXiv:2005.12729](https://arxiv.org/abs/2005.12729) — 指出程式碼層級的實作細節會強烈影響 PPO 與 TRPO 的比較。
- Mnih 等人（2015），"Human-level control through deep reinforcement learning"，*Nature* 518, 529–533。https://doi.org/10.1038/nature14236 — Atari 測試組上的深度基於價值基準。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*，第 2 版。MIT Press, 2018。http://incompleteideas.net/book/the-book-2nd.html — 標準教科書中策略梯度方法與信賴域概念的背景知識。
