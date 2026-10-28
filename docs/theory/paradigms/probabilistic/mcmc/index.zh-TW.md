---
translation_reviewed: 2026-10-28
---

# 馬可夫鏈蒙地卡羅

馬可夫鏈蒙地卡羅（MCMC）透過從一條馬可夫鏈抽取樣本來近似機率分布，該鏈的穩態分布即為目標分布。它是從無法精確積分的後驗抽樣的主要工具。本頁是[機率與貝氏方法](../index.md)的一部分。

## 概述

許多貝氏計算需要後驗 \(p(\theta\mid D)\) 下的期望值，而後驗只能確定到正規化常數的比例。MCMC 建立一條鏈 \(\theta^{(1)}, \theta^{(2)}, \dots\)，其長期分布即為目標分布。對鏈上的樣本取平均可估計期望值，而且永遠不需要正規化常數。鏈必須能夠混合，也就是能在整個分布上移動，而不是停留在某個區域。

基本做法是提出一個移動，並以能保持目標分布不變的機率接受它。[Metropolis–Hastings](metropolis-hastings.md)、[吉布斯抽樣](gibbs-sampling.md)與[哈密頓蒙地卡羅](hamiltonian-monte-carlo.md)是最著名的實現方式。

## 關鍵概念

- **馬可夫鏈**：每個狀態只依賴前一個狀態的序列。其穩態分布即為目標。
- **細緻平衡**：使鏈保持目標分布不變的充分條件，要求任意兩個狀態之間的流量相等。
- **燃燒期**：最初的樣本會被丟棄，因為鏈尚未到達目標分布。
- **混合與自相關**：高度相關的樣本所含資訊較少。有效樣本數衡量一條鏈相當於多少個獨立樣本。
- **診斷**：例如比較多條鏈，或計算潛在尺度縮減因子，用來檢查鏈是否已探索整個目標分布。

## 運作方式

對於目標 \(\pi(\theta)\)，一般的 MCMC 步驟是：從提議分布提出 \(\theta'\)，以機率 \(\alpha\) 接受，否則停留在 \(\theta\)。選擇 \(\alpha\) 使細緻平衡成立，就能讓 \(\pi\) 成為穩態分布。Andrieu 等人（2003）為機器學習讀者給出一般介紹，在同一框架中說明這些條件與標準演算法。

有了樣本，任意函數 \(f\) 的期望值可以估計為 \(\frac{1}{N}\sum_{t} f(\theta^{(t)})\)（去除燃燒期後）。其誤差大致以 \(1/\sqrt{N_{\text{eff}}}\) 遞減，因此決定精確度的是有效樣本數，而非抽樣的次數。

## 主要方法

- [Metropolis–Hastings](metropolis-hastings.md)：從任意提議分布提出移動，並以 Metropolis–Hastings 比率接受。是最一般的方法。
- [吉布斯抽樣](gibbs-sampling.md)：依序從各變數的條件分布抽樣。不需要接受步驟，適合具共軛條件分布的模型。
- [哈密頓蒙地卡羅](hamiltonian-monte-carlo.md)：利用梯度與模擬的動力學，提出遠距離且仍有高接受率的移動。它是 Stan 等工具中 No-U-Turn 抽樣器的基礎。

## 與其他頁面的連結

- [變分推論](../variational-inference/index.md)是以最佳化為基礎的替代方法。它較快但有偏差，MCMC 則漸近精確。
- [機率與統計](../../../math/probability-statistics/index.md)提供 MCMC 所近似的後驗與期望值計算。
- [基於得分的擴散模型](../../unsupervised/density-and-generative-models/diffusion/index.md)藉由反轉加噪過程產生樣本。其抽樣方法與朗之萬動力學密切相關，而朗之萬動力學是以梯度為基礎的 MCMC 方法。
- 腦與認知：以抽樣為基礎的知覺理論主張，神經活動是從隱藏原因的後驗中抽樣。這是活躍的假說，而非既定結果。

## 應用

- **貝氏迴歸與階層模型**：後驗樣本給出可信區間（Gelman et al., 2013）。
- **機率程式設計**：HMC/NUTS 等通用抽樣器為使用者撰寫的模型執行推論（Hoffman & Gelman, 2014）。
- **科學推論**：物理、生態與流行病學中的參數估計，其概似往往很複雜。

## 開放問題

- 診斷收斂很困難，因為鏈可能看起來已收斂，卻遺漏了遠處的模態。
- 高維與多模態的後驗混合緩慢。適應性方法有幫助，但其理論保證仍有缺口。
- 將 MCMC 與大型神經網路結合仍然困難，因為梯度有雜訊，而後驗規模極大。

## 參考文獻

### 奠基性論文

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics*. https://doi.org/10.1063/1.1699114 — 提出 Metropolis 演算法，用於從玻爾茲曼分布抽樣。
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — 把 Metropolis 規則推廣到非對稱提議分布。
- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B* 195, 216. https://ui.adsabs.harvard.edu/abs/1987PhLB..195..216D/abstract — 提出混合（哈密頓）蒙地卡羅方法。

### 綜述與教科書

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50. https://www.cs.ox.ac.uk/publications/publication7533-abstract.html — 為機器學習撰寫的 MCMC 導論，涵蓋 Metropolis–Hastings、吉布斯抽樣及其關係。
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. In *Handbook of Markov Chain Monte Carlo*. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — 綜述 HMC、其調校方式，以及相較隨機漫步抽樣器的優勢。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋 MCMC 方法及其診斷。

### 文章與文件

- Hoffman, M. D. & Gelman, A. (2014). The No-U-Turn sampler: adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research* 15. https://jmlr.org/papers/v15/hoffman14a.html — 提出 NUTS，自動調整 HMC 的路徑長度。
