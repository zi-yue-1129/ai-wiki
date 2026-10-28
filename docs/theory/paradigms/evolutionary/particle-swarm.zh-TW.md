---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/evolutionary
  - theory/optimization
tags:
  - swarm
  - population-based
  - optimisation
aliases:
  - 粒子群最佳化
  - PSO
---

# 粒子群最佳化

粒子群最佳化（PSO）以一群粒子搜尋連續空間。每個粒子在空間中移動，同時被拉向它自己找到的最佳位置，以及其鄰居找到的最佳位置。它不使用梯度。

## 概觀

本頁是[演化計算與群體智慧](index.zh-TW.md)的子頁面。上層概述會把 PSO 與遺傳演算法、演化策略及螞蟻演算法比較。

## 問題

許多連續目標可以評估但無法微分，或是有雜訊且多峰。我們需要一個只用函數值探索空間的方法，而且不需要族群收斂到一點。

## 核心想法

Kennedy 與 Eberhart（1995）將每個粒子視為具有位置 \(x_i\) 與速度 \(v_i\)。每一步中，速度會被拉向兩個吸引子：該粒子曾經到達的最佳位置 \(p_i\)，以及整群或其鄰域所找到的最佳位置 \(g\)。由於速度會保留上一步的動量，粒子會衝過吸引子，並在其周圍搜尋，而不會停在上面。

## 演算法

在每一步從 \([0,1]\) 均勻抽取隨機數 \(r_1, r_2\)，標準形式為

\[
v_i \leftarrow \omega\, v_i + c_1 r_1 (p_i - x_i) + c_2 r_2 (g - x_i), \qquad x_i \leftarrow x_i + v_i,
\]

其中 \(\omega\) 是慣性權重，\(c_1\) 與 \(c_2\) 分別權衡朝個體最佳與鄰域最佳移動的拉力。每次移動後，若新位置更好，就更新 \(p_i\) 與 \(g\)。此方法一般不保證收斂；實務上，群體會停留在搜尋到的最佳區域附近。慣性項由 Shi 與 Eberhart（1998）後來加入；1995 年的原始形式沒有這一項。

## 關鍵結果

本頁不引用 Kennedy 與 Eberhart（1995）的結果，因為尚未對照全文查核。

## 限制

- 一般而言沒有收斂保證。結果取決於慣性與吸引參數，需要調校。
- 在高維問題中表現下降，因為固定數量的粒子只能覆蓋很小一部分空間。
- 限制條件與離散變數需要額外處理；基本方法假設是連續且有盒狀邊界的空間。

## 關聯

- [演化計算與群體智慧](index.zh-TW.md)把 PSO 放在族群方法之中。
- [螞蟻演算法](ant-colony.zh-TW.md)是處理離散路徑問題的群體方法。
- [零階與演化最佳化](../../optimization/zeroth-order-and-evolutionary.zh-TW.md)涵蓋以函數值估計搜尋方向的無梯度方法。

## 應用

- 無法取得梯度時的超參數與參數調校。
- 以模擬器為唯一目標的工程設計。

## 未解問題

- 慣性與吸引參數應如何設定，或在執行中如何調整？
- 與基於梯度的方法相比，PSO 在高維深度學習問題上的擴展性如何？

## 參考文獻

### 開創性論文

- Kennedy, J. & Eberhart, R. (1995). *Particle swarm optimization*. Proceedings of ICNN'95 - International Conference on Neural Networks, 4, 1942–1948. https://doi.org/10.1109/ICNN.1995.488968 — 提出 PSO，每個粒子朝向自身最佳位置與群體最佳位置移動。
- Eberhart, R. C. & Shi, Y. (2001). *Particle swarm optimization: developments, applications and resources*. Proceedings of the IEEE Congress on Evolutionary Computation. https://doi.org/10.1109/cec.2001.934374 — 回顧 PSO 的早期發展與應用。
- Shi, Y. & Eberhart, R. (1998). *A modified particle swarm optimizer*. Proceedings of the 1998 IEEE International Conference on Evolutionary Computation, 69–73. https://doi.org/10.1109/ICEC.1998.699146 — 在速度更新中加入慣性權重，即上方方程式所用的形式。
- Clerc, M. & Kennedy, J. (2002). *The particle swarm: explosion, stability, and convergence in a multidimensional complex space*. IEEE Transactions on Evolutionary Computation, 6, 58–73. https://doi.org/10.1109/4235.985692 — 分析粒子動態，並為速度更新引入收縮係數。
- Poli, R. (2008). *Analysis of the publications on the applications of particle swarm optimisation*. Journal of Artificial Evolution and Applications. https://doi.org/10.1155/2008/685175 — 綜述已發表的 PSO 應用。
- Bonyadi, M. R. & Michalewicz, Z. (2017). *Particle swarm optimization for single objective continuous space problems: a review*. Evolutionary Computation, 25, 1–54. https://doi.org/10.1162/evco_r_00180 — 綜述針對單目標連續問題的 PSO 變體。

## 延伸學習

- [維基百科的粒子群最佳化條目](https://en.wikipedia.org/wiki/Particle_swarm_optimization)對各種變體有淺顯的概述。
