---
translation_reviewed: 2026-10-28
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/world-models
tags:
- neuroscience
- navigation
- cognitive maps
- representation learning
aliases:
  - 空間導航與認知地圖
  - 認知地圖
  - 空間導航
  - Spatial navigation
  - Cognitive maps
  - Cognitive map
  - Place cells
---

# 空間導航與認知地圖

動物找路時，會在內部建立自己所在位置、以及各處如何相連的表徵。這些表徵若形成一張**認知地圖**，也就是一個能支持規劃與新捷徑的環境模型，那麼導航就與記憶和決策連在一起。同樣的想法也出現在 AI 中：智慧體學習自己世界的模型，並建立可在目標改變時重複使用的表徵。

本頁是總覽。每種方法都有自己的頁面，列在下方的「關鍵方法」一節。

## 概述

一個核心問題是：大腦如何把移動與感官輸入，轉成對所在位置的感覺。在齧齒類動物中，研究最多的有三種細胞：

| 細胞類型 | 位置 | 訊號內容 |
|---|---|---|
| 位置細胞 | 海馬迴 | 動物位於某個特定地點 |
| 頭部方向細胞 | 邊緣系統與鄰近區域 | 頭部朝向某個特定方向 |
| 格狀單元 | 內嗅皮質 | 排列成規則格網的許多地點，提供距離的度量 |

格狀單元的細節見[導航網路中的格狀單元](../neuroai/grid-like-units/index.md)，本頁不重複該內容。

認知地圖的想法早於這些記錄。Tolman（1948）在一篇關於大鼠與人的論文中提出「認知地圖」一詞。這樣的地圖能讓動物算出一條從未走過的路。之後的問題是，哪些神經結構承載這樣的地圖，以及它採取什麼形式。

## 關鍵概念

- **位置細胞**：海馬迴中的神經元，當動物位於環境的特定部分時會強烈放電；該區域稱為其位置場。
- **頭部方向細胞**：放電取決於頭部朝向的神經元，與位置無關（Taube 等人，1990）。
- **認知地圖**：對環境佈局的內部表徵，或對項目之間關係的表徵，用於彈性行為。
- **路徑積分**：只靠自身移動估計位置，不依賴地標。
- **後繼表徵（SR）**：用狀態會通往的未來狀態來描述該狀態。見[後繼表徵](successor-representation/index.md)。
- **Tolman–Eichenbaum 機器（TEM）**：透過共用的結構化表徵，把空間記憶與關係記憶連在一起的模型。見[Tolman–Eichenbaum 機器](tolman-eichenbaum-machine/index.md)。

## 運作方式

頭部方向細胞的放電隨動物的朝向而變化。此訊號及其來源由 Taube（2007）回顧。其計算面見[計算神經科學](../computational-neuroscience/index.md)。

## 關鍵方法

- [Tolman–Eichenbaum 機器（Whittington 等人，2020）](tolman-eichenbaum-machine/index.md)：把空間導航與關係記憶視為同一個問題，並從共用結構中產生類似格狀與位置的單元。
- [後繼表徵（Dayan，1993）](successor-representation/index.md)：儲存狀態未來被佔據的期望值，使狀態之間轉移的結構與各狀態的獎勵分開。
- [位置細胞與認知地圖假說（O'Keefe 與 Dostrovsky，1971）](place-cells/index.md)：對自由移動大鼠單元活動的初步報告，並以其標題提出海馬迴是一張空間地圖。

## 關聯

- **記憶**：海馬迴同時是情節記憶與導航的核心。[記憶與學習的神經機制](../memory-learning/index.md)涵蓋更完整的圖像，[互補學習系統](../memory-learning/complementary-learning-systems/index.md)說明快速的海馬迴學習如何與慢速的皮質學習相關。
- **規劃與決策**：認知地圖讓規劃成為可能，這就是[有模型與無模型控制](../decision-reward/model-based-vs-model-free/index.md)中描述的有模型策略。規劃在選擇中的整體角色見[決策、多巴胺與獎勵](../decision-reward/index.md)。
- **強化學習**：後繼表徵由時序差分學習建構，與多巴胺被認為傳遞的更新屬於同一類（Gershman，2018 回顧其計算邏輯）。見[強化學習](../../theory/paradigms/reinforcement-learning/index.md)與[多巴胺的獎勵預測誤差](../neuroscience/dopamine-reward-prediction-error/index.md)。
- **預測處理**：預測地圖的想法與大腦是預測機器的觀點相關，見[預測編碼與自由能原理](../predictive-coding/index.md)。
- **AI**：學習得來的世界模型與地圖式表徵，見[世界模型與具身智慧](../../theory/models/world-models/index.md)。更廣的 NeuroAI 圖像見[NeuroAI：大腦與 AI 的雙向啟發](../neuroai/index.md)。

## 應用

- **模擬人類學習**：Momennejad 等人（2017）以兩項人類行為研究檢驗後繼表徵，考察人類選擇如何隨事件順序與獎勵的改變而變化。
- **訓練出的導航智慧體**：只受過導航訓練的人工智慧體能否出現格狀單元，見[格狀單元頁面](../neuroai/grid-like-units/index.md)。

## 未解問題

- **地圖的通用程度？** TEM 主張同一結構同時服務空間與關係知識。Behrens 等人（2018）討論認知地圖作為組織知識的一般方式，不只限於實體空間，但範圍仍有爭議。
- **位置細胞編碼什麼？** 有些觀點把位置細胞視為位置的地圖。Stachenfeld 等人（2017）則提出預測地圖。
- **格狀編碼是否依賴設計選擇？** 受訓練的智慧體中出現格狀單元的情況仍有爭議，[NeuroAI 頁面](../neuroai/index.md)有相關說明。
- **生物與人工導航者是否共享機制？** 行為或細胞類型相符，本身並不能說明機制相同。

## 參考文獻

### 開創性論文

- O'Keefe, J. 與 Dostrovsky, J.（1971）。The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat. *Brain Research*。https://doi.org/10.1016/0006-8993(71)90358-1 — 以自由移動大鼠的單元活動提供初步證據，其標題提出海馬迴是一張空間地圖。
- Tolman, E. C.（1948）。Cognitive maps in rats and men。*Psychological Review*。https://doi.org/10.1037/h0061626 — 在一篇關於大鼠與人的論文中提出「認知地圖」一詞，即本頁所用概念的來源。
- Taube, J. S.、Muller, R. U. 與 Ranck, J. B.（1990）。Head-direction cells recorded from the postsubiculum in freely moving rats. I. Description and quantitative analysis。*Journal of Neuroscience*。https://doi.org/10.1523/JNEUROSCI.10-02-00420.1990 — 描述後下托中放電取決於頭部方向的細胞。
- Hafting, T. 等人（2005）。Microstructure of a spatial map in the entorhinal cortex。*Nature*。https://doi.org/10.1038/nature03721 — 描述內嗅皮質中的格狀細胞。列為背景資料；格狀細胞的細節見格狀單元頁面。
- Dayan, P.（1993）。Improving generalization for temporal difference learning: the successor representation。*Neural Computation*。https://doi.org/10.1162/neco.1993.5.4.613 — 示範時序差分學習如何學到一種表徵，其中每個狀態由其後繼狀態描述。
- Whittington, J. C. R. 等人（2020）。The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation。*Cell*。https://doi.org/10.1016/j.cell.2020.10.024 — 提出一個模型，說明海馬迴與內嗅結構如何同時支持空間與關係記憶。
- Stachenfeld, K. L.、Botvinick, M. M. 與 Gershman, S. J.（2017）。The hippocampus as a predictive map。*Nature Neuroscience*。https://doi.org/10.1038/nn.4650 — 借鏡強化學習，提出海馬迴把空間表徵為預測地圖。

### 綜述與教科書

- Behrens, T. E. J. 等人（2018）。What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior。*Neuron*。https://doi.org/10.1016/j.neuron.2018.10.002 — 回顧認知地圖，包括其延伸至抽象知識的部分。
- Gershman, S. J.（2018）。The Successor Representation: Its Computational Logic and Neural Substrates。*Journal of Neuroscience*。https://doi.org/10.1523/JNEUROSCI.0151-18.2018 — 回顧後繼表徵的計算邏輯與大腦中的證據。
- Taube, J. S.（2007）。The Head Direction Signal: Origins and Sensory-Motor Integration。*Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.neuro.29.051605.112854 — 回顧頭部方向訊號的來源，以及它如何與移動整合。

### 文章與文件

- Momennejad, I. 等人（2017）。The successor representation in human reinforcement learning。*Nature Human Behaviour*。https://doi.org/10.1038/s41562-017-0180-8 — 把後繼表徵應用於人類強化學習。
