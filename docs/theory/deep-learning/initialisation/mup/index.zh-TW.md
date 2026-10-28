---
translation_reviewed: 2026-10-28
---

# 最大更新參數化（muP）

最大更新參數化（muP）是一套規則，規定初始化尺度與各層學習率應如何隨網路寬度改變，使網路變大時，每一層都以相近的速度學習。Yang 與 Hu 於 2021 年在無限寬網路的研究中提出此方法。它的實際用途是超參數遷移：在小模型上調好的學習率，可以直接用於大得多的模型。它是上層[權重初始化](../index.md)頁面中所比較的方法之一。

## 概述

實務上，人們通常依據某一模型大小的經驗，選擇每一層的初始化方式（例如 He 或 Glorot），並設定一個整體的學習率。模型變寬時，最佳學習率通常會移動，因此每個模型大小都需要各自搜尋，而對最大的模型來說，這樣的搜尋成本過高。

Yang 與 Hu（2021）探討寬度趨於無限時，訓練會有什麼變化。他們證明，標準參數化與神經正切核（NTK）參數化，都不存在能讓特徵學習的無限寬極限。在標準參數化中，隨著寬度增加，不同層的更新會變得不平衡。他們提出一種修改後的參數化，使每一層的更新大小保持可比。Yang 等人（2022）在 Tensor Programs V 中顯示，在此參數化下，許多最佳超參數會隨模型成長而保持穩定，因此可以在小模型上調整，再把結果遷移到大模型。

## 關鍵概念

- **標準參數化（SP）。** 常見框架的預設設定：初始變異數與扇入的倒數成正比，學習率不隨寬度而變。
- **特徵學習。** 隱藏表徵在訓練中大幅改變的學習方式。在標準與 NTK 參數化的無限寬極限中，隱藏特徵不會改變。
- **muTransfer。** 在 muP 下於小模型上調整，再把設定遷移到較大的模型。

## 運作方式

此規則規定每個參數的初始變異數與學習率如何隨寬度縮放。對於 Adam 最佳化器，Yang 等人（2022）給出以下的縮放方式，其中 \(\text{fan\_in}\) 為該層的輸入數：

| 參數類型 | 初始變異數（muP） | Adam 學習率（muP） |
|---|---|---|
| 輸入權重與偏置 | \(1/\text{fan\_in}\) | 不隨寬度改變 |
| 隱藏權重 | \(1/\text{fan\_in}\) | \(1/\text{fan\_in}\) |
| 輸出權重 | \(1/\text{fan\_in}^2\) | \(1/\text{fan\_in}\) |

在標準參數化中，隱藏層的學習率不隨寬度改變，這正是不平衡的來源。隱藏層的初始化與 He 初始化所用的扇入縮放相同，因此主要的改變在輸出層與學習率。對於 Transformer，論文另外把注意力的 logits 以 \(1/d_{\text{head}}\) 而非 \(1/\sqrt{d_{\text{head}}}\) 縮放。論文的表格為 SGD 與 Adam 分別列出學習率，因為兩者的縮放方式不同。

muTransfer 的程序如下：

1. 以 muP 參數化撰寫目標模型。
2. 以相同架構但不同寬度訓練數個小模型，並在其上調整學習率與其他超參數。
3. 以小模型上的最佳設定訓練大模型，而不直接調整大模型。

在 Tensor Programs V 中，以此方式找到的最佳設定在不同寬度間保持穩定，而在標準參數化下，最佳值會移動。

## 結果

以下數字為論文本身的結果，取自其摘要。Yang 等人（2022）在 Transformer 與 ResNet 上驗證了 muTransfer。將一個 1,300 萬參數模型的預訓練超參數遷移過來，所得結果超過了已發表的 BERT-large（3.5 億參數）數字，而總調整成本等同於預訓練一次 BERT-large。從一個 4,000 萬參數的模型遷移，則超過了已發表的 67 億參數 GPT-3 數字，調整成本約為總預訓練成本的 7%。

Yang 與 Hu（2021）也報告，他們的極限在 Word2Vec 以及 Omniglot 上以 MAML 進行的少樣本學習中，優於 NTK 基準與有限寬網路；這兩項任務都依賴特徵學習。

## 限制

- **理論處理的是寬度。** 跨深度的遷移不在同一論證的範圍內，論文的規則也未解決此問題。
- **極限是無限的，實務是有限的。** 規則是在寬度趨於無限時推導的，其在有限寬度下的準確性是以實驗顯示，而非證明。
- **與架構和最佳化器有關。** Transformer 需要改變注意力的縮放，而且 SGD 與 Adam 的縮放方式不同，為其中一種推導的設定不能直接套用到另一種。
- **並非所有超參數都涵蓋。** 論文的遷移實驗主要著眼於學習率、初始化尺度與乘數。其他設定需要另外檢驗。

## 開放問題

- 是否存在對應於深度的 muP 類比，能同時遷移寬度與深度的設定。
- 無限寬分析所報告的特徵學習優勢，是否也適用於實務中的模型與任務，而不僅限於論文中的例子。
- muP 如何與正規化層互動。正規化層會移除參數化所控制的部分尺度依賴。

## 參考文獻

### 開創性論文

- Yang, G. & Hu, E. J. (2021). *Feature Learning in Infinite-Width Neural Networks*. arXiv. https://arxiv.org/abs/2011.14522 — 顯示標準與 NTK 參數化沒有能讓特徵學習的無限寬極限，並提出最大更新參數化。
- Yang, G., Hu, E. J., Babuschkin, I., Sidor, S., Liu, X., Farhi, D. et al. (2022). *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*. arXiv. https://arxiv.org/abs/2203.03466 — 提出 muTransfer，在小模型上調整超參數，再將其遷移到大型 Transformer 與 ResNet。
- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — 標準化初始化，是一種以扇入為基礎的縮放，標準參數化即採用這類縮放。
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — 推導整流網路的扇入縮放初始化，muP 對隱藏層保留的正是這種縮放。
- Lee, J., Bahri, Y., Novak, R., Schoenholz, S. S., Pennington, J. & Sohl-Dickstein, J. (2018). *Deep Neural Networks as Gaussian Processes*. arXiv. https://arxiv.org/abs/1711.00165 — 證明無限寬的深度網路等價於高斯過程，即標準參數化在寬度很大時所達到的核體制。
