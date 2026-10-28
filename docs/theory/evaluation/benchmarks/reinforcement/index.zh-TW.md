---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
  - theory/paradigms/reinforcement-learning
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
aliases:
  - Reinforcement learning benchmarks
  - 強化學習基準
---

# 強化學習基準

強化學習基準是讓代理採取行動、並依其累積回報計分的環境。結果取決於環境版本、步數上限、隨機種子數量，以及情節如何平均，因此這些都必須與分數一起報告。

## 概述

強化學習基準是一個具有固定獎勵、觀測格式與動作空間的模擬器或遊戲，加上在其上執行代理的協定。Arcade Learning Environment（ALE）把 Atari 2600 遊戲變成這樣的測試平台。作者把它描述為評估通用代理的平台與方法論，提供數百款遊戲的介面，並報告了其中超過 55 款的結果（Bellemare et al., 2013）。Deep Q-Networks 之後也在這些遊戲上評估，使 ALE 成為以價值為基礎的深度強化學習的參照點（Mnih et al., 2015）。

連續控制的基準則改用物理模擬器。MuJoCo 是為模型式控制而建構的物理引擎（Todorov et al., 2012）。OpenAI Gym 為許多這類環境提供共同的介面與共享的結果回報處，使方法能跨不同套件比較（Brockman et al., 2016）。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [Arcade Learning Environment](ale.md) | 以離散動作、從像素玩 Atari 2600 遊戲 | 每款遊戲的遊戲分數，跨遊戲彙總 |
| [MuJoCo](mujoco.md) | 以連續動作控制模擬身體 | 情節回報 |

兩者著重的面向不同。ALE 在許多遊戲中測試單一代理，動作是離散選擇，獎勵稀疏。MuJoCo 則在物理模型上測試平滑、高維度的控制，其獎勵通常由人工撰寫。

## 關鍵概念

- **回報**：代理在一個情節中累積的獎勵總和，通常帶有折扣。
- **環境版本**：模擬器或遊戲的特定發行版，包含其動力學、包裝器與設定。
- **種子**：單次執行的隨機數產生器設定。多個種子的分數顯示單次執行所隱藏的變異。

## 運作方式

代理與環境互動固定的步數，或直到情節結束。每個情節的回報會被記錄，依情節與種子平均後，連同環境版本與步數上限一起報告。ALE 在此之上還有方法論規則，後續研究彙整了這些選擇的最佳實務，並在此規範下報告新的基準結果（Machado et al., 2018）。

## 常見問題

- **環境版本。** 模擬器或包裝器的改變可能改變分數，因此必須記錄版本。ALE 的作者重新檢視其協定，並引入 sticky actions 為環境加入隨機性（Machado et al., 2018）。
- **種子變異。** 結果會因隨機種子而不同，標準環境中的非確定性也會使所報告的進步難以解讀。應與平均值一同報告跨種子的分散程度（Henderson et al., 2017）。
- **模擬落差。** 在模擬中的結果不保證在實體硬體上的表現。

## 相關連結

- [強化學習](../../../paradigms/reinforcement-learning/index.md) 是這些基準所比較的方法所屬的學習範式。
- [推理與代理](../reasoning-agents/index.md) 涵蓋文字與網路情境中的代理。
- [協定](../../protocols/index.md) 涵蓋切分與報告方式。

## 開放問題

- 一組遊戲或模擬身體能否以可預測新任務表現的方式為方法排名。
- 如何讓種子數量與評估預算標準化到足以直接比較已發表的進步。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [機器人](../../../../applications/robotics/index.md) 說明模擬控制的結果最終必須在其中測試的實體環境。

## 參考文獻

### 開創性論文

- Bellemare, M. G., Naddaf, Y., Veness, J. & Bowling, M. (2013). *The Arcade Learning Environment: An Evaluation Platform for General Agents*. Journal of Artificial Intelligence Research, 47, 253–279. https://doi.org/10.1613/jair.3912 — 介紹 Atari 平台與比較代理的方法論，並報告超過 55 款遊戲的結果。
- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature, 529–533. https://doi.org/10.1038/nature14236 — 以相同的輸入與設定，在多款 Atari 遊戲上評估深度 Q 網路。
- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — 描述用於模擬控制任務的物理引擎。

### 文章與文件

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — 描述許多環境所遵循的共同介面與共享的基準集合。
- Machado, M. C. et al. (2017). *Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents*. arXiv. https://arxiv.org/abs/1709.06009 — 檢視 ALE 的評估方式、提出最佳實務，並引入 sticky actions。
- Henderson, P. et al. (2017). *Deep Reinforcement Learning that Matters*. arXiv. https://arxiv.org/abs/1709.06560 — 說明非確定性與種子變異如何使已報告的深度強化學習結果難以解讀。
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — 關於獎勵、回報與情節的免費線上教科書。
