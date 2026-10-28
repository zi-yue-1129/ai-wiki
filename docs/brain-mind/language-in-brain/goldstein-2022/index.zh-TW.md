---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/llm
- theory/models/transformer
tags:
- neuroscience
- language
aliases:
  - Goldstein 2022
  - 人類與深度語言模型的共享計算原則
  - 語境嵌入與下一詞預測
---

# 人類與深度語言模型的共享計算原則（Goldstein 等人，2022）

Goldstein 等人（2022）探問：在真實聆聽時，自迴歸語言模型與人腦是否共享計算原則？還是相似只出現在最終預測上？他們在人們聆聽 podcast 時記錄皮質腦電圖（ECoG），並把神經訊號與 GPT-2 在三個性質上比較：字詞被聽到之前的預測、聽到之後的驚訝，以及每個詞的語境嵌入。兩者的吻合在語境嵌入上最強，並隨語境增長而提高。

本頁是[大腦中的語言](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

語言模型會預測下一個詞，聽者也會。未解的問題是：在自然語音中，大腦的預測與模型的預測是否逐詞吻合，而內部表徵是否也同樣吻合。先前的研究多半在句子或最終輸出上比較模型與大腦，因此吻合的時間結構並不清楚。

## 方法

九位受試者聆聽一段 30 分鐘的 podcast，同時以基於臨床需要而放置的電極記錄 ECoG。對每個詞，作者把三件事與 GPT-2 比較：人類對該詞的可預測性、聽到該詞之後的驚訝訊號，以及該詞的語境嵌入。他們也用 GloVe（一種靜態詞嵌入）作為基準。

步驟如下：

1. 收集人類受試者對每個詞的預測，並與 GPT-2 對同一詞的預測比較。
2. 測量每個電極的訊號對 GPT-2 嵌入與 GloVe 嵌入的編碼程度。
3. 檢驗詞彙起始前的神經活動能否預測即將出現的詞，以及起始後的活動是否追蹤驚訝程度。
4. 從神經訊號解碼詞彙身分，並比較不同嵌入類型的解碼表現。

第 2 步把語境嵌入與靜態嵌入區分開來。能編碼 GPT-2 的電極，可以逐位點與能編碼 GloVe 的電極相比。

## 結果

人類的可預測性與 GPT-2 的預測相關為 r = 0.79。吻合隨語境增加而提高，從兩個詞時的 r = 0.46，到約 100 個詞時的約 0.79。

GPT-2 語境嵌入在 208 個左半球電極與 34 個右半球電極上被編碼；左半球的位點中，有 71 個在 GloVe 下未被發現。以 GPT-2 嵌入解碼詞彙身分的平均 ROC-AUC 為 0.74，GloVe 為 0.68。對於未被預測的詞，起始後的活動在約 400 毫秒時達到高峰。

## 限制

- 研究只有九位受試者，個體之間的普遍性有限。
- 皮質腦電圖只能記錄臨床需要所在位置的電極，這限制了能研究的區域。
- 作者主張一個生物上可行的框架，但結果並未顯示大腦實際上實作了 Transformer。

## 與其他主題的關聯

- **方法家族**：以 Transformer 模型比較大腦反應的研究，也見於 [Schrimpf 等人（2021）](../schrimpf-2021/index.md)。後者使用句子上的 fMRI 與 ECoG，而非連續的 podcast。
- **模型家族**：本研究使用的自迴歸模型見[大型語言模型](../../../theory/models/llm/index.md)，Transformer 架構見 [Transformer](../../../theory/models/transformer/index.md)。
- **靜態嵌入**：研究中作為基準的 GloVe 是靜態詞嵌入，見 [Pennington 等人（2014）](https://aclanthology.org/D14-1162/)。
- **較早的框架**：用來解讀本研究所涉區域的路徑，見 [Hickok 與 Poeppel（2007）](../hickok-poeppel-2007/index.md)。

## 開放問題

- **這種吻合能否推廣到其他人與其他語言？** 九位受試者與一段 podcast，使普遍性仍然開放。
- **這種相似是機制性的嗎？** 表徵與預測的吻合是共享結構的證據，但不是共享計算的證據。

## 參考文獻

### 開創性論文

- Goldstein, A., Zada, Z., Buchnik, E., Schain, M., Price, A., 等人（2022）。Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*。https://doi.org/10.1038/s41593-022-01026-4 — 比較人類皮質腦電圖與 GPT-2 在預測、驚訝與語境嵌入上的反應，材料為一段 podcast。
- Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B. & Fedorenko, E.（2021）。The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*。https://doi.org/10.1073/pnas.2105646118 — 顯示效能最強的 Transformer 模型能預測句子神經反應中幾乎全部的可解釋變異。
- Pennington, J., Socher, R. & Manning, C. D.（2014）。GloVe: Global Vectors for Word Representation. *EMNLP*。https://aclanthology.org/D14-1162/ — 研究中作為基準的靜態詞嵌入。
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I.（2017）。Attention Is All You Need. *NeurIPS*。https://arxiv.org/abs/1706.03762 — 提出產生語境嵌入的 Transformer 架構。

### 文章與原始研究

- Caucheteux, C. & King, J.-R.（2022）。Brains and algorithms partially converge in natural language processing. *Communications Biology*。https://doi.org/10.1038/s42003-022-03036-1 — 比較語言模型表徵與大腦記錄，並報告兩者部分趨同。
- Hickok, G. & Poeppel, D.（2007）。The cortical organization of speech processing. *Nature Reviews Neuroscience*。https://doi.org/10.1038/nrn2113 — 為研究區域提供框架的雙路徑模型。
