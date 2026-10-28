---
translation_reviewed: 2026-10-28
---

# 訓練能源成本（Strubell 等人，2019）

!!! info "屬於「AI 的環境影響」"
    本方法頁隸屬於[AI 的環境影響](index.zh-TW.md)。它詳細說明一項估算；上層頁面則將它與其他估算比較。

Strubell、Ganesh 與 McCallum（2019）估算了訓練數個 NLP 模型的大約財務與環境成本。他們以這些估算主張，研究應在準確度之外，同時衡量能源使用。這篇論文常被引用，是因為其表格把模型的二氧化碳當量（以磅計）與美元成本列在模型名稱旁邊。

## 問題

NLP 的準確度進步伴隨著運算量的快速成長，但多數論文並未報告這些運算在能源、金錢或碳排上的成本。沒有這些數字，讀者便無法比較不同方法的成本，模型的碳足跡也就一直隱而不見。

## 核心概念

依每個模型的硬體與訓練時間估算其耗能，再把能量換算為碳排放量與雲端運算價格。結果是每個模型大致、但可相互比較的「價格標籤」。

## 估算方式

1. **計算硬體與時間。** 取得各模型所用的處理器與報告的訓練時間。
2. **估算能量。** 將硬體功率與時間換算為千瓦時。表格欄位標示為 kWh·PUE，代表能量乘上了資料中心的額外負荷係數。
3. **換算為碳排放。** 以假設的電網碳強度，將能量換算為二氧化碳當量，單位為磅。
4. **換算為金錢。** 以雲端價格計算同樣的時數，給出以美元表示的區間。

表格列出了各列的輸入，確切的乘數則在論文中。

## 結果

論文的表格列出數個模型的估算數字。以下為部分例子：

| 模型 | 硬體 | 時數 | CO2e（磅） | 雲端成本（美元） |
|---|---|---|---|---|
| Transformer（base） | 8 × P100 | 12 | 26 | $41–$140 |
| Transformer（big） | 8 × P100 | 84 | 192 | $289–$981 |
| ELMo | 3 × P100 | 336 | 262 | $433–$1,472 |
| BERT（base） | 64 × V100 | 79 | 1,438 | $3,751–$12,571 |
| 神經架構搜尋（NAS） | 8 × P100 | 274,120 | 626,155 | $942,973–$3,201,722 |

NAS 那一列是極端值。它是架構的搜尋，而非單次訓練，論文的重點正是此類搜尋的成本可能極為龐大。表中沒有 BERT（large）的列，而 BERT（base）則列出了兩種硬體設定。由於作者找不到 TPU 的公開功耗資料，TPU 執行的功率與排放欄位留白。

## 限制

- **粗略的估計。** 數字取決於假設的功耗、價格與電網碳強度。它們適合用來比較，但不宜當作會計數字。
- **僅涵蓋訓練。** 估算只包括訓練，不含部署模型每日所耗用的能源；對一個模型的整個生命週期而言，後者可能更大。
- **舊模型。** 2019 年的模型與硬體已有所改變，因此這些數字是歷史快照。
- **硬體取得性。** 多數列依賴雲端價格與多數研究者無法自由選擇的硬體。

## 與其他頁面的連結

- 後來的計算器改進了這項方法，見[機器學習排放計算器](emissions-calculator.zh-TW.md)與[BLOOM 全生命週期估算](life-cycle-estimate.zh-TW.md)。
- 降低成本的方法見[節能訓練](energy-efficient-training.zh-TW.md)。
- 把成本列為評估標準的論點見[綠色 AI](green-ai.zh-TW.md)。

## 開放問題

- 模型的成本應如何在其訓練與之後的大量使用之間分配？
- 對於硬體與訓練時間未公開的模型，能否做出可相互比較的成本估算？

## 參考文獻

### 開創性論文

- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — 本頁所述的研究。預印本：https://arxiv.org/abs/1906.02243
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2020). Green AI. *Communications of the ACM*, 63(12), 54–63. doi:[10.1145/3381831](https://doi.org/10.1145/3381831) — 主張應報告訓練的價格標籤，並把效率列為評估標準。預印本：https://arxiv.org/abs/1907.10597
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv 預印本。https://arxiv.org/abs/1910.09700 — 以伺服器地點與 GPU 型號改進估算的計算器。
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248)。https://www.jmlr.org/papers/v21/20-312.html — 建議為 ML 實驗報告能源與碳排。
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv 預印本。https://arxiv.org/abs/2104.10350 — 估算數個大型模型的能源與排放，並顯示模型、資料中心與處理器的選擇會改變足跡。
