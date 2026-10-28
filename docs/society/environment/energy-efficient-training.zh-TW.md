---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - 節能訓練
  - Energy-efficient training
---

# 節能訓練（Patterson 等人，2021）

!!! info "屬於 AI 的環境影響"
    本方法頁隸屬於 [AI 的環境影響](index.zh-TW.md)。它詳細說明一項分析；上層頁面則將它與其他分析並列比較。

Patterson 等人（2021）分析了模型、資料中心與處理器的選擇，如何改變訓練大型神經網路的碳足跡。他們的主要訊息是：這些選擇影響極大，妥善搭配可以把碳足跡降低很多倍，而稀疏模型是最重要的槓桿之一。

## 問題

大型模型常被當作排放量由其規模固定決定。如果真是如此，唯一的槓桿就是訓練較小的模型。問題在於：只要更審慎地選擇架構、地點與硬體，能否以低得多的排放完成同樣的工作？

## 核心想法

把碳足跡拆解為實務工作者可以控制的因素，並測量每個因素能改變多少。論文將這些因素分為模型架構、資料中心與其能源組合，以及處理器三類，再觀察它們如何組合。

## 分析如何運作

1. **模型架構。** 比較稠密模型與參數數量相近或更多、但只稀疏啟動的模型。
2. **資料中心與地點。** 比較不同地點與時間的無碳電力比例，並比較雲端資料中心與一般資料中心。
3. **處理器。** 比較機器學習加速器與通用系統。
4. **組合。** 估算同時選擇架構、資料中心與處理器的綜合效果。

摘要給出各因素的範圍，論文中的詳細計算則是任何特定情境所需要的。

## 結果

摘要指出，大型但只稀疏啟動的模型，在不犧牲準確度的情況下，耗能可低於大型稠密模型的十分之一。摘要指出，即使在同一國家、同一機構內，無碳能源比例與由此產生的排放量也會相差大約五到十倍。雲端資料中心的效率約高 1.4 到 2 倍，面向機器學習的加速器則約高 2 到 5 倍。綜合選擇模型、資料中心與處理器，可使碳足跡降低大約 100 到 1000 倍。

## 限制

- **取決於比較基準。** 降幅是相對於特定的稠密基準與特定設定而言。在其他設定下，收益可能較小。
- **能源組合的估算。** 地點的影響取決於當地電網在訓練時的無碳比例，而這個比例會變動。
- **準確度與取得性。** 「準確度沒有損失」的說法只適用於所研究的模型。稀疏模型也較難部署，且在某些硬體上較難執行。
- **範圍。** 分析涵蓋訓練，並未確定模型大規模部署後，總體碳足跡會降低多少。

## 與其他主題的連結

- 本分析所依賴的估算方法，在[訓練能源成本（Strubell 等人，2019）](training-energy-cost.zh-TW.md)中有討論。
- 稀疏架構是一種高效設計。各模型家族的概覽見[模型](../../theory/models/index.md)。
- 這些因素中硬體的部分，見[AI 硬體](../../engineering/hardware/index.md)。

## 開放問題

- 模型效率的提升，在使用量成長後，能有多少轉化為總排放的下降？
- 訓練的地點與時間應如何報告，才能使排放可以比較？
- 能否在保持效率的同時，不讓模型對算力較少的人更難使用？

## 參考資料

### 開創性論文

- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — 本頁所述的分析，探討模型、資料中心與處理器的選擇如何改變碳足跡。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — 較早估算訓練 NLP 模型的成本，促成了這一系列研究。
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — 對一個大型模型的實測碳足跡，顯示本分析的選擇在實務中如何適用。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — 以硬體、執行時長與地點為輸入的排放計算工具。
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — 建議報告本分析所依賴的各項因素。
