---
translation_reviewed: 2026-10-28
---

# 深度 Q 網路（Mnih 等人，2015）

卷積網路從原始畫面近似動作價值函數，並以經驗回放與目標網路穩定訓練。

## 問題

如何用同一個演算法，直接從原始像素學會多種不同遊戲的控制策略？

## 核心想法

卷積網路從原始畫面近似動作價值函數 Q。兩項改動讓訓練更穩定：經驗回放（隨機抽取過去的轉移）與目標網路（只偶爾更新）。

## 方程式或演算法

網路被訓練以降低相對於目標網路的平方時序差分誤差：

\[
L(\theta) = \mathbb{E}\left[\left(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta)\right)^2\right]
\]

## 結果

同一個網路與訓練程序，能從原始像素學會多款 Atari 2600 遊戲。

## 限制

動作必須是離散的，而且訓練需要大量經驗。後續的 Double DQN 與 Rainbow 處理了部分殘留的不穩定性，見上方的演算法表。

## 連結

- 母頁：[強化學習](../index.md)
- 同一主題的另一方法：[近端策略最佳化](../proximal-policy-optimisation/index.md)

## 參考文獻

### 開創性論文

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518. https://doi.org/10.1038/nature14236 — DQN 論文，開啟了大規模深度強化學習的起點。
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — AlphaGo，結合學習得到的網路與搜尋。
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, arXiv:1706.03741 — 從人類的成對比較中學習獎勵函數，是 RLHF 的基礎。
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — PPO，實務上最常用的策略梯度方法。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 標準強化學習教科書，提供免費線上草稿，涵蓋上方表格中的演算法家族。
- Levine, S., Kumar, A., Tucker, G. & Fu, J. (2020), "Offline reinforcement learning: tutorial, review, and perspectives on open problems", arXiv:2005.01643 — 從固定資料集學習的教學與綜述。
