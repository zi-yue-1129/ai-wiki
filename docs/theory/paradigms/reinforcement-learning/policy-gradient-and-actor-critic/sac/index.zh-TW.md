---
translation_reviewed: 2026-10-28
---

# 軟演員–評論家（Haarnoja 等人，2018）

一種用於連續控制的離策略演員–評論家方法，最大化獎勵加上策略熵，使用隨機演員與兩個 Q 函數。

## 問題

像 DDPG 這類離策略確定性方法很脆弱，而像 PPO 這類同策略方法需要大量樣本。Haarnoja 等人探討：離策略演員–評論家能否同時穩定且樣本有效率，以及在獎勵之外同時最大化熵，能否讓探索與穩健性更容易。

## 核心想法

目標函數在每一步的期望獎勵上加入策略熵，並以溫度 \(\alpha\) 決定兩者的權衡。由此得到的軟價值函數 \(V(s) = \mathbb{E}_{a}[Q(s,a) - \log \pi(a \mid s)]\) 會推動策略盡可能保持獎勵允許的隨機性。演員是隨機的，並透過重參數化技巧訓練，使其取樣的動作可微分。訓練兩個 Q 函數，並以兩者的最小值計算價值與策略梯度，與 TD3 一樣可限制高估。

## 方程式或演算法

最大熵目標為

\[
J(\pi) = \sum_t \mathbb{E}\left[r(s_t, a_t) + \alpha\, \mathcal{H}\big(\pi(\cdot \mid s_t)\big)\right]
\]

軟 Q 目標為 \(\hat{Q}(s_t, a_t) = r(s_t, a_t) + \gamma\, \mathbb{E}\big[V_{\bar{\psi}}(s_{t+1})\big]\)，其中 \(\bar{\psi}\) 是目標價值網路的權重。策略以最小化 KL 散度更新；若以重參數化的動作 \(a_t = f_\phi(\epsilon; s_t)\) 表示，此目標為 \(\mathbb{E}\big[\log \pi_\phi(f_\phi(\epsilon; s_t) \mid s_t) - Q_\theta(s_t, f_\phi(\epsilon; s_t))\big]\)。目標價值網路以軟更新率 \(\tau\) 更新。流程如下：

1. 以隨機策略收集轉移，並儲存於回放緩衝區。
2. 取樣小批量，以目標價值網路計算軟 Q 目標，並更新兩個 Q 函數。
3. 以兩個 Q 函數的最小值更新價值網路與策略。
4. 以速率 \(\tau\) 更新目標價值網路，然後重複。

在論文研究的版本中，溫度 \(\alpha\) 是固定的，而獎勵尺度是唯一需要調整的超參數。

## 結果

論文指出，SAC「以相當大的差距超越先前最先進的離策略深度強化學習方法」，並顯示其在效能與樣本效率上「相較於離策略與同策略的先前方法都有實質改進」。在較困難的 Gym MuJoCo 任務（Hopper、Walker2d、HalfCheetah、Ant 與 Humanoid）上，它以大幅差距超越 DDPG、PPO、軟 Q 學習與 TD3，而 DDPG 在 Ant 與 Humanoid 上無法取得進展。結果為五個隨機種子的平均，作者報告不同種子之間的表現非常接近。

## 限制

- **溫度敏感。**效能取決於獎勵尺度，它在此版本中決定了實際的熵權重。後續工作會自動學習 \(\alpha\)；本論文不包含該步驟。
- **兩個評論家與隨機演員。**此方法比 DDPG 多了網路，每次更新的計算量較大。
- **連續動作。**此方法針對連續控制設計，論文的結果來自模擬的運動任務。

## 連結

- 母頁：[策略梯度與演員–評論家](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 其確定性前身是 [DDPG](../ddpg/index.md)，其高估修正與 [TD3](../td3/index.md) 的想法相通。
- 它是離策略方法，與同策略的 [PPO](../../proximal-policy-optimisation/index.md) 形成對比。

## 應用

- **模擬機器人運動。**論文中的 MuJoCo 任務是報告的應用，此方法也是連續控制的標準基線。

## 未解問題

- 如何在獎勵尺度不同的任務間，自動調整或學習溫度。
- 此方法在真實機器人上的表現，論文尚未測試。

## 參考文獻

### 開創性論文

- Haarnoja, Zhou, Abbeel & Levine (2018), "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor", arXiv:1801.01290 — The SAC paper, with the maximum-entropy objective and the MuJoCo results above.
- Fujimoto, van Hoof & Meger (2018), "Addressing function approximation error in actor-critic methods", arXiv:1802.09477 — TD3, which uses the same two-critic minimum against overestimation.
- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, arXiv:1509.02971 — DDPG, the deterministic off-policy baseline that SAC outperforms.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — The on-policy baseline in the SAC comparison.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on actor-critic methods and the value functions used by SAC.
