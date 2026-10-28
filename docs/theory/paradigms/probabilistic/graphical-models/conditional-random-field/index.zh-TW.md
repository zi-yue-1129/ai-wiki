---
translation_reviewed: 2026-10-28
---

# 條件隨機場

條件隨機場（conditional random field, CRF）是一種無向圖模型，定義在給定觀測輸入下某個標籤序列的機率。在神經網路取代之前，它是自然語言處理中標註序列的主要方法之一，也是[機率圖模型](../index.md)涵蓋的方法之一。

## 概述

序列標註是為輸入中的每個位置指定一個標籤，例如詞性標註、淺層剖析與命名實體辨識。[隱馬可夫模型](../hidden-markov-model/index.md)透過建模標籤如何產生詞來解決這類問題，這是生成式任務。CRF 則直接在給定詞的條件下建模標籤。輸入是被條件化的，而不是被生成的，因此模型可以使用輸入中彼此重疊、不獨立的特徵，例如大小寫、字尾與相鄰的詞，而不必對這些特徵的分布建模。

Sha 與 Pereira（2003）顯示，在 CoNLL-2000 分塊資料上訓練的 CRF，與當時已報告的最佳結果相當。這個方法也是 HMM 鏈的判別式對應。在線性鏈的情況下，其依賴結構與 HMM 相同，但訓練目標是判別式的。

## 核心概念

- **線性鏈 CRF**：標籤序列 \(y_1,\dots,y_T\) 上的無向鏈，每個標籤連到輸入 \(x\) 與其相鄰標籤。
- **特徵函數** \(f_k(y_{t-1}, y_t, x, t)\)：相鄰標籤、輸入與位置的實值函數。特徵可以重疊，也可以依賴整個輸入。
- **權重** \(\lambda_k\)：學到的特徵重要性。
- **配分函數** \(Z(x)\)：對所有標籤序列的求和，以前向演算法計算。

## 運作方式

標籤序列的條件分布為

\[
p(y \mid x) = \frac{1}{Z(x)}\exp\Big(\sum_{t}\sum_{k}\lambda_k\, f_k(y_{t-1}, y_t, x, t)\Big),
\]

其中 \(Z(x)\) 是對所有標籤序列 \(y'\) 求和的同一式子。訓練會最大化標註資料的條件對數概似。每個權重的梯度，是資料中觀測到的特徵計數與模型下其期望值之差：

\[
\frac{\partial \ell}{\partial \lambda_k} = \sum_{i}\sum_{t} f_k\big(y^{(i)}_{t-1}, y^{(i)}_t, x^{(i)}, t\big) - \sum_{i}\mathbb{E}_{p(y\mid x^{(i)})}\Big[\sum_{t} f_k(y_{t-1}, y_t, x^{(i)}, t)\Big].
\]

期望值是透過沿鏈的前向與後向遍歷計算的，成本與一次 HMM 遍歷相同。程序如下：

1. 依輸入與標籤集合定義特徵函數。
2. 執行前向與後向遍歷，計算 \(Z(x)\) 與期望特徵計數。
3. 以基於梯度的最佳化器更新權重，通常是 L-BFGS 或共軛梯度法。
4. 預測時，使用 Viterbi 演算法找出最可能的標籤序列。

## 實驗結果

Sha 與 Pereira（2003）在 CoNLL-2000 共享任務的名詞片語分塊上評估，最佳模型使用約 380 萬個特徵。他們的 CRF 達到 94.38% 的 F 分數。這與 Kudo 與 Matsumoto 的 SVM 組合（94.39%）接近，並高於最大熵馬可夫模型（93.70%）。[^1] 在他們的檢定下，CRF 與 SVM 的差異不具統計顯著性，而 CRF 與 MEMM 的差異則具顯著性。在較小的特徵集上，L-BFGS 花 84 分鐘達到目標訓練目標，而預條件共軛梯度法需要 130 分鐘。

後來的神經系統保留了 CRF 層。Ma 與 Hovy（2016）結合字元層級的 CNN、雙向 LSTM 與 CRF，報告在 Penn Treebank 詞性標註上達到 97.55% 的準確率，在 CoNLL 2003 命名實體辨識上達到 91.21 的 F1。Huang 等人（2015）報告，在詞性標註、分塊與命名實體資料上，準確率達到最先進水準或接近，並使用過去與未來的輸入。

## 限制

- **局部結構。**線性鏈只建模相鄰標籤之間的依賴。較長距離的標籤依賴需要更複雜的圖，會使推論更困難。
- **特徵工程。**經典 CRF 依賴大量人工設計的特徵集。淺層剖析系統使用了約 380 萬個特徵。
- **訓練成本。**每一步梯度都需要對每個訓練序列執行前向與後向遍歷。
- **沒有輸入模型。**CRF 無法說明一個輸入有多可能出現，因此既不能生成資料，也無法標記不尋常的輸入。

## 開放問題

- 在大型預訓練編碼器之上，CRF 層是否仍有價值，還是編碼器會自行學到標籤依賴？
- 標籤結構能在多大程度上擴展到鏈以外，例如樹或圖，同時又不使推論變得難以處理？

[^1]: F 分數取自 Sha 與 Pereira（2003）的表 2，顯著性檢定取自其表 4。

## 參考文獻

### 開創性論文

- Sha, F. & Pereira, F. (2003). Shallow Parsing with Conditional Random Fields. *NAACL-HLT*. https://aclanthology.org/N03-1028/ — 顯示 CRF 在 CoNLL-2000 名詞片語分塊任務上與已報告的最佳結果相當，且比 MEMM 更準確。

### 綜述與教科書

- Sutton, C. & McCallum, A. (2010). *An Introduction to Conditional Random Fields*. arXiv. https://arxiv.org/abs/1011.4088 — 面向結構化預測的 CRF 教學文章，包括推論與參數估計，寫給不具圖模型背景的讀者。

### 文章與文件

- Ma, X. & Hovy, E. (2016). *End-to-end Sequence Labeling via Bi-directional LSTM-CNNs-CRF*. arXiv. https://arxiv.org/abs/1603.01354 — 結合字元與詞彙表示、雙向 LSTM 與 CRF 層，並報告詞性標註與命名實體辨識的結果。
- Huang, Z., Xu, W. & Yu, K. (2015). *Bidirectional LSTM-CRF Models for Sequence Tagging*. arXiv. https://arxiv.org/abs/1508.01991 — 比較 LSTM、雙向 LSTM 與 CRF 輸出模型的序列標註效果，並發現雙向 LSTM-CRF 較不依賴詞嵌入。
- Collins, M. (2002). Discriminative Training Methods for Hidden Markov Models: Theory and Experiments with Perceptron Algorithms. *EMNLP 2002*. https://aclanthology.org/W02-1001/ — 判別式訓練標註模型的替代方法，以感知器式更新取代最大熵與 CRF 訓練，並在標註與分塊上進行實驗。
