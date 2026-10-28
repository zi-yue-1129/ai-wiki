---
translation_reviewed: 2026-10-28
---

# 變分推論

變分推論（VI）以較簡單、易於計算的分布族中最接近的分布，來近似難以計算的後驗分布。它把推論轉化為最佳化：最大化對數證據的下界，即證據下界（ELBO）。本頁是[機率與貝氏方法](../index.md)的一部分。

## 概述

貝氏推論要求得到資料 \(x\) 之下、潛在變數 \(z\) 的後驗 \(p(z\mid x)\)。計算它需要證據 \(p(x)=\int p(x,z)\,dz\)，通常是無法解析的積分。[MCMC](../mcmc/index.md) 等抽樣方法以一串樣本來估計後驗。變分推論則在容易處理的分布族中選出一個分布 \(q(z)\)，並使其儘可能接近 \(p(z\mid x)\)。

接近程度以 Kullback–Leibler 散度 \(\mathrm{KL}(q\|p)\) 衡量。由於證據固定，最小化此散度等同於最大化 ELBO。此方法以精確度換取速度與可擴展性，其準確性取決於分布族 \(q\) 的表達能力。

## 關鍵概念

- **證據**：\(p(x)\)，即使後驗成為機率分布的正規化常數。它衡量模型解釋資料的程度。
- **證據下界（ELBO）**：\(\mathcal{L}(q) = \mathbb{E}_q[\log p(x,z)] - \mathbb{E}_q[\log q(z)]\)。它滿足 \(\log p(x) = \mathcal{L}(q) + \mathrm{KL}(q(z)\|p(z\mid x))\)，因此 \(\mathcal{L}(q)\le\log p(x)\)。
- **變分分布族**：候選分布 \(q\) 的集合。平均場分布族在變數之間做因式分解；較豐富的分布族包括正規化流後驗。
- **攤銷推論**：由單一神經網路為每個資料點輸出近似後驗，而非為每個點各自最佳化一個 \(q\)。

## 運作方式

最大化 ELBO 同時改進近似並給出證據的下界。對於觀測 \(x\) 與潛在變數 \(z\) 的模型，ELBO 對 \(q\) 參數的梯度可以用 \(q\) 的樣本估計。當 \(q\) 為高斯時，重參數化技巧使梯度的變異數較低；得分函數估計量適用於任何 \(q\)，但變異數較高（Ranganath et al., 2014）。

定義一個變分方法的有三個選擇：\(q\) 的分布族、如何最佳化 ELBO，以及最佳化是針對每個資料點進行，還是跨整個資料集攤銷。

## 主要方法

實務上有四條主要途徑。其中兩條在本節有獨立頁面，第三條則由 VAE 頁面涵蓋。

- [平均場變分推論](mean-field.md)：把 \(q\) 在潛在變數之間做因式分解，並逐一更新各因子。對於共軛模型，存在閉式的座標更新（Jordan et al., 1999）。
- [隨機變分推論](stochastic-variational-inference.md)：以資料小批次的雜訊梯度最佳化 ELBO，因此可擴展到非常大的資料集（Hoffman et al., 2013）。
- [變分自編碼器](../../unsupervised/density-and-generative-models/vae/index.md)：攤銷的變分推論，其中編碼器網路產生 \(q\)，解碼器網路對資料建模（Kingma & Welling, 2014）。

## 與其他頁面的連結

- [機率與統計](../../../math/probability-statistics/index.md)提供本方法所用的後驗、證據與 KL 散度。
- [馬可夫鏈蒙地卡羅](../mcmc/index.md)是抽樣的替代方法。MCMC 漸近精確但較慢；VI 有偏差但較快。
- 神經科學中的自由能原理提出，大腦會最小化一個與 ELBO 密切相關的量。這是理論主張而非既定結果，相關討論見[神經科學與 AI 的連結](../../../../brain-mind/neuroai/index.md)。

## 應用

- **主題模型**：為潛在狄利克雷分配及相關模型提供可擴展的後驗近似（Blei et al., 2017）。
- **生成模型**：用於影像、語音與分子的 VAE，採用攤銷的變分推論（Kingma & Welling, 2014）。
- **貝氏深度學習**：對網路權重的近似後驗，用來估計不確定性（Blei et al., 2017）。

## 開放問題

- ELBO 可能很鬆，因此近似分布族限制了準確性。較豐富的分布族（如正規化流）能縮小差距，但計算成本增加。
- 平均場的因式分解會低估後驗變異數，其原因與補救方法是活躍的研究主題。
- 攤銷引入額外的差距，而在特定資料集上衡量其大小並不容易。

## 參考文獻

### 奠基性論文

- Jordan, M. I., Ghahramani, Z., Jaakkola, T. S. & Saul, L. K. (1999). An introduction to variational methods for graphical models. *Machine Learning* 37. https://doi.org/10.1023/A:1007665907178 — 介紹圖模型的變分方法，包括該界限與平均場更新。
- Kingma, D. P. & Welling, M. (2014). Auto-encoding variational Bayes. *ICLR*. arXiv:1312.6114. https://arxiv.org/abs/1312.6114 — 提出 VAE，即使用重參數化技巧的攤銷變分推論。
- Ranganath, R., Gerrish, S. & Blei, D. M. (2014). Black box variational inference. *AISTATS*. https://proceedings.mlr.press/v33/ranganath14.html — 為 ELBO 提出一般的梯度估計量，適用於不具共軛性的模型。
- Hoffman, M. D., Blei, D. M., Wang, C. & Paisley, J. (2013). Stochastic variational inference. *Journal of Machine Learning Research* 14. https://www.jmlr.org/papers/v14/hoffman13a.html — 以隨機自然梯度的小批次更新，把變分推論擴展到大型資料集。

### 綜述與教科書

- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2017). Variational inference: a review for statisticians. *Journal of the American Statistical Association*. arXiv:1601.00670. https://arxiv.org/abs/1601.00670 — 為統計學家撰寫的變分推論綜述，說明 ELBO、平均場與隨機方法。
- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — 專著，把變分方法與指數族及對數分割函數連結起來。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；與抽樣推論並列介紹變分推論。
