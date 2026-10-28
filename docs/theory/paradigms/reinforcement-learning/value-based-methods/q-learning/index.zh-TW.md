---
translation_reviewed: 2026-10-28
---

# Q 學習（Watkins 與 Dayan，1992）

一種離策略的時序差分方法，從取樣得到的轉移中學出最佳動作價值，不需要環境模型。

## 問題

若智能體不知道轉移機率，就必須從經驗中學出每個狀態下哪個動作最好。動態規劃需要模型，蒙地卡羅方法則必須等待整段回合結束。問題是：如何在每一步之後更新，從取樣經驗中學出最佳動作價值。

## 核心想法

保存一張動作價值表 \(Q(x, a)\)。在狀態 \(x\)、動作 \(a\)、獎勵 \(r\) 與下一狀態 \(y\) 之後，把 \(Q(x, a)\) 朝 \(r + \gamma \max_b Q(y, b)\) 移動。目標使用下一狀態的貪婪最大值，不論智能體實際下一步選了哪個動作。因此即使智能體以不同策略探索，學到的價值仍描述最佳策略。

## 方程式或演算法

Watkins 與 Dayan 以依訪問次數而定的學習因子 \(\alpha_n\) 寫出更新式：

\[
Q_n(x,a) = (1 - \alpha_n)\, Q_{n-1}(x,a) + \alpha_n \left[ r_n + \gamma \max_b Q_{n-1}(y_n, b) \right]
\]

此式適用於第 \(n\) 步被訪問的組合 \((x, a)\)，其他組合不變。流程如下：

1. 初始化所有組合的 \(Q(s, a)\)。
2. 從狀態 \(s\) 開始一個回合。
3. 以探索規則（如基於 \(Q\) 的 ε-貪婪）從 \(s\) 選擇 \(a\)。
4. 執行 \(a\)，觀察 \(r\) 與下一狀態 \(s'\)。
5. 更新 \(Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{b} Q(s', b) - Q(s, a) \right]\)。
6. 令 \(s \leftarrow s'\)，直到回合結束為止。

**收斂性。**Watkins 與 Dayan 證明，若每個狀態–動作組合都被無限次訪問、獎勵有界、\(0 \le \alpha_n < 1\) 且每個組合的學習率滿足 \(\sum_n \alpha_n = \infty\)、\(\sum_n \alpha_n^2 < \infty\)，並且 \(0 < \gamma < 1\)，則 \(Q_n\) 以機率一收斂到 \(Q^*\)。Tsitsiklis（1994）以非同步隨機逼近證明了同樣的收斂性。

## 結果

Watkins 與 Dayan 的貢獻是收斂定理，而非實證基準。其實用範圍來自函數近似。深度 Q 網路以神經網路套用相同的最大值目標，並在許多 Atari 遊戲上達到人類水準（Mnih 等人，2015）。

## 限制

- **表格形式。**對大型或連續的空間，為每個狀態–動作組合保存一格並不實際。
- **最大化偏誤。**對含雜訊的估計取最大值，往往高估價值。Double DQN 論文報告，DQN 在所有 49 款測試的 Atari 遊戲中都有高估（van Hasselt 等人，2016）。
- **收斂條件。**保證需要每個組合被無限次訪問，以及特定的學習率排程。這兩個假設在實務中都可能不成立；使用函數近似時，保證已不再適用。

## 連結

- 母頁：[值函數方法](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 深度版本是[深度 Q 網路](../../deep-q-networks/index.md)，高估問題的修正是 [Double DQN](../double-dqn/index.md)。
- 同策略的對應方法是 [SARSA](../sarsa/index.md)，它學習的是智能體實際遵循之策略的價值。
- 更新中使用的時序差分誤差，與母頁所討論的多巴胺訊號有關。

## 應用

- **教學與小型離散問題**，例如格子世界，表格小到可以完整保存。Sutton 與 Barto（2018）在時序差分相關章節中大量使用這類例子。

## 未解問題

- 在函數近似與離策略資料下的穩定學習，其收斂保證並不延續。
- 在含雜訊的環境中得到可靠的價值估計，同時避免高估偏誤。

## 參考文獻

### 開創性論文

- Watkins & Dayan (1992), "Q-learning", *Machine Learning* 8(3–4), 279–292. https://doi.org/10.1007/bf00992698 — The paper that defines Q-learning and proves its convergence to optimal action values.
- Tsitsiklis (1994), "Asynchronous stochastic approximation and Q-learning", *Machine Learning* 16(3), 185–202. https://doi.org/10.1007/bf00993306 — Proves convergence of Q-learning through asynchronous stochastic approximation.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep version of Q-learning, with replay and a target network.
- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", [arXiv:1509.06461](https://arxiv.org/abs/1509.06461) — Shows that DQN overestimates action values and reduces the bias.
- Mnih et al. (2013), "Playing Atari with deep reinforcement learning", [arXiv:1312.5602](https://arxiv.org/abs/1312.5602) — Early preprint that applied a Q-learning-based network to raw Atari frames.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Covers tabular Q-learning in its temporal-difference chapter, with the convergence context.
