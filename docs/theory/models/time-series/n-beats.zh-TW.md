---
translation_reviewed: 2026-11-06
related:
  - theory/models/mlp/index.md
---

# N-BEATS

N-BEATS 是一種深層的純全連接架構，用於單變量點預測。它使用殘差區塊堆疊，每個區塊產生對其輸入的回推（backcast）以及對未來的預測。可解釋的變體把預測限制為趨勢與季節成分。它是[時間序列預測](index.md)頁面比較的三個代表性方法之一。

## 問題

在 M 系列競賽中，單變量預測表現最好的是統計方法，以及結合統計與神經元件並使用人工設計特徵的混合方法。單純的深度網路並未獲勝。N-BEATS 要問的是：沒有任何時間序列專用元件的一般深度網路，能否匹敵或超越這些方法？而深度模型是否也能具有可解釋性，讓規劃者讀懂趨勢與季節模式的預測。

## 核心想法

網路是由區塊組成的堆疊。每個區塊接收近期歷史的一個視窗，經過四層或更多層的全連接網路，產生兩個輸出：

- **回推（backcast）**：它對輸入視窗中能被解釋的部分所做的估計；以及
- **預測（forecast）**：對序列下一段的預測。

區塊以殘差方式串接。每個區塊在把輸入交給下一個區塊之前，先減去自己的回推，因此每個區塊建模的是前面區塊尚未解釋的部分。最終預測是所有區塊預測的總和。

可解釋版本改變了區塊能輸出的內容，使用兩個堆疊。趨勢堆疊的預測是時間的低次多項式，季節堆疊的預測是正弦與餘弦項之和（傅立葉基底）。作者報告，此版本相較一般版本，準確率損失很小。

## 方程式與演算法

對於輸入為 $x_\ell$ 的區塊 $\ell$，全連接網路產生參數 $\theta^b_\ell$ 與 $\theta^f_\ell$。回推與預測是對基底矩陣 $V^b_\ell$ 與 $V^f_\ell$ 的線性投影：

$$\hat{x}_\ell = V^b_\ell\, \theta^b_\ell, \qquad \hat{y}_\ell = V^f_\ell\, \theta^f_\ell.$$

下一個區塊接收 $x_{\ell+1} = x_\ell - \hat{x}_\ell$，最終預測為 $\hat{y} = \sum_\ell \hat{y}_\ell$。一般版本的基底矩陣是學習得到的；可解釋版本則是固定的：趨勢堆疊使用正規化時間索引的多項式次方，季節堆疊使用正弦與餘弦函數。

作者以不同的回看長度與損失函數訓練此類模型的集成。損失函數包括 sMAPE、MASE 與 MAPE，論文指出 TOURISM 資料集只使用 MAPE。

## 結果

摘要報告，N-BEATS 相較統計基準提升預測準確率 11%，相較上一屆 M4 競賽冠軍提升 3%。在 M4 上，論文的一般模型達到整體加權準確率（OWA）0.797，而 M4 冠軍為 0.821，最佳統計方法為 0.861。論文也報告在 M3 與 TOURISM 上達到最先進的結果。這些數字來自論文自身的表格，重複使用前應先查閱原文。

## 限制

- **僅限單變量。** 此方法只根據序列自身的過去預測該序列。基本設計不接受共變量，因此無法直接使用假日或已規劃的價格。
- **點預測。** 每一步的輸出是單一數值。不確定性需要另外的方法處理，例如集成或分位數擴充。
- **成本。** 最好的結果來自許多已訓練模型的集成，成本遠高於單一模型。
- **依賴基準。** 最有力的證據來自 M 系列競賽的資料。論文並未充分證明其在具有間歇性需求或大量共變量的工業資料上的表現。

## 關聯

N-BEATS 是具有殘差連接的深層[多層感知器](../mlp/index.md)，並顯示預測不需要遞迴或注意力。其機率式對應方法是 [DeepAR](deepar.md)，以注意力為基礎的替代方法是 [Informer](informer.md)。

## 參考文獻

### 開創性論文

- Oreshkin, B. N., Carpov, D., Chapados, N. & Bengio, Y. (2019). *N-BEATS: Neural basis expansion analysis for interpretable time series forecasting*. arXiv. https://arxiv.org/abs/1905.10437 — 原始論文：具有一般與可解釋兩種變體的殘差全連接區塊堆疊，在 M3、M4 與 TOURISM 上評估。
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014 — N-BEATS 所比較的競賽冠軍來自此競賽，也是基準的來源。
- Hyndman, R. J. & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, 22(4), 679–688. https://doi.org/10.1016/j.ijforecast.2006.03.001 — 討論可跨序列比較預測的無尺度誤差指標，包括 MASE 所用的比例誤差。

### 綜述與教科書

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — 綜述深度預測架構，包括 N-BEATS 所屬的非遞迴設計。
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — 可免費閱讀的教科書，涵蓋可解釋版本以神經形式重現的古典趨勢與季節方法。
- Gneiting, T. & Katzfuss, M. (2014). Probabilistic Forecasting. *Annual Review of Statistics and Its Application*, 1, 125–151. https://doi.org/10.1146/annurev-statistics-062713-085831 — 回顧點預測與機率預測的評估方式，這是此處點預測結果的背景。
