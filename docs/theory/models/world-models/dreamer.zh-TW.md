---
translation_reviewed: 2026-10-28
tags:
  - world models
  - reinforcement learning
  - model-based
aliases:
  - Dreamer
  - 夢想家
  - 想像式強化學習
---

# Dreamer

Dreamer 是一系列強化學習代理人。它們從經驗中學習潛在世界模型，再透過在該模型內想像軌跡來學習行為，而不是每次更新都要在真實環境中行動。

## 概述

Dreamer 代理人有三個學習的部分。世界模型把觀測編碼成緊湊的潛在狀態，並預測狀態如何隨動作、獎勵與延續訊號改變。行動者（actor）負責選擇動作。評論者（critic）估計狀態的價值。行動者與評論者是在世界模型產生的想像潛在軌跡上訓練，因此一次真實經驗可以支持許多次學習更新。這是[以模型為基礎的強化學習](../../paradigms/reinforcement-learning/model-based-rl/index.md)在潛在想像形式下的核心想法。

## 關鍵概念

- **潛在狀態（latent state）**：把觀測壓縮後的表徵，模型在其上向前預測。
- **想像展開（imagined rollout）**：不接觸環境，僅由模型產生的潛在狀態與預測獎勵序列。
- **在想像上做 actor-critic**：透過想像序列計算預測價值的梯度，來改進策略。

## 運作方式

1. 把真實經驗存入回放緩衝區。
2. 訓練世界模型，讓它能從潛在狀態重建觀測並預測獎勵，使潛在狀態保留與控制相關的資訊。
3. 從取樣到的真實狀態出發，在潛在模型內以固定時程讓策略向前展開。
4. 用想像的回報訓練評論者，並訓練行動者最大化預測價值，梯度穿過想像的序列反向傳播。

## 關鍵方法

- **DreamerV1（Hafner 等人, 2019）**：透過潛在空間中的想像軌跡，把價值估計反向傳播來學習行為。[arXiv:1912.01603](https://arxiv.org/abs/1912.01603)。
- **DreamerV2（Hafner 等人, 2021）**：世界模型使用離散的類別潛在變數。摘要將它描述為第一個在 55 個 Atari 任務的基準上達到人類水準的代理人。
- **DreamerV3（Hafner 等人, 2025）**：根據摘要，同一組固定設定可用於超過 150 個跨領域任務，且不需逐任務調參。

各版本的主要差異在於潛在狀態的形式與訓練配方，核心迴圈保持不變。各版本的細部訓練設定見各自論文，重用前應先閱讀。

## 與其他主題的連結

Dreamer 與本站其他[世界模型](index.md)屬於同一家族。它的潛在預測是學習得來的前向模型的一種形式。想像機制是否對應大腦中的歷程，是尚待驗證的假說，Dreamer 論文並未建立這一點。神經科學端對規劃與模擬的討論，見[計算神經科學](../../../brain-mind/computational-neuroscience/index.md)。

## 應用

Dreamer 式的代理人已用於連續控制、二維與三維遊戲環境，以及從影像觀測學習。DreamerV3 論文報告了跨領域的結果，這是其通用性的主要證據。

## 開放問題

- 在長時程想像中，模型誤差會累積到什麼程度，才會讓行動者從誤導的價值中學習。
- 同一組設定，對於與基準套件差異很大的任務是否同樣有效。
- 世界模型應如何處理不改變觀測的動作，這是 [動作可控性](action-controllability.md) 所討論的問題。

## 參考文獻

### 奠基性論文

- Hafner, D.、Lillicrap, T.、Ba, J. 等人 (2019). *Dream to Control: Learning Behaviors by Latent Imagination*. arXiv 預印本. https://arxiv.org/abs/1912.01603 — 提出 Dreamer，透過潛在想像軌跡反向傳播來學習行為。
- Hafner, D.、Lillicrap, T.、Norouzi, M. 與 Ba, J. (2021). *Mastering Atari with Discrete World Models*. ICLR 2021. https://arxiv.org/abs/2010.02193 — DreamerV2，使用離散潛在狀態，並報告 Atari 基準上的結果。
- Hafner, D.、Pasukonis, J.、Ba, J. 與 Lillicrap, T. (2025). *Mastering diverse control tasks through world models*. Nature 640. https://doi.org/10.1038/s41586-025-08744-2 — DreamerV3 的期刊版本，同一組設定適用於超過 150 個任務。arXiv 預印本題為 *Mastering Diverse Domains through World Models*，見 https://arxiv.org/abs/2301.04104。

### 綜述與教科書

- Moerland, T. M. 等人 (2020). *Model-based Reinforcement Learning: A Survey*. arXiv 預印本. https://arxiv.org/abs/2006.16712 — 以模型為基礎的強化學習綜述，涵蓋學習得來的動力學模型，以及它們在規劃與策略學習中的用法。

### 文章與文件

- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv 預印本. https://arxiv.org/abs/1803.10122 — 早期的潛在世界模型，策略可以在模型自身模擬的環境中訓練，是 Dreamer 的前身。
