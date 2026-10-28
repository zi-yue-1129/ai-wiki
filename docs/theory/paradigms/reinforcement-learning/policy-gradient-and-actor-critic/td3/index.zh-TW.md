---
translation_reviewed: 2026-10-28
---

# 雙延遲深度確定性策略梯度（Fujimoto 等人，2018）

DDPG 的變體：以兩個 Q 函數修正評論家的高估，讓演員的更新頻率低於評論家，並以雜訊平滑目標動作。

## 問題

Fujimoto、van Hoof 與 Meger 指出，DDPG 的評論家會高估動作價值，而且演員依循的是評論家當前不準確的估計，因此誤差會在策略更新中累積。他們的問題是：如何在保留 DDPG 確定性演員的前提下，減少演員–評論家方法中的函數近似誤差。

## 核心想法

TD3 以三種方式修改 DDPG：

1. **截斷的雙 Q 學習。**訓練兩個評論家，目標使用兩者估計中較小的那一個，以限制高估。
2. **延遲的策略更新。**演員與目標網路的更新頻率低於評論家，此處為每兩次評論家更新一次，使策略追逐較準確的價值。
3. **目標策略平滑。**在目標動作上加入截斷的雜訊，使價值目標平均於一小段動作區域，無法利用評論家上的尖峰。

## 方程式或演算法

TD3 的目標為

\[
y = r + \gamma \min_{i=1,2} Q_{\theta'_i}\big(s', \pi_{\phi'}(s') + \epsilon\big), \qquad \epsilon \sim \text{clip}\big(\mathcal{N}(0, \sigma), -c, c\big)
\]

論文使用策略延遲 \(d = 2\)、目標雜訊標準差 \(\sigma = 0.2\)、雜訊截斷 \(c = 0.5\)，以及軟目標更新率 \(\tau = 0.005\)。每一步的流程：

1. 從回放緩衝區取樣一個小批量。
2. 以目標演員計算平滑後的目標動作，並形成截斷雙 Q 目標 \(y\)。
3. 讓兩個評論家都朝 \(y\) 更新。
4. 每 \(d\) 步，以第一個評論家的梯度更新演員，然後更新目標網路。

## 結果

論文在七個 OpenAI Gym MuJoCo 任務上評估，結果為十次執行、每次一百萬個時間步的平均。摘要指出，此方法在每個測試環境中都超越了當時的最先進方法。表 1 列出 TD3、DDPG 與 PPO 的最大平均回報：

| 環境 | TD3 | DDPG | PPO |
|---|---|---|---|
| HalfCheetah | 9636.95 | 3305.60 | 1795.43 |
| Hopper | 3564.07 | 2020.46 | 2164.70 |
| Walker2d | 4682.82 | 1843.85 | 3317.69 |
| Ant | 4372.44 | 1005.30 | 1083.20 |
| Reacher | −3.60 | −6.51 | −6.18 |
| InvertedPendulum | 1000.00 | 1000.00 | 1000.00 |
| InvertedDoublePendulum | 9337.47 | 9355.52 | 8977.94 |

此表為論文原始數值。在 InvertedDoublePendulum 上，DDPG 略高於 TD3，因此「每個環境都更好」的說法在該任務上不成立。

## 限制

- **評估範圍。**主要結果在連續的 MuJoCo 控制上，任務數固定為七個，論文未測試離散動作或像素輸入。
- **確定性探索。**演員是確定性的，因此探索依賴加在動作上的雜訊，與 DDPG 相同。
- **額外超參數。**策略延遲、目標雜訊與雜訊截斷是論文新增的設定，結果依賴這些數值。

## 連結

- 母頁：[策略梯度與演員–評論家](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- TD3 建立在 [DDPG](../ddpg/index.md) 之上；其雙 Q 的想法呼應離散動作中修正高估的 [Double DQN](../../value-based-methods/double-dqn/index.md)。
- 同樣處理高估問題的隨機替代方案是 [SAC](../sac/index.md)。

## 應用

- **模擬運動控制。**MuJoCo 基準任務（如 Hopper、Walker2d 與 Ant）是論文的主要應用。

## 未解問題

- 這三項修正對於隨機或維度極高的動作是否仍是正確的選擇。
- 穩定性的提升能否從模擬運動延伸到真實機器人。

## 參考文獻

### 開創性論文

- Fujimoto, van Hoof & Meger (2018), "Addressing function approximation error in actor-critic methods", *Proceedings of ICML 2018*, arXiv:1802.09477 — The TD3 paper, with the three changes and the MuJoCo comparison above.
- Lillicrap et al. (2016), "Continuous control with deep reinforcement learning", ICLR, arXiv:1509.02971 — DDPG, the deterministic method that TD3 modifies.
- Haarnoja et al. (2018), "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor", arXiv:1801.01290 — A stochastic actor-critic method compared against the same family.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — The on-policy baseline in the TD3 MuJoCo comparison.
- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", arXiv:1509.06461 — Double Q-learning in discrete actions, the origin of the clipped double-Q idea.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on actor-critic methods and overestimation in value learning.
