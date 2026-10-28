---
translation_reviewed: 2026-10-28
---

# Metropolis–Hastings

Metropolis–Hastings 演算法從簡單分布提出移動，並以能保持目標分布不變的比率接受，藉此從目標分布抽取樣本。它是最一般的 MCMC 方法，也是其他方法的起點。本頁是[馬可夫鏈蒙地卡羅](index.md)的一部分。

## 概述

要從 \(\pi(\theta)\) 抽樣而不知道其正規化常數，演算法從提議分布 \(q(\theta'\mid\theta)\) 提出新狀態 \(\theta'\)，並以機率 \(\alpha\) 接受。\(\alpha\) 只取決於 \(\pi\) 與 \(q\) 的比值。正規化常數會消去，因此此方法適用於後驗。提議分布可以是任何能到達整個目標分布的分布。

## 關鍵概念

- **提議分布**：\(q(\theta'\mid\theta)\)，由使用者選擇。常見的預設是隨機漫步的高斯提議。
- **接受比率**：\(\alpha = \min\!\big(1, \frac{\pi(\theta')\,q(\theta\mid\theta')}{\pi(\theta)\,q(\theta'\mid\theta)}\big)\)。
- **對稱提議**：當 \(q(\theta'\mid\theta)=q(\theta\mid\theta')\) 時，比率化為 \(\pi(\theta')/\pi(\theta)\)，即原始的 Metropolis 規則。
- **接受率調校**：提議過寬則常被拒絕，過窄則移動緩慢。好的做法是瞄準適中的接受率。

## 運作方式

一步的演算法如下：

1. 給定當前狀態 \(\theta\)，提出 \(\theta' \sim q(\cdot\mid\theta)\)。
2. 由上述接受比率計算 \(\alpha\)。
3. 以機率 \(\alpha\) 將下一個狀態設為 \(\theta'\)；否則保持 \(\theta\)。

Metropolis 等人（1953）為物理系統提出了對稱版本。Hastings（1970）把它推廣到非對稱提議，即今日使用的形式。\(\alpha\) 的選擇保證對 \(\pi\) 的細緻平衡成立，因此 \(\pi\) 是該鏈的穩態分布。

## 主要方法

- [吉布斯抽樣](gibbs-sampling.md)：特殊情形，每個提議都被接受，因為每次移動都是從精確的條件分布抽樣。
- [哈密頓蒙地卡羅](hamiltonian-monte-carlo.md)：利用梯度資訊，提出仍可能被接受的遠距離狀態。

## 與其他頁面的連結

- [馬可夫鏈蒙地卡羅](index.md)說明整體框架與搭配使用的診斷。
- [機率與統計](../../../math/probability-statistics/index.md)說明本演算法所要的後驗。
- [變分推論](../variational-inference/index.md)是比抽樣更快但屬近似的替代方法。

## 應用

- **貝氏估計**：對不具共軛結構的模型進行後驗抽樣（Andrieu et al., 2003）。
- **統計物理**：最初的應用，抽取相互作用粒子的組態（Metropolis et al., 1953）。

## 開放問題

- 隨機漫步提議隨維度增加而表現不佳，因為接受率隨參數數量增加而下降。
- 提議尺度需要試跑來調校。適應性版本若設計不當，可能破壞細緻平衡。

## 參考文獻

### 奠基性論文

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics* 21(6), 1087–1092. https://doi.org/10.1063/1.1699114 — 提出對稱的 Metropolis 接受規則。
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — 把規則推廣到非對稱提議，並給出今日使用的接受比率。

### 綜述與教科書

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50, 5–43. https://doi.org/10.1023/A:1020281327116 — 為機器學習讀者推導 Metropolis–Hastings 演算法及其細緻平衡證明。
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — 在高維下比較隨機漫步 Metropolis 與以梯度為基礎的替代方法。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；以實例說明 Metropolis–Hastings 的提議與接受規則。
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 抽樣方法一章涵蓋 Metropolis 演算法。
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — 涵蓋 Metropolis 型抽樣器，以及為後驗模擬調整提議尺度的方法。
