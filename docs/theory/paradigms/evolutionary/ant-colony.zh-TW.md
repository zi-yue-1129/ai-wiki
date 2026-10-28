---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/evolutionary
  - theory/paradigms/symbolic-ai
tags:
  - swarm
  - combinatorial
  - optimisation
aliases:
  - 螞蟻演算法
  - ACO
---

# 螞蟻演算法

螞蟻演算法（ACO）以一群人工螞蟻解決離散問題，例如尋找較短的路線。螞蟻逐步建構解，通往好解的路徑會獲得更多費洛蒙，使之後的螞蟻更可能跟隨。

## 概觀

本頁是[演化計算與群體智慧](index.zh-TW.md)的子頁面。上層概述會把 ACO 與連續空間的群體方法[粒子群最佳化](particle-swarm.zh-TW.md)及遺傳方法比較。

## 問題

旅行推銷員問題等組合問題的候選路線太多，無法全部列舉。我們需要一個方法，能從簡單的局部決策建構好解，並在多次嘗試之間共享資訊，而不需要中央規劃者。

## 核心想法

Dorigo、Maniezzo 與 Colorni（1996）取材於真實螞蟻的穩態合作（stigmergy）：它們在走過的路徑上留下費洛蒙，其他螞蟻偏好費洛蒙較多的路徑。在人工版本中，每隻螞蟻依賴費洛蒙與啟發值（對旅行推銷員問題而言是距離的倒數）的機率選擇下一座城市來建構路線。所有螞蟻完成路線後，費洛蒙在各處揮發，並在較短路線的邊上加強。

## 演算法

螞蟻位於城市 \(i\)、在未拜訪城市 \(j\) 間選擇時，機率為

\[
p_{ij} = \frac{\tau_{ij}^{\alpha}\, \eta_{ij}^{\beta}}{\sum_{k \in \mathcal{N}_i} \tau_{ik}^{\alpha}\, \eta_{ik}^{\beta}},
\]

其中 \(\tau_{ij}\) 是邊上的費洛蒙，\(\eta_{ij}\) 是啟發值，\(\alpha\) 與 \(\beta\) 為其權重，\(\mathcal{N}_i\) 是未拜訪的鄰居集合。每次迭代後，費洛蒙更新為 \(\tau_{ij} \leftarrow (1-\rho)\,\tau_{ij} + \Delta\tau_{ij}\)，其中 \(\rho\) 是揮發率，\(\Delta\tau_{ij}\) 是路線使用邊 \((i,j)\) 的螞蟻所存入的量。

## 關鍵結果

Dorigo 等人（1996）介紹 Ant System，並應用於旅行推銷員問題。本頁不引用論文中的數值結果。

## 限制

- 此方法為離散問題設計。連續變數需要離散化或其他方法。
- 費洛蒙可能太快集中在單一路線上，因此變體會加入費洛蒙上下限或額外的探索機制，例如 MAX–MIN Ant System（Stützle & Hoos, 2000）。
- 效能取決於啟發式的選擇，以及參數 \(\alpha\)、\(\beta\) 與 \(\rho\) 的設定。

## 關聯

- [演化計算與群體智慧](index.zh-TW.md)把 ACO 放在族群方法之中。
- [粒子群最佳化](particle-swarm.zh-TW.md)是連續空間的群體方法。
- Ant Colony System（Dorigo & Gambardella, 1997）是較早的變體，加強了對最佳路線的偏好。

## 應用

- 車輛路線規劃、排程與網路路由，好的解來自一連串局部選擇。

## 未解問題

- 應如何設定費洛蒙的上下限與探索，使群體持續找到更好的路線，而不會過早鎖定？
- 在大型實例上，ACO 與學習型的組合求解器相比表現如何？

## 參考文獻

### 開創性論文

- Dorigo, M., Maniezzo, V. & Colorni, A. (1996). *Ant system: optimization by a colony of cooperating agents*. IEEE Transactions on Systems, Man, and Cybernetics, Part B, 26, 29–41. https://doi.org/10.1109/3477.484436 — 提出 Ant System，人工螞蟻在費洛蒙與啟發值的引導下建構路線。
- Dorigo, M. & Gambardella, L. M. (1997). *Ant colony system: a cooperative learning approach to the traveling salesman problem*. IEEE Transactions on Evolutionary Computation, 1, 53–66. https://doi.org/10.1109/4235.585892 — 提出 Ant Colony System，採用局部費洛蒙更新，並更偏好最佳路線。
- Stützle, T. & Hoos, H. H. (2000). *MAX–MIN Ant System*. Future Generation Computer Systems, 16, 889–914. https://doi.org/10.1016/S0167-739X(00)00043-1 — 提出 MAX–MIN Ant System，以費洛蒙上下限限制過早收斂。
- Dorigo, M. & Blum, C. (2005). *Ant colony optimization theory: a survey*. Theoretical Computer Science, 344, 243–278. https://doi.org/10.1016/j.tcs.2005.05.020 — 綜述 ACO 的理論結果。
- Dorigo, M., Birattari, M. & Stützle, T. (2006). *Ant colony optimization: artificial ants as a computational intelligence technique*. IEEE Computational Intelligence Magazine, 1, 28–39. https://doi.org/10.1109/MCI.2006.329691 — 以計算智慧技術的角度概述 ACO。

## 延伸學習

- [維基百科的螞蟻演算法條目](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)概述了主要的變體。
