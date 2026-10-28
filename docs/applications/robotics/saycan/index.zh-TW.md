---
translation_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/paradigms/reinforcement-learning
aliases:
  - SayCan
  - Do As I Can, Not As I Say
  - 語言模型規劃
---

# SayCan（Ahn 等人，2022）

Ahn 等人想知道：一個對世界知識豐富、卻沒有身體經驗的語言模型，如何引導機器人完成任務。他們的系統 SayCan 讓語言模型提出步驟，而由學習得來的價值函數檢查機器人實際上能執行哪些步驟。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

語言模型能為「幫我拿杯飲料」這類任務提出合理的步驟，但它不知道機器人在當前場景中能否執行這些步驟。缺少這種與實體環境的連結，它的計畫可能流暢卻不可行。

## 核心想法

機器人擁有一組預訓練的技能，每個技能都配有一個價值函數，估計該技能在當前場景中成功的可能性。對每個候選技能，SayCan 把語言模型對該技能的評分與其價值結合起來。語言模型提供任務層級的計畫，而機器人的技能與感知則把這個計畫落實到實體環境中。

## 程序

1. 列出機器人可用的候選技能。
2. 把語言模型對每個技能的機率與其價值函數結合，為每個技能評分。
3. 執行最佳技能、觀察結果，並重複直到任務完成。

## 結果

論文摘要報告，在移動式操作機器人上的真實任務評估，系統能處理冗長、抽象的自然語言指令。量化數字需要查閱全文。

## 限制

- 技能庫決定了機器人能做什麼。超出技能庫的任務，單靠規劃無法解決。
- 每項技能的價值函數都需要學習，因此需要資料。
- 論文的評估只在作者的機器人與技能組合上進行。

## 連結

- 在執行過程中加入語言回饋的後續工作 Inner Monologue（Huang 等人，2022）列於參考文獻。
- 學習技能與價值函數與[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)相關。

## 參考文獻

### 開創性論文

- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — 在真實任務上，把語言模型與預訓練機器人技能的學習價值函數結合。
- Huang, W. et al. (2022). Inner Monologue: Embodied Reasoning through Planning with Language Models. arXiv. https://arxiv.org/abs/2207.05608 — 在語言模型規劃中加入來自環境的語言回饋，以提升機器人完成任務的能力。
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — 以大量真實機器人資料訓練的 transformer 機器人策略，是 SayCan 可以組合的那類技能。

### 教科書與綜述

- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — 機器人強化學習的綜述，價值函數的思路即來自此領域。
- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — 基礎模型的報告，包含語言模型在機器人中的落實。
