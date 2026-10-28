---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation/behavioural-cloning
  - theory/paradigms/imitation/interactive-imitation/dagger.md
  - theory/paradigms/imitation/interactive-imitation/dart.md
  - theory/paradigms/supervised
tags:
  - imitation learning
  - causal inference
  - behavioural cloning
aliases:
  - causal confusion
  - causal misidentification
  - 因果混淆
---

# 模仿學習中的因果混淆

因果混淆是[行為克隆](index.md)的一種失誤：學到的策略依賴的觀測與專家動作在示範中相關，但並不是造成該動作的原因。加入更多觀測有時反而會讓策略變差，因為每個新特徵都提供了另一種抓住虛假相關的方式。此術語與分析來自 de Haan、Jayaraman 與 Levine（2019），論文正文稱此失誤為*因果誤判*（causal misidentification）。

## 概述

被克隆的策略以觀測預測專家動作來進行訓練。在示範上的預測準確度，並不能告訴學習者專家實際回應的是哪些觀測。當某個虛假觀測與專家動作之間的關係在測試時改變，策略就會失敗，即使它的訓練損失很低。論文主張，根本原因在於行為克隆忽略了連結專家、環境與觀測的因果結構。

## 核心概念

- **因果特徵與虛假特徵**：若專家的決策取決於某特徵，該特徵就是因果的；若它只是透過其他變數與決策相關，例如動作的後果，則是虛假的。
- **因果誤判**：論文對「把虛假特徵當成原因」的策略所用的名稱。
- **定向介入**：改變學習者所見或所做的查詢，例如詢問專家某個選定狀態，或在環境中執行候選策略，使專家的回應揭示哪些輸入重要。
- **共變量偏移與因果混淆**：共變量偏移是學習者自身錯誤造成的狀態分布改變，[DAgger](../interactive-imitation/dagger.md) 處理的正是這個問題。因果混淆則是輸入選擇錯誤，光是在學習者的分布上收集更多資料，不一定能解決。

## 運作方式

論文的方法把輸入的選擇視為一個因果模型，並以介入來選定：

1. 在數個候選因果圖上訓練同一個策略。每個圖 \(G\) 選出觀測變數的子集 \(S_G\)，策略只以 \(o_{S_G}\) 為條件，因此可以在許多組輸入下評估。
2. 進行定向介入，以估計每個圖對專家行為的解釋程度。論文使用兩種模式：
    - **專家查詢**：專家標註候選策略彼此意見分歧的狀態。
    - **策略執行**：在環境中執行每個候選策略，以其回合報酬作為證據。
3. 選出最可能的圖，並以它指定的輸入作為因果模型。

若以標準的克隆目標寫出，基準方法是在所有觀測 \(o\) 上最小化 \(\sum_{(o,a)\in\mathcal D}\ell(\pi_\theta(o), a)\)。修正方式是對選定的圖 \(G^\star\)，把 \(o\) 限制在因果子集 \(S_{G^\star}\) 上。

## 關鍵方法

### Causal Confusion in Imitation Learning（de Haan、Jayaraman 與 Levine，2019）

- **問題：** 在豐富觀測上做行為克隆，在分布偏移下可能失敗。若策略看到一個與專家動作相關的特徵，即使該特徵其實是動作的結果而非原因，策略仍可能依賴它。論文引言的例子是：當煞車被踩下，車子儀表板上的指示燈會亮起。若策略從指示燈學會煞車，就是把結果當成了原因。
- **核心想法：** 把策略當作因果結構的探針。在候選的輸入集合上訓練，再以定向介入找出專家行為實際由哪一組輸入解釋，並保留該組。
- **公式或演算法：** 基準是在完整觀測上的克隆目標 \(\sum\ell(\pi_\theta(o),a)\)。此方法在取樣的圖上訓練以圖為條件的策略 \(\pi_G(a\mid o_{S_G})\)，以專家查詢或策略執行的介入為每個圖評分，並選出最可能的圖 \(G^\star\)。
- **結果：** 在 MountainCar 上，論文的表 2 顯示：解耦狀態下，策略執行的報酬為 \(-137\)，專家查詢為 \(-140\)；糾纏狀態下則分別為 \(-145\) 與 \(-165\)。表 1 的駕駛比較（GTA-V 設定，引自 Wang 等人）顯示，HISTORY 模型的驗證困惑度較低（0.834 對 0.989），但介入次數較多（2.94 對 1.30）、碰撞次數也較多（6.49 對 3.38）。附錄文字指出，在 MountainCar 上 DAgger 需要數百次查詢、在 Hopper 上需要數萬次查詢，才能達到相近的報酬。Atari 的結果以定性方式呈現。
- **限制：** 實驗規模小（MountainCar、Hopper、三款 Atari 遊戲與一個駕駛設定）。依論文所述，候選圖是建立在預先定義的觀測變數集合上，因此方法只能在給定的輸入中選擇。介入步驟依賴專家查詢或環境回合，成本可能很高。論文也沒有報告因果混淆在真實世界中發生的頻率。

## 相關失誤：複製型策略

Wen 等人（2020）研究 *copycat agents*，也就是從觀測歷史做行為克隆時，策略預測的是前一個專家動作而非下一個動作。由於專家動作在時間上常高度相關，複製上一個動作是降低訓練損失的簡單方法。這是同一機制的具體例子：一個捷徑特徵在示範上能很好地預測目標，卻不反映真正想學的行為。

## 關聯

因果混淆是分布偏移的一種形式，與 [DAgger](../interactive-imitation/dagger.md) 所修正的共變量偏移不同。僅在學習者自己的狀態上收集更多資料，並不能告訴策略哪些輸入重要。[DART](../interactive-imitation/dart.md) 以離線方式改善覆蓋範圍，但同樣有這個盲點。學習虛假相關的問題也出現在其他領域；人類從他人行動推斷原因的面向，見[認知科學](../../../../brain-mind/cognitive-science/index.md)。

## 應用

具有多個感測器串流的駕駛與機器人策略。單一的虛假訊號，例如指示燈、前一個指令或過去狀態的特徵，可能主導學到的策略，並在感測器或操作者習慣改變時失效。

## 開放問題

- 當介入成本高（例如每次查詢都需要人類專家）時，如何找出因果結構。
- 因果發現方法能否擴展到高維的感測器輸入，而不需要人工列出候選變數。
- 在真實資料集中，如何區分因果混淆與一般的共變量偏移，因為兩者都會產生相似的錯誤。

## 參考文獻

### 奠基性論文

- de Haan, P.、Jayaraman, D. 與 Levine, S.（2019）. Causal Confusion in Imitation Learning. NeurIPS 2019（第 33 屆神經資訊處理系統會議）. [arXiv:1905.11979](https://arxiv.org/abs/1905.11979) — 說明克隆策略可能依賴非因果特徵，並提出以定向介入選出因果輸入。
- Wen, C.、Lin, J.、Darrell, T.、Jayaraman, D. 與 Gao, Y.（2020）. Fighting Copycat Agents in Behavioral Cloning from Observation Histories. NeurIPS 2020. https://proceedings.neurips.cc/paper/2020/hash/1b113258af3968aaf3969ca67e744ff8-Abstract.html — 研究 copycat 失誤，即策略預測前一個專家動作。
- Ross, S.、Gordon, G. J. 與 Bagnell, J. A.（2011）. A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. AISTATS 2011, PMLR 15. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — 提供克隆的共變量偏移分析，這與因果混淆不同，但常被混為一談。
- Ross, S. 與 Bagnell, J. A.（2010）. Efficient Reductions for Imitation Learning. AISTATS 2010, PMLR 9. https://proceedings.mlr.press/v9/ross10a.html — 同一作者較早在模仿學習的歸約觀點上的工作。

### 綜述與教科書

- Osa, T. 等人（2018）. An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics. [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — 模仿學習方法的綜述，包含行為克隆及其失誤模式的背景。

### 文章與預印本

- Geirhos, R. 等人（2020）. Shortcut Learning in Deep Neural Networks. [arXiv:2004.07780](https://arxiv.org/abs/2004.07780) — 描述捷徑學習，即模型依賴與目標相關、卻不反映預期任務的特徵。這是因果混淆背後的一般模式。
