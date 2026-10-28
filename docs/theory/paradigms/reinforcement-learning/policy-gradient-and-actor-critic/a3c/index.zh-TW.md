---
translation_reviewed: 2026-10-28
---

# 異步優勢演員–評論家（Mnih 等人，2016）

多個平行的執行者（actor-learner）在 CPU 執行緒上共享同一個網路並異步更新，使它們的資料彼此去相關，因此不需要回放緩衝區。

## 問題

DQN 式的智能體需要回放緩衝區，而且在論文所報告的設定中，需要以 GPU 訓練多日。以相關性很高的連續資料學習的策略梯度方法，常常不穩定。Mnih 等人探討：平行的異步執行者能否在不使用回放的情況下，自行穩定線上的演員–評論家學習。

## 核心想法

多個工作者各自執行一份環境，並以共享的策略行動。每個工作者收集自己的少量經驗，從中計算梯度，並在不等待其他工作者的情況下，將梯度套用到共享參數上。由於任一時刻各工作者處於不同的狀態，它們的更新比單一智能體連續步驟的更新更不相關。更新使用優勢，即 \(n\) 步回報減去價值估計，並加入熵項以維持策略的探索性。

## 方程式或演算法

對一個工作者，若自上次更新以來經過 \(k\) 步（\(k\) 至多為 \(t_{\max}\)），梯度為

\[
\nabla_{\theta'} \log \pi(a_t \mid s_t; \theta')\,\big(R_t - V(s_t; \theta_v)\big) + \beta\, \nabla_{\theta'} H\big(\pi(s_t; \theta')\big)
\]

其中 \(R_t\) 是折現的 \(n\) 步回報，\(H\) 是策略熵。每個工作者的流程：

1. 複製共享參數。
2. 行動最多 \(t_{\max}\) 步，或直到回合結束。
3. 以最後一個狀態的價值估計自舉計算 \(R\)；若回合已結束，則從零開始。
4. 由後往前逐步累積上述梯度。
5. 將累積梯度異步套用到共享參數上，然後重複。

Atari 實驗使用 \(t_{\max} = 5\) 與熵權重 \(\beta = 0.01\)。

## 結果

論文報告 Atari 上的人類標準化結果（表 1）。其前饋式 A3C 智能體在 CPU 上訓練 4 天，平均為 496.8%，中位數為 116.6%。LSTM 版本的平均為 623.0%，中位數為 112.6%。以 GPU 訓練 8 天的對決 DDQN，平均為 343.8%，中位數為 117.1%。摘要指出，A3C 在單一多核心 CPU、不使用 GPU 的情況下，以一半的訓練時間超越了 Atari 上的最先進方法。優勢在平均值上最明顯，中位數則相近。

論文還報告了 TORCS 賽車結果：A3C 在約 12 小時內達到人類測試者分數的約 75% 至 90%。在連續的 MuJoCo 任務上，它在不到 24 小時內找到良好解；在隨機生成的 3D 迷宮中，它能從視覺輸入學到合理的探索策略。

## 限制

- **沒有回放，因此樣本重複利用有限。**每筆經驗只用於一次更新，以樣本效率換取平行的吞吐量。
- **參數過時。**異步更新是根據可能已被其他工作者改變的參數計算的。
- **同步變體。**之後的同步基線 A2C 被用作 PPO 論文中的比較對象（Schulman 等人，2017），該論文報告 PPO 在 Atari 上的樣本複雜度優於 A2C。

## 連結

- 母頁：[策略梯度與演員–評論家](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 其優勢形式承襲 [REINFORCE](../reinforce/index.md)，並加入學習得到的基線。[近端策略最佳化](../../proximal-policy-optimisation/index.md)是之後同樣建立在優勢概念上的策略梯度方法。
- 以回放為基礎的替代方案是[深度 Q 網路](../../deep-q-networks/index.md)。

## 應用

- **Atari 與 3D 導航。**論文的實驗涵蓋 Atari 與來自視覺輸入的隨機 3D 迷宮，是測試此方法的基準。
- **機器人與模擬控制。**MuJoCo 的結果顯示此方法在連續控制上的表現。

## 未解問題

- 一旦使用同步的硬體，異步加速是否仍值得其參數過時的代價。
- 如何在不同任務之間調整熵權重。

## 參考文獻

### 開創性論文

- Mnih et al. (2016), "Asynchronous methods for deep reinforcement learning", arXiv:1602.01783 — The A3C paper, with the parallel actor-learner design and the Atari results reported above.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The replay-based deep value method that A3C is compared against.
- Schulman et al. (2016), "High-dimensional continuous control using generalized advantage estimation", arXiv:1506.02438 — Advantage estimation used in the same family of actor-critic methods.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — Reports the A2C comparison and the sample-complexity results against which A3C-style methods are measured.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Actor-critic methods and the role of advantages in the standard textbook.
