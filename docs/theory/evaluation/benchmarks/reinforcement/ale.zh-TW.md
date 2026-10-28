---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
---

# Arcade Learning Environment

Arcade Learning Environment（ALE）是把 Atari 2600 遊戲當作強化學習任務執行的平台，也是建立於其上的基準。它的設計目的，是透過同一個介面，在許多遊戲上評估通用代理（Bellemare et al., 2013）。之後，Atari 遊戲上的深度強化學習結果也在此基準上報告（Mnih et al., 2015）。

## 任務與資料

代理接收遊戲畫面，並從離散的搖桿動作中選擇，目標是最大化遊戲分數。原始論文報告了超過 55 款遊戲的結果（Bellemare et al., 2013）。每款遊戲都有自己的規則與回饋結構，因此方法必須從各自的經驗中學習每一款。

## 協定與指標

分數是每回合結束時遊戲本身的分數，按遊戲分別報告。論文通常會對多個種子取平均，並跨整組遊戲彙總。跳幀數、動作集合與回合長度等細節都會改變結果，因此必須說明。

## 它能說明什麼

它顯示同一個通用方法，在輸入格式相同的情況下，於許多不同遊戲上的表現。它的結果描述的是遊戲表現，而非通用智能。

## 限制

- **決定性設定。** 原始設定是決定性的，使代理有機會利用固定的動作序列。
- **分數尺度差異。** 各遊戲的原始分數尺度不同，跨遊戲彙總需要正規化，而論文對此的處理方式不同。
- **領域狹窄。** Atari 遊戲是離散且以視覺為主的，無法代表機器人或語言任務。

## 相關

- [強化學習概述](index.md) 比較強化學習基準。
- [MuJoCo](mujoco.md) 涵蓋連續控制。

## 參考文獻

### 開創性論文

- Bellemare, M. G. et al. (2013). *The Arcade Learning Environment: An Evaluation Platform for General Agents*. Journal of Artificial Intelligence Research 47. https://doi.org/10.1613/jair.3912 — 介紹平台、遊戲與評估方法。
- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature. https://doi.org/10.1038/nature14236 — 報告在 Atari 遊戲上評估的深度強化學習代理。

### 文章與文件

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — 描述許多強化學習環境所遵循的共通介面。

### 補充來源

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 標準強化學習教科書的免費草稿。
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張在固定任務上的技能是衡量智能的弱指標。
