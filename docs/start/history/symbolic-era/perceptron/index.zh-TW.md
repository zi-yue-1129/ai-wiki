---
translation_reviewed: 2026-10-28
---

# 感知器與 Minsky–Papert 批判

感知器是一個由可訓練閾值單元組成的網路，由 Frank Rosenblatt 於 1958 年提出，作為大腦學習的模型。1969 年，Marvin Minsky 與 Seymour Papert 分析了單層此類單元無法計算的東西，這項分析常被解讀為讓神經網路研究停擺約十年。它是[符號時代](../index.md)中最主要的神經網路里程碑。

## 概述

Rosenblatt 的感知器從範例中學習。給定一個模式與其標籤，它會產生一個輸出；若輸出錯誤，就調整其數值權重。Rosenblatt 把它當作大腦如何組織資訊的理論來提出，而當時大多數 AI 研究都採用符號與規則。

這項批判來自 AI 內部，出自符號派的領導研究者之手，並指出單層感知器有固定的限制。之後的歷史學家認為，這本書的接受情形，以及隨之而來的神經網路研究長期低迷，反映的與其說是數學本身，不如說是符號 AI 日益增強的制度力量（Olazaran, 1996）。

## 關鍵概念

- **閾值單元（threshold unit）**：對輸入計算加權和並加上偏置，若和為正則輸出 1，否則輸出 0 的單元。
- **線性可分性（linear separability）**：若一條直線（或超平面）能把一組點與另一組點分置於兩側，兩組點便是線性可分的。單一閾值單元只能分類這樣的點集。
- **誤差修正學習（error-correction learning）**：只有在單元出錯時才改變權重，並朝減少目前這個範例誤差的方向調整。
- **單層（single layer）**：沒有隱藏層的網路，也就是批判所分析的架構。

## 運作方式

對於輸入 $\mathbf{x}$、權重 $\mathbf{w}$ 與偏置 $b$，單元的輸出為

$$
\hat{y} = \mathbf{1}\left[\mathbf{w}^\top \mathbf{x} + b > 0\right].
$$

訓練遵循一個對帶標籤範例 $(\mathbf{x}, y)$（$y \in \{0, 1\}$）的簡單迴圈：

1. 將權重與偏置設為零或小的數值。
2. 對每個範例，以目前的權重計算 $\hat{y}$。
3. 若 $\hat{y} \neq y$，更新 $\mathbf{w} \leftarrow \mathbf{w} + \eta\,(y - \hat{y})\,\mathbf{x}$ 與 $b \leftarrow b + \eta\,(y - \hat{y})$，其中 $\eta$ 為學習率。
4. 反覆掃過資料，直到沒有範例被誤分類，或達到最大掃描次數。

感知器收斂定理是線性分類器的標準結果，它說：若資料是線性可分的，此程序只會犯有限次錯誤，並以一條分隔線結束。若資料不可分，它則永遠不會收斂。

Minsky–Papert 的論證關心的是這個模型根本能表示什麼。互斥或（exclusive-or）函數在兩個輸入恰有一個為 1 時輸出 1，它不是線性可分的，因此沒有任何單層單元能計算它，而在同一層加入更多單元也無濟於事。要解決這類問題，需要一個隱藏層，以及訓練它的方法。

## 結果

Rosenblatt 1958 年的論文報告了一些實驗，網路能從範例學會分類簡單的視覺模式，而不需要手工撰寫的規則。這些證據是定性的。

Minsky 與 Papert 的證據是數學性的。他們證明了單層感知器能計算的範圍有限，互斥或是最簡單的例子。Block 1962 年的綜述更早從物理學讀者的角度分析過感知器，包括其學習行為與限制。

## 限制

- **線性限制。** 單層只能分開線性可分的類別，這是一個精確的限制，更多訓練也無法消除。
- **隱藏層沒有實用的規則。** 1960 年代沒有被廣泛採用的隱藏單元訓練規則，因此這項限制在實務上無法被克服。
- **過度解讀。** 這項批判常被簡化為「神經網路不可能成功」的證明。但數學所討論的只是一種架構（Olazaran, 1996）。

## 開放問題

- 為什麼對某一種架構的限制，會被解讀為整個方法的限制？這段歷史的爭論至今仍在進行。
- 單層的結果究竟延後了多層網路學習規則多久？Rumelhart、Hinton 與 Williams 1986 年關於反向傳播的論文，通常被視為轉折點。
- 誤差修正學習是否描述了大腦學習的任何部分？

## 關聯

感知器建立在 McCulloch 與 Pitts 1943 年把神經元視為閾值邏輯單元的模型之上，它也是今日標準多層[神經網路](../../../../theory/deep-learning/index.md)的祖先。至於生物面向，見[感受野](../../../../brain-mind/neuroscience/receptive-fields-hubel-wiesel/index.md)與 [NeuroAI](../../../../brain-mind/neuroai/index.md)。

## 參考文獻

### 開創性論文

- Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. *Psychological Review*. https://doi.org/10.1037/h0042519 — 介紹感知器，一種可訓練的閾值單元網路，被提出作為大腦如何儲存與組織資訊的模型。
- McCulloch, W. S. & Pitts, W. (1943). A logical calculus of the ideas immanent in nervous activity. *The Bulletin of Mathematical Biophysics*. https://doi.org/10.1007/BF02478259 — 把神經元建模為閾值邏輯單元，是感知器所建立的模型基礎。
- Minsky, M. & Papert, S. (2017). *Perceptrons*. MIT Press. https://doi.org/10.7551/mitpress/11301.001.0001 — 1988 年擴充版的再版，內容是 1969 年對感知器能計算什麼所做的分析，也是本文討論之批判的來源。
- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*. https://doi.org/10.1038/323533a0 — 描述透過反向傳播誤差來訓練具隱藏層的網路，這個方法回應了單層的限制。

### 綜述與教科書

- Block, H. D. (1962). The perceptron: A model for brain functioning. I. *Reviews of Modern Physics*. https://doi.org/10.1103/RevModPhys.34.123 — 從物理學讀者的角度，把感知器當作大腦功能的模型來綜述，並分析其學習行為與限制。

### 文章與文件

- Olazaran, M. (1996). A sociological study of the official history of the perceptrons controversy. *Social Studies of Science*. https://doi.org/10.1177/030631296026003005 — 探討 1969 年的批判如何被解讀為神經網路研究的終點，並主張制度性因素塑造了這種解讀。
