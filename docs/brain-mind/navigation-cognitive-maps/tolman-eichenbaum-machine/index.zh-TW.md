---
translation_reviewed: 2026-10-28
---

# Tolman–Eichenbaum 機器（Whittington et al., 2020）

Tolman–Eichenbaum 機器（TEM）是 Whittington et al.（2020）提出的模型，其中同一套海馬迴—內嗅系統同時支持空間導航與關係記憶。它的核心主張是，兩者其實是同一個問題：從經驗中學習事物之間如何相關，會連帶產生類位置與類網格的編碼。它是[空間導航與認知地圖](../index.md)背後的方法之一。

## 概述

海馬迴對空間導航是必要的，對關係記憶也是必要的。關係記憶指的是知道項目、事件或狀態彼此如何相連，而不只是知道每個項目是什麼。Tolman 的認知地圖（Tolman, 1948）是一個關係性的概念，而網格細胞與位置細胞則是在空間層次上被發現的。
TEM 統合了兩者。內側內嗅皮質表徵結構性知識，也就是跨情境共享的狀態之間的關係；海馬迴則把這些結構性編碼與感覺內容綁定。共享的結構性編碼讓模型能泛化到新環境。

## 核心概念

- **關係記憶**：對項目或狀態如何相連的知識，它使動物能做出從未直接經歷過的推論。
- **結構表徵**：狀態之間關係的表徵，與狀態看起來如何無關。TEM 主張這種編碼由內嗅細胞承載。
- **感覺表徵**：經驗的內容，例如某個地點看到什麼。TEM 主張海馬迴把它綁定到結構表徵上。
- **重映射**：環境的感覺內容改變時，海馬迴細胞的放電隨之改變。TEM 把重映射視為在保留的結構上，內容發生了改變。

## 運作方式

TEM 是一個生成模型，經過訓練去預測接下來會觀察到什麼。以下步驟簡化了論文的架構。

1. 每一步，內嗅式編碼 $g_t$ 會由前一個編碼與所採取的動作更新，即 $g_t = f(g_{t-1}, a_t)$，使 $g$ 追蹤動物在所學結構中的位置。
2. 目前的觀察 $x_t$ 與 $g_t$ 綁定，形成海馬迴式編碼 $p_t$，並寫入一個聯想記憶。
3. 為了預測觀察，模型會擷取結構編碼與目前相近的已儲存記憶，並讀出與之相連的感覺內容。
4. 參數的學習方式，是在共享相同關係結構的許多環境中，減少經驗序列上的預測誤差。損失形式為 $\mathcal{L} = -\sum_t \log p_\theta(x_t \mid \text{第 } t \text{ 步擷取的記憶})$。

## 結果

本節的摘要取自該論文預印本的摘要（Whittington et al., 2019）。經學習後，模型內嗅式編碼的單元類似網格細胞，此外還有帶狀細胞、邊界細胞與物件向量細胞。海馬迴式編碼的單元則類似位置細胞與地標細胞，並且在不同環境之間發生重映射。模型也能預測複雜非空間任務中所記錄到的表徵。它最具特色的預測是，重映射並非隨機：結構性知識會跨環境保留，論文報告這一點已在同時記錄的位置細胞與網格細胞中得到證實。證據來自模擬與所記錄的神經資料。
## 限制

- TEM 是一個計算理論，它與大腦的對應是部分以類比方式建立的。- 任務是簡化的，環境是模擬的。在真實而多變的經驗中的泛化，尚未以同樣的細節加以展示。
- 能重現某些細胞類型，並不能證明模型是正確的。其他訓練過的網路也會發展出類網格單元，見[導航網路中的格狀單元](../../neuroai/grid-like-units/index.md)頁面的描述。

## 未解問題

- **大腦中的結構性編碼，對空間與非空間關係是否相同？** Behrens et al.（2018）主張可能是相同的，而 TEM 是這項主張的一個具體版本。
- **如何從少數幾次經驗學習新結構？** 大腦如何從單次接觸就形成結構性編碼，目前較不清楚。
- **TEM 與後繼表徵的關係為何？** 後繼表徵主張海馬迴具有預測性、類地圖的編碼（Stachenfeld et al., 2017）。這種編碼與 TEM 的結構性編碼之間的關係，尚未完全釐清。
- **它的哪些預測可以直接檢驗？** 保留結構的重映射，是論文報告已獲證實的一項預測。其他預測則需要有針對性的實驗。

## 連結

TEM 建立在位置細胞與網格細胞的發現之上，相關內容見[位置細胞](../place-cells/index.md)與[網格細胞](../grid-cells/index.md)頁面。它與記憶的連結見[記憶與學習的神經機制](../../memory-learning/index.md)；透過對關係結構的興趣，它也連到[有模型強化學習](../../../theory/paradigms/reinforcement-learning/model-based-rl/index.md)。

## 參考文獻

### 奠基性論文

- Whittington, J. C. R. et al. (2020). The Tolman-Eichenbaum Machine: Unifying space and relational memory through generalization in the hippocampal formation. *Cell*. https://doi.org/10.1016/j.cell.2020.10.024 — 提出一個模型，讓內嗅與海馬迴編碼透過泛化同時支持空間記憶與關係記憶。
- Whittington, J. C. R. et al. (2019). The Tolman-Eichenbaum Machine: Unifying space and relational memory through generalisation in the hippocampal formation. bioRxiv preprint. https://doi.org/10.1101/770495 — 同一研究的預印本，是本頁所總結結果的來源。
- Tolman, E. C. (1948). Cognitive maps in rats and men. *Psychological Review*. https://doi.org/10.1037/h0061626 — 主張迷宮中的老鼠會習得一種類似地圖的環境知識，TEM 則把這個想法延伸到關係記憶。
- Stachenfeld, K. L., Botvinick, M. M. & Gershman, S. J. (2017). The hippocampus as a predictive map. *Nature Neuroscience*. https://doi.org/10.1038/nn.4650 — 主張位置場可理解為類後繼式的預測性地圖。
- Banino, A. et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — 顯示格狀單元會在訓練來導航的循環代理人中出現，並幫助它以向量方式導航。

### 綜述與教科書

- Behrens, T. E. J. et al. (2018). What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior. *Neuron*. https://doi.org/10.1016/j.neuron.2018.10.002 — 主張認知地圖組織的是一般知識而非只有空間，並回顧相關證據。
