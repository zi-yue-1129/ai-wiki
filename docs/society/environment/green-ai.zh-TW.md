---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Green AI
  - 綠色 AI
  - 以效率作為評估標準
---

# 綠色 AI（Schwartz 等人，2019）

!!! info "屬於 AI 的環境影響"
    本方法頁隸屬於 [AI 的環境影響](index.zh-TW.md)。它詳細說明一項主張；上層頁面則將它與其他做法並列比較。

Schwartz、Dodge、Smith 與 Etzioni（2019）主張，效率應與準確度並列，成為 AI 研究的評估標準。他們稱之為「綠色 AI」，與之相對的是幾乎不計算力耗費、只追求準確度的研究。這篇論文是一篇立場文章：它提出的是研究成果應如何報告與評斷的改變，而不是一個新演算法。

## 問題

深度學習研究所用的運算量成長非常快，實驗的碳足跡與財務成本也隨之增加。多數論文報告準確度，卻沒有報告得出這個準確度所花的成本。一個靠大量運算提高準確度的方法看起來是進步，而一個花費較少、準確度相當的方法卻看不出優勢。預算有限的研究者，也因為負擔不起比較所需的實驗而被排除在外。

## 核心想法

讓效率成為評估的一部分，而不是註腳。報告開發、訓練與執行模型的價格標籤，讓結果的成本與準確度並列可見。一旦報告了成本，效率較高的方法就有了可以比較的基準，並能被視為本身就是改進。

## 主張如何運作

1. **報告成本。** 說明開發、訓練與執行模型的財務價格標籤。
2. **把效率列為評估標準。** 與準確度及相關指標一併評估結果的效率。
3. **依成本設定基準。** 在相近的成本下比較方法，讓較便宜的方法能被證明與昂貴的方法表現相當。
4. **降低門檻。** 讓運算資源有限的研究者也能參與比較。

摘要描述了這些要素。具體的效率指標應如何定義，則留給各領域決定。

## 結果

作為立場文章，綠色 AI 本身沒有實驗。摘要指出，深度學習研究所用的運算量在 2012 至 2018 年間成長約 30 萬倍，並以此作為提出主張的理由。它的影響，最好從之後出現的報告做法來看，例如[訓練能源成本](training-energy-cost.zh-TW.md)與[排放計算器](emissions-calculator.zh-TW.md)頁面中的估算。

## 限制

- **沒有單一指標。** 只有當成本指標能在不同硬體、不同雲端與不同年份之間比較時，報告成本才有用。論文並未決定哪一種指標應成為標準。
- **報告不等於減量。** 要求報告效率本身並不會降低排放，成效取決於人們是否使用這些數字。
- **誘因。** 評估標準會塑造研究者的追求，新的標準也可能被操弄，或擠壓其他目標。

## 與其他主題的連結

- 使成本可見的估算，見[訓練能源成本](training-energy-cost.zh-TW.md)頁面。
- 隨每次實驗一併報告能源與排放的具體做法，見[能源與排放的報告](reporting-framework.zh-TW.md)頁面。
- 降低訓練成本的方法，見[節能訓練](energy-efficient-training.zh-TW.md)。

## 開放問題

- 一個領域應採用哪一種效率指標作為標準評估項目？
- 在不同硬體上執行的方法，應如何比較效率？
- 學術發表場所是否會把效率列為評估的必要部分？

## 參考資料

### 開創性論文

- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — 本頁所述的立場文章，主張效率應與準確度並列為評估標準。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — 估算訓練 NLP 模型的成本，為這項主張提供具體數字。
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — 提出隨每次實驗報告能源與排放的實際做法。
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — 顯示模型、資料中心與處理器的選擇如何改變碳足跡，正是綠色 AI 所要求的比較。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — 讓任何研究者都能取得排放估算的計算工具。
