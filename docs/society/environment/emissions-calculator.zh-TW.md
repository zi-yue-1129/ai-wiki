---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - 機器學習排放計算器
  - Machine Learning Emissions Calculator
---

# 機器學習排放計算器（Lacoste 等人，2019）

!!! info "屬於 AI 的環境影響"
    本方法頁隸屬於 [AI 的環境影響](index.zh-TW.md)。它詳細說明一項計算工具；上層頁面則將它與其他工具並列比較。

Lacoste 等人（2019）推出了機器學習排放計算器，這是一個用來估算訓練機器學習模型所排放碳量的工具。它把研究者容易記錄的少數輸入，轉換為排放估算，使這個數字能隨實驗一併報告。

## 問題

研究者很少報告實驗排放了多少碳，部分原因是若沒有專業資料，這個數字很難估算。一個簡單而透明的計算工具，能讓每位訓練模型的人都取得這個數字，也讓不同實驗之間可以相互比較。

## 核心想法

從三個已知或容易記錄的輸入估算排放：所用的硬體、執行的時長，以及伺服器所在的地點。地點決定了電力的碳強度，因此同一次訓練在不同地點的排放並不相同。

## 計算工具如何運作

1. **硬體。** 記錄所用處理器的品牌與型號。
2. **時長。** 記錄訓練執行的時間。
3. **地點。** 記錄伺服器所在位置，這決定了電網的碳強度。
4. **估算。** 把以上數值結合，得出這次執行的排放量。

摘要列出工具使用的這些因素。確切的功率假設與排放係數，則記錄在工具本身的文件中。

## 結果

摘要介紹了這個計算工具，並描述它用於估算訓練機器學習模型的碳排放。由於論文的重點是工具本身，它並未報告基準結果。其價值在於：同一次執行可以得到一致的估算，而且地點是一個清楚可見的因素。

## 限制

- **只有三個輸入。** 估算未計入製造硬體所隱含的排放、冷卻，以及訓練前後所用的能源，因此低估了完整的碳足跡。
- **假設的係數。** 結果取決於功率與電網的假設，而這些假設未必符合實際的執行情況。
- **只計訓練。** 它估算的是訓練，而不是模型服務使用者時的排放。

## 與其他主題的連結

- 單一大型模型較完整的全生命週期估算，見 [BLOOM 全生命週期估算](life-cycle-estimate.zh-TW.md)頁面。
- 本計算工具所改進的早期成本估算，見[訓練能源成本](training-energy-cost.zh-TW.md)頁面。
- 地點與能源組合是[節能訓練](energy-efficient-training.zh-TW.md)分析的核心。

## 開放問題

- 計算工具是否應預設納入硬體製造的隱含排放？
- 當電網碳強度在訓練過程中變動時，計算工具應如何處理？

## 參考資料

### 開創性論文

- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — 本頁所述的研究，介紹了排放計算工具。
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — 對單一模型較完整的估算，顯示這個計算工具遺漏了什麼。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — 較早的成本估算，促成了透明計算工具的發展。
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — 建議隨實驗一併報告這些數字。
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — 顯示地點與硬體的選擇會改變計算工具所報告的數字。
