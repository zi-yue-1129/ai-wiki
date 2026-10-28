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
  - MuJoCo
  - MuJoCo 物理引擎
---

# MuJoCo

MuJoCo 是用於模擬關節式物體與接觸的物理引擎，為模型式控制而建構（Todorov et al., 2012）。作為基準時，它透過連續控制任務來使用，例如模擬的步行者與手臂。Gym 的 2D 與 3D 機器人任務以 MuJoCo 執行（Brockman et al., 2016）。

## 概述

MuJoCo 的建構目的是作為模型式控制的物理引擎，使機器人與其他關節式物體的控制方法能在模擬中開發與測試。模型式控制表示控制器可以利用身體動力學的模型（Todorov et al., 2012）。當它作為基準使用時，身體與任務是固定的，學習演算法必須只靠互動找到控制器。

## 任務與資料

代理在每一步對模擬身體施加連續的力矩或作用力，並接收關節位置與速度的觀測。獎勵依任務設計，通常結合朝目標前進的進度與對耗費力氣的懲罰。動力學由模擬器提供。任務則定義獎勵以及結束情節的規則。

## 協定與指標

常用指標是情節回報，即在固定步數上限的情節中獎勵的總和，並依隨機種子平均。只報告平均值會隱藏種子之間的差異，因此也應報告其分散程度。模擬器版本、時間步長與獎勵定義都會改變結果，必須說明。

## 關鍵概念

- **關節式物體**：由剛性連桿以關節相連而成的結構，例如步行者或機器手臂。
- **連續控制**：動作是實數值的力矩或作用力，而非在離散動作之間選擇。
- **模型式控制**：使用身體動力學模型的控制器，這正是 MuJoCo 設計的目的。

## 它顯示什麼

連續控制任務顯示方法學習平滑、高維度動作控制的能力。它們也讓方法能在相同的動力學下比較，而這在實體機器人上較難做到，因為每次試驗都要花真實時間並損耗硬體。然而，在某個固定的模擬任務上的分數，所能說明的範圍有限（Raji et al., 2021）。

## 限制

- **模擬落差。** 在模擬中有效的策略，若無進一步工作，未必能轉移到實體機器人上。
- **獎勵設計。** 任務獎勵由人工撰寫，因此分數反映的獎勵與學習方法同樣多。
- **版本漂移。** 模擬器更新可能改變動力學，使先前的分數難以重現。
- **種子變異。** 不同種子之間的結果可能差異很大，因此單次執行的比較證據薄弱（Henderson et al., 2017）。

## 相關連結

- [機器人](../../../../applications/robotics/index.md) 說明模擬控制的結果最終必須在其上測試的實體機器人。
- [強化學習](../../../paradigms/reinforcement-learning/index.md) 說明學習這些控制器的方法。

## 相關

- [強化學習概述](index.md) 比較各強化學習基準。
- [Arcade Learning Environment](ale.md) 涵蓋離散動作的遊戲。

## 參考文獻

### 開創性論文

- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — 描述物理引擎及其在控制上的用途。

### 文章與文件

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — 描述許多連續控制套件所遵循的共同介面與共享的基準集合。
- Henderson, P. et al. (2017). *Deep Reinforcement Learning that Matters*. arXiv. https://arxiv.org/abs/1709.06560 — 說明種子變異與非確定性如何使單次執行的比較難以解讀。
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — 解釋獎勵、回報與情節的免費線上教科書。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 檢視基準的建構效度，以及廣泛宣稱的限制。
