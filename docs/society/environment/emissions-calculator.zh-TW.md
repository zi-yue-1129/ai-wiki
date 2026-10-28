---
translation_reviewed: 2026-10-28
---

# 機器學習排放計算器（Lacoste 等人，2019）

!!! info "屬於「AI 的環境影響」"
    本方法頁隸屬於[AI 的環境影響](index.zh-TW.md)。它詳細說明一個計算器；上層頁面則比較各種計算器。

Lacoste 等人（2019）提出了機器學習排放計算器，這是一種工具，能以三項輸入估算一次訓練的碳排放：伺服器所在的區域、GPU 的型號，以及訓練時間。其目標是讓這個數字簡單到任何研究者都能記錄，並在報告實驗時一併列出。

## 問題

研究者很少報告實驗產生了多少碳排放。若沒有專門的硬體、功耗與電力供應資料，這個數字很難估計，因此通常被省略。若有一個透明、只需少數資訊的計算器，每位訓練模型的人都能取得這個數字，實驗之間也因此能互相比較。

## 核心概念

先由 GPU 型號與訓練時間估算一次執行所用的能量，再以伺服器所在地的電力碳強度，把能量換算為排放量。地點之所以重要，是因為同一次執行若使用潔淨電網，排放會遠低於使用以燃煤為主的電網。

## 計算器的運作方式

1. **地點。** 記錄伺服器所在的地理區域。作者假設每個雲端區域都使用當地的電網，並將公開的電網資料對應到主要雲端供應商的區域。
2. **硬體。** 記錄 GPU 型號。能量估計採用該 GPU 的額定功率與效能數據。
3. **時長。** 記錄訓練時間。
4. **估算。** 將這些數據合併為約略的能量，再乘以該電網的碳強度，得出二氧化碳當量。

論文將供應商的抵換（offset）列為變數之一，但沒有說明它如何進入計算，因此工具的主要輸出仍取決於上述三項輸入。

## 結果

本文的重點是工具本身，並未報告基準測試結果。論文的示例數字顯示地點的重要性。碳強度從魁北克的約 20 gCO2eq/kWh，到愛荷華州的約 737 gCO2eq/kWh 不等，在論文所考慮的區域中相差約 40 倍。作者指出，對於以數個 GPU 訓練數週的 VGG 或 BERT 等模型，選擇低碳地區可以避免數百公斤的二氧化碳當量排放。

## 限制

- **近似值。** 作者稱此計算器為近似估算，能源與碳排的數字誤差可能很大，部分原因是各機構分享的資料有限。
- **理論功率。** 能量估算依賴額定功率與理論峰值效能，而非實際測得的功耗。作者表示，若改用實測資料會更準確。
- **僅涵蓋訓練。** 推論被排除在外，因此數字不涵蓋服務模型的排放。
- **遺漏的因素。** 電源使用效率（PUE）雖有討論，但並非輸入項；製造硬體所產生的嵌入式碳排也未納入。
- **全球負載平衡。** 若雲端工作在區域之間調度，選擇低碳地區的好處可能會縮小。

## 與其他頁面的連結

- 納入嵌入式排放與閒置功率、針對單一大型模型的完整估算，見[BLOOM 全生命週期估算](life-cycle-estimate.zh-TW.md)。
- NLP 訓練的早期成本估算見[訓練能源成本](training-energy-cost.zh-TW.md)。
- 在執行期間測量能源、而非事先估算的工具，見[能源與排放的報告](reporting-framework.zh-TW.md)。
- 地點與能源結構是[節能訓練](energy-efficient-training.zh-TW.md)的核心。

## 開放問題

- 計算器是否應預設納入硬體製造的嵌入式排放？
- 計算器應如何處理在一次訓練執行過程中變動的電網碳強度？
- 計算器的準確度要達到多少，其數字才能用於決定在哪裡訓練？

## 參考文獻

### 開創性論文

- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv 預印本。https://arxiv.org/abs/1910.09700 — 本頁所述的論文，提出計算器及其三項輸入。
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). *Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model*. arXiv 預印本。https://arxiv.org/abs/2211.02001 — 對單一模型的實測足跡，顯示簡單計算器遺漏了什麼。
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — 較早的 NLP 訓練成本估算，促成了透明計算器的需求。
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248)。https://www.jmlr.org/papers/v21/20-312.html — 建議隨實驗報告能源與碳排，並使用實測而非估計的數字。
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv 預印本。https://arxiv.org/abs/2104.10350 — 顯示硬體與地點的選擇會改變計算器所報告的數字。
