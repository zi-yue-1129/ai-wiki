---
translation_reviewed: 2026-10-28
---

# 深度 Q 網路（Mnih 等人，2015）

卷積網路從原始畫面近似動作價值函數，並以經驗回放與目標網路穩定訓練。

## 問題

值函數型強化學習很難直接套用在原始感官輸入上。以神經網路進行 Q 學習並不穩定：連續的觀測高度相關，而目標值會隨每次更新移動。問題是：同一種架構與同一套訓練程序，能否直接從螢幕畫面為許多 Atari 2600 遊戲學出控制策略？

## 核心想法

卷積網路接收最近四個前處理後的畫面，為每個動作輸出一個 Q 值。訓練使用兩項穩定化技巧。經驗回放保存最近一百萬個畫面的轉移，並以均勻抽樣、批次大小 32 的小批量進行訓練。目標網路的參數 θ⁻ 只每隔 C 步從線上網路複製一次。獎勵被裁剪為 +1 與 −1，智能體以 ε-貪婪方式行動。論文對所有遊戲使用相同的架構、學習演算法與超參數，但每款遊戲各自訓練一個網路。

## 方程式或演算法

網路被訓練以降低相對於目標網路的平方時序差分誤差：

\[
L(\theta) = \mathbb{E}\left[\left(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta)\right)^2\right]
\]

依論文方法部分的流程：

1. 初始化回放記憶體 \(D\) 與線上網路（權重 \(\theta\)），並令 \(\theta^- = \theta\)。
2. 每一步以機率 \(\varepsilon\) 隨機選擇動作，否則選擇貪婪動作 \(\arg\max_a Q(s_t, a; \theta)\)。論文讓 \(\varepsilon\) 在前一百萬個畫面內從 1.0 線性遞減到 0.1，之後固定為 0.1。
3. 執行動作，並將其重複 \(k = 4\) 個畫面。裁剪獎勵後，把轉移存入 \(D\)。
4. 從 \(D\) 抽取 32 筆轉移組成小批量。
5. 終止轉移的目標為 \(y = r\)，否則為 \(y = r + \gamma \max_{a'} Q(s', a'; \theta^-)\)。以 RMSProp 進行一步更新，降低 \((y - Q(s, a; \theta))^2\)。
6. 每 \(C\) 步令 \(\theta^- \leftarrow \theta\)。

## 結果

在 49 款 Atari 2600 遊戲上，使用相同設定，DQN 在 29 款遊戲中達到人類分數的 75% 以上，並在 43 款遊戲中優於先前最好的強化學習方法。每款遊戲訓練 5,000 萬個畫面，評估時使用 \(\varepsilon = 0.05\)。

## 限制

- **只適用離散動作。**必須精確計算所有動作上的最大值，對大型或連續的動作空間並不實際。
- **高估偏誤。**目標中的最大值運算會使價值估計偏高。van Hasselt 等人（2016）在部分 Atari 遊戲中觀察到明顯高估，並以 Double DQN 降低。
- **均勻回放。**所有儲存的轉移權重相同。Schaul 等人（2016）顯示，在 49 款遊戲中的 41 款，優先回放優於均勻回放。
- **長程規劃。**論文指出，需要更長時程規劃的遊戲（例如 Montezuma's Revenge）仍是 DQN 的重大挑戰。
- **獎勵裁剪。**裁剪無法區分不同大小的獎勵，作者指出這可能影響表現。
- **樣本成本高。**每款遊戲都需要數千萬個畫面的經驗。

後續工作結合了多項改進。Rainbow 融合六項 DQN 擴充，包括 Double Q 學習與優先回放，並報告了 Atari 上的最佳表現（Hessel 等人，2018）。

## 連結

- 母頁：[強化學習](../index.md)
- 回放與目標網路的概念見[經驗回放](../experience-replay/index.md)，方法家族的比較見[值函數方法](../value-based-methods/index.md)。
- ε-貪婪探索見[探索](../exploration/index.md)。
- 同一主題的另一方法：[近端策略最佳化](../proximal-policy-optimisation/index.md)，採取基於策略的路線。
- 母頁討論了經驗回放與海馬迴回放之間的類比。

## 應用

- **基準測試。**DQN 之後，Atari 2600 遊戲成為值函數型智能體的標準測試環境，Rainbow 仍在此套件上報告結果（Hessel 等人，2018）。

## 未解問題

- 樣本效率：如何在不犧牲穩定性的前提下，用更少的畫面學習。
- 稀疏獎勵遊戲（例如 Montezuma's Revenge）中的探索。
- 回放與目標網路為何能穩定訓練，理論上只得到部分解釋。

## 參考文獻

### 開創性論文

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The DQN paper: a convolutional Q-network with replay and a target network, trained on 49 Atari games.
- Mnih et al. (2013), "Playing Atari with deep reinforcement learning", arXiv:1312.5602 — The earlier preprint, which learned seven Atari games from raw pixels.
- van Hasselt, Guez & Silver (2016), "Deep reinforcement learning with double Q-learning", arXiv:1509.06461 — Shows that DQN overestimates action values and reduces the bias with double Q-learning.
- Schaul, Quan, Antonoglou & Silver (2016), "Prioritized experience replay", arXiv:1511.05952 — Replays important transitions more often, beating uniform replay on 41 of 49 games.
- Hessel et al. (2018), "Rainbow: Combining improvements in deep reinforcement learning", arXiv:1710.02298 — Combines six DQN extensions and reports state-of-the-art Atari performance.

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — The standard RL textbook, with a free online draft that covers value-based methods.
