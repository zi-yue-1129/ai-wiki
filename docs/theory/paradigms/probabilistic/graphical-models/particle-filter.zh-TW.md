---
translation_reviewed: 2026-11-15
---

# 粒子濾波器

粒子濾波器（Particle filter）使用一群帶有權重的樣本近似序列貝氏濾波分布。與以單一高斯分布表示信念的[卡爾曼濾波器](kalman-filter.md)不同，粒子濾波可處理非高斯乃至多峰後驗，但會受到有限樣本誤差影響。經典的 Bootstrap filter／抽樣重要性重採樣（SIR）版本由 [Gordon 等人（1993）](https://doi.org/10.1049/ip-f-2.1993.0015)提出。

## 核心概念

對具有狀態轉移 $p(x_t\mid x_{t-1})$ 及觀測概似 $p(y_t\mid x_t)$ 的狀態空間模型，貝氏濾波先由前一時刻後驗預測，再利用最新量測更新權重。粒子近似可寫為：

$$
p(x_t\mid y_{1:t})\approx\sum_{i=1}^{N}w_t^{(i)}\delta(x_t-x_t^{(i)}),\qquad \sum_iw_t^{(i)}=1.
$$

對 Bootstrap proposal，每個粒子由轉移模型抽出，其未正規化的重要性權重就是觀測概似：

$$
\tilde w_t^{(i)}=p(y_t\mid x_t^{(i)}),\qquad
w_t^{(i)}=\frac{\tilde w_t^{(i)}}{\sum_j\tilde w_t^{(j)}}.
$$

接著進行**重採樣**：依權重比例選取祖先粒子，產生權重相等的新粒子群。重採樣不會憑空增加後驗資訊，只是重新分配有限的計算資源，保留更可能的狀態。

## 教學動畫：觀測加權與祖先重採樣

<div class="concept-motion-scroll" style="max-width:100%;overflow-x:auto" tabindex="0">
<img data-source-asset-urls src="../../../../assets/concept-animations/particle-weight-resampling-still.svg" data-motion-src="../../../../assets/concept-animations/particle-weight-resampling-motion.svg" data-still-src="../../../../assets/concept-animations/particle-weight-resampling-still.svg" alt="粒子概似加權與系統性重採樣的祖先選擇" style="width:640px;min-width:640px;max-width:none;height:auto">
</div>

*原創教學動畫，CC BY-SA 4.0。* [GitHub 可讀的最終靜態圖](../../../../assets/concept-animations/particle-weight-resampling-still.svg)。MkDocs 網站提供**播放／暫停**與鍵盤操作，偏好減少動態效果時顯示靜態粒子群；窄螢幕請水平捲動。

十個**人工設定**的一維預測粒子狀態為：

$$
x=(1.0,2.1,2.9,3.7,4.4,5.3,6.1,6.6,7.4,8.8).
$$

假設觀測 $y=6.6$、概似 $p(y\mid x)\propto\exp(-(x-y)^2/(2\cdot1.3^2))$。將各粒子的概似值正規化後，得到圖中的權重長條。以固定起始偏移量執行**系統性重採樣**，門檻 $(0.045,0.145,\ldots,0.945)$ 選出**從 0 開始編號的祖先索引** $(4,5,6,6,6,7,7,8,8,9)$。

動畫把每個被選中的後代，由祖先所在位置移往下方；為了看清重複粒子，圖中加上一點水平位移，**純粹是畫面錯開，不是程序雜訊或粒子突變**。所有數值與抽樣結果都只是教學示意，**不代表實際觀測、實測後驗或模型運算軌跡**。

## 互動計算：概似、ESS 與系統性重採樣

調整人工**觀測值** $y$、概似標準差 $\sigma$，以及系統性重採樣偏移量 $u_0\in[0,0.1)$。逐步檢視預測樣本、概似權重、累積權重及所選後代。介面在重採樣前計算 $\mathrm{ESS}=1/\sum_i w_i^2$。改變 $u_0$ 可能改變祖先選擇，**卻不會改變正規化的重要性權重**；重複出現的後代只是複製祖先，並未加入新的轉移或雜訊。

**新增計算視覺：用累積權重反函數找出祖先。** 第二張 SVG 將 $[0,1]$ 切成寬度等於各粒子權重 $w_i$ 的區間，再以 $u_j=u_0+j/10$ 畫出十條等距門檻；每個門檻落入的累積區間決定祖先索引，第四階段才顯示選擇結果。調整 $u_0$ 只會移動門檻，不改變區間寬度或**重採樣前** ESS。下方 GitHub 回退圖使用人工預設值，並非實測重採樣效能。

![系統性重採樣門檻與粒子累積權重區間的 GitHub 靜態預覽](../../../../assets/concept-animations/particle-cdf-thresholds-still.svg)

**預期與實際後代份額。** 第三張即時計算 SVG 比較 $Nw_i$ 與系統性重採樣**實際選出的整數祖先複本數**。藍色份額在加權階段顯示，橘色實際份額只在最後的重採樣階段出現。調整偏移量可能改變複本數與保留的祖先種類，卻不會改變權重或**重採樣前** ESS。兩種份額的總數都為 10；這些值不是模型實測或重複試驗的統計。

![系統性重採樣下預期重要性權重後代份額與實際祖先複本](../../../../assets/concept-animations/particle-offspring-still.svg)

**新增互動計算：重採樣造成的平均值位移。** 第四張同步 SVG 比較重採樣前的加權平均值 $\bar x_w=\sum_iw_ix_i$ 與抽得後代的等權平均值 $\bar x_r=N^{-1}\sum_jx_{a_j}$。改變系統性偏移量可能改變這個**有限樣本有號差值**，卻不會改變原始權重或重採樣前 ESS。後代標記只在最後的重採樣階段出現。此確定性人工範例**不能視為濾波準確度提升或實測不確定性**。

![粒子重採樣前的加權平均值與後代等權平均值在共同狀態軸上的比較](../../../../assets/concept-animations/particle-mean-shift-still.svg)

**新增互動計算：累積後代數與期望質量的偏差。** 系統性重採樣使用等間距門檻；新圖對每個祖先邊界 $i$ 重新計算「實際累積複本數」減去「依權重預期的累積後代數」：

$
D_i=\sum_{j=1}^{i}N_j-N\sum_{j=1}^{i}w_j,\qquad |D_i|<1 \quad (u_0\in[0,1/N),\;i=1,\dots,N).
$

這個嚴格界限來自同一個隨機平移的等間距門檻序列，**不是**假設各祖先獨立抽樣；它限制的是各個**累積前綴**的偏差，不表示每個祖先的絕對誤差總和小於一。只有重採樣階段才揭露偏差軌跡；調整 $u_0$ 可改變實際複本數，卻不改變原始權重與期望值。十粒子均屬可重現的人工教學數值，非效能實測。

![系統性重採樣的累積實際後代數減去期望質量：GitHub 靜態回退預覽](../../../../assets/concept-animations/particle-systematic-discrepancy-still.svg)

<div class="bayesian-filter-lab" data-lab="particle" data-lang="zh"><p class="bayesian-filter-fallback">互動數值實驗需要 JavaScript；上方靜態預覽與手算範例仍可閱讀。</p></div>

十個位置與觀測均屬於**人工教學數值**，不是實際估計結果。每個步驟是同一次更新的展示階段，不代表額外執行濾波迭代。

## 解讀與限制

- 高權重粒子在這次重採樣實例中得到更多後代；低權重祖先可能消失。整體分布仍是近似而非精確後驗。
- 常用有效樣本數 $\mathrm{ESS}=1/\sum_i(w_t^{(i)})^2$ 判斷是否需要重採樣；每一步都重採樣可能加重樣本貧化。
- 粒子數太少或初始覆蓋不佳，可能完全錯過重要分布模式；增加粒子數則提高運算成本。
- 重採樣之後，**下一次預測**才會根據轉移核產生新粒子。重採樣本身是有放回的選擇，不是擴散步驟。
- 當觀測比轉移模型提供更尖銳的限制時，Bootstrap proposal 的效率可能不佳；可考慮其他提議分布或輔助粒子濾波器。

## 參考文獻

### 奠基性論文

- Gordon, N. J., Salmond, D. J. & Smith, A. F. M. (1993). *Novel approach to nonlinear/non-Gaussian Bayesian state estimation*. IEE Proceedings F. https://doi.org/10.1049/ip-f-2.1993.0015 — 提出 Bootstrap 粒子濾波。
- Kitagawa, G. (1996). *Monte Carlo Filter and Smoother for Non-Gaussian Nonlinear State Space Models*. Journal of Computational and Graphical Statistics. https://doi.org/10.1080/10618600.1996.10474692 — 以蒙地卡羅方法進行非線性系統的濾波與平滑。

### 綜述與教科書

- Arulampalam, M. S., Maskell, S., Gordon, N. & Clapp, T. (2002). *A Tutorial on Particle Filters for Online Nonlinear/Non-Gaussian Bayesian Tracking*. IEEE Transactions on Signal Processing. https://doi.org/10.1109/78.978374 — 說明 SIS、SIR、退化現象與實務變體。
- Doucet, A. (2006). *Sequential Monte Carlo Methods*. Encyclopedia of Statistical Sciences. https://doi.org/10.1002/0471667196.ess5089 — 回顧序列重要性抽樣與重採樣。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 貝氏濾波與推論的入門教材。
