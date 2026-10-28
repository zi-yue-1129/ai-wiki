---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - start/history/symbolic-era
tags:
  - history
  - expert systems
  - AI winter
aliases:
  - 專家系統
  - AI 寒冬
  - 專家系統與寒冬
  - Expert systems and AI winters
---

# 歷史：專家系統與 AI 寒冬（1974–2006）

在最初的樂觀之後，AI 進入了專家系統、大型公共計畫與經費削減並存的時期。隨後出現了兩段經費與興趣縮減的時期，通稱 AI 寒冬。這段歷史的結尾是神經網路的回歸，它依賴遠大於以往的資料與運算預算。本頁涵蓋通用目標的衰退、專家系統的興衰，以及方法上逐步的轉變，這些轉變為[下一章](../deep-learning-revolution/index.zh-TW.md)的深度學習革命鋪路。

## 概述

早期的符號計畫曾承諾通用智能，但在問題超出玩具領域時便陷入困難。1972 年，Lighthill 為英國科學研究委員會所做的綜述認為，AI 未能實現其廣泛的目標，並指出組合爆炸是主要障礙 [(Lighthill, 1972)](https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm)。報告之後英國的基礎研究經費被大幅削減，通常被視為第一次寒冬的開端。

## 關鍵概念

- **專家系統**：以規則編碼領域專家知識，並以規則推導結論的程式。專家系統是 1980 年代最主要的商用 AI 形式。
- **知識工程**：擷取並編碼專家知識的過程，事後證明既緩慢又難以維護。
- **AI 寒冬**：在過度承諾的技術未能達到預期後，經費與興趣減少的時期。
- **反向傳播**：計算多層網路梯度的方法，使神經網路在 1980 年代重新可以訓練。

## 專家系統

專家系統把規則式推理應用於專門領域，包括醫療診斷與設備組態。它們在狹窄範圍內很有用，但代價也很高。知識必須從專家身上擷取並持續更新，規則之間的互動難以預測，而且系統無法從資料中學習。1980 年代對它們的商業興趣快速成長，之後隨著維護成本上升，以及它們所依賴的部分硬體市場改變，興趣又逐漸下降。

## 神經網路的回歸

1986 年，Rumelhart、Hinton 與 Williams 展示了反向傳播可以訓練多層網路，學習內部表徵，這回應了對單層感知器批評的一部分 [(Rumelhart, Hinton and Williams, 1986)](https://doi.org/10.1038/323533a0)。這個結果重新點燃了對連結主義模型的興趣。神經網路的經費與熱情在 1990 年代又經歷起伏，領域也轉向支持向量機與機率模型等統計方法，這些方法有較強的理論基礎，而且在當時的資料上表現良好。轉向統計方法是整個機器學習的一項廣泛改變，其影響遠超過神經網路本身。

## 資料與運算

到了 2000 年代，標記資料與運算能力已成長到足以改變什麼是可行的。大型標記影像資料庫 ImageNet，提供了一個足夠大的基準，可以測試大規模的深度網路 [(Deng et al., 2009)](https://doi.org/10.1109/cvpr.2009.5206848)。從手寫規則轉向學習表徵的變革，在 1980 年代已經開始，此時終於有了資料與之配合。

## 與其他頁面的關聯

這段時期承接前面的[符號時代歷史](../symbolic-era/index.zh-TW.md)，也與[符號 AI](../../../theory/paradigms/symbolic-ai/index.zh-TW.md)頁面中的規則式系統相連。取代專家系統的方法見[機器學習](../../../theory/machine-learning/index.zh-TW.md)，反向傳播本身則見[自動微分](../../../theory/math/automatic-differentiation/index.zh-TW.md)。

## 應用

專家系統被用於醫療、金融、電腦系統組態與工業診斷。它們的遺產可見於商業規則引擎與決策支援軟體，這些軟體今日仍會在學習模型旁使用明確的規則。

## 開放問題

- 寒冬是因為過度承諾、方法本身，還是當時的經費結構所造成？
- 為什麼專家系統無法擴展？當規則仍需人工撰寫、並與學習模型並存時，同樣的問題是否會再次出現？
- 轉向統計方法，在多大程度上延後了神經網路的回歸？

## 參考文獻

### 重要論文

- Rumelhart、Hinton 與 Williams，*Learning representations by back-propagating errors*，Nature（1986）。https://doi.org/10.1038/323533a0 — 展示反向傳播可以訓練多層網路學習有用的內部表徵。
- Deng 等人，*ImageNet: A large-scale hierarchical image database*，IEEE Conference on Computer Vision and Pattern Recognition（2009）。https://doi.org/10.1109/cvpr.2009.5206848 — 描述後來成為深度網路基準的大型標記影像資料庫。

### 綜述與教科書

- Lighthill，*Artificial Intelligence: A General Survey*，Science Research Council（1972）。https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm — 批判性綜述，其結論促成英國 AI 研究經費的削減。

### 文章與文件

- Hinton、Osindero 與 Teh，*A Fast Learning Algorithm for Deep Belief Nets*，Neural Computation（2006）。https://doi.org/10.1162/neco.2006.18.7.1527 — 通常被視為深度學習復甦起點的論文，詳見[下一章](../deep-learning-revolution/index.zh-TW.md)。
- Krizhevsky、Sutskever 與 Hinton，*ImageNet Classification with Deep Convolutional Neural Networks*，NeurIPS（2012）。https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，標誌著深度網路在大型資料上的規模化。
