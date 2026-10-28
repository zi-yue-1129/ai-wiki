---
translation_reviewed: 2026-10-28
---

# Metropolis–Hastings 演算法

Metropolis–Hastings 演算法是最基本的[馬可夫鏈蒙地卡羅](../index.md)演算法。它從目前狀態提出一個移動，並以某個機率接受它，使目標分布保持不變。幾乎所有其他 MCMC 方法，若不是它的特例，就是它的接受－拒絕步驟的變體。

## 概述

此演算法只需要目標的未正規化密度，因此不必計算那個使貝氏推論變得困難的正規化常數。它適用於任何能夠計算密度的目標，也不需要梯度。此方法由 Metropolis 等人（1953）為統計物理中的狀態方程而提出。Hastings（1970）把接受規則推廣到不必對稱的提議，也就是今日通行的形式。Chib 與 Greenberg（1995）清楚說明了接受規則及其推導。

這種通用性的代價是探索緩慢：隨機漫步提議需要許多微小的步，所需步數隨維度快速增加。

## 核心概念

- **提議分布** $q(x' \mid x)$：從目前狀態 $x$ 提出新狀態 $x'$ 的規則。隨機漫步提議是在 $x$ 上加入高斯雜訊。
- **接受機率**：移動到提議狀態的機率，由目標密度與提議密度的比值決定。
- **拒絕**：若提議被拒絕，鏈就停在原地，這會拖慢混合。
- **步長**：提議的尺度。步長太大常被拒絕，太小則移動緩慢，因此必須取得平衡。

## 運作方式

設 $\tilde\pi$ 為未正規化的目標。提議 $x'$ 以下列機率被接受：

$$
\alpha(x, x') = \min\!\left(1,\; \frac{\tilde\pi(x')\,q(x \mid x')}{\tilde\pi(x)\,q(x' \mid x)}\right).
$$

正規化常數在比值中被消去。若提議對稱，即 $q(x\mid x') = q(x'\mid x)$，此因子就化為 Metropolis 比值 $\tilde\pi(x')/\tilde\pi(x)$。演算法如下：

1. 把 $x_0$ 設為任一滿足 $\tilde\pi(x_0) > 0$ 的狀態。
2. 對 $t = 1, \dots, N$，抽取 $x' \sim q(\cdot \mid x_{t-1})$。
3. 抽取 $u \sim \mathrm{Uniform}(0, 1)$。若 $u < \alpha(x_{t-1}, x')$，令 $x_t = x'$；否則令 $x_t = x_{t-1}$。

此規則滿足細緻平衡。從 $x$ 移到 $x'$ 的機率為 $q(x'\mid x)\,\alpha(x,x')$，而兩個方向的流量之比等於目標密度之比，因此目標是平穩的。之後的使用方式如[上層頁面](../index.md)所述。

在實務上，起始樣本仍受起點影響，因此要丟棄燃燒期；調校步長時也要監控接受率。

## 實驗結果

Metropolis 等人（1953）把此方法應用於二維的剛性球體系統。他們把模擬得到的狀態方程，與自由體積方程及四項維里展開式作比較。這篇論文說明了，一條簡單的隨機移動鏈可以算出用解析方法很難得到的性質。論文沒有現代意義下的基準測試，證據只是與參考結果的定性吻合。

Metropolis–Hastings 在統計學中的主要理論指引出現得較晚。Roberts 與 Rosenthal（1998）針對一個密切相關、以梯度為基礎的提議指出，使演算法在高維中效率最高的接受率約為 0.574，而且計算成本隨維度增加的速度比隨機漫步提議慢。

## 限制

- **探索緩慢**。隨機漫步提議以擴散式的小步移動。在高維中步長必須縮小，所需步數迅速增加。
- **相關的目標**。若目標是一條不與座標軸對齊的窄脊，每次只改變一個座標的提議幾乎總會被拒絕。
- **調校**。提議尺度必須人工設定，或以保持目標不變的適應性方法調整，這增加了實務上的複雜度。
- **多峰目標**。從某一模態出發的鏈，可能需要很長時間才找到其他模態。

## 開放問題

- 如何在執行中調整提議，又不失去目標精確的保證？
- 除了最佳尺度理論所涵蓋的類高斯情形之外，對於某一族目標，哪種提議的縮放效果最好？

## 參考文獻

### 開創性論文

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of State Calculations by Fast Computing Machines. *Journal of Chemical Physics*. https://doi.org/10.1063/1.1699114 — 提出以接受－拒絕鏈計算交互作用粒子狀態方程的 Metropolis 方法。
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika*. https://doi.org/10.1093/biomet/57.1.97 — 將接受規則推廣到非對稱提議，形成今日通行的 Metropolis–Hastings 演算法。

### 綜述與教科書

- Chib, S. & Greenberg, E. (1995). Understanding the Metropolis-Hastings Algorithm. *The American Statistician*. https://doi.org/10.1080/00031305.1995.10476177 — 清楚推導接受規則，並說明其在實務中的用法。
- Robert, C. P. & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer. https://doi.org/10.1007/978-1-4757-4145-2 — 研究所層級的教科書，涵蓋蒙地卡羅與 MCMC 方法的理論與實作。
- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An Introduction to MCMC for Machine Learning. *Machine Learning*. https://doi.org/10.1023/A:1020281327116 — 為機器學習讀者解說主要 MCMC 演算法的入門教程。

### 文章與文件

- Roberts, G. O. & Rosenthal, J. S. (1998). Optimal Scaling of Discrete Approximations to Langevin Diffusions. *JRSS B*. https://doi.org/10.1111/1467-9868.00123 — 給出朗之萬擴散導出之 Metropolis 型提議的最佳接受率與維度縮放。
- Geyer, C. J. (1992). Practical Markov Chain Monte Carlo. *Statistical Science*. https://doi.org/10.1214/ss/1177011137 — 主張推論應建立在單一長執行上，並從自相關估計蒙地卡羅誤差。
