---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - applications/climate-energy
  - engineering/hardware
  - society/governance
tags:
  - environment
  - energy
  - carbon emissions
aliases:
  - Environmental impact of AI
  - 碳足跡
  - Carbon footprint
  - Green AI
---

# AI 的環境影響

訓練與執行大型模型會耗用大量電力，而執行這些工作的硬體，也是以能源與材料製造出來的。本頁說明如何估算 AI 的環境成本、為什麼不同的估算會有出入，以及有哪些做法可以降低它。

## 概述

模型的環境成本很難確定，因為它取決於計入什麼。一項估算可能只計入訓練時處理器的用電，也可能同時計入冷卻、整個資料中心、硬體製造，以及之後提供模型服務所用的能源。每一個選擇都會得出不同的數字，同一次訓練也可能得出相差很大的結果。

這個領域早期的研究，讓成本變得可見。Strubell 等人（2019）估算了訓練數個 NLP 模型的價格標籤，並主張能源應與準確度一併報告。之後的研究則改進了估算，並把計算範圍寫得更清楚。

## 關鍵概念

- **能源用量**：處理器與容納它們的資料中心所耗用的電力。
- **碳強度**：每單位電力的排放量，取決於當地的能源組合，因此也取決於模型在哪裡訓練。
- **隱含排放**：製造硬體所產生的排放。全生命週期估算會把它加到營運排放之上。
- **系統範圍**：估算所計入的內容。只有範圍不同的兩項估算，結果可能差很多。

## 運作方式

大多數估算依循三個步驟。

1. **測量或估算能源。** 以硬體、訓練時間與處理器的耗電功率，估算所用的能源。
2. **換算為排放。** 把能源乘上執行地點電力的碳強度。
3. **擴大範圍。** 若估算的目的是完整的碳足跡，則加入冷卻、更大的系統，以及硬體製造。

把模型提供給大量使用者，會產生一筆持續的成本，而訓練的估算並未涵蓋這部分。下列方法主要聚焦於訓練，並清楚說明它們計入了哪一部分的成本。

## 關鍵方法

每個方法都有自己的頁面，說明問題、方法、結果與限制。下表做簡要比較。

| 方法 | 所問的問題 | 主要結果（依摘要） | 延伸閱讀 |
|---|---|---|---|
| 訓練能源成本（Strubell 等人，2019） | 訓練數個 NLP 模型要花多少金錢與排放？ | 數個近期 NLP 模型的大約成本估算；各模型的數字在論文表格中 | [訓練能源成本](training-energy-cost.zh-TW.md) |
| 機器學習排放計算器（Lacoste 等人，2019） | 能否從幾個容易記錄的輸入估算訓練排放？ | 以硬體、時長與地點為輸入的計算工具；摘要未報告基準結果 | [排放計算器](emissions-calculator.zh-TW.md) |
| 節能訓練（Patterson 等人，2021） | 模型、資料中心與處理器的選擇，能使碳足跡改變多少？ | 稀疏模型的耗能可低於稠密模型的十分之一；綜合選擇可使碳足跡降低大約 100 到 1000 倍 | [節能訓練](energy-efficient-training.zh-TW.md) |
| BLOOM 全生命週期估算（Luccioni 等人，2022） | 系統範圍的差異，會使一個模型的碳足跡改變多少？ | 只計動態功耗約為 24.7 公噸二氧化碳當量，計入完整生命週期則為 50.5 公噸 | [BLOOM 全生命週期估算](life-cycle-estimate.zh-TW.md) |
| 綠色 AI（Schwartz 等人，2019） | 效率是否應與準確度並列評斷？ | 立場文章，主張報告成本並將其列為評估標準；本身沒有實驗 | [綠色 AI](green-ai.zh-TW.md) |
| 能源與排放的報告（Henderson 等人，2020） | 如何為每次實驗一致地追蹤並報告能源與排放？ | 執行期間追蹤的框架、標準化的線上附錄，以及節能強化學習的排行榜 | [能源與排放的報告](reporting-framework.zh-TW.md) |

## 因應措施

| 做法 | 作用 | 限制 |
|---|---|---|
| 隨每次實驗報告能源與排放 | 讓不同論文的數字可以比較，如[能源與排放的報告](reporting-framework.zh-TW.md)所提出 | 需要追蹤工具，以及雙方同意的範圍 |
| 把效率列為評估標準 | 使成本與準確度並列考量，如[綠色 AI](green-ai.zh-TW.md)所主張 | 取決於研究社群如何評斷研究成果 |
| 採用高效的架構與硬體 | 降低每單位工作的能源，如 Patterson 等人（2021）所示 | 效益取決於比較基準，也可能使服務變得更複雜 |
| 使用低碳電力訓練 | 相同的能源用量下降低排放 | 取決於當地電網資料與可用的運算地點 |

## 與其他主題的連結

- AI 的能源用量屬於更大的能源與氣候脈絡（見[氣候與能源](../../applications/climate-energy/index.md)）。
- 這裡計入其能源用量與製造的硬體，見 [AI 硬體](../../engineering/hardware/index.md)。
- 各模型家族的概覽見[模型](../../theory/models/index.md)。
- 其他領域的能源與排放報告要求，屬於治理的問題（見[法律、政策與治理](../governance/index.md)）。

## 應用

- **研究論文的報告**：為每次實驗記錄能源與排放，讓讀者能把成本與準確度一併比較。
- **規劃訓練時選擇硬體與地點**，並把排放當作其中一項考量。
- **實務中的效率工作**，例如稀疏模型與高效加速器，其目標就是節能。

## 開放問題

- 全生命週期的範圍應如何標準化，才能比較不同的模型？
- 隨著使用量成長，效率的提升是否會降低總排放，還是會使 AI 更便宜、因而被更多地使用？
- 模型提供服務的排放，應如何與訓練它的排放一併計算？
- 對於未公布硬體與訓練時間的模型，能否作出可比較的估算？

## 參考資料

### 開創性論文

- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — 估算數個 NLP 模型的訓練財務與環境成本，開啟了機器學習研究中能源問題的討論。
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — 主張報告訓練成本，並將效率列為評估標準。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — 介紹以硬體、時長與地點估算排放的計算工具。
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — 建議系統性地報告能源與排放，並提出追蹤框架。
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — 顯示模型、資料中心與處理器的選擇如何改變碳足跡，以及能降低多少。
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — 為同一次訓練給出兩個以系統範圍區分的碳足跡。
