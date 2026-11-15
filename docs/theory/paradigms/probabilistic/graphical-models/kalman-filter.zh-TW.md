---
translation_reviewed: 2026-11-15
---

# 卡爾曼濾波器

卡爾曼濾波器（Kalman filter）結合線性動態模型與有雜訊的觀測，遞迴估計隱藏狀態。在高斯初始分布與加性高斯雜訊的假設下，僅需維護平均向量與共變異數矩陣，就能精確表示每一步的濾波後驗分布。這是[機率圖模型](index.md)在連續狀態空間中的特例。

## 問題與假設

狀態轉移與量測模型：

$$
x_t=F_tx_{t-1}+B_tu_t+w_t,\quad w_t\sim\mathcal N(0,Q_t),
$$

$$
y_t=H_tx_t+v_t,\quad v_t\sim\mathcal N(0,R_t).
$$

假設程序雜訊與量測雜訊獨立、模型矩陣已知，而且先驗為高斯分布。濾波器交替執行**預測**與**量測修正**；共變異數表示估計的不確定性，並非單條實現軌跡的實際誤差。[Kalman（1960）](https://doi.org/10.1115/1.3662552)提出這套遞迴估計方法。

## 遞迴更新

**預測：**

$$
\hat x_t^-=F_t\hat x_{t-1}^++B_tu_t,\qquad
P_t^-=F_tP_{t-1}^+F_t^\top+Q_t.
$$

**修正：**

$$
S_t=H_tP_t^-H_t^\top+R_t,\qquad
K_t=P_t^-H_t^\top S_t^{-1},
$$

$$
\hat x_t^+=\hat x_t^-+K_t(y_t-H_t\hat x_t^-).
$$

在精確運算下，共變異數可寫成 $P_t^+=(I-K_tH_t)P_t^-$。若考慮浮點數精度，常採用 Joseph form：$(I-KH)P^-(I-KH)^\top+KRK^\top$，以改善對稱性與半正定性。卡爾曼增益依據相對不確定性，決定創新量（innovation）應修正多少預測。

## 教學動畫：增益加權的高斯融合

<div class="concept-motion-scroll" style="max-width:100%;overflow-x:auto" tabindex="0">
<img data-source-asset-urls src="../../../../assets/concept-animations/kalman-gain-fusion-still.svg" data-motion-src="../../../../assets/concept-animations/kalman-gain-fusion-motion.svg" data-still-src="../../../../assets/concept-animations/kalman-gain-fusion-still.svg" alt="卡爾曼濾波預測、量測概似與增益加權後驗更新" style="width:640px;min-width:640px;max-width:none;height:auto">
</div>

*原創教學動畫，CC BY-SA 4.0。* [GitHub 可讀的最終靜態圖](../../../../assets/concept-animations/kalman-gain-fusion-still.svg)。MkDocs 網站提供**播放／暫停**；可用 Tab 與 Enter／Space 操作按鈕，偏好減少動態效果時顯示靜態圖。手機請水平捲動圖面。

在**人工建構的一維示例**中，設定 $H=1$、預測均值 $\hat x^-=3$、預測變異數 $P^-=1.44$、觀測 $y=7$、量測變異數 $R=0.64$：

$$
K=\frac{1.44}{1.44+0.64}=0.6923,\quad
\hat x^+=3+K(7-3)\approx5.769,
$$

$$
P^+=(1-K)1.44\approx0.443.
$$

虛線分別表示先驗與形似概似函數的觀測資訊，實線則逐漸變成修正後的高斯信念。**為了比較形狀，三條曲線都將峰值正規化，而非以相同機率密度面積比例繪製。** 轉場是視覺插值，**不是額外的濾波迭代，也不是模型實測結果**；觀測曲線是以隱藏狀態為變數的概似，不是另一個後驗分布。

## 互動計算：卡爾曼增益與高斯修正

調整**預測變異數** $P^-$、**量測變異數** $R$，或人工觀測值 $y$，並使用「上一步／下一步」與進度滑桿檢視預測、創新量和修正。圖表即時計算 $K=P^-/(P^-+R)$、$\hat x^+=3+K(y-3)$ 及 $P^+=(1-K)P^-$；預測平均值固定為 3。**三條曲線皆正規化至相同峰值**，用於比較形狀，不代表相同面積尺度的機率密度。提高 $R$ 會讓修正更偏向先驗；提高 $P^-$ 則讓修正更仰賴觀測。

**新增計算視覺：創新量與修正量的差異。** 第二張三軌 SVG 使用相同狀態座標軸，依序呈現預測均值、量測值、更新後均值。位移精確等於 $K(y-3)$，只有 $K=1$ 才等於完整創新量 $y-3$；後驗變異數為 $(1-K)P^-$。圖形與原本的參數及逐步控制同步。下方 GitHub 靜態預覽採人工預設數值，不是實測濾波軌跡。

![一維卡爾曼預測、量測與均值修正三軌示意的 GitHub 回退預覽](../../../../assets/concept-animations/kalman-innovation-lab-still.svg)

**標準化創新量診斷。** 第三張即時計算的 SVG 使用 $z=(y-3)/\sqrt{P^-+R}$ 與 $\mathrm{NIS}=z^2$ 呈現創新量的尺度。陰影 $|z|\leq1.96$ 是創新量依照模型假設服從高斯分布時的 95% 參考範圍，**不能用一次人工觀測判定濾波器已通過或未通過統計驗證**。在預測階段尚不顯示觀測標記，進入量測階段才出現；原有播放、單步、進度和鍵盤控制會同步更新此圖。

![卡爾曼人工標準化創新量及高斯參考區間](../../../../assets/concept-animations/kalman-nis-still.svg)

**新增互動計算：預測與觀測的權重。** 第四張同步 SVG 顯示一維精確加權公式 $\mu^+=(1-K)\mu^-+Ky$，其中 $K=P^-/(P^-+R)$。藍色與橘色區段表示兩者的**相對權重**，三個標記則在相同狀態軸上表示預測、觀測及後驗平均值。降低 $R$ 將提高觀測權重，但不能解讀為訓練產生的信任分數或實測校準。只有修正階段才揭露後驗標記。

![卡爾曼增益對預測與觀測分配的相對權重及後驗平均值位置](../../../../assets/concept-animations/kalman-trust-weights-still.svg)

**新增互動計算：Joseph 變異數來源分解。** 同步 SVG 將一維 Joseph 共變異數更新拆成「預測不確定性」與「量測雜訊」兩個非負貢獻：

$
P^+=(1-K)^2P^-+K^2R,\qquad K=\frac{P^-}{P^-+R}.
$

人工預設值下，兩項分別約為 $0.136$ 與 $0.307$，合計 $P^+\approx0.443$。所有長條共用**絕對變異數尺度**，後驗長條比先驗短；不能解讀為真實感測器誤差來源的實測比例。只有進入修正階段才揭露 Joseph 兩項貢獻；原有播放／暫停、單步、進度滑桿與變異數參數控制會同步重新計算。

![卡爾曼 Joseph 更新中預測誤差與量測雜訊對後驗變異數的貢獻：GitHub 靜態回退預覽](../../../../assets/concept-animations/kalman-joseph-contributions-still.svg)

<div class="bayesian-filter-lab" data-lab="kalman" data-lang="zh"><p class="bayesian-filter-fallback">互動數值實驗需要 JavaScript；上方靜態預覽與手算範例仍可閱讀。</p></div>

這些數值及轉換是**獨立計算的一維人工示意**，不是實測估計誤差，也不是連續多次量測的結果。

## 優點與限制

- 在所述線性高斯條件下，遞迴更新計算效率高且具有精確性；Kalman–Bucy 濾波則延伸相關思想至連續時間。
- 雜訊共變異數設定不準確，可能造成增益過度自信或反應遲緩；數值實作還須留意矩陣條件數。
- 非線性、多峰或強烈非高斯後驗通常無法由單一高斯分布表達。可比較採樣式的[粒子濾波器](particle-filter.md)。
- 濾波只使用截至時間 $t$ 的觀測；*平滑*（smoothing）可另外使用未來的觀測，兩者解決的問題不同。

## 參考文獻

### 奠基性論文

- Kalman, R. E. (1960). *A New Approach to Linear Filtering and Prediction Problems*. Journal of Basic Engineering. https://doi.org/10.1115/1.3662552 — 提出狀態空間中的濾波遞迴。
- Kalman, R. E. & Bucy, R. S. (1961). *New Results in Linear Filtering and Prediction Theory*. Journal of Basic Engineering. https://doi.org/10.1115/1.3658902 — 推導連續時間的共變異數方程式。
- Gordon, N. J., Salmond, D. J. & Smith, A. F. M. (1993). *Novel approach to nonlinear/non-Gaussian Bayesian state estimation*. IEE Proceedings F. https://doi.org/10.1049/ip-f-2.1993.0015 — 提出非高斯濾波的抽樣替代方法。

### 綜述與教科書

- Wainwright, M. J. & Jordan, M. I. (2008). *Graphical Models, Exponential Families, and Variational Inference*. Foundations and Trends in Machine Learning. https://doi.org/10.1561/2200000001 — 從機率圖模型觀點說明推論問題。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 包含高斯推論與狀態空間模型的教科書。
