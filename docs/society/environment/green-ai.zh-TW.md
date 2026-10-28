---
translation_reviewed: 2026-10-28
---

# 綠色 AI（Schwartz 等人，2019）

!!! info "屬於「AI 的環境影響」"
    本方法頁隸屬於[AI 的環境影響](index.zh-TW.md)。它詳細說明一項提案；上層頁面則比較各項提案。

Schwartz、Dodge、Smith 與 Etzioni（2019，2020 年正式發表）主張，效率應與準確度並列，作為 AI 研究的評估標準。他們稱此為*綠色 AI*，以對照那些一味追求準確度、不顧運算需求的研究。此文是立場文章：它提出的是改變研究的報告與評斷方式，而非一種新演算法。

## 問題

深度學習研究所用的運算量成長非常快，實驗的碳足跡與財務成本也隨之上升。摘要引述的估計顯示，2012 至 2018 年間的運算量增加了約 30 萬倍。多數論文只報告準確度，而不報告取得該準確度的成本。一個靠大量運算換取準確度的方法看起來像是進步，而一個同樣準確但較便宜的方法卻沒有明顯的優勢。預算有限的研究者，也被排除在他們負擔不起的比較之外。

## 核心概念

讓效率成為評估的一部分，而不是註腳。報告開發、訓練與執行一個模型的價格標籤，使結果的成本與準確度並列可見。一旦成本被報告，高效方法就有了可以對照的基準，並能被視為本身即是進步。

## 提案的運作方式

1. **報告成本。** 說明開發、訓練與執行模型的價格標籤。
2. **把效率列為評估標準。** 在準確度與相關指標之外，同時評斷效率。
3. **依相近成本比較。** 以成本設定基準，使較便宜的方法能被證明可以匹敵昂貴的方法。
4. **降低門檻。** 讓運算資源有限的研究者也能參與比較，作者認為這會讓 AI 更具包容性。

論文將具體的效率指標如何定義留給整個領域。

## 結果

作為立場文章，綠色 AI 本身沒有實驗。它的影響最好從之後形成的報告做法來理解，例如[訓練能源成本](training-energy-cost.zh-TW.md)與[機器學習排放計算器](emissions-calculator.zh-TW.md)頁面的估算，以及[能源與排放的報告](reporting-framework.zh-TW.md)頁面中，在實驗執行期間記錄能源的追蹤工具。

## 限制

- **沒有單一的衡量標準。** 只有當衡量標準能跨硬體、雲端與年份比較時，報告成本才有用。論文並未決定哪一種應成為標準。
- **報告不等於減量。** 要求報告效率本身不會降低排放，效果取決於人們是否使用這些數字。
- **誘因。** 評估標準會塑造研究者的追求。新的標準可能被操弄，也可能排擠其他目標。

## 與其他頁面的連結

- 讓成本變得可見的估算，見[訓練能源成本](training-energy-cost.zh-TW.md)頁面。
- 隨每次實驗報告能源與碳排的具體做法，見[能源與排放的報告](reporting-framework.zh-TW.md)頁面。
- 降低訓練成本的方法，見[節能訓練](energy-efficient-training.zh-TW.md)。

## 開放問題

- 領域應採用哪一種效率衡量作為標準評估指標？
- 在不同硬體上執行的方法，效率應如何比較？
- 學術期刊與會議是否會把效率列為評估的必要部分？

## 參考文獻

### 開創性論文

- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2020). Green AI. *Communications of the ACM*, 63(12), 54–63. doi:[10.1145/3381831](https://doi.org/10.1145/3381831) — 本頁所述的立場文章，主張效率應與準確度並列作為評估標準。預印本：https://arxiv.org/abs/1907.10597
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — 估算訓練 NLP 模型的成本，使論點有了具體數字。
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248)。https://www.jmlr.org/papers/v21/20-312.html — 隨每次實驗報告能源與碳排的一種實用方法。
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv 預印本。https://arxiv.org/abs/2104.10350 — 顯示模型、資料中心與處理器的選擇如何改變足跡，正是綠色 AI 所要求的比較。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv 預印本。https://arxiv.org/abs/1910.09700 — 讓任何研究者都能取得排放估算的計算器。
