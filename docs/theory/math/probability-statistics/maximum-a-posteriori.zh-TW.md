---
translation_reviewed: 2026-10-28
---

# 最大後驗估計

最大後驗估計（MAP）選出後驗機率最高的參數。它在最大概似上加入先驗，先驗知識與正規化因此得以進入估計。本頁是[機率與統計](index.md)的一部分。

## 概述

貝氏定理給出後驗 \(p(\theta\mid D) \propto p(D\mid\theta)\,p(\theta)\)。MAP 選出後驗最大的 \(\theta\)。資料項 \(p(D\mid\theta)\) 把估計拉向能解釋資料的數值，先驗 \(p(\theta)\) 則把估計拉向在看到資料之前就合理的數值。

## 關鍵概念

- **先驗**：在看到資料之前，對參數的信念所對應的分布。
- **後驗**：看到資料之後，參數的分布。
- **眾數**：密度最高的點。MAP 是後驗的眾數，而不是後驗均值。
- **正規化項**：加在損失上的懲罰。對數先驗加到對數概似上時，即扮演正規化項。

## 運作方式

MAP 估計求解

\[
\hat\theta_{\text{MAP}} = \arg\max_\theta \big[\log p(D\mid\theta) + \log p(\theta)\big].
\]

若先驗為高斯分布 \(p(\theta)\propto \exp(-\lambda\|\theta\|_2^2/2)\)，對數先驗即變為 L2 懲罰；在高斯概似下即為嶺迴歸。若先驗為拉普拉斯分布，則變為 L1 懲罰，即套索迴歸。因此許多熟悉的正規化項都可以視為先驗。Bishop（2006）在線性迴歸中推導了這個對應關係。

MAP 估計是後驗的眾數。對高斯後驗而言，眾數、均值與中位數重合，因此 MAP 與後驗均值一致；對其他後驗則可能不同。

## 主要方法

- [最大概似估計](maximum-likelihood.md)：先驗為平坦時的特殊情形。

## 與其他頁面的連結

- [機率與貝氏方法](../../paradigms/probabilistic/index.md)涵蓋完整後驗，而 MAP 以單一點近似它。
- [變分推論](../../paradigms/probabilistic/variational-inference/index.md)與 [MCMC](../../paradigms/probabilistic/mcmc/index.md) 是超越後驗眾數的方法。
- 就腦與認知而言，貝氏大腦假說把先前期望視為知覺的一部分。MAP 是描述這種結合的一個簡單計算模型，而非神經實現的主張。

## 應用

- **正規化迴歸**：嶺迴歸與套索迴歸是分別以高斯與拉普拉斯先驗得到的 MAP 估計（Bishop, 2006）。
- **權重衰減**：訓練神經網路時常用的 L2 懲罰，對應於對權重取高斯先驗。
- **小樣本估計**：資料稀少時，先驗能使估計穩定。

## 開放問題

- MAP 對重新參數化不具不變性：改變變數會改變眾數，因此估計取決於模型的寫法。
- 點估計忽略後驗不確定性，因而可能過度自信。要得到校準的不確定性，需要近似完整的後驗。

## 參考文獻

### 奠基性論文

- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A*. https://digital.library.adelaide.edu.au/handle/2440/15172 — 最大概似的來源，MAP 即是在其上加入先驗而得。
- 對 Fisher（1922）的評論，PubMed Central。https://pmc.ncbi.nlm.nih.gov/articles/PMC4360088/ — 同儕審查的評論，討論該論文及其對概似的處理。

### 綜述與教科書

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 以高斯與拉普拉斯先驗推導嶺迴歸與套索迴歸，作為 MAP 估計。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋 MAP 估計及其與正規化的關係。
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — 討論後驗眾數，並比較它與後驗均值及完整後驗。
