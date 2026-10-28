---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- brain-mind/neuroscience
tags:
- neuroscience
- learning
aliases:
  - Whittington 與 Bogacz 2017
  - 預測編碼近似反向傳播
  - 預測編碼中的局部赫柏式學習
---

# 預測編碼近似反向傳播（Whittington 與 Bogacz，2017）

Whittington 與 Bogacz（2017）顯示，具有明確預測誤差單元的預測編碼網路，只需局部的赫柏式可塑性，就能近似誤差反向傳播演算法。每個突觸的改變只取決於它所連接的兩個神經元，以及局部的預測誤差，而不依賴遠端神經元的資訊。在適當的參數設定下，權重更新與反向傳播的一致，該網路在 MNIST 手寫數字辨識上的表現也與標準網路相近。

本頁是[預測編碼與自由能原理](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

反向傳播是有效的學習演算法，但它的權重更新依賴於沿網路向後傳遞的誤差訊號。真實的突觸無法取得遠端神經元的活動，因此反向傳播很難與已知的皮質迴路相容。問題在於：一個具生物合理性、使用局部學習的網路，能否得到相同的權重更新。

## 方法

作者使用預測編碼網路，其中每一層都有預測誤差單元，編碼該層活動與其由上層所作預測之間的失配。學習由這些誤差驅動，每個突觸的改變只使用它所連接的兩個神經元。

步驟如下：

1. 固定輸入與輸出層，讓隱藏層活動收斂，使預測誤差最小化。
2. 只用突觸兩端神經元的活動與局部預測誤差來更新該突觸。
3. 對訓練樣本重複。在適當的參數設定下，權重變化與反向傳播的一致。

第 1 步使此方案具有局部性。隱藏層的活動完成了反向傳播中向後傳遞所做的工作，而誤差在每一層都可直接取得，無需從他處傳來。

## 結果

作者顯示，在適當的參數下，權重更新收斂到反向傳播的更新。在這些條件下，該網路在 MNIST 手寫數字辨識上的表現與標準網路相近。

## 限制

- 吻合依賴參數選擇，只在特定設定下成立。
- 作者認為大腦很可能不會精確實作反向傳播，因為真實訊號在多個層級都有雜訊。這個結果是對該演算法的近似，並非皮質實際實作它的證據。
- 基準規模很小。本論文並未證明在大型深度網路上，此方法能與反向傳播相當。

## 與其他主題的關聯

- **視覺預測編碼**：皮質反應的原始預測編碼解釋，見 [Rao 與 Ballard（1999）](../rao-ballard-1999/index.md)。
- **綜述**：預測處理是皮質中重複出現的計算，這個主張見上層頁面所引的 Keller 與 Mrsic-Flogel（2018）。
- **NeuroAI**：反向傳播的生物合理替代方案，以及它們與深度網路的比較，見 [NeuroAI](../../neuroai/index.md)。
- **神經科學背景**：多巴胺的預測誤差訊號，是另一個系統中以誤差為基礎的學習規則，見[神經科學基礎](../../neuroscience/index.md)。

## 開放問題

- **皮質是否實作這些誤差單元？** 模型是一個候選迴路，而獨立的誤差與預測群體需要直接的證據。
- **這個近似在大規模下是否成立？** 小型基準上的結果令人鼓舞，但尚未證明大型網路在局部學習下能與反向傳播相當。

## 參考文獻

### 開創性論文

- Whittington, J. C. R. & Bogacz, R.（2017）。An Approximation of the Error Backpropagation Algorithm in a Predictive Coding Network with Local Hebbian Synaptic Plasticity. *Neural Computation*。https://pmc.ncbi.nlm.nih.gov/articles/PMC5467749/ — 顯示在適當參數下，具局部可塑性的預測編碼可近似反向傳播。
- Rao, R. P. N. & Ballard, D. H.（1999）。Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*。https://pubmed.ncbi.nlm.nih.gov/10195184/ — 本網路所延伸的階層式預測編碼模型，回饋攜帶預測、前饋連接攜帶誤差。

### 綜述與回顧

- Keller, G. B. & Mrsic-Flogel, T. D.（2018）。Predictive Processing: A Canonical Cortical Computation. *Neuron*。https://pmc.ncbi.nlm.nih.gov/articles/PMC6400266 — 主張預測處理是皮質各處重複出現的電路層級計算，並討論如何檢驗它。
- Friston, K.（2010）。The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*。https://pubmed.ncbi.nlm.nih.gov/20068583/ — 提出大腦會最小化預測誤差，作為知覺、行動與學習的統一框架。
- Clark, A.（2013）。Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*。https://pubmed.ncbi.nlm.nih.gov/23663408/ — 將預測處理視為知覺、行動與認知的統一框架的回顧。
