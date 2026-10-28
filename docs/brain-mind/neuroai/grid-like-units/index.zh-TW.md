---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- navigation
- reinforcement learning
aliases:
  - 網格狀單元
  - Grid cells
  - Grid-like units
---

# 導航網路中的網格狀單元（Banino et al., 2018）

一個只為了導航而訓練的循環代理，會發展出放電形成空間上六角形網格的單元，類似哺乳動物內嗅皮質中的網格細胞。這個結果顯示，網格狀編碼可能只因導航的需求就會出現。

本頁屬於[NeuroAI](../index.md)。它詳細說明一種方法。

## 概述

動物靠著對自身位置的內在感知找到路。在大鼠的大腦中，內嗅皮質的網格細胞會在許多位置放電，而這些位置排列成規律的六角形圖樣。Banino 等人問的是：一個被訓練來導航的神經網路，是否也會學到類似的編碼，而且不需要有人告訴它這麼做。

## 核心概念

- **網格細胞（grid cell）**：在環境中多個位置放電的神經元，這些位置排列成規律的三角形或六角形格點。
- **路徑積分（path integration）**：透過隨時間累積自身運動訊號（例如速度），來估計位置。
- **向量式導航（vector-based navigation）**：利用對目標方向與距離的儲存表徵，找到通往目標的路。
- **循環代理（recurrent agent）**：隱藏狀態會把資訊從一個時間步傳到下一步的網路，因此能隨時間整合運動。

## 問題

只為導航而訓練的網路，是否會出現網格狀表徵？大腦用網格狀表徵來表示位置。先前的模型是在設計時就把網格圖樣寫入模型。問題在於：這種圖樣能否從任務本身自然出現。

## 核心想法

以強化學習訓練一個循環代理，讓它在虛擬環境中，依速度與視覺輸入導航到目標位置。論文報告，網格狀單元會在代理的隱藏層中自行出現，而不是預先內建。作者也顯示，具這種結構的單元能幫助代理以向量方式導航，而網格式編碼正是讓這種導航成為可能的原因。

## 方法

1. 從模擬環境給代理速度與視覺輸入。
2. 以強化學習訓練它到達目標位置。
3. 檢查它的隱藏單元，看在整個環境中是否出現六角形的放電圖樣。
4. 測試它能否導航到新位置上的目標。

## 結果

論文報告，代理隱藏單元中有一部分具有網格狀放電，其規律的格點與生物網格細胞相似。論文也報告，代理能以向量方式導航到目標，而網格式編碼支持這種導航。這些結果來自模擬環境與特定的架構，論文並未給出單一的基準分數。

## 限制

- **簡單、人工的環境。**代理與其環境都很簡單，因此這個結果並不能顯示網格式編碼如何推廣到自然的導航。
- **設計選擇很重要。**網路架構、輸入與訓練設定，都會影響網格狀單元是否會出現；不同的設計可能不會產生它們。
- **生物學並未完全重現。**生物網格細胞與其他空間細胞並存，例如方向細胞與邊界細胞，而本研究並未直接處理這些細胞。

## 與其他主題的關聯

- **空間認知**：這個問題的生物學面向，以及相關的位置細胞與網格細胞，見[神經科學基礎](../../neuroscience/index.md)。
- **強化學習**：代理以強化學習訓練，此框架見[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)。
- **效能最佳化網路**：一種比較訓練後網路與大腦資料的相關 NeuroAI 方法，見[效能最佳化網路預測視覺皮質](../performance-optimised-networks/index.md)。

## 應用

- **機器人與導航**：網格狀表徵被研究作為一種精簡的位置編碼，用於移動機器人與代理的路徑規劃。
- **神經科學假說**：訓練後的網路提供了一個可檢驗的模型，說明網格式編碼可能如何出現，之後可由實驗加以驗證。

## 開放問題

- **哪些訓練壓力會產生網格式編碼？**論文展示了一組條件，其一般規則尚未確立。
- **網格細胞如何與大腦中其他空間細胞互動？**包含方向與邊界訊號的模型，是活躍的研究領域。
- **人工網格單元在細節上是否與生物一致？**可以把模型單元的格點間距與放電性質，與記錄到的網格細胞相比較，這項比較仍在進行。

## 參考文獻

### 開創性論文

- Banino, A., et al.（2018）。Vector-based navigation using grid-like representations in artificial agents. *Nature*。https://doi.org/10.1038/s41586-018-0102-6 — 顯示一個被訓練來導航的循環代理會出現網格狀單元，且此編碼支持向量式導航。
- Yamins, D. L. K., et al.（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*。https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識訓練的深度網路，能預測高階視覺皮質的神經反應，是比較訓練後網路與大腦資料的早期例子。

### 綜述與回顧

- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M.（2017）。Neuroscience-Inspired Artificial Intelligence. *Neuron*。https://doi.org/10.1016/j.neuron.2017.06.011 — 關於神經科學如何啟發 AI，以及 AI 如何檢驗大腦假說的經典回顧。
- Richards, B. A., et al.（2019）。A deep learning framework for neuroscience. *Nature Neuroscience*。https://doi.org/10.1038/s41593-019-0520-2 — 主張透過目標函數、學習規則與架構來研究大腦。
- Schrimpf, M., et al.（2021）。The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*。https://doi.org/10.1073/pnas.2105646118 — 顯示預測下一個詞的語言模型能預測語言網路的大腦反應，而預測得越好，與大腦的吻合度也越高。
