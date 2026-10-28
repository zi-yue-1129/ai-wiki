---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/model-based-rl
  - brain-mind/computational-neuroscience
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

Dreamer 是一系列強化學習代理人，由 Danijar Hafner 與同事提出。每個代理人都從自身經驗學習潛在世界模型，再透過在模型內想像軌跡來學習行為，因此一段真實經驗可以支持許多次學習更新。這個系列已發表三個版本：DreamerV1、V2 與 V3。它們保持相同的核心迴圈，但改變潛在狀態的形式與訓練配方。

## 概述

Dreamer 代理人有三個學習得來的部分。世界模型把觀測編碼成緊湊的潛在狀態，預測狀態在給定動作後如何改變，並由此預測獎勵。行動者（actor）負責選擇動作，評論者（critic，即價值模型）估計潛在狀態的價值。行動者與評論者是在世界模型產生的想像潛在軌跡上訓練。這是[以模型為基礎的強化學習](../../paradigms/reinforcement-learning/model-based-rl/index.md)在潛在想像形式下的做法。

## 關鍵概念

- **潛在狀態（latent state）**：把觀測壓縮後的表徵，模型在其上向前預測。DreamerV1 中它是對角高斯分布；DreamerV2 與 V3 則由離散變數組成。
- **想像展開（imagined rollout）**：不接觸環境，僅由模型產生的潛在狀態與預測獎勵序列。
- **在想像上做 actor-critic**：利用想像序列上的 λ 加權價值目標，透過預測價值的梯度來改進策略。

## 運作方式

1. 把真實經驗存入回放緩衝區。
2. 訓練世界模型，讓它能從潛在狀態重建觀測並預測獎勵，使潛在狀態保留與控制相關的資訊。在 DreamerV1 中，這是一個變分目標（見下）。
3. 從取樣到的真實狀態出發，在潛在模型內以固定時程 \(H\) 讓行動者向前展開。
4. 用想像的 λ 回報訓練評論者，並訓練行動者最大化預測價值，梯度穿過想像的序列反向傳播。

對 DreamerV1 而言，想像狀態上的 λ 加權價值目標（折扣為 \(\gamma\)，混合權重為 \(\lambda\)）為

\[
V_\lambda(s_\tau) \doteq (1-\lambda)\sum_{n=1}^{H-1}\lambda^{n-1}V^{n}_{N}(s_\tau) + \lambda^{H-1}V^{H}_{N}(s_\tau)
\]

其中 \(V^{k}_{N}\) 是 \(k\) 步估計，會加總想像的獎勵，並由學到的價值函數做自舉（bootstrap）。行動者最大化沿想像軌跡的價值總和，

\[
\max_{\phi}\ \mathbb{E}\Big[\sum_{\tau=t}^{t+H} V_\lambda(s_\tau)\Big]
\]

世界模型則最大化由觀測、獎勵與 KL 項組成的變分下界，

\[
J_{\text{REC}} = \mathbb{E}_p\Big[\sum_t \big(\ln q(o_t\mid s_t) + \ln q(r_t\mid s_t) - \beta\,\mathrm{KL}[\,p(s_t\mid s_{t-1},a_{t-1},o_t)\,\|\,q(s_t\mid s_{t-1},a_{t-1})\,]\big)\Big] + \text{const}
\]

## 關鍵方法

### DreamerV1（Hafner 等人, 2020）

- **問題：** PlaNet 是 DreamerV1 所比較並建立於其上的潛在動態代理人，它在每次決策時都用模型做規劃。本文探討能否改為透過想像的潛在軌跡，以梯度學到一個策略。
- **核心想法：** 學習一個動作模型與一個價值模型，並把預測的 λ 價值沿想像的潛在軌跡反向傳播，以訓練動作模型。潛在模型使用高斯潛在變數與遞迴的狀態空間結構。
- **方程式或演算法：** 即上文「運作方式」中的 \(V_\lambda\) 目標、行動者目標與世界模型的下界。主要設定為 \(H = 15\)、\(\gamma = 0.99\)、\(\lambda = 0.95\)。
- **結果：** 在 DeepMind Control Suite 的 20 個視覺任務上，觀測為 64×64×3 的影像。論文報告 Dreamer 在 5 × 10⁶ 環境步數後平均分數為 823；同樣預算下 PlaNet 為 332。無模型的 D4PG 達到 786，但需要 10⁸ 步（附錄 G 的表）。
- **限制：** 主要實驗只涵蓋一個基準家族，且動作重複次數為 2。離散動作的實驗（Atari 與 DeepMind Lab）放在附錄。想像回報的品質受限於學到的模型在該時程內的準確度；論文掃描了時程（圖 4），而不是從理論推導。

### DreamerV2（Hafner 等人, 2021）

- **問題：** 在一個學習行為的世界模型內訓練的代理人，能否在 55 款遊戲的 Atari 基準上與最好的無模型代理人匹敵？
- **核心想法：** 把 V1 的高斯潛在變數換成離散的類別潛在變數。使用 KL 平衡，對 KL 項中先驗與後驗兩部分給予不同權重。想像軌跡上的 actor-critic 則保留。
- **方程式或演算法：** 潛在狀態由 32 個類別變數組成，每個變數有 32 類，因此是長度 1024 的二元向量中有 32 個啟用位元。KL 的先驗部分權重為 \(\alpha = 0.8\)，後驗部分為 \(1-\alpha\)；Atari 的整體 KL 尺度為 \(\beta = 0.1\)。想像使用 \(H = 15\) 與 \(\lambda = 0.95\)。訓練進行 2 億（200M）環境步，動作重複次數為 4。
- **結果：** 表 1（Atari，2 億步）中，DreamerV2 的 gamer 正規化中位數為 2.15，gamer 正規化平均數為 11.33。同表中 IQN 的中位數為 1.29，Rainbow 為 1.47，C51 為 1.09，DQN 為 0.65。DreamerV2 在該表每一欄都是最高。摘要宣稱它是第一個在 55 個 Atari 任務的基準上達到人類水準的代理人。論文也報告它能從影像學會類人機器人的站立與行走。
- **限制：** 結果使用 2 億步，遠超出資料效率的範圍，論文沒有 Atari 100k 的結果。「人類水準」的說法取決於所用的正規化方式；論文內文在不同段落給出的折扣值也不一致（內文為 0.999，表 D.1 為 0.995）。重用前應先核對附錄的設定。

### DreamerV3（Hafner 等人, 2023；Nature 2025）

- **問題：** 一套固定的超參數配置，能在許多領域中運作，無需逐任務調參。
- **核心想法：** 使用正規化與穩健化技巧，讓同一組設定在訊號尺度不同時仍能運作。包括對尺度差異大的訊號使用 symlog 轉換、搭配 free bits 的 KL 平衡，以及根據回報範圍做回報正規化。
- **方程式或演算法：** symlog 定義為 \(\operatorname{symlog}(x) = \operatorname{sign}(x)\ln(|x|+1)\)，反函數為 \(\operatorname{symexp}(x) = \operatorname{sign}(x)(\exp(|x|)-1)\)。論文將世界模型的損失權重設為 \(\beta_{\text{pred}} = 1\)、\(\beta_{\text{dyn}} = 1\)、\(\beta_{\text{rep}} = 0.1\)，並把動態與表徵損失截斷在 1 nat（約 1.44 bits）以下。回報範圍由回報批次的第 5 到第 95 百分位計算。論文定義了六種名義模型大小，從 1,200 萬到 4 億參數。
- **結果：** 摘要報告，同一組配置能在超過 150 個多樣任務上勝過專用方法。論文在固定超參數下評估 8 個領域。摘要也指出，Dreamer 是第一個在不使用人類資料或課程的情況下，從零開始在 Minecraft 中收集到鑽石的演算法。Minecraft 的實驗使用 1 億（100M）環境步的預算。
- **限制：** 通用性的主張是在作者所選的任務集上衡量，單一配置不代表它對每個任務都是最佳設定。Minecraft 的結果只在一個步數預算下報告，摘要也沒有列出基準名稱。

## 與其他主題的連結

Dreamer 與本站其他[世界模型](index.md)屬於同一家族。它的潛在預測是學習得來的前向模型的一種形式。它的脈絡來自 PlaNet（Hafner 等人, 2019），DreamerV1 建立在其遞迴潛在模型之上；另一脈絡則是 Ha 與 Schmidhuber（2018）提出的，在學習得來的模型內訓練控制器的想法。想像機制是否對應大腦中的歷程，是尚待驗證的假說，Dreamer 論文並未建立這一點。神經科學端對規劃與模擬的討論，見[計算神經科學](../../../brain-mind/computational-neuroscience/index.md)。

生成可供使用者操作之像素的影片分支，見 [Genie](genie.md)。Dreamer 的潛在模型則預測用於控制的緊湊狀態。

## 應用

Dreamer 式的代理人已用於以像素進行的連續控制（DreamerV1，DeepMind Control Suite）、Atari 與類人機器人控制（DreamerV2），以及以單一配置處理的多種領域，包括 Minecraft（DreamerV3）。DreamerV3 論文報告了跨領域的結果，這是其通用性的主要證據。

## 開放問題

- 在長時程想像中，模型誤差會累積到什麼程度，才會讓行動者從誤導的價值中學習。
- 同一組設定，對於與基準套件差異很大的任務是否同樣有效。
- 世界模型應如何處理不改變觀測的動作，這是 [動作可控性](action-controllability.md) 所討論的問題。

## 參考文獻

### 奠基性論文

- Hafner, D.、Lillicrap, T.、Ba, J. 與 Norouzi, M. (2020). *Dream to Control: Learning Behaviors by Latent Imagination*. ICLR 2020. https://arxiv.org/abs/1912.01603 — 提出 Dreamer，透過想像的潛在軌跡反向傳播來學習行為。
- Hafner, D.、Lillicrap, T.、Norouzi, M. 與 Ba, J. (2021). *Mastering Atari with Discrete World Models*. ICLR 2021. https://arxiv.org/abs/2010.02193 — DreamerV2，使用離散潛在狀態，並報告 55 款遊戲的 Atari 基準結果。
- Hafner, D.、Pasukonis, J.、Ba, J. 與 Lillicrap, T. (2025). *Mastering diverse control tasks through world models*. Nature 640. https://doi.org/10.1038/s41586-025-08744-2 — DreamerV3 的期刊版本，同一組配置適用於超過 150 個任務。arXiv 預印本題為 *Mastering Diverse Domains through World Models*，見 https://arxiv.org/abs/2301.04104。
- Hafner, D.、Lillicrap, T.、Fischer, I.、Villegas, R.、Ha, D.、Lee, H. 與 Davidson, J. (2019). *Learning Latent Dynamics for Planning from Pixels*. ICML 2019. https://proceedings.mlr.press/v97/hafner19a.html — PlaNet，即 DreamerV1 所比較並建立於其上的潛在動態規劃代理人。
- Ha, D. 與 Schmidhuber, J. (2018). *World Models*. arXiv 預印本. https://arxiv.org/abs/1803.10122 — 早期的潛在世界模型，控制器可在模型自身模擬的展開中訓練，是 Dreamer 的前身。

### 綜述與教科書

- Moerland, T. M.、Broekens, J.、Plaat, A. 與 Jonker, C. M. (2020). *Model-based Reinforcement Learning: A Survey*. arXiv 預印本. https://arxiv.org/abs/2006.16712 — 以模型為基礎的強化學習綜述，涵蓋學習得來的動力學模型，以及它們在規劃與策略學習中的用法。

## 延伸閱讀

- Hafner, D.，*Dreamer* 專案頁面. https://danijar.com/project/dreamer/ — 作者的 Dreamer 系列專案頁面。
