---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- brain-mind/visual-perception
tags:
- neuroscience
- learning
aliases:
  - Rao 與 Ballard 1999
  - 視覺皮質的預測編碼
  - 超古典感受野效應
---

# 視覺皮質的預測編碼（Rao 與 Ballard，1999）

Rao 與 Ballard（1999）提出，來自較高視覺區域的回饋連接攜帶對較低層活動的預測，前饋連接則攜帶殘差誤差。在他們於自然影像小塊上訓練的階層式網路中，特徵偵測器類似簡單細胞，而攜帶誤差的單元表現出終止（endstopping）等超古典感受野效應。這篇論文首次為皮質反應為何取決於古典感受野之外的脈絡，提供了明確的計算解釋。

本頁是[預測編碼與自由能原理](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

初級視覺皮質的神經元只對視野中的一小塊區域反應，也就是其古典感受野。它們的反應也會受到該區域之外的刺激調節，這種調節稱為超古典效應。問題在於這些效應有什麼用途，以及攜帶它們的回饋連接為何存在。

## 方法

作者建立了一個階層式網路，每一層保有對其輸入的估計，並向下一層送出預測。每一層的預測誤差，也就是該層輸入與其預測之差，被向上傳遞。網路從自然影像小塊學習權重，使預測隨時間減少誤差。

步驟如下：

1. 建立階層式網路，每一層保有對輸入的估計，並向下一層送出預測。
2. 在每一層計算殘差誤差，即該層的輸入與其預測之差。
3. 把誤差向上傳遞，並更新每一層的估計，使預測能減少誤差。
4. 在自然影像小塊上訓練連接權重，使網路學出一組特徵。

關鍵假設是誤差單元與預測單元是各自獨立的群體，因此模型能對哪些神經元應表現哪些效應，提出可檢驗的主張。

## 結果

摘要指出，訓練後的網路發展出類似簡單細胞的感受野，而一部分攜帶誤差的單元表現出終止與其他超古典效應。這些結果是定性的。摘要沒有給出模型與記錄神經元吻合程度的數值，因此本頁不引用任何數字。

## 限制

- 此模型是原理驗證，並非對記錄神經元的擬合，與特定反應性質的吻合是定性的。
- 論文將周邊效應歸因於皮質間的回饋。驗證這個主張需要後續的實驗。
- 網路使用線性生成模型與簡單的更新規則，大幅簡化了皮質。

## 與其他主題的關聯

- **學習規則**：後續以局部可塑性在預測編碼網路中近似反向傳播的研究，見 [Whittington 與 Bogacz（2017）](../whittington-bogacz-2017/index.md)。
- **綜述**：預測處理是皮質中重複出現的計算，這個主張由 Keller 與 Mrsic-Flogel（2018）提出，見[上層頁面](../index.md)。
- **視覺階層**：本模型所依據的腹側路徑與感受野背景，見[知覺與視覺系統](../../visual-perception/index.md)。
- **NeuroAI**：以預測目標與網路作為皮質模型的做法，見 [NeuroAI](../../neuroai/index.md)。

## 開放問題

- **誤差單元與預測單元是否為獨立群體？** 模型做了這個假設，而支持不同細胞類型的證據仍在收集中。
- **周邊效應有多少來自回饋？** 回饋與局部迴路機制都是候選，要區分兩者需要有針對性的實驗。

## 參考文獻

### 開創性論文

- Rao, R. P. N. & Ballard, D. H.（1999）。Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*。https://doi.org/10.1038/4580 — 提出回饋攜帶預測、前饋連接攜帶誤差，並顯示在自然影像上訓練的階層式網路會重現數種周邊效應。
- Whittington, J. C. R. & Bogacz, R.（2017）。An Approximation of the Error Backpropagation Algorithm in a Predictive Coding Network with Local Hebbian Synaptic Plasticity. *Neural Computation*。https://doi.org/10.1162/NECO_a_00949 — 顯示在適當參數下，具局部可塑性的預測編碼可近似反向傳播。
- Hubel, D. H. & Wiesel, T. N.（1962）。Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*。https://doi.org/10.1113/jphysiol.1962.sp006837 — 本論文所依據的古典感受野研究。（此參考文獻沿用自神經科學基礎頁面，本頁未重新檢驗。）

### 綜述與回顧

- Keller, G. B. & Mrsic-Flogel, T. D.（2018）。Predictive Processing: A Canonical Cortical Computation. *Neuron*。https://doi.org/10.1016/j.neuron.2018.10.003 — 主張預測處理是皮質各處重複出現的電路層級計算，並討論如何檢驗它。
- Friston, K.（2010）。The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*。https://doi.org/10.1038/nrn2787 — 提出大腦會最小化預測誤差，作為知覺、行動與學習的統一框架。（此參考文獻沿用自上層頁面，本頁未重新檢驗。）
