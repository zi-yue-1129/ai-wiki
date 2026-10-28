---
translation_reviewed: 2026-10-28
---

# 哈密頓蒙地卡羅

哈密頓蒙地卡羅（HMC）透過模擬一個在目標分布中運動的粒子之物理動力學，來提出遠距離的狀態，再以 Metropolis 步驟修正結果。利用梯度使它在高維下遠比隨機漫步提議有效率。本頁是[馬可夫鏈蒙地卡羅](index.md)的一部分。

## 概述

隨機漫步提議在高維中移動緩慢，因為多數提議的移動落在低機率區域而被拒絕。HMC 引入輔助的動量變數 \(p\)，並遵循哈密頓動力學，使總能量近似守恆。軌跡沿著平滑的長路徑探索分布，最後狀態再被接受或拒絕，以修正數值誤差。

## 關鍵概念

- **位能**：\(U(\theta) = -\log\pi(\theta)\)，因此低能量區域即高機率區域。
- **動能**：\(K(p) = \tfrac12 p^\top M^{-1} p\)，質量矩陣 \(M\) 通常為對角矩陣。
- **蛙跳積分器**：一種辛數值方法，以步長 \(\varepsilon\) 的小步模擬動力學，並近似守恆能量。
- **步長與路徑長度**：步長決定精確度，步數決定軌跡走多遠。
- **No-U-Turn 抽樣器（NUTS）**：自動選擇步數的延伸方法，當軌跡開始折返時停止（Hoffman & Gelman, 2014）。

## 運作方式

每次 HMC 迭代做三件事：

1. 抽取新的動量 \(p \sim \mathcal{N}(0, M)\)。
2. 從 \((\theta, p)\) 出發，以蛙跳法模擬哈密頓動力學 \(L\) 步，得到 \((\theta^\*, p^\*)\)。
3. 以機率 \(\min\!\big(1, \exp(H(\theta,p)-H(\theta^\*,p^\*))\big)\) 接受 \((\theta^\*, p^\*)\)，其中 \(H = U + K\)。

由於蛙跳積分器近似守恆 \(H\)，即使軌跡很長，接受機率仍然很高。Neal（2011）綜述此方法，並說明為何動力學能給出既遠距離又可能被接受的提議。最初的想法由 Duane 等人（1987）以混合蒙地卡羅的名稱，在格點物理中提出。

Hoffman 與 Gelman（2014）顯示 NUTS 無需手動設定路徑長度即表現良好，使 HMC 在機率程式設計系統中變得實用。

## 主要方法

- [Metropolis–Hastings](metropolis-hastings.md)：HMC 所改進的隨機漫步方法，HMC 仍然使用其接受修正。
- No-U-Turn 抽樣器（NUTS）：參考文獻中描述的適應性變體，無需手動設定路徑長度。

## 與其他頁面的連結

- [馬可夫鏈蒙地卡羅](index.md)描述 HMC 所屬的一般框架。
- [微積分與最佳化](../../../math/calculus/index.md)提供驅動動力學的梯度，[最佳化](../../../optimization/index.md)則涵蓋同類函數上的梯度方法。
- 不帶動量的朗之萬動力學與 HMC 相關，而其梯度抽樣也與[基於得分的擴散模型](../../unsupervised/density-and-generative-models/diffusion/index.md)所用的抽樣相關。

## 應用

- **機率程式設計**：Stan 等系統的預設抽樣器，使用者撰寫模型，抽樣器執行推論（Hoffman & Gelman, 2014）。
- **階層模型**：隨機漫步抽樣器難以處理的後驗幾何，由 HMC 處理得較好（Neal, 2011）。
- **格點場論**：最初的應用，該方法最初即為模擬量子場論而提出（Duane et al., 1987）。

## 開放問題

- 梯度成本：每一步都需要對數密度的梯度，對大型模型而言很昂貴。
- 在 NUTS 之外，質量矩陣與步長的調校仍部分依賴手動，而適應性方案的保證有限。
- 多模態後驗可能使軌跡困在單一模態內，因此 HMC 仍需其他方法互補。

## 參考文獻

### 奠基性論文

- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B* 195, 216. https://ui.adsabs.harvard.edu/abs/1987PhLB..195..216D/abstract — 提出結合分子動力學與 Metropolis 修正的混合方法。
- Hoffman, M. D. & Gelman, A. (2014). The No-U-Turn sampler: adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research* 15. https://jmlr.org/papers/v15/hoffman14a.html — 提出 NUTS，自動選擇路徑長度。

### 綜述與教科書

- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. In *Handbook of Markov Chain Monte Carlo*. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — HMC 綜述，包括蛙跳積分器、能量守恆與調校。
- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50. https://www.cs.ox.ac.uk/publications/publication7533-abstract.html — 把 HMC 置於一般 MCMC 演算法之中的導論。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋 HMC 及其對梯度的需求。
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — 討論在應用模型中以 HMC 與 NUTS 進行後驗模擬。
