---
translation_reviewed: 2026-10-28
---

# 網格細胞（Hafting et al., 2005）

Hafting et al.（2005）在大鼠的內側內嗅皮質中記錄神經元，發現一些細胞的放電場會在規則的三角形格子點上重複，格子涵蓋整個圍場。這個結果在海馬迴的位置地圖旁，加入了第二種幾何性的空間編碼，也成為之後大量路徑整合研究的基礎。它是[空間導航與認知地圖](../index.md)背後的方法之一。

## 概述

海馬迴中的位置細胞只在單一地點放電，這是 O'Keefe 與 Dostrovsky（1971）所示範的，見[位置細胞](../place-cells/index.md)頁面。海馬迴的空間輸入有很大一部分經由內嗅皮質而來，那是緊鄰海馬迴的皮質區域。Hafting 與同事在老鼠於開放圍場中自由覓食時，記錄該區域中較內側的部分，也就是 MEC。

他們發現的細胞與位置細胞不同。每個網格細胞有數個放電場，而不是一個，而且這些場以規則的型態排列，接近間距相等的六角形，覆蓋整個圍場。論文標題「空間地圖的微結構」反映了這一點：內嗅皮質含有一張精細的、具度量性的空間地圖。

## 核心概念

- **網格場**：網格細胞數個放電場中的一個。
- **格子**：網格場的規則排列。論文中的格子大致為三角形，即一種六角形型態。
- **間距與方向**：相鄰場之間的距離與格子的角度。兩者在各個細胞之間都有差異。
- **路徑整合**：藉由累積自我運動來估計位置。網格細胞是其神經基礎的主要候選者（McNaughton et al., 2006）。

## 運作方式

這項研究可以讀作一個編號的程序：

1. 在內側內嗅皮質植入電極，讓老鼠在開放圍場中自由覓食。
2. 在追蹤老鼠位置的同時記錄單一單元，並把每個單元的棘波畫在動物的行進路徑上。
3. 為每個單元建立放電率地圖，並尋找具有多個放電場的單元。
4. 檢查這些場是否排列在規則的格子上，並以格子的間距與方向描述每個網格細胞。

一個常見的理想化模型，把網格場描述為三個餘弦波之和，三個波的波向量彼此相隔 60 度。以相位 $\phi_j$ 與波向量 $\mathbf{k}_j$ 表示，放電率為

$$
\lambda(\mathbf{x}) = \max\Bigl(0,\; \textstyle\sum_{j=1}^{3} \cos(\mathbf{k}_j \cdot \mathbf{x} + \phi_j)\Bigr)
$$

這是後續研究中使用的建模慣例，並非取自 2005 年論文本身的公式。它抓住了週期性的六角形排列，而間距由波向量的長度決定。
## 結果

主要證據是開放圍場中，個別內嗅單元的放電地圖。許多單元有多個放電場，而每個單元的場形成覆蓋圍場的規則格子。相鄰的細胞在格子間距與方向上有差異。由於本頁撰寫時無法取得論文全文，而且 Crossref 紀錄中也沒有摘要，因此本節只以定性方式描述結果，不引用任何數字。

## 限制

- 研究使用的動物數量少，環境也簡單。格子型態如何隨環境的形狀或大小改變，是之後研究的問題。
- 格子是對放電地圖的描述。論文並未確立網格細胞的用途。網格編碼可以支持路徑整合，但也可能服務於其他目的。

## 未解問題

- **格子從哪裡來？** 吸引子型模型主張連結性產生這種型態，而學習型模型則主張經驗塑造了它。訓練過的網路會出現類網格單元（Banino et al., 2018；Cueva & Wei, 2018），但結果取決於訓練設定，哪些特徵對大腦而言真正重要，仍不清楚。
- **間距由什麼決定？** 網格細胞常與鄰近細胞共享間距與方向，其原因仍有爭議（Moser et al., 2008）。
- **網格編碼的用途是什麼？** 路徑整合是主要候選，但同樣的結構也可能用來索引記憶，或組織非空間的知識。[Tolman–Eichenbaum 機器](../tolman-eichenbaum-machine/index.md)採取後一種觀點。

## 連結

網格細胞與位置細胞是一對：網格細胞提供環境的度量編碼，位置細胞則結合它與感覺地標來使用。能重現類網格單元的訓練網路，見[導航網路中的格狀單元](../../neuroai/grid-like-units/index.md)頁面。
## 參考文獻

### 奠基性論文

- Hafting, T., Fyhn, M., Molden, S., Moser, M.-B. & Moser, E. I. (2005). Microstructure of a spatial map in the entorhinal cortex. *Nature*. https://doi.org/10.1038/nature03721 — 報告內側內嗅皮質中的網格細胞，其放電場在開放圍場中形成規則的三角形格子。
- O'Keefe, J. & Dostrovsky, J. (1971). The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat. *Brain Research*. https://doi.org/10.1016/0006-8993(71)90358-1 — 建立海馬迴空間編碼的位置細胞研究，網格細胞則被發現是餵入這套編碼的上游。
- Cueva, C. J. & Wei, X.-X. (2018). Emergence of grid-like representations by training recurrent neural networks to perform spatial localization. arXiv. https://arxiv.org/abs/1803.07770 — 顯示訓練來進行空間定位的循環網路，會發展出網格狀調諧。
- Banino, A. et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — 顯示格狀單元會在訓練來導航的循環代理人中出現，並幫助它以向量方式導航。

### 綜述與教科書

- Moser, E. I., Kropff, E. & Moser, M.-B. (2008). Place cells, grid cells, and the brain's spatial representation system. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.31.061307.090723 — 回顧網格細胞、它與位置細胞的關係，以及更廣的空間系統。
- McNaughton, B. L. et al. (2006). Path integration and the neural basis of the 'cognitive map'. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1932 — 回顧網格細胞及相關細胞如何在內嗅—海馬迴系統中執行路徑整合。
