---
translation_reviewed: 2026-10-28
---

# 吉布斯抽樣

吉布斯抽樣透過反覆地從每個變數在其他所有變數條件下的條件分布中抽樣，來從聯合分布抽樣。每個提議都被接受，因此不需要接受–拒絕步驟。它是具共軛條件分布模型的標準抽樣器。本頁是[馬可夫鏈蒙地卡羅](index.md)的一部分。

## 概述

假設一個變數 \((\theta_1,\dots,\theta_d)\) 上的聯合分布難以直接抽樣，但每個條件分布 \(p(\theta_j\mid\theta_{-j})\) 都容易抽樣。吉布斯抽樣依序循環各變數，並從其條件分布重新抽樣。所得的鏈以聯合分布為穩態分布。在階層貝氏模型中，許多條件分布是標準分布，因此此方法很方便。

## 關鍵概念

- **完全條件分布**：\(p(\theta_j\mid\theta_{-j})\)，即其他所有變數固定時，單一變數的分布。
- **掃描順序**：系統掃描以固定順序更新變數，隨機掃描則隨機挑選一個變數。
- **分塊**：同時更新數個相關變數，通常能改善混合。
- **摺疊吉布斯抽樣**：以解析方式積分掉部分變數，可降低其餘變數之間的相關性。

## 運作方式

抽樣器的一次掃描為：

1. 對 \(j = 1,\dots,d\)，抽取 \(\theta_j^{(t+1)} \sim p(\theta_j \mid \theta_1^{(t+1)},\dots,\theta_{j-1}^{(t+1)}, \theta_{j+1}^{(t)},\dots,\theta_d^{(t)})\)。

每次更新都是一個以完全條件分布為提議的 Metropolis–Hastings 移動，因此其接受機率為一（Andrieu et al., 2003）。於是每一步都滿足細緻平衡，聯合分布保持不變。

當變數高度相關時，此方法的混合可能很慢，因為每次更新只沿一個座標移動。常見的補救方法是分塊與重新參數化。

## 主要方法

- [Metropolis–Hastings](metropolis-hastings.md)：一般方法，吉布斯抽樣是其中所有提議都被接受的特殊情形。
- [哈密頓蒙地卡羅](hamiltonian-monte-carlo.md)：沿聯合分布的幾何移動，因此較能處理相關變數，但需要梯度。

## 與其他頁面的連結

- [馬可夫鏈蒙地卡羅](index.md)提供框架與診斷。
- [機率與統計](../../../math/probability-statistics/index.md)提供使吉布斯步驟容易計算的條件分布與共軛性。
- 在共軛模型中，吉布斯抽樣與平均場變分推論密切相關。抽樣器從後驗抽樣，平均場更新則近似後驗，參見[變分推論](../variational-inference/index.md)。

## 應用

- **階層貝氏模型**：共軛條件分布使吉布斯抽樣對許多標準模型都有效率（Gelman et al., 2013）。

## 開放問題

- 相關性強的後驗可能使吉布斯抽樣極慢，而若不比較多條鏈，很難診斷這一點。
- 一般而言，分塊方式與掃描順序的自動選擇仍未解決。

## 參考文獻

### 奠基性論文

- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — 給出一般的接受比率框架，吉布斯更新是其特例。
- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50. https://www.cs.ox.ac.uk/publications/publication7533-abstract.html — 說明吉布斯更新是接受機率為一的 Metropolis–Hastings 移動。

### 綜述與教科書

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 抽樣一章以實例涵蓋吉布斯抽樣。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋圖模型的吉布斯抽樣。
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — 在階層模型中使用吉布斯抽樣，並討論其收斂檢查。
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — 在相關性強的情境中比較吉布斯型與以梯度為基礎的抽樣器。
