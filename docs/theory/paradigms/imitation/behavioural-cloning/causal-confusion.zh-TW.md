---
translation_reviewed: 2026-10-28
tags:
  - imitation learning
  - causal inference
  - behavioural cloning
aliases:
  - causal confusion
  - 因果混淆
---

# 模仿學習中的因果混淆

因果混淆是行為克隆的一種失誤：學到的策略依賴的特徵與專家動作在示範中相關，但並不是造成該動作的原因。加入更多觀測有時反而會讓策略變差，因為新的特徵提供了更多抓住這種虛假相關的方式。

## 問題

被克隆的策略會在專家資料上最小化預測誤差。若某個觀測（例如前一個動作或儀表板指示）能很好地預測專家的下一個動作，策略就可能用它取代真正驅動專家決策的狀態。此時策略在示範上看起來很準，但測試時一旦相關性改變，就會失敗。

## 核心想法

de Haan、Jayaraman 與 Levine（2019）主張，行為克隆忽略了連結專家、環境與觀測的因果結構。沒有因果模型，學習者無法分辨哪些觀測是專家動作的原因、哪些只是相關。論文提出以定向探測（例如查詢專家或與環境互動）來找出正確的因果模型。

## 運作方式

1. 以包含一個相關但非因果特徵的觀測，用行為克隆訓練策略。
2. 觀察到當該特徵與專家動作的關係改變時，策略的測試表現下降。
3. 使用定向介入，例如在選定的狀態查詢專家，或改變該特徵，來找出專家真正回應的觀測。
4. 選出因果子集，並在該子集上訓練。

## 相關的失誤：複製前一個動作

Wen 等人（2020）描述了一個相近的情況，稱為 copycat。當專家動作在時間上高度相關時，被克隆的策略可能直接預測前一個專家動作，而非下一個動作，因為這是降低訓練損失最容易的方法。他們的補救方法是一種對抗式特徵學習，從策略的特徵中移除前一個動作的資訊。

## 與其他主題的連結

因果混淆是分布偏移的一種形式。它也說明了為什麼 [DAgger](../interactive-imitation/dagger.md) 與 [DART](../interactive-imitation/dart.md) 能處理覆蓋範圍，卻無法判斷哪些特徵重要。在人類的對應情境中，從行動推斷原因的研究見[認知科學](../../../../brain-mind/cognitive-science/index.md)。

## 應用

具有多個感測器串流的駕駛與機器人策略，單一的虛假訊號就可能主導學到的策略。

## 開放問題

當介入成本高時，如何找出因果結構；以及因果發現方法能否擴展到高維的感測器輸入。

## 參考文獻

### 奠基性論文

- de Haan, P.、Jayaraman, D. 與 Levine, S.（2019）. *Causal Confusion in Imitation Learning*. arXiv:1905.11979. https://arxiv.org/abs/1905.11979 — 說明行為克隆可能抓住非因果特徵，並提出以定向介入來做因果辨識。
- Wen, C.、Lin, J.、Darrell, T.、Jayaraman, D. 與 Gao, Y.（2020）. *Fighting Copycat Agents in Behavioral Cloning from Observation Histories*. arXiv:2010.14876. https://arxiv.org/abs/2010.14876 — 提出 copycat 失誤（策略預測前一個專家動作），並提出對抗式的補救方法。

### 文章與預印本

- Ross, S.、Gordon, G. J. 與 Bagnell, J. A.（2011）. *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS 2011, PMLR 15:627–635. https://proceedings.mlr.press/v15/ross11a.html — 描述共變量偏移造成的失誤，這與因果混淆不同，但常被混為一談。
- Ross, S. 與 Bagnell, J. A.（2010）. *Efficient Reductions for Imitation Learning*. AISTATS 2010, PMLR 9:661–668. https://proceedings.mlr.press/v9/ross10a.html — 分析克隆策略部署後誤差如何累積。
- Kelly, M. 等人（2018）. *HG-DAgger: Interactive Imitation Learning with Human Experts*. arXiv:1810.02890. https://arxiv.org/abs/1810.02890 — 在學習者到達的狀態上收集專家標註的互動路徑，是發現虛假特徵的一種方式。
