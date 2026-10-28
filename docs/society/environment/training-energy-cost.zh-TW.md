---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - 訓練能源成本
  - Training energy cost
---

# 訓練能源成本（Strubell 等人，2019）

!!! info "屬於 AI 的環境影響"
    本方法頁隸屬於 [AI 的環境影響](index.zh-TW.md)。它詳細說明一項估算；上層頁面則將它與其他估算並列比較。

Strubell、Ganesh 與 McCallum（2019）估算了訓練數個近期 NLP 模型的大約財務與環境成本，並以此主張研究應把能源用量與準確度一併納入考量。這篇論文是最早為大型語言模型的訓練估算成本的研究之一，也為一個過去大多只報告準確度的領域，建立了討論的框架。

## 問題

NLP 的準確度提升伴隨著快速成長的運算量，但多數論文並未報告這些運算耗費的能源、金錢或排放量。沒有這些數字，讀者就無法比較不同方法的成本，模型的碳足跡也就隱而不見。

## 核心想法

依據每個模型所用的硬體與訓練時間估算其耗能，再把能源換算為財務成本與排放量。結果雖然粗略，卻提供了一個可以互相比較的「價格標籤」。

## 估算如何運作

1. **計算硬體與時間。** 取得每個模型所用的處理器與回報的訓練時長。
2. **估算能源。** 依處理器的典型功耗，把硬體功率與時間換算為能源。
3. **換算為金錢與排放。** 套用雲端價格得出財務成本，並套用電網的碳強度得出排放量。
4. **比較。** 把不同模型的成本並列。

摘要將這種方法描述為對大約成本的估算，確切的乘數則在論文中。

## 結果

摘要指出，大型 NLP 模型帶來顯著的準確度提升，但這些提升依賴「極為龐大的運算資源」，並引用了「驅動現代張量處理硬體所需的碳足跡」。摘要表示，論文估算了訓練數個近期模型的財務與環境成本，並提出降低成本、提升公平性的建議。摘要未提供各模型的數字，因此應從論文的表格中讀取。

## 限制

- **粗略估算。** 結果取決於假設的功耗、價格與電網碳強度。它們適合用來比較，而不宜當作會計數字。
- **只計訓練。** 估算涵蓋訓練，未涵蓋已部署模型每天消耗的能源；在模型的整個生命週期中，後者可能更多。
- **模型較舊。** 2019 年的模型與硬體此後已經改變，因此這些數字是歷史快照。

## 與其他主題的連結

- 這個估算方法後來被更精細的計算工具與全生命週期估算所改進。見[機器學習排放計算器（Lacoste 等人，2019）](emissions-calculator.zh-TW.md)與[BLOOM 全生命週期估算](life-cycle-estimate.zh-TW.md)。
- 降低成本的做法見[節能訓練（Patterson 等人，2021）](energy-efficient-training.zh-TW.md)。
- 能源用量的更大脈絡見[氣候與能源](../../applications/climate-energy/index.md)。

## 開放問題

- 模型的成本應如何在其訓練與之後的大量使用之間分攤？
- 對於未公布硬體與訓練時間的模型，能否作出可比較的成本估算？

## 參考資料

### 開創性論文

- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — 本頁所述的研究，估算數個 NLP 模型的訓練成本。
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — 主張報告訓練的價格標籤，並將效率列為評估標準。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — 為訓練的排放提出計算工具，改進了本頁的估算。
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — 建議報告機器學習實驗的能源與排放，並提出追蹤框架。
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — 顯示模型、資料中心與處理器的選擇會大幅改變碳足跡。
