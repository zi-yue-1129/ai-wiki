---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - DDPG
  - 深度確定性策略梯度
---

# 深度確定性策略梯度（Lillicrap 等人，2016）

一種用於連續動作的離策略演員–評論家方法：以確定性的演員搭配深度 Q 函數評論家，並採用 DQN 式的回放與緩慢更新的目標網路。

## 問題

DQN 需要對離散的動作集合取最大值，連續動作時無法這樣做。策略梯度可以處理連續動作，但需要大量同策略樣本。Lillicrap 等人探討：能讓 DQN 從原始像素學習的想法，能否與確定性策略梯度結合，用於連續控制。

## 核心想法

演員 \(\mu(s \mid \theta^\mu)\) 直接輸出動作，不做取樣。評論家 \(Q(s, a \mid \theta^Q)\) 估計狀態–動作對的價值。演員沿著評論家對動作的梯度更新，這就是確定性策略梯度。評論家則以目標演員與目標評論家計算的時序差分目標訓練，兩個目標網路以很小的軟更新跟隨學習中的網路。轉換資料存入回放緩衝區，並像 DQN 一樣以小批次抽樣。

## 方程式與演算法

以確定性策略梯度表示，演員的更新為

\[
\nabla_{\theta^\mu} J \approx \mathbb{E}_{s}\left[\nabla_a Q(s, a \mid \theta^Q)\big|_{a = \mu(s)}\, \nabla_{\theta^\mu} \mu(s \mid \theta^\mu)\right]
\]

評論家最小化平方損失 \(L = \frac{1}{N}\sum_i (y_i - Q(s_i, a_i \mid \theta^Q))^2\)，其中

\[
y_i = r_i + \gamma\, Q'\big(s_{i+1}, \mu'(s_{i+1} \mid \theta^{\mu'}) \mid \theta^{Q'}\big)
\]

目標網路以 \(\theta' \leftarrow \tau\theta + (1 - \tau)\theta'\) 更新，論文中 \(\tau = 0.001\)。回放緩衝區保存 \(10^6\) 筆轉換；低維狀態的小批次大小為 64，從像素學習時為 16。折扣因子為 \(\gamma = 0.99\)。

## 結果

摘要指出，此演算法能以同一套學習演算法、同一種架構與同一組超參數，「穩健地解決超過 20 個模擬物理任務」。論文也指出，在許多任務上，此方法能直接從原始像素輸入端到端地學習策略。

## 限制

- **評論家高估。** 評論家只使用單一 Q 函數，可能像 DQN 一樣高估價值。[TD3](../td3/index.zh-TW.md)直接處理這個問題。
- **訓練脆弱。** 學習依賴目標網路的更新速率、回放設計與加在動作上的探索噪聲，對這些設定相當敏感。
- **確定性策略。** 演員對每個狀態只輸出一個動作，因此探索必須從外部加入，而策略本身無法表示不確定性。[SAC](../sac/index.zh-TW.md)改用隨機演員。

## 關聯

- 上層主題：[策略梯度與演員–評論家](../index.md)，以及更廣的[強化學習](../../index.zh-TW.md)概觀。
- DDPG 是[深度 Q 網路](../../deep-q-networks/index.zh-TW.md)在連續動作上的對應方法，使用相同的回放與目標網路概念。
- 它的後繼方法包括修正高估問題的 [TD3](../td3/index.zh-TW.md)，以及使用帶熵正則化的隨機演員的 [SAC](../sac/index.zh-TW.md)。

## 應用

- **模擬機器人控制。** 論文的物理任務是模擬的機器人與移動問題，也是連續控制方法的標準設定。
- **從像素學習。** 報告中從原始影像端到端學習的結果，顯示此方法不限於以狀態為輸入的控制。

## 未解問題

- 如何在不仔細手動調整噪聲與目標更新速率的情況下，讓確定性的演員–評論家方法保持穩定。
- 當演員是確定性的時，如何在連續控制中表示不確定性。

## 參考文獻

### 開創性論文

- Lillicrap 等人（2016），"Continuous control with deep reinforcement learning"，ICLR，[arXiv:1509.02971](https://arxiv.org/abs/1509.02971) — DDPG 論文，包含確定性演員、目標網路與上述物理任務結果。
- Mnih 等人（2015），"Human-level control through deep reinforcement learning"，*Nature* 518, 529–533。https://doi.org/10.1038/nature14236 — DDPG 所調整至連續動作的回放與目標網路設計。
- Silver 等人（2014），"Deterministic policy gradient algorithms"，*Proceedings of ICML 2014*，PMLR 32, 387–395。https://proceedings.mlr.press/v32/silver14.html — DDPG 演員更新所依據的確定性策略梯度定理。
- Fujimoto、van Hoof 與 Meger（2018），"Addressing function approximation error in actor-critic methods"，[arXiv:1802.09477](https://arxiv.org/abs/1802.09477) — TD3，修正 DDPG 高估問題的後續方法。
- Haarnoja 等人（2018），"Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor"，[arXiv:1801.01290](https://arxiv.org/abs/1801.01290) — DDPG 在連續控制上的隨機後繼方法。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*，第 2 版。MIT Press, 2018。http://incompleteideas.net/book/the-book-2nd.html — 策略梯度與演員–評論家方法的背景知識。
