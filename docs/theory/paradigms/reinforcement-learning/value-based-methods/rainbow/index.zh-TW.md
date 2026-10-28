---
translation_reviewed: 2026-10-28
---

# Rainbow（Hessel 等人，2018）

把 DQN 的六項獨立改進整合成單一學習者的智能體，並在 Atari 2600 基準上報告了最先進的表現。

## 問題

到了 2018 年，DQN 的許多擴充各自修正一項弱點：高估、均勻回放、價值函數的形式、單步目標、回報分布的建模，以及以 ε-貪婪進行探索。這些改進通常各自單獨測試。Hessel 等人想知道它們組合起來的效果如何，以及一起使用時哪些最重要。

## 核心想法

Rainbow 以 DQN 智能體為基礎，整合六項組件，每一類各取一項：

- **Double Q 學習**把動作選擇與評估分開，以減少高估（van Hasselt 等人，2016）。
- **優先回放**較常抽樣學習潛力高的轉移（Schaul 等人，2016）。
- **對決網路（dueling networks）**把網路分成價值分支與優勢分支，兩者共享編碼器。
- **多步學習**以 n 步回報自舉，而非單步目標。
- **分布式強化學習**使用 51 個原子建模完整的回報分布，而不只是其平均值。
- **雜訊網路**在線性層中加入可學習的雜訊，以取代 ε-貪婪進行探索。

論文也把這些組件合併為單一學習程序，這正是它成為單一智能體、而非一組各自獨立修正的原因。

## 方程式或演算法

Rainbow 保留 DQN 的回放、目標網路與小批量更新結構，並改動上述各部分。輸出是 51 個原子上的回報分布；多步組件使用 \(n = 3\)，論文比較 \(n = 1, 3, 5\) 後發現此值表現最好。完整的損失函數、虛擬碼與超參數表請參閱論文，實作時應以原文為準。

## 結果

在論文評估的 57 款 Atari 遊戲中：

- **人類標準化分數的中位數，無動作開場：**Rainbow 為 223%。
- **人類標準化分數的中位數，人類開場：**Rainbow 為 153%。
- **最佳單一組件：**分布式 DQN 在無動作開場下為 164%，對決 DDQN 為 151%，優先 DDQN 為 140%。在人類開場下，優先 DDQN 為最佳單一組件，達 128%。

消融研究發現，優先回放與多步學習是最重要的兩個組件，分布式學習緊隨其後。

## 限制

- **複雜度。**合併後的智能體有許多互相作用的部分，使結果較難歸因與重現。
- **離散動作。**此方法針對有限動作集合的 Atari 設定而設計。
- **結果範圍。**結果來自 Atari 遊戲，論文並未顯示同樣的組合適用於連續控制。

## 連結

- 母頁：[值函數方法](../index.md)，以及更大範圍的[強化學習](../../index.md)總覽。
- 它把 [Double DQN](../double-dqn/index.md) 與 [深度 Q 網路](../../deep-q-networks/index.md) 基礎智能體結合。
- 優先回放在[經驗回放](../../experience-replay/index.md)頁面中討論。
- 以雜訊網路進行探索，與[探索](../../exploration/index.md)頁面所談的「促使智能體嘗試新動作」主題相關。

## 應用

- **Atari 基準。**Rainbow 是 Atari 2600 套件上值函數型智能體的參考點（Hessel 等人，2018）。

## 未解問題

- 在更大規模訓練的複雜智能體中，哪些組件仍然有用。
- 結果有多少能延伸到連續控制與遊戲以外的領域。

## 參考文獻

### 開創性論文

- Hessel et al. (2018), "Rainbow: Combining improvements in deep reinforcement learning", [arXiv:1710.02298](https://arxiv.org/abs/1710.02298) — The Rainbow paper, with its six-component ablation and the reported Atari results.
- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", [arXiv:1509.06461](https://arxiv.org/abs/1509.06461) — The double Q-learning component, which reduces overestimation.
- Schaul, Quan, Antonoglou & Silver (2016), "Prioritized experience replay", [arXiv:1511.05952](https://arxiv.org/abs/1511.05952) — The prioritised replay component, reported to beat uniform replay on 41 of 49 games.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The base DQN agent that Rainbow extends.
- Mnih et al. (2013), "Playing Atari with deep reinforcement learning", [arXiv:1312.5602](https://arxiv.org/abs/1312.5602) — The early preprint that introduced the Atari setting used throughout.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on multi-step returns and temporal-difference learning.
