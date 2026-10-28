---
translation_reviewed: 2026-10-28
---

# 全生命週期碳排估算（BLOOM，2022）

!!! info "屬於「AI 的環境影響」"
    本方法頁隸屬於[AI 的環境影響](index.zh-TW.md)。它詳細說明一項估算；上層頁面則比較各項估算。

Luccioni、Viguier 與 Ligozat（2022）估算了訓練 BLOOM（一個 1,760 億參數語言模型）的碳足跡。他們針對同一次訓練執行報告了兩個數字，兩者的差別在於計入的範圍。這個差距顯示，範圍的選擇可能使結果相差很大，而要為 ML 模型給出精確的碳排數字十分困難。

## 問題

一個模型的單一排放數字，掩蓋了背後的各種選擇。若只計入訓練期間處理器用掉的電力，得到的數字會比同時計入硬體製造與閒置機器耗電的數字來得小。問題在於展示範圍的選擇有多重要，並為一個真實模型提供透明的估算。

## 核心概念

測量訓練期間處理器實際耗用的能量，以電網碳強度換算，然後分階段向外擴展估算範圍。在每個範圍界定處都報告數字，讓讀者看見每個數字包含了什麼。

## 估算方式

1. **動態功率。** 以訓練時 GPU 的耗電功率乘上電網的碳強度。作者排除了 CPU 的功耗，也不計入抵換或熱能回收。
2. **閒置功率。** 加上叢集在閒置時的耗電，這是維持硬體可供使用的成本。
3. **嵌入式排放。** 加上製造伺服器與 GPU 所產生的排放。作者以代理數據而非精確的硬體資料估算這部分。
4. **分別報告各範圍。** 為每個階段給出總量，讓讀者可以比較僅計動態功率的數字與完整生命週期的數字。

論文並未嘗試「從搖籃到墳墓」的完整評估。網路交換器與冷卻設備未計入嵌入式排放。

## 結果

本次訓練使用約 433 MWh 的動態能量，共約 108 萬 GPU 小時，歷時 118 天。硬體為法國國家叢集中的 Nvidia A100 GPU，該處電網的碳強度約為 57 gCO2eq/kWh。兩個主要數字為：

- **僅計動態功率：** 約 24.7 公噸 CO2eq。
- **完整生命週期：** 約 50.5 公噸 CO2eq。這再加上伺服器與 GPU 的嵌入式排放約 11.2 公噸，以及叢集閒置功率約 14.6 公噸。

作者也測量了一個服務部署：16 個 A100 GPU 位於雲端執行個體上，在約 18 天內處理約 23 萬次請求，耗電 914 kWh，當地電網碳強度為 394 gCO2eq/kWh。這在追蹤期間約為 340 公斤 CO2eq。作者將這些數字都描述為估算值。

## 限制

- **單一模型與單一叢集。** 估算描述的是一種硬體設定下的一次訓練執行，不能代表 ML 的一般排放率。
- **代理輸入。** 訓練功耗並未即時追蹤，因此以 GPU 的額定功率為代理；嵌入式排放的數字也依賴代理資料。
- **未計入的部分。** CPU 功耗、網路交換器與冷卻設備都不在數字之內，因此總量並不完整。
- **服務是另一種情況。** 推論數字來自單一部署，可能無法代表其他設定。

## 與其他頁面的連結

- 只計三項輸入的較簡單計算器，見[機器學習排放計算器](emissions-calculator.zh-TW.md)。
- 降低訓練足跡的方法，見[節能訓練](energy-efficient-training.zh-TW.md)。
- 被計入全生命週期數字的硬體，見[AI 硬體](../../engineering/hardware/index.zh-TW.md)。
- 每篇論文都應附上這類數字的論點，見[能源與排放的報告](reporting-framework.zh-TW.md)。

## 開放問題

- 應如何標準化全生命週期的範圍界定，才能比較不同模型？
- 模型的服務排放應如何與其訓練排放合併計算？

## 參考文獻

### 開創性論文

- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). *Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model*. arXiv 預印本。https://arxiv.org/abs/2211.02001 — 本頁所述的研究，一次訓練執行的兩個足跡數字，以及兩者之間的範圍界定。
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv 預印本。https://arxiv.org/abs/1910.09700 — 只計三項輸入的較簡單計算器。
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv 預印本。https://arxiv.org/abs/2104.10350 — 顯示模型、資料中心與處理器的選擇如何改變足跡。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — 較早的訓練成本估算，此類估算是在它的基礎上延伸。
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248)。https://www.jmlr.org/papers/v21/20-312.html — 建議報告能源與排放時，應同時說明範圍界定。
