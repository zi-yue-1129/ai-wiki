---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - A3C
  - 異步優勢演員–評論家
---

# 異步優勢演員–評論家（Mnih 等人，2016）

數個平行的行動者–學習者（actor-learner）在 CPU 執行緒上共用同一個網路，並以非同步方式更新它。由於各執行緒同時處於不同狀態，它們的資料彼此相關性較低，因此不需要經驗回放緩衝區。

## 問題

DQN 式的智能體需要經驗回放緩衝區，而在論文所報告的設定中，還需要以 GPU 訓練許多天。使用連續而彼此相關資料學習的策略梯度方法，往往不穩定。Mnih 等人提出的問題是：不使用回放，非同步的平行行動者能否單靠自己穩定線上的演員–評論家學習。

## 核心想法

多個工作者各自持有一份環境副本，並以共用的策略行動。每個工作者收集自己的幾步經驗，據此計算梯度，然後套用到共用參數上，不必等待其他工作者。由於任一時刻各工作者處於不同狀態，它們的更新比同一個智能體連續的步驟更不相關。更新使用**優勢（advantage）**，即 \(n\) 步回報減去價值估計；此外還加入熵項，使策略保持探索性。

## 方程式與演算法

對某個工作者而言，自上次更新後最多 \(t_{\max}\) 步，梯度為

\[
\nabla_{\theta'} \log \pi(a_t \mid s_t; \theta')\,\big(R_t - V(s_t; \theta_v)\big) + \beta\, \nabla_{\theta'} H\big(\pi(s_t; \theta')\big)
\]

其中 \(R_t\) 是折扣後的 \(n\) 步回報，\(H\) 是策略的熵。每個工作者的流程如下：

1. 複製共用參數。
2. 行動最多 \(t_{\max}\) 步，或直到回合結束。
3. 計算 \(R\)：若回合未結束，從最後狀態的價值估計自舉；若已結束，則設為零。
4. 由後往前走過各步，累積上式的梯度。
5. 非同步地把累積的梯度套用到共用參數，然後重複。

Atari 實驗使用 \(t_{\max} = 5\)，熵權重 \(\beta = 0.01\)。

## 結果

論文報告了 Atari 上的人類標準化結果（表 1）。其前饋式 A3C 智能體在 CPU 上訓練 4 天，平均為 496.8%，中位數為 116.6%。LSTM 版本的平均為 623.0%，中位數為 112.6%。以 GPU 訓練 8 天的 Dueling DDQN，平均為 343.8%，中位數為 117.1%。摘要指出，A3C 在單一多核心 CPU、不使用 GPU 的情況下，以一半的訓練時間超越了 Atari 上的最先進方法。優勢在平均值上最明顯，中位數則相近。

論文也報告了 TORCS 駕駛的結果：在四種 TORCS 設定上，A3C 達到人類測試者分數的約 75% 至 90%。在連續的 MuJoCo 任務上，它在不到 24 小時內找到良好的解；對於從視覺輸入的隨機三維迷宮，它學會了合理的探索策略。

## 限制

- **沒有回放，樣本重用有限。** 每筆經驗只用於一次更新，以樣本效率換取平行的吞吐量。
- **參數過時。** 非同步更新所用的參數，在套用時可能已經改變。
- **同步變體。** 後來的同步基線 A2C，被 PPO 論文（Schulman 等人，2017）用作比較對象；該論文報告，在 Atari 上 PPO 的樣本複雜度優於 A2C。

## 關聯

- 上層主題：[策略梯度與演員–評論家](../index.zh-TW.md)，以及更廣的[強化學習](../../index.zh-TW.md)概觀。
- 優勢概念承接自[REINFORCE](../reinforce/index.zh-TW.md)並加上學習得到的基線。[近端策略最佳化](../../proximal-policy-optimisation/index.zh-TW.md)是較晚出現、建立在相同優勢概念上的策略梯度方法。
- 以回放為基礎的替代方案是[深度 Q 網路](../../deep-q-networks/index.zh-TW.md)。

## 應用

- **Atari 與三維導航。** 論文的實驗涵蓋 Atari 與從視覺輸入的隨機三維迷宮，這些是用來測試此方法的基準。
- **機器人與模擬控制。** MuJoCo 的結果展示了此方法在連續控制上的表現。

## 未解問題

- 在使用同步硬體後，非同步加速是否仍值得付出過時更新的代價。
- 熵權重應如何針對不同任務調整。

## 參考文獻

### 開創性論文

- Mnih 等人（2016），"Asynchronous methods for deep reinforcement learning"，[arXiv:1602.01783](https://arxiv.org/abs/1602.01783) — A3C 論文，包含平行行動者–學習者的設計與上述 Atari 結果。
- Mnih 等人（2015），"Human-level control through deep reinforcement learning"，*Nature* 518, 529–533。https://doi.org/10.1038/nature14236 — A3C 所比較的、以回放為基礎的深度價值方法。
- Schulman 等人（2016），"High-dimensional continuous control using generalized advantage estimation"，[arXiv:1506.02438](https://arxiv.org/abs/1506.02438) — 同類演員–評論家方法所使用的優勢估計。
- Schulman 等人（2017），"Proximal policy optimization algorithms"，[arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — 報告與 A2C 的比較及樣本複雜度結果，是 A3C 類方法常被衡量的標準。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 第 2 版。MIT Press, 2018。http://incompleteideas.net/book/the-book-2nd.html — 標準教科書，介紹演員–評論家方法與優勢的角色。
