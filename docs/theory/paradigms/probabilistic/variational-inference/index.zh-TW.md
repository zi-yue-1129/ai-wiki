---
translation_reviewed: 2026-11-18
---

# 變分推論

變分推論（VI）在較簡單、易於計算的分布族中尋找接近的分布，來近似難以計算的後驗分布。它透過最大化證據下界（ELBO），把推論轉化為最佳化。本頁是[機率與貝氏方法](../index.md)的一部分。[^blei]

## 概述

貝氏推論要求得到資料 $x$ 之下、潛在變數 $z$ 的後驗 $p(z\mid x)$。計算它需要證據 $p(x)=\int p(x,z)\,dz$，這個積分可能難以計算。變分推論選擇候選分布族 $\mathcal{Q}$，並尋找

$$
q^\star = \underset{q\in\mathcal{Q}}{\arg\min}\,
\mathrm{KL}\!\left(q(z)\,\|\,p(z\mid x)\right).
$$

此 KL 散度在 $q$ 下平均對數密度比值。方向很重要，交換兩個分布就會改變目標函數。變分推論的準確性取決於所選分布族，以及最佳化能否找到其中最合適的成員。[^blei]

## 關鍵概念

- **證據** $p(x)$ 是貝氏法則中的正規化常數。
- **變分分布族** $\mathcal{Q}$ 是候選分布的集合。平均場分布族在變數或區塊之間做因式分解，較豐富的分布族則能描述更多相依性。
- **ELBO** 是可由聯合模型 $p(x,z)$ 與近似分布 $q(z)$ 計算的目標函數。
- **攤銷推論**使用共用網路，為每筆觀測產生近似後驗。[^vae]

## 運作方式

### 從後驗散度推導目標函數

假設 $0<p(x)<\infty$、相關期望值有限，而且 $q$ 只在後驗的支撐集內分配機率質量。將 $p(z\mid x)=p(x,z)/p(x)$ 代入 KL 散度，可得[^blei]

$$
\begin{aligned}
\mathrm{KL}(q\|p(z\mid x))
&= \mathbb{E}_q[\log q(z)-\log p(x,z)] + \log p(x),\\
\mathcal{L}(q)
&= \mathbb{E}_q[\log p(x,z)]-\mathbb{E}_q[\log q(z)],\\
\log p(x)
&= \mathcal{L}(q)+\mathrm{KL}(q\|p(z\mid x)).
\end{aligned}
$$

由於 KL 散度非負，$\mathcal{L}(q)\leq\log p(x)$。固定模型與觀測時，精確的 ELBO 增加多少，對後驗的 KL 散度就減少多少。最佳化時可略去證據項，但 ELBO 中的期望值仍可能需要解析推導或蒙地卡羅估計。[^bbvi]

### 已知答案的高斯例子

考慮示範模型 $z\sim\mathcal{N}(0,1)$、$x\mid z\sim\mathcal{N}(z,1)$，並觀測到 $x=2$。這裡 $\mathcal{N}(m,v)$ 表示平均數為 $m$、**變異數**為 $v$ 的高斯分布。對聯合密度配方可得 $p(z\mid x=2)=\mathcal{N}(1,1/2)$，對 $z$ 積分則得到 $p(x)=\mathcal{N}(x;0,2)$。

令 $q(z)=\mathcal{N}(m,s^2)$ 且 $s>0$，它對此後驗的 KL 散度為

$$
\mathrm{KL}(q\|p(z\mid x=2))
=\frac{1}{2}\left[
\frac{s^2+(m-1)^2}{1/2}-1+\log\frac{1/2}{s^2}
\right].
$$

對數證據固定為 $\log p(2)=-\tfrac12\log(4\pi)-1\approx-2.2655$。使用自然對數，透過上述恆等式可得以下數值。

| 候選分布 $q$ | 對後驗的 KL 散度 | ELBO |
|---|---:|---:|
| $\mathcal{N}(0,1)$ | $1.1534$ | $-3.4189$ |
| $\mathcal{N}(1,1)$ | $0.1534$ | $-2.4189$ |
| $\mathcal{N}(1,1/2)$ | $0$ | $-2.2655$ |

這些是手算的候選分布。先匹配平均數、再匹配變異數，就能將 ELBO 提升到對數證據。此分布族包含精確後驗，因此最佳解的近似誤差為零。較難的模型，其後驗可能落在所選分布族之外。

### 最佳化變分參數

定義一個變分方法的有三個選擇：$q$ 的分布族、如何最佳化 ELBO，以及參數是針對每筆觀測個別擬合，還是跨資料集共用。

對可微分的連續模型，重參數化能將高斯抽樣寫成 $z=\mu+\sigma\odot\epsilon$，其中 $\epsilon\sim\mathcal{N}(0,I)$，$\odot$ 表示逐元素相乘。這讓梯度可以通過抽出的值傳遞。[^vae] 在所需正則條件成立時，得分函數估計量提供另一條途徑，而變異數縮減有助於實際運用。[^bbvi]

## 主要方法

- [平均場變分推論](mean-field.md)把 $q$ 做因式分解，並支援座標更新，共軛模型可得到閉式更新。[^jordan]
- [隨機變分推論](stochastic-variational-inference.md)利用資料小批次更新全域近似分布，將推論擴展到大型資料集。[^svi]
- [變分自編碼器](../../unsupervised/density-and-generative-models/vae/index.md)以編碼器產生 $q_\phi(z\mid x)$，並以解碼器對觀測建模。[^vae]

## 與其他頁面的連結

- [機率與統計](../../../math/probability-statistics/index.md)提供本方法所用的後驗、證據與 KL 散度。
- [馬可夫鏈蒙地卡羅](../mcmc/index.md)利用樣本近似後驗期望值，準確性取決於混合狀況與有限執行時間造成的誤差。變分推論的準確性取決於分布族與最佳化，計算上的取捨則隨模型而異。[^blei]
- [神經科學與 AI 的連結](../../../../brain-mind/neuroai/index.md)討論研究大腦與心智的機率方法。

## 應用

- **主題模型**以變分推論，為潛在狄利克雷分配及相關模型提供可擴展的後驗近似。[^svi]
- **生成模型**利用攤銷變分推論學習潛在變數模型，並推論觀測的編碼。[^vae]
- **貝氏深度學習**以網路權重的近似後驗表示不確定性。[^blei]

## 限制與開放問題

- **分布族與最佳化誤差。** 受限的分布族限制了可達到的最佳 ELBO。局部最佳解與未完成的最佳化會留下額外差距。解讀隨機估計的 ELBO 上升時，也需要考慮抽樣雜訊。[^blei][^bbvi]
- **不確定性。** 平均場近似捨棄因子間的相依性，可能低估邊際變異數。程度取決於後驗與分布族，上面的高斯精確擬合例子也呈現了這一點。[^blei]
- **攤銷。** 固定模型與分布族時，令 $q_x^\star$ 為針對觀測 $x$ 個別最大化 ELBO 的分布。編碼器輸出 $q_\phi(z\mid x)$ 所留下的差距，可分解為[^cremer]

$$
\log p(x)-\mathcal{L}(q_\phi)
=
\underbrace{\log p(x)-\mathcal{L}(q_x^\star)}_{\text{approximation gap}}
+
\underbrace{\mathcal{L}(q_x^\star)-\mathcal{L}(q_\phi)}_{\text{amortisation gap}}.
$$

較有表達力的分布族可以縮小第一項「近似差距」，更充分地擬合每筆觀測則可改善第二項「攤銷差距」。實務上，若不知道證據與分布族內的最佳解，這些差距就難以估計。[^cremer]

[^blei]: Blei 等人（2017）第 2.1 至 2.4 節與第 5 節說明 KL 目標、ELBO、平均場限制與推論取捨。
[^jordan]: Jordan 等人（1999）第 6 至 7 節推導圖模型的因式分解近似與變分參數更新。
[^vae]: Kingma 與 Welling（2014）第 2 至 3 節提出推論網路與重參數化梯度估計量。
[^bbvi]: Ranganath 等人（2014）第 2 至 3 節推導用於 ELBO 最佳化的得分函數梯度與變異數縮減方法。
[^svi]: Hoffman 等人（2013）第 2 至 3 節針對含全域與區域潛在變數的模型，推導隨機推論，並討論主題模型。
[^cremer]: Cremer 等人（2018）第 3.1 節針對固定生成模型，定義近似差距與攤銷差距。

## 參考文獻

### 奠基性論文

- Jordan, M. I., Ghahramani, Z., Jaakkola, T. S. & Saul, L. K. (1999). An introduction to variational methods for graphical models. *Machine Learning* 37(2), 183–233. https://people.eecs.berkeley.edu/~jordan/papers/variational-intro.pdf — 介紹圖模型的變分方法，包括該界限與平均場更新。
- Kingma, D. P. & Welling, M. (2014). Auto-encoding variational Bayes. *ICLR*. arXiv:1312.6114. https://arxiv.org/abs/1312.6114 — 提出 VAE，即使用重參數化技巧的攤銷變分推論。
- Ranganath, R., Gerrish, S. & Blei, D. M. (2014). Black box variational inference. *AISTATS*. https://proceedings.mlr.press/v33/ranganath14.html — 為 ELBO 提出一般的梯度估計量，適用於不具共軛性的模型。
- Hoffman, M. D., Blei, D. M., Wang, C. & Paisley, J. (2013). Stochastic variational inference. *Journal of Machine Learning Research* 14. https://www.jmlr.org/papers/v14/hoffman13a.html — 以隨機自然梯度的小批次更新，把變分推論擴展到大型資料集。

- Cremer, C., Li, X. & Duvenaud, D. (2018). *Inference Suboptimality in Variational Autoencoders*. ICML. https://proceedings.mlr.press/v80/cremer18a.html — 區分變分自編碼器的近似差距與攤銷差距，並研究兩者的影響。

### 綜述與教科書

- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2017). Variational inference: a review for statisticians. *Journal of the American Statistical Association* 112(518), 859–877. https://arxiv.org/abs/1601.00670 — 為統計學家撰寫的變分推論綜述，說明 ELBO、平均場與隨機方法。
- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — 專著，把變分方法與指數族及對數分割函數連結起來。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；與抽樣推論並列介紹變分推論。
