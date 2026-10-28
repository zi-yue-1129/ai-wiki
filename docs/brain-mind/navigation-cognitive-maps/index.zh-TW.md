---
translation_reviewed: 2026-10-28
---

# 空間導航與認知地圖

動物與人都會持續追蹤自己身在何處，以及如何抵達想去的地方。海馬迴與鄰近的內嗅皮質中的神經元，會編碼位置、朝向與距離。這些編碼構成一張內在地圖，也就是*認知地圖*，它把空間導航與記憶和規劃連結起來。

## 概述

要抵達目標，動物需要三樣東西：自己的位置、目標的位置，以及兩者之間的路線。1940 年代，Edward Tolman 主張，迷宮中的老鼠學到的不只是一連串的轉向。它們似乎獲得了一種類似地圖的場地知識，讓牠們能走過從未走過的路線（Tolman, 1948）。這個想法在當時引起爭論，至今仍是這個領域的核心。

神經層次的證據出現在 1970 年代。O'Keefe 與 Dostrovsky（1971）在自由活動的老鼠海馬迴中記錄單一神經元，發現某些細胞只在動物位於特定地點時才活躍。之後又發現了其他細胞類型。頭方向細胞會訊號化頭部所指的方向（Taube et al., 1990）。內嗅皮質中的網格細胞，會在環境中許多地點放電，這些地點形成規則的格子（Hafting et al., 2005）。這些細胞合起來構成一套空間編碼，今日仍被深入研究。海馬迴在記憶中的角色，見[記憶與學習的神經機制](../memory-learning/index.md)。

## 核心概念

- **位置細胞**：海馬迴中的神經元，只在環境的某一局部放電，該局部稱為其位置場。
- **網格細胞**：內嗅皮質中的神經元，其放電場會在涵蓋環境的規則、近似三角形的格子點上重複出現。
- **頭方向細胞**：當動物頭部朝向某個特定方向時放電的神經元，與它所在的位置無關。
- **路徑整合**：從已知的起點出發，累積自我運動訊號（例如速度與朝向）來估計自己的位置，不依賴地標。
- **認知地圖**：對地點之間關係的內在表徵，可用來規劃新路線與捷徑。Behrens et al.（2018）以更廣的意義使用這個詞，指任何對狀態之間關係的結構化知識。
- **後繼表徵**：以每個狀態會導向的未來狀態來描述它的一種編碼，並依抵達的遠近加權（Dayan, 1993）。它是一種類似地圖的編碼，對強化學習很有用。

## 運作方式

內側顳葉中的空間編碼是分層建構的。頭方向細胞提供動物的朝向。內側內嗅皮質（MEC）中的網格細胞結合朝向與速度。許多模型主張，這種結合執行路徑整合，隨著動物移動更新其位置的估計（McNaughton et al., 2006）。海馬迴中的位置細胞同時接收網格細胞的輸入與感覺資訊，特別是地標，使每個位置場錨定在環境之中。

```mermaid
flowchart LR
  HD[頭方向細胞] --> GC[網格細胞，MEC]
  SP[速度與朝向] --> GC
  GC --> PC[位置細胞，海馬迴]
  LM[地標與感覺輸入] --> PC
  PC --> CM[認知地圖：路線、捷徑、規劃]
```

後繼表徵提供了另一條通往類地圖知識的路徑。在策略 $\pi$ 下，矩陣 $M(s, s')$ 給出從狀態 $s$ 出發時，未來造訪狀態 $s'$ 的期望折扣次數：

$$
M(s, s') = \mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^{t}\,\mathbf{1}[s_t = s'] \;\middle|\; s_0 = s\right]
$$

狀態的價值，則是它所導向各狀態的獎勵 $R(s')$ 的加權和，即 $V(s) = \sum_{s'} M(s, s')\,R(s')$。由於 $M$ 不依賴獎勵，獎勵改變時只需更新 $R$。Stachenfeld et al.（2017）提出，海馬迴的位置場可以理解為這種預測性地圖。Momennejad et al.（2017）報告，人類在序列決策任務中的選擇，與後繼式學習一致。

人工系統也能出現類網格單元。Cueva 與 Wei（2018）以及 Banino et al.（2018）訓練循環網路進行定位與導航任務，發現具有網格狀放電的隱藏單元。這個結果見[導航網路中的格狀單元](../neuroai/grid-like-units/index.md)頁面。

## 關鍵方法

每個方法都有自己的頁面。此表只做比較。

| 方法 | 區別所在 | 頁面 |
|---|---|---|
| 位置細胞（O'Keefe & Dostrovsky, 1971） | 最早的單細胞證據，顯示海馬迴神經元編碼位置 | [位置細胞](place-cells/index.md) |
| 網格細胞（Hafting et al., 2005） | 內嗅皮質中的細胞，其多個放電場在整個圍場上形成規則格子 | [網格細胞](grid-cells/index.md) |
| 導航網路中的格狀單元（Banino et al., 2018） | 網格狀編碼出現在訓練來導航的人工代理人中，而非在動物身上記錄到 | [導航網路中的格狀單元](../neuroai/grid-like-units/index.md) |
| Tolman–Eichenbaum 機器（Whittington et al., 2020） | 一個模型，讓空間記憶與非空間的關係記憶共用海馬迴—內嗅架構 | [Tolman–Eichenbaum 機器](tolman-eichenbaum-machine/index.md) |

## 連結

- **記憶**：海馬迴最初是作為記憶系統被研究的。確立它對新記憶不可或缺的損傷證據，見[記憶與學習的神經機制](../memory-learning/index.md)與[病人 H.M. 與內側顳葉損傷](../memory-learning/medial-temporal-lesions/index.md)。位置細胞把這些證據連結到空間。
- **重播**：位置細胞在休息與睡眠時重播近期的移動軌跡，見[睡眠、重播與記憶鞏固](../sleep-and-consolidation/index.md)。
- **決策與規劃**：對任務結構的地圖式表徵，支持有模型的選擇（見[有模型與無模型控制](../decision-reward/model-based-vs-model-free/index.md)）。後繼表徵則是一種較省資源、部分無模型的替代方案。Russek et al.（2017）主張，預測性表徵可以連結這兩類控制。
- **NeuroAI**：格狀單元是把網路當作大腦模型的一個清楚例子，見 [NeuroAI](../neuroai/index.md)。

## 應用

- **機器人定位與建圖**：機器人以同步定位與建圖（SLAM）解決同樣的問題，相關內容見[機器人](../../applications/robotics/index.md)。Kanitscheider 與 Fiete（2016）訓練循環網路執行類 SLAM 的二維導航任務，其隱藏單元展現出海馬迴位置細胞的若干性質。
- **強化學習**：儲存後繼表徵的代理人，在獎勵改變時能快速重新評估各選項，因為環境的結構與獎勵是分開儲存的。Gershman（2018）回顧了其計算邏輯，以及神經資料中的相關證據。
- **人類導航研究**：Epstein et al.（2017）回顧人類認知地圖的證據，並探討這個概念能延伸到導航之外多遠。

## 未解問題

- **認知地圖只涉及空間嗎？** Behrens et al.（2018）與 Bellmund et al.（2018）主張，相同的編碼原則可能也組織抽象的非空間知識。這方面的證據仍在發展中。
- **網格編碼從哪裡來？** 訓練過的網路會發展出類網格單元，但結果取決於架構、訓練目標與環境。人工代理人學到的編碼，是否與大腦中產生網格細胞的特徵相同，仍在研究中。
- **預測性地圖與空間地圖是同一回事嗎？** Stachenfeld et al.（2017）主張兩者相同，但要直接檢驗這點並不容易。
- **線索與自我運動如何整合？** 地標與路徑整合可能相互矛盾。大腦如何解決這類衝突，是活躍的研究問題。

## 參考文獻

### 奠基性論文

- Tolman, E. C. (1948). Cognitive maps in rats and men. *Psychological Review*. https://doi.org/10.1037/h0061626 — 主張迷宮中的老鼠會習得一種類似地圖的環境知識，使牠們能走過未曾走過的路線。
- O'Keefe, J. & Dostrovsky, J. (1971). The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat. *Brain Research*. https://doi.org/10.1016/0006-8993(71)90358-1 — 報告自由活動的老鼠海馬迴中，有單元在動物位於特定地點時放電。
- Taube, J. S., Muller, R. U. & Ranck, J. B. (1990). Head-direction cells recorded from the postsubiculum in freely moving rats. I. Description and quantitative analysis. *Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.10-02-00420.1990 — 描述大鼠後下托中的神經元，其放電取決於頭部朝向的方向，而非位置或行為。
- Hafting, T. et al. (2005). Microstructure of a spatial map in the entorhinal cortex. *Nature*. https://doi.org/10.1038/nature03721 — 報告內側內嗅皮質中的網格細胞，其放電場在開放圍場中形成規則的三角形格子。
- Dayan, P. (1993). Improving generalization for temporal difference learning: the successor representation. *Neural Computation*. https://doi.org/10.1162/neco.1993.5.4.613 — 提出後繼表徵，這是一種以時序差分方法學習的狀態編碼，並以導航任務加以說明。
- Stachenfeld, K. L., Botvinick, M. M. & Gershman, S. J. (2017). The hippocampus as a predictive map. *Nature Neuroscience*. https://doi.org/10.1038/nn.4650 — 主張海馬迴的位置場可理解為環境中類後繼式的預測性地圖。
- Momennejad, I. et al. (2017). The successor representation in human reinforcement learning. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-017-0180-8 — 將後繼式與有模型的預測，與人類在序列決策任務中的選擇加以比較。
- Cueva, C. J. & Wei, X.-X. (2018). Emergence of grid-like representations by training recurrent neural networks to perform spatial localization. arXiv. https://arxiv.org/abs/1803.07770 — 顯示訓練來進行空間定位的循環網路，會發展出網格狀調諧，這與 Banino et al.（2018）的結果平行。
- Banino, A. et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — 顯示格狀單元會在訓練來導航的循環代理人中出現，並幫助它以向量方式導航。
- Whittington, J. C. R. et al. (2020). The Tolman-Eichenbaum Machine: Unifying space and relational memory through generalization in the hippocampal formation. *Cell*. https://doi.org/10.1016/j.cell.2020.10.024 — 提出一個模型，讓內嗅與海馬迴編碼透過泛化同時支持空間記憶與關係記憶。
- Kanitscheider, I. & Fiete, I. (2016). Training recurrent networks to generate hypotheses about how the brain solves hard navigation problems. arXiv. https://arxiv.org/abs/1609.09059 — 訓練循環網路執行類 SLAM 的導航任務，並發現具有位置細胞式性質的隱藏單元。

### 綜述與教科書

- Moser, E. I., Kropff, E. & Moser, M.-B. (2008). Place cells, grid cells, and the brain's spatial representation system. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.31.061307.090723 — 回顧位置細胞、網格細胞及相關細胞，以及它們如何共同表徵空間。
- McNaughton, B. L. et al. (2006). Path integration and the neural basis of the 'cognitive map'. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1932 — 回顧自我運動訊號如何被整合，以在海馬迴結構中維持認知地圖。
- Epstein, R. A. et al. (2017). The cognitive map in humans: spatial navigation and beyond. *Nature Neuroscience*. https://doi.org/10.1038/nn.4656 — 回顧人類認知地圖的證據，並探討這個概念如何延伸到空間導航之外。
- Behrens, T. E. J. et al. (2018). What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior. *Neuron*. https://doi.org/10.1016/j.neuron.2018.10.002 — 主張認知地圖組織的是一般知識而非只有空間，並回顧相關證據。
- Bellmund, J. L. S. et al. (2018). Navigating cognition: Spatial codes for human thinking. *Science*. https://doi.org/10.1126/science.aat6766 — 回顧空間編碼如何支持非空間的思考，結合認知科學與神經科學的觀點。
- Gershman, S. J. (2018). The successor representation: its computational logic and neural substrates. *Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.0151-18.2018 — 回顧後繼表徵作為計算工具的角色，以及與之相關的神經資料。
- Russek, E. M. et al. (2017). Predictive representations can link model-based reinforcement learning to model-free mechanisms. *PLOS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1005768 — 主張類後繼式的預測性表徵，可以連結有模型與無模型控制。
