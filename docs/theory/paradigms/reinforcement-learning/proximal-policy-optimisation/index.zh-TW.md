---
translation_reviewed: 2026-10-28
---

# 近端策略最佳化（Schulman 等人，2017）

一種策略梯度方法，裁剪新舊策略的機率比，使每次更新都保持在舊策略附近。

## 問題

單純的策略梯度可能走出過大的一步，使表現崩潰；信賴域方法雖穩定，但實作複雜。

## 核心想法

在代理目標中裁剪新舊動作機率的比值，使更新無法因遠離舊策略而得利。如此，同一批資料可以用於多個小批次的迭代更新。

## 方程式或演算法

令機率比為 \(r_t(\theta) = \pi_\theta(a_t \mid s_t) / \pi_{\theta_{\text{old}}}(a_t \mid s_t)\)，優勢估計為 \(\hat{A}_t\)：

\[
L^{\text{CLIP}}(\theta) = \mathbb{E}_t\left[\min\left(r_t(\theta)\hat{A}_t,\ \text{clip}\left(r_t(\theta), 1-\epsilon, 1+\epsilon\right)\hat{A}_t\right)\right]
\]

## 結果

論文報告，在其基準任務（包括模擬的機器人運動與 Atari）上，PPO 優於其他線上策略梯度方法，並在樣本效率、簡單性與實際時間之間取得良好平衡。

## 限制

證據是經驗性的，裁剪是啟發式做法，並不保證改進。PPO 也是同策略方法，每批資料只能支持少數幾次更新。

## 連結

- 母頁：[強化學習](../index.md)
- 同一主題的另一方法：[深度 Q 網路](../deep-q-networks/index.md)

## 參考文獻

### 開創性論文

- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518. https://doi.org/10.1038/nature14236 — DQN 論文，開啟了大規模深度強化學習的起點。
- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529. https://research.google/pubs/mastering-the-game-of-go-with-deep-neural-networks-and-tree-search/ — AlphaGo，結合學習得到的網路與搜尋。
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", NeurIPS, [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) — 從人類的成對比較中學習獎勵函數，是 RLHF 的基礎。
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — PPO，實務上最常用的策略梯度方法。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 標準強化學習教科書，提供免費線上草稿，涵蓋上方表格中的演算法家族。
- Levine, S., Kumar, A., Tucker, G. & Fu, J. (2020), "Offline reinforcement learning: tutorial, review, and perspectives on open problems", [arXiv:2005.01643](https://arxiv.org/abs/2005.01643) — 從固定資料集學習的教學與綜述。
