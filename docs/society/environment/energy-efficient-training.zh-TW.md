---
translation_reviewed: 2026-10-28
---

# 節能訓練（Patterson 等人，2021）

!!! info "屬於「AI 的環境影響」"
    本方法頁隸屬於[AI 的環境影響](index.zh-TW.md)。它詳細說明一項分析；上層頁面則比較各項分析。

Patterson 等人（2021）分析了模型、資料中心與處理器的選擇，如何改變訓練大型神經網路的碳足跡。他們的主要論點是，這些選擇非常重要：若搭配得當，可大幅降低足跡，而稀疏激活模型是最有力的槓桿之一。

## 問題

大型模型常被當成排放量由其規模固定的東西來討論。若真是如此，唯一的槓桿就只剩下訓練較小的模型。問題在於，能否透過更審慎地選擇架構、地點與硬體，以低得多的排放完成相當的工作。

## 核心概念

把足跡拆解為實務工作者可以控制的因素，並衡量每個因素能改變多少。論文將它們分為模型架構、資料中心及其能源結構，以及處理器，再觀察這些因素如何相互結合。

## 分析方式

1. **模型架構。** 比較大型稠密模型，與參數數量相同或更多的大型稀疏激活模型。
2. **資料中心與地點。** 比較各地的無碳能源比例，並比較雲端資料中心與一般資料中心。
3. **處理器。** 比較機器學習加速器與現成系統。
4. **估算總量。** 估計近期大型模型的能源與 CO2e，包括 T5、Meena、GShard、Switch Transformer 與 GPT-3，並修正先前對 Evolved Transformer 所用架構搜尋的估算。

## 結果

摘要報告了以下範圍：

- 大型稀疏激活模型的能耗可低於大型稠密模型的十分之一，且沒有準確度損失。
- 無碳能源的比例，進而 CO2e，即使在同一國家與同一機構內，也會因地點而相差約 5 至 10 倍。
- 雲端資料中心的能源效率約為一般資料中心的 1.4 至 2 倍。
- 機器學習加速器的效能約為現成系統的 2 至 5 倍。
- 模型、資料中心與處理器的選擇合併起來，可使足跡降低至多約 100 至 1000 倍。

論文也主張，ML 論文應報告能源與 CO2e，並將其視為關鍵的評估指標，此點與[綠色 AI](green-ai.zh-TW.md)相互呼應。

## 限制

- **相對於基準。** 降幅是相對於特定的稠密模型與設定而言。在其他設定下，收益可能較小。
- **能源結構會變動。** 地點的影響取決於訓練時當地電網的無碳比例，而這一比例會隨時間改變。
- **僅涵蓋訓練。** 分析只涵蓋訓練，並未說明模型大規模部署後，總排放會降低多少。
- **估算數字。** 近期大型模型的總量是根據公開資訊估算，並非對每次執行的實測。

## 與其他頁面的連結

- 本分析所依賴的估算方法，見[訓練能源成本（Strubell 等人，2019）](training-energy-cost.zh-TW.md)。
- 一個大型模型的完整生命週期估算（包括嵌入式排放），見[BLOOM 全生命週期估算](life-cycle-estimate.zh-TW.md)。
- 稀疏架構是高效設計的一種，各模型家族見[模型](../../theory/models/index.zh-TW.md)。
- 硬體面的因素見[AI 硬體](../../engineering/hardware/index.zh-TW.md)。

## 開放問題

- 隨著使用量成長，模型效率的提升能在多大程度上轉化為總排放的降低？
- 訓練的地點與時間應如何報告，才能讓排放數字可以比較？
- 能否在不讓運算資源較少的群體更難使用模型的前提下，保留效率的提升？

## 參考文獻

### 開創性論文

- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv 預印本。https://arxiv.org/abs/2104.10350 — 本頁所述的分析，探討模型、資料中心與處理器的選擇如何改變足跡。其摘要提供了上述的範圍。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — 較早的 NLP 訓練成本估算，促成了這一系列研究。
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). *Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model*. arXiv 預印本。https://arxiv.org/abs/2211.02001 — 一個大型模型的實測足跡，並列出總量所依賴的範圍界定。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv 預印本。https://arxiv.org/abs/1910.09700 — 一種計算器，輸入為伺服器地點、GPU 與訓練時間。
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248)。https://www.jmlr.org/papers/v21/20-312.html — 建議報告決定足跡的各項因素。
