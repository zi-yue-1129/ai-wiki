---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - 全生命週期估算
  - BLOOM carbon footprint
  - Life-cycle estimate
---

# 全生命週期碳估算（BLOOM，2022）

!!! info "屬於 AI 的環境影響"
    本方法頁隸屬於 [AI 的環境影響](index.zh-TW.md)。它詳細說明一項估算；上層頁面則將它與其他估算並列比較。

Luccioni、Viguier 與 Ligozat（2022）估算了訓練 BLOOM 的碳足跡。BLOOM 是一個擁有 1760 億參數的語言模型。他們針對同一次訓練執行給出兩個數字，兩者的差別在於計入的範圍。這項估算顯示，計入什麼會使結果相差很大，而且要為機器學習模型得出精確的碳數字相當困難。

## 問題

模型排放的單一數字，會隱藏背後的各種選擇。只計訓練時的用電，得到的數字會比同時計入硬體製造與整個系統的結果小。問題在於如何顯示計算範圍的影響有多大，並為一個真實的模型提供透明的估算。

## 核心想法

先測量訓練實際消耗的能源，再分階段向外延伸估算：從處理器的耗電功率，到整個系統，最後到設備製造的排放。在每一個範圍都報告數字，讓讀者可以看出每個數字包含什麼。

## 估算如何運作

1. **測量動態功率。** 記錄訓練期間處理器所用的能源。
2. **加入系統。** 計入處理器所在的更大系統，例如冷卻與其他設備。
3. **加入生命週期。** 計入設備製造的排放，以及訓練以外所用能源的排放。
4. **報告每個範圍。** 針對每個範圍給出結果，讓讀者可以比較。

摘要描述了這些範圍及由此得出的兩個數字。逐項的計算則在論文中。

## 結果

摘要指出，若只計動態功耗，估算約為 24.7 公噸二氧化碳當量；若計入所有過程，從設備製造到營運能源，則為 50.5 公噸。兩者的差距來自範圍的選擇，作者也強調，要為機器學習模型得出精確的碳估算相當困難。

## 限制

- **只有一個模型。** 估算描述的是一個模型在一套硬體設定上的一次訓練，無法推導出一般性的比率。
- **假設的輸入。** 系統範圍的部分數值，依賴無法從外部完整測量的設備與能源假設。
- **只計訓練。** 數字涵蓋的是訓練，不包括模型部署後提供服務的排放。

## 與其他主題的連結

- 不計較更大範圍的較簡單計算工具，見[機器學習排放計算器](emissions-calculator.zh-TW.md)頁面。
- 降低訓練碳足跡的做法，見[節能訓練](energy-efficient-training.zh-TW.md)頁面。
- 全生命週期數字中所計入的硬體製造，相關內容見[AI 硬體](../../engineering/hardware/index.md)。

## 開放問題

- 全生命週期的範圍應如何標準化，才能比較不同的模型？
- 模型提供服務的排放，應如何與訓練的排放一併計算？

## 參考資料

### 開創性論文

- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — 本頁所述的研究，為同一次訓練給出兩個以範圍區分的碳足跡。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — 只以三個輸入進行估算的計算工具。
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — 顯示模型、資料中心與處理器的選擇如何改變碳足跡。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — 較早估算訓練成本，這類估算即是在其基礎上延伸。
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — 建議報告能源與排放時，須一併說明範圍。
