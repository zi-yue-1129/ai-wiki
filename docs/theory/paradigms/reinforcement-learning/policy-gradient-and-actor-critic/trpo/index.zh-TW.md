---
translation_reviewed: 2026-10-28
---

# 信賴區域策略最佳化（Schulman 等人，2015）

一種策略梯度方法，在限制新舊策略之間平均 KL 散度的條件下，最大化代理目標。

## 問題

過大的策略梯度步可能使策略崩潰，而用來估計收益的代理目標只在目前策略附近成立。Schulman 等人探討如何選擇一個有保證能依代理目標改進策略、並使新策略仍接近舊策略的更新。

## 核心想法

TRPO 最佳化期望回報的局部代理目標，該目標使用舊的狀態訪問頻率，以及新舊策略之間的機率比。代理目標只有在兩策略接近時才是良好估計，因此更新被限制在信賴區域內。限制條件是平均 KL 散度，而非論文認為過於嚴格、約束太多而不切實際的最大 KL 限制。

## 方程式或演算法

實際問題為

\[
\max_\theta\ L_{\theta_{\text{old}}}(\theta) \quad \text{subject to} \quad \bar{D}_{\text{KL}}(\theta_{\text{old}}, \theta) \le \delta
\]

其中 \(L\) 是代理目標，\(\bar{D}_{\text{KL}}\) 是在被訪問狀態上的平均 KL 散度。論文以重要性抽樣從樣本估計這兩個量。論文給出兩種抽樣方案：單路徑方法與 vine 方法。流程如下：

1. 以目前策略 \(\pi_{\theta_{\text{old}}}\) 收集軌跡。
2. 從這些樣本估計優勢或動作價值項。
3. 求解受限問題，得到在 KL 上界 \(\delta\) 內的更新。
4. 令 \(\theta_{\text{old}} \leftarrow \theta\)，然後重複。

論文在所有實驗中使用 \(\delta = 0.01\)。

## 結果

- **模擬的運動控制。**單路徑與 vine 版 TRPO 解決了全部三個 MuJoCo 任務（Swimmer、Hopper、Walker），論文報告它們在所比較的方法中給出最佳解。學習曲線是五次執行的平均。
- **Atari。**在七款遊戲上，論文表示 TRPO「只在部分遊戲上優於先前方法」，但「一貫達到合理的分數」。在 Q\*bert 上，TRPO-vine 得分 7732.5，深度 Q 學習為 1952，UCC-I 為 20025，顯示此方法並非每款遊戲都最好。每個結果只執行一次，因此 Atari 結果沒有誤差統計。

## 限制

- **實作複雜。**受限最佳化與取樣的 KL 估計，使此方法比裁剪目標更難實作與調參。
- **並非每款 Atari 遊戲都最佳。**論文自身的結果顯示，此方法不是每款遊戲都最好。
- **實務上已被取代。**[近端策略最佳化](../../proximal-policy-optimisation/index.md)保留了限制單步幅度的目標，但以裁剪目標取代硬性約束，實作更簡單。PPO 論文在實驗中與 TRPO 比較。

## 連結

- 母頁：[策略梯度與演員–評論家](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 它使用的優勢估計與 [A3C](../a3c/index.md) 中的相同。
- 後繼方法是 [PPO](../../proximal-policy-optimisation/index.md)；在 Atari 上的值函數比較對象是[深度 Q 網路](../../deep-q-networks/index.md)。

## 應用

- **模擬機器人運動。**MuJoCo 實驗是論文主要的連續控制證據。
- **從像素進行 Atari 控制。**七款遊戲的 Atari 研究顯示此方法對原始畫面輸入也適用。

## 未解問題

- 在控制實作細節後，是否真的需要硬性信賴區域，或較軟的懲罰已足夠。
- 對於論文以外的任務，應如何設定 KL 上界 \(\delta\)。

## 參考文獻

### 開創性論文

- Schulman, Levine, Moritz, Jordan & Abbeel (2015), "Trust region policy optimization", *Proceedings of the 31st International Conference on Machine Learning (ICML)*, arXiv:1502.05477 — The TRPO paper, with the surrogate, the KL constraint and the MuJoCo and Atari results above.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — The simpler clipped method that replaces the constraint.
- Schulman et al. (2016), "High-dimensional continuous control using generalized advantage estimation", arXiv:1506.02438 — Advantage estimation for the policy-gradient updates that trust-region methods rely on.
- Engstrom et al. (2020), "Implementation matters in deep policy gradients: a case study on PPO and TRPO", arXiv:2005.12729 — Shows that code-level details account for much of the gap between PPO and TRPO.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep value-based baseline on the Atari suite.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on policy-gradient methods and trust-region ideas in the standard textbook.
