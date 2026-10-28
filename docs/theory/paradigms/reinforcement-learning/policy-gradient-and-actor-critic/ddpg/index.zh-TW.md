---
translation_reviewed: 2026-10-28
---

# 深度確定性策略梯度（Lillicrap 等人，2016）

一種用於連續動作的離策略演員–評論家方法：以確定性的演員搭配深度 Q 函數評論家，並採用 DQN 式的回放與緩慢更新的目標網路。

## 問題

DQN 需要對離散的動作集合取最大值，連續動作時無法這樣做。策略梯度可以處理連續動作，但需要大量同策略樣本。Lillicrap 等人探討：能讓 DQN 從原始像素學習的想法，能否與確定性策略梯度結合，用於連續控制。

## 核心想法

演員 \(\mu(s \mid \theta^\mu)\) 直接輸出動作，不做取樣。評論家 \(Q(s, a \mid \theta^Q)\) 估計狀態–動作對的價值。演員沿著評論家對動作的梯度更新，這就是確定性策略梯度。評論家以由目標演員與目標評論家計算出的時序差分目標訓練，兩個目標網路都以小步幅的軟更新跟隨學習中的網路。轉移儲存在回放緩衝區中，並如 DQN 一樣以小批量抽樣。

## 方程式或演算法

依確定性策略梯度，演員的更新為

\[
\nabla_{\theta^\mu} J \approx \mathbb{E}_{s}\left[\nabla_a Q(s, a \mid \theta^Q)\big|_{a = \mu(s)}\, \nabla_{\theta^\mu} \mu(s \mid \theta^\mu)\right]
\]

評論家最小化平方損失 \(L = \frac{1}{N}\sum_i (y_i - Q(s_i, a_i \mid \theta^Q))^2\)，其中

\[
y_i = r_i + \gamma\, Q'\big(s_{i+1}, \mu'(s_{i+1} \mid \theta^{\mu'}) \mid \theta^{Q'}\big)
\]

目標網路以 \(\theta' \leftarrow \tau\theta + (1 - \tau)\theta'\) 更新，論文中 \(\tau = 0.001\)。回放緩衝區容納 \(10^6\) 筆轉移，低維狀態的小批量為 64，從像素學習時為 16。折扣 \(\gamma = 0.99\)。

## 結果

摘要指出，此演算法以同一套學習演算法、網路架構與超參數，「穩健地解決了超過 20 個模擬物理任務」。論文也報告，對許多任務而言，此方法能從原始像素端到端地學習策略。

## 限制

- **評論家高估。**評論家使用單一 Q 函數，可能如 DQN 一樣高估價值。[TD3](../td3/index.md) 直接處理此問題。
- **訓練脆弱。**學習依賴目標網路的更新速率、回放設計以及加在動作上的探索雜訊，且對這些設定很敏感。
- **確定性策略。**演員對每個狀態只輸出一個動作，因此探索必須從外部加入，策略本身也不表示不確定性。[SAC](../sac/index.md) 改用隨機演員。

## 連結

- 母頁：[策略梯度與演員–評論家](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- DDPG 是 [深度 Q 網路](../../deep-q-networks/index.md) 在連續動作上的對應方法，使用相同的回放與目標網路想法。
- 其後繼方法為修正高估的 [TD3](../td3/index.md)，以及使用隨機演員與熵正則化的 [SAC](../sac/index.md)。

## 應用

- **模擬機器人控制。**論文的物理任務是模擬機器人與運動問題，是連續控制方法的標準情境。
- **從像素學習。**論文報告的端到端結果（來自原始影像）顯示此方法不限於以狀態為基礎的控制。

## 未解問題

- 如何在不仔細手動調整雜訊與目標更新率的情況下，讓確定性演員–評論家方法保持穩定。
- 當演員是確定性的時，如何在連續控制中表示不確定性。

## 參考文獻

### 開創性論文

- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, [arXiv:1509.02971](https://arxiv.org/abs/1509.02971) — The DDPG paper, with the deterministic actor, the target networks and the physics results above.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The replay and target-network design that DDPG adapts to continuous actions.
- Silver et al. (2014), "Deterministic policy gradient algorithms", *Proceedings of ICML 2014*, PMLR 32, 387–395. https://proceedings.mlr.press/v32/silver14.html — The deterministic policy gradient theorem on which DDPG's actor update rests.
- Fujimoto, van Hoof & Meger (2018), "Addressing function approximation error in actor-critic methods", [arXiv:1802.09477](https://arxiv.org/abs/1802.09477) — TD3, a later method that corrects DDPG's overestimation.
- Haarnoja et al. (2018), "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor", [arXiv:1801.01290](https://arxiv.org/abs/1801.01290) — A stochastic successor to DDPG for continuous control.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on policy gradients and actor-critic methods.
