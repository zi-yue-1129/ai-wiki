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
  - Schrimpf 2021
  - 語言的神經架構
  - 語言的整合建模
---

# 語言模型預測大腦對句子的反應（Schrimpf 等人，2021）

Schrimpf 等人（2021）探問：語言模型的哪些計算特徵，能解釋人腦對句子的反應？他們對許多 Transformer 模型評分，看其內部表徵預測神經反應的能力，結果發現效能最強的模型能解釋幾乎全部的可解釋變異。大腦擬合度比其他語言任務的表現更貼近下一詞預測的準確度，作者據此主張支持預測處理的觀點。

本頁是[大腦中的語言](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

語言模型與人類聽者都處理句子，但在語言任務上表現良好的模型，未必以與大腦相同的方式處理句子。問題在於：模型的哪些性質（若有的話）能預測其表徵與神經反應的吻合程度，而這些性質是否正是它能預測詞彙的原因。

## 方法

作者把同一批句子呈現給人類受試者與一組 Transformer 語言模型。神經反應以功能性磁振造影（fMRI）與皮質腦電圖（ECoG）記錄，並為相同的句子擷取每個模型的內部激活。

步驟如下：

1. 把同一批句子呈現給人類受試者與一組 Transformer 語言模型。
2. 以 fMRI 與 ECoG 記錄大腦反應，並擷取每個模型的內部激活。
3. 從模型激活到大腦反應做迴歸擬合，測量它能解釋多少可解釋的變異。
4. 把每個模型的大腦擬合度，與其下一詞預測準確度及其他語言任務分數相互對照。

第 4 步是關鍵的比較。它把追蹤大腦的性質，與模型可能具有的許多其他性質區分開來。

## 結果

效能最強的模型，能預測跨資料集與兩種影像模態下，句子神經反應中幾乎 100% 的可解釋變異。大腦擬合與行為擬合都與下一詞預測準確度強烈相關；它們並未追蹤其他語言任務的表現，作者將此視為支持預測處理的證據。

## 限制

- 可解釋變異取決於各資料集的雜訊上限，因此這個數字是相對於該上限，而非對擬合度的絕對測量。
- 結果顯示的是預測與大腦擬合之間的相關，並不表示大腦實作了相同的機制。
- 模型架構也明顯影響擬合程度。作者將其視為另一個獨立因素，這表示預測準確度並非唯一重要的事。

## 與其他主題的關聯

- **方法家族**：以語言模型比較大腦反應的研究，也見於 [Goldstein 等人（2022）](../goldstein-2022/index.md)。後者採用不同的記錄方法，並提出更偏向時間性的問題。
- **語言網路**：本研究中的反應來自語言網路，論文依賴 [Fedorenko 等人（2010）](https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923)的定位方法。
- **模型家族**：比較中使用的 Transformer 架構見 [Transformer](../../../theory/models/transformer/index.md)，語言模型家族見[大型語言模型](../../../theory/models/llm/index.md)。
- **較早的框架**：用來解讀本研究所涉區域的皮質路徑，見 [Hickok 與 Poeppel（2007）](../hickok-poeppel-2007/index.md)。

## 開放問題

- **是預測解釋了擬合，還是只是相關？** 與下一詞準確度的相關很強，但要建立因果關係，需要對模型進行介入。
- **結果能否推廣到這些資料集之外？** 雜訊上限與記錄位點都是各研究特有的，跨研究比較需要謹慎。

## 參考文獻

### 開創性論文

- Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B. & Fedorenko, E.（2021）。The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*。https://doi.org/10.1073/pnas.2105646118 — 顯示效能最強的 Transformer 模型能預測句子神經反應中幾乎全部的可解釋變異。
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I.（2017）。Attention Is All You Need. *NeurIPS*。https://arxiv.org/abs/1706.03762 — 提出本研究所比較模型使用的 Transformer 架構。
- Hickok, G. & Poeppel, D.（2007）。The cortical organization of speech processing. *Nature Reviews Neuroscience*。https://doi.org/10.1038/nrn2113 — 提供研究區域的皮質架構背景的雙路徑模型。
- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S. & Kanwisher, N.（2010）。New method for fMRI investigations of language: defining ROIs functionally in individual subjects. *Journal of Neurophysiology*。https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923 — 本研究所用的個人層級語言網路定位方法。

### 文章與原始研究

- Goldstein, A., Zada, Z., Buchnik, E., Schain, M., Price, A., 等人（2022）。Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*。https://doi.org/10.1038/s41593-022-01026-4 — 比較人類皮質腦電圖與 GPT-2 在預測、驚訝與語境嵌入上的反應，材料為一段 podcast。
- Caucheteux, C. & King, J.-R.（2022）。Brains and algorithms partially converge in natural language processing. *Communications Biology*。https://doi.org/10.1038/s42003-022-03036-1 — 比較語言模型表徵與大腦記錄，並報告兩者部分趨同。
