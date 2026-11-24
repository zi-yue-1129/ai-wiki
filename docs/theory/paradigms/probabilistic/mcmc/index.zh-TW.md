---
translation_reviewed: 2026-11-19
---

# 馬可夫鏈蒙地卡羅

馬可夫鏈蒙地卡羅（MCMC）利用一連串相依的抽樣來估計期望值，並設計馬可夫鏈的轉移，使其保留目標分布。當直接取得獨立樣本很困難時，後驗推論常使用這種方法。本頁是[機率與貝氏方法](../index.md)的一部分。[^intro]

## 概述

許多貝氏計算需要後驗 $\pi(\theta)=p(\theta\mid D)$ 下的期望值，但後驗只能確定到正規化常數的比例。MCMC 設計從目前狀態到下一個狀態的轉移。在適當的收斂條件下，沿著鏈取平均會趨近 $\pi$ 下的期望值。[^intro]

[Metropolis–Hastings](metropolis-hastings.md)、[吉布斯抽樣](gibbs-sampling.md)與[哈密頓蒙地卡羅](hamiltonian-monte-carlo.md)頁面說明各自的轉移規則。選擇有效的規則，以及評估輸出探索目標分布的效率，都是使用 MCMC 的一部分。

## 關鍵概念

- **馬可夫性質**表示在給定目前狀態後，下一個狀態與更早的狀態條件獨立。
- **穩態分布**是經過轉移後保持不變的分布。若以此分布初始化一條鏈，後續每個狀態的邊際分布都會相同。
- **混合**描述鏈探索目標分布、消除初始狀態影響的速度。
- **暖身期或燃燒期**是從報告的樣本中排除的初始片段。暖身期也可用來調整抽樣器設定，例如 NUTS。[^nuts]
- **有效樣本數（ESS）**描述特定估計量的蒙地卡羅精度，並將抽樣之間的相依性納入考量。[^stan]

## 運作方式

### 保留目標分布並建立收斂條件

在有限狀態空間中，令 $P_{ij}$ 為從狀態 $i$ 移動到狀態 $j$ 的機率，每一列的總和為一。將 $\pi$ 寫成列向量時，穩態條件為

$$
\pi P=\pi.
$$

**細緻平衡** $\pi_iP_{ij}=\pi_jP_{ji}$ 是一個充分條件，讓穩態下兩個方向的機率流量相等。對有限狀態的鏈，不可約性與非週期性能確保它收斂到唯一的穩態分布。不可約性表示任兩個狀態之間都可到達，非週期性則排除只能按固定週期返回的情況。連續狀態空間需要相應的一般狀態空間條件。[^intro]

單位矩陣能保留任何分布，但使用它的鏈會永遠停在初始狀態。因此，僅檢查穩態條件，無法確立一次執行是否探索了目標分布。

### 估計一個量及其蒙地卡羅誤差

對 $N$ 個保留的抽樣與純量函數 $f$，以以下方式估計期望值

$$
\widehat{\mu}_f=\frac{1}{N}\sum_{t=1}^{N} f(\theta^{(t)}).
$$

計算一般的鏈平均時，應保留因拒絕提議而重複的狀態，因為它們代表鏈在該狀態停留的時間。[^intro]

對已處於穩態的鏈，令 $\rho_f(k)$ 為 $f(\theta^{(t)})$ 在延遲 $k$ 的自相關。在變異數有限、自相關級數可加總，且馬可夫鏈中央極限定理成立時，定義積分自相關時間與對應的漸近 ESS 為[^stan]

$$
\tau_f=1+2\sum_{k=1}^{\infty}\rho_f(k),
\qquad
N_{\mathrm{eff},f}=\frac{N}{\tau_f}.
$$

估計平均數的蒙地卡羅標準誤約為

$$
\operatorname{MCSE}(\widehat{\mu}_f)
\approx
\sqrt{\frac{\operatorname{Var}_{\pi}(f)}{N_{\mathrm{eff},f}}}.
$$

這衡量期望值的數值估計誤差。後驗標準差則描述模型目標分布中的不確定性。ESS 取決於 $f$，因此同一組抽樣對平均數與尾端機率可能有不同的精度。[^diagnostics]

### 具有相同目標分布的兩條鏈

考慮一個示範用的雙狀態目標分布，在狀態 $A,B$ 上有 $\pi=(1/4,3/4)$。對 $0<a<1/4$，定義

$$
P_a=
\begin{pmatrix}
1-3a & 3a\\
a & 1-a
\end{pmatrix}.
$$

因為 $(1/4)(3a)=(3/4)a$，兩個方向的流量平衡。兩個狀態互相可達，且各自具有自我轉移，所以鏈會收斂到 $\pi$，但速度強烈取決於 $a$。

令 $f(B)=1$、$f(A)=0$，則穩態平均數為 $3/4$，變異數為 $3/16$。中心化後的函數是 $P_a$ 的特徵向量，對應特徵值 $\lambda=1-4a$。因此 $\rho_f(k)=\lambda^k$，且 $\tau_f=(1+\lambda)/(1-\lambda)$。

| 轉移參數 | $\lambda$ | $\tau_f$ | $N=1000$ 時的漸近 ESS |
|---|---:|---:|---:|
| $a=1/6$ | $1/3$ | $2$ | $500$ |
| $a=1/100$ | $0.96$ | $49$ | $20.4$ |

這些是針對穩態鏈的解析計算。第二條鏈在每個狀態停留更久，因此相同抽樣次數對 $B$ 的機率所提供的資訊明顯較少。有效的穩態分布本身，無法決定取樣效率。

## 主要方法

- [Metropolis–Hastings](metropolis-hastings.md)提出移動，再依同時考量正向與反向提議的接受比率決定是否接受。[^intro]
- [吉布斯抽樣](gibbs-sampling.md)從完整條件分布抽樣，更新變數或區塊。[^intro]
- [哈密頓蒙地卡羅](hamiltonian-monte-carlo.md)利用梯度與模擬動力學探索連續目標分布。[^neal] NUTS 則會調整軌跡長度。[^nuts]

## 關聯與應用

- [變分推論](../variational-inference/index.md)透過最佳化近似後驗。MCMC 與變分推論有不同的誤差來源與計算成本。
- [機率與統計](../../../math/probability-statistics/index.md)提供 MCMC 所近似的後驗與期望值計算。
- 後驗抽樣可用於貝氏估計、可信區間與預測。機率程式設計系統會使用 NUTS 等抽樣器，對使用者定義的模型執行推論。[^nuts]

## 診斷與限制

- **比較多條鏈。** 使用分散的初始值，並檢查軌跡圖或排名圖。經排名正規化、分割與折疊的 $\widehat{R}$ 診斷，能偵測不同鏈之間的位置與尺度差異。Vehtari 等人建議將 $\widehat{R}<1.01$ 作為整體診斷評估的一部分。[^diagnostics]
- **檢查報告的估計量。** 檢查分布主體與尾端的 ESS，並對實際關心的平均數、分位數或機率計算 MCSE。以排名為基礎的主體 ESS 是診斷量，無法直接給出原始後驗平均數的 MCSE。[^diagnostics]
- **評估探索狀況。** 丟棄固定數量的暖身抽樣，無法確立收斂。多條鏈可能互相一致，卻全部漏掉孤立的模態，因此診斷所提供的是在有限狀態探索下，對一次有限長度執行的證據。[^diagnostics]
- **考量每個有效樣本的成本。** 小步移動可能造成強烈的正自相關。HMC 能減少隨機漫步行為，但計算梯度與軌跡也需要成本。[^neal] 應在計算預算內比較關心估計量的精度。

[^intro]: Andrieu 等人（2003）第 3 節說明轉移核、穩態分布、收斂條件與標準 MCMC 演算法。
[^stan]: Stan 開發團隊的〈Posterior Analysis〉推導以自相關定義的 ESS，以及平均數的蒙地卡羅標準誤。
[^diagnostics]: Vehtari 等人（2021）第 2 至 4 節提出排名診斷、區域 ESS 與蒙地卡羅誤差估計，並討論收斂檢查的限制。
[^neal]: Neal（2011）綜述哈密頓動力學、隨機漫步行為，以及 MCMC 的計算取捨。
[^nuts]: Hoffman 與 Gelman（2014）說明 NUTS、軌跡長度的選擇，以及暖身期的調整。

## 參考文獻

### 奠基性論文

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics* 21(6), 1087–1092. https://doi.org/10.1063/1.1699114 — 提出 Metropolis 演算法，用於從玻爾茲曼分布抽樣。
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — 把 Metropolis 規則推廣到非對稱提議分布。
- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B* 195(2), 216–222. https://doi.org/10.1016/0370-2693(87)91197-X — 提出混合（哈密頓）蒙地卡羅方法。

### 綜述與教科書

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50, 5–43. https://www.cs.ubc.ca/~nando/papers/mlintro.pdf — 為機器學習撰寫的 MCMC 導論，涵蓋 Metropolis–Hastings、吉布斯抽樣及其關係。
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. In *Handbook of Markov Chain Monte Carlo*. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — 綜述 HMC、其調校方式，以及相較隨機漫步抽樣器的優勢。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋 MCMC 方法及其診斷。

- Vehtari, A., Gelman, A., Simpson, D., Carpenter, B. & Bürkner, P.-C. (2021). *Rank-normalization, folding, and localization: An improved R-hat for assessing convergence of MCMC*. Bayesian Analysis. https://arxiv.org/abs/1903.08008 — 提出排名正規化的收斂診斷，並研究分布不同區域的有效樣本數。

### 文章與文件

- Hoffman, M. D. & Gelman, A. (2014). The No-U-Turn sampler: adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research* 15. https://jmlr.org/papers/v15/hoffman14a.html — 提出 NUTS，自動調整 HMC 的路徑長度。

- Stan Development Team. *Stan Reference Manual: Posterior Analysis*. https://mc-stan.org/docs/reference-manual/analysis.html — 說明多鏈診斷、自相關、有效樣本數與蒙地卡羅標準誤。
