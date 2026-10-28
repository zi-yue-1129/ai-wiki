---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
---

# MuJoCo

MuJoCo 是模擬關節式身體與接觸的物理引擎，專為模型式控制而設計（Todorov et al., 2012）。作為基準，它是透過連續控制任務使用的，例如常見強化學習工具包中附帶的模擬行走者與手臂（Brockman et al., 2016）。

## 任務與資料

代理對模擬身體施加連續的力矩或力，並因前進或達成目標而獲得回報。模擬器提供動力學，任務則定義回報與結束回合的規則。

## 協定與指標

常用指標是回合回報，即固定步數上限內回報的總和，並對隨機種子取平均。模擬器版本、時間步長與回報定義都會改變結果，因此必須說明。

## 它能說明什麼

連續控制任務顯示方法學習平滑、高維動作控制的能力，也讓方法能在相同動力學上互相比較。

## 限制

- **模擬落差。** 在模擬中有效的策略，未經額外工作可能無法轉移到實體機器人。
- **回報設計。** 任務回報是人工撰寫的，因此分數反映回報設計與方法同樣多（Raji et al., 2021）。
- **版本漂移。** 模擬器更新可能改變動力學，使過去的分數難以重現。

## 相關

- [強化學習概述](index.md) 比較強化學習基準。
- [Arcade Learning Environment](ale.md) 涵蓋離散動作的遊戲。

## 參考文獻

### 開創性論文

- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — 描述物理引擎及其在控制上的用途。

### 文章與文件

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — 描述連續控制任務所遵循的共通介面。
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 解釋回報、回報總和與回合的免費草稿。

### 補充來源

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張在固定任務上的技能是衡量智能的弱指標。
