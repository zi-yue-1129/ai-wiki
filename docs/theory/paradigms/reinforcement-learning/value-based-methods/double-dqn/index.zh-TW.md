---
translation_reviewed: 2026-10-28
---

# Double DQN（van Hasselt 等人，2016）

修改 DQN 的目標：由線上網路選擇動作，由目標網路評估該動作，減少最大值運算所帶來的高估。

## 問題

DQN 的目標對同一個網路的估計取最大值，既用來挑選動作，也用來為它打分。當估計含有雜訊時，最大值會向上偏誤。van Hasselt、Guez 與 Silver 指出，DQN 在他們測試的全部 49 款 Atari 遊戲中都高估了動作價值，而且這種高估可能損害表現。

## 核心想法

DQN 的目標本來就包含第二個網路，也就是緩慢更新的目標網路。Double DQN 以不同方式使用它：線上網路挑出貪婪的下一步動作，目標網路則為該動作打分。把選擇與評估分開，可以使最大值較不容易挑中正向雜訊。論文指出，這不需要額外的網路或參數，只增加極少的計算。

## 方程式或演算法

DQN 的目標為

\[
Y_t^{\text{DQN}} = R_{t+1} + \gamma \max_a Q(S_{t+1}, a; \theta^-_t)
\]

Double DQN 的目標為

\[
Y_t^{\text{DoubleDQN}} = R_{t+1} + \gamma\, Q\big(S_{t+1}, \arg\max_a Q(S_{t+1}, a; \theta_t); \theta^-_t\big)
\]

其中 \(\theta\) 為線上參數，\(\theta^-\) 為目標參數。DQN 訓練程序的其餘部分，包括回放與平方損失，維持不變，只有目標改變。

## 結果

論文在 49 款 Atari 遊戲上報告結果，評估方式與 DQN 相同：

- **人類標準化分數的中位數，無動作開場：**DQN 為 93.5%，Double DQN 為 114.7%。
- **平均值，無動作開場：**DQN 為 241.1%，Double DQN 為 330.3%。
- **中位數，人類開場：**DQN 為 47.5%，Double DQN 為 88.4%。

論文也直接測量高估程度，在每次 125,000 步的評估階段中取平均價值估計。

## 限制

- **高估被減輕，但未被消除。**分離後的目標降低了偏誤，但學到的價值仍可能不準確，論文也未提供一般性保證。
- **回放與自舉方式不變。**Double DQN 仍使用單步目標與均勻回放。優先回放（Schaul 等人，2016）與多步回報是另外的改進，後來合併於 Rainbow。
- **離散動作。**對動作取 argmax 仍需要有限的動作集合。

## 連結

- 母頁：[值函數方法](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 它修改的是[深度 Q 網路](../../deep-q-networks/index.md)的目標，它所處理的表格高估問題在[Q 學習](../q-learning/index.md)中討論。
- 它是 [Rainbow](../rainbow/index.md) 所合併的六項組件之一。

## 應用

- **Atari 基準智能體。**此方法在 Atari 2600 套件上評估，該套件成為值函數型智能體的標準測試環境（van Hasselt 等人，2016；Hessel 等人，2018）。

## 未解問題

- 雙估計器仍殘留多少偏誤，以及何時會造成傷害。
- 在動作空間連續、取 argmax 本身困難的情況下，分離選擇與評估是否仍有幫助。

## 參考文獻

### 開創性論文

- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", [arXiv:1509.06461](https://arxiv.org/abs/1509.06461) — The Double DQN paper, showing DQN's overestimation and the decoupled target.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The DQN paper whose target Double DQN modifies.
- Schaul, Quan, Antonoglou & Silver (2016), "Prioritized experience replay", [arXiv:1511.05952](https://arxiv.org/abs/1511.05952) — A separate DQN improvement that replays transitions by their learning potential.
- Hessel et al. (2018), "Rainbow: Combining improvements in deep reinforcement learning", [arXiv:1710.02298](https://arxiv.org/abs/1710.02298) — Combines Double DQN with five other DQN extensions.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on temporal-difference targets and maximisation bias in value learning.
