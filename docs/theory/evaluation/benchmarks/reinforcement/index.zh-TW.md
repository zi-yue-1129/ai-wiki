---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
---

# 強化學習基準

強化學習基準是讓代理與環境互動、再以其累積回報評分的環境。結果取決於環境版本、步數上限、隨機種子數量與回合平均方式，因此必須與分數一併報告。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [Arcade Learning Environment](ale.md) | 以離散動作從畫面遊玩 Atari 2600 遊戲 | 每款遊戲的遊戲分數，跨遊戲彙總 |
| [MuJoCo](mujoco.md) | 以連續動作控制模擬身體 | 每回合回報 |

## 常見問題

- **環境版本。** 模擬器或包裝器的變動可能改變分數，因此必須記錄版本。
- **種子變異。** 結果會因隨機種子而不同，因此應同時報告平均值與跨種子的範圍。
- **模擬落差。** 模擬中的結果不保證在實體硬體上的表現。

## 相關

- [基準測試概述](../index.md) 列出所有家族。
- [推理與代理](../reasoning-agents/index.md) 涵蓋文字與網頁情境中的代理。
- [協定](../../protocols/index.md) 說明切分與報告方式。

## 參考文獻

### 開創性論文

- Bellemare, M. G. et al. (2013). *The Arcade Learning Environment: An Evaluation Platform for General Agents*. Journal of Artificial Intelligence Research 47. https://doi.org/10.1613/jair.3912 — 介紹 Atari 平台，以及在其上比較代理的方法。
- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — 描述用於模擬控制任務的物理引擎。

### 文章與文件

- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature. https://doi.org/10.1038/nature14236 — 報告在 Atari 遊戲上評估的深度強化學習代理。
- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — 描述許多強化學習環境所遵循的共通介面。

### 補充來源

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 標準強化學習教科書的免費草稿。
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張在固定任務上的技能是衡量智能的弱指標。
