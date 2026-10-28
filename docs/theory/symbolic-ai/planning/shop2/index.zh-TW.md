---
translation_reviewed: 2026-10-28
---

# SHOP2

SHOP2 是一個階層任務網路（HTN）規劃器。它不搜尋目標狀態，而是利用人為每類任務所寫的方法，把高階任務逐步分解為子任務，直到只剩下基本行動為止。它由 Dana Nau 及同事於 2003 年發表，並在 2002 年國際規劃競賽中獲獎。它是[自動規劃概述](../index.md)中具代表性的方法之一。

## 概述

許多實際問題本身就有已知的做法。要送達一個包裹，機器人先取得它，再開到目的地，然後交給收件人。HTN 規劃器把這種知識編碼為方法。每個方法說明它解決哪一類任務、在什麼條件下適用，以及會產生哪些子任務。因此規劃器搜尋的是方法的組合，而不是所有可能的行動序列。

與[STRIPS](../strips/index.md)不同，STRIPS 必須自行發現解的結構，而 HTN 規劃器則由作者提供部分結構。這使它能處理更長的計畫，代價是它依賴方法的品質。

## 關鍵概念

- **任務（Task）**：需要完成的事情。**基本任務**是可以直接執行的行動；**複合任務**則必須被分解。
- **方法（Method）**：適用於複合任務的規則。它有一個針對當前狀態的前提條件，以及一串子任務；當前提成立時，子任務取代該任務。
- **任務網路（Task network）**：仍待執行的任務的有序或偏序清單。
- **依序分解（Ordered decomposition）**：SHOP2 依照寫定的順序處理子任務。

## 運作方式

方法 $m$ 是由一個複合任務、一個關於狀態的前提條件與一串子任務組成的三元組。規劃器從左到右處理任務網路，使每一步的狀態都是已知的。程序如下。

1. 給定當前狀態 $s$ 與任務網路 $T$。若 $T$ 為空，回傳至此已建立的計畫。
2. 取出 $T$ 中的第一個任務 $t$。
3. 若 $t$ 是基本任務，檢查它在 $s$ 中的前提條件。若成立，把對應的運算子套用到 $s$、加入計畫，然後繼續處理 $T$ 的其餘部分。
4. 若 $t$ 是複合任務，找出在 $s$ 中前提成立的 $t$ 的方法。依序嘗試每個方法：以其子任務取代 $t$，然後從第 1 步重複。
5. 若沒有任何方法能導出完整計畫，回溯到最近的選擇。

由於每一步都知道狀態，前提條件可以檢驗完整的當前狀態。2003 年的論文描述了 SHOP2 在時間與度量特性上的功能，這是它在競賽中表現良好的原因。[^1]

## 結果

論文指出，SHOP2 在 2002 年國際規劃競賽中獲得傑出表現獎之一。它把成果歸因於處理時間與度量領域的功能，並詳細描述了這些功能。[^1] 我沒有讀完整的基準表格，因此這裡不引用數字。

## 限制

- **撰寫成本。**方法由人手寫，因此規劃器的表現受限於所給的知識。缺少一個方法，即使解存在也找不到。
- **依賴分解。**階層結構可能排除不符合方法的好計畫，因此規劃器並不是對所有計畫的一般搜尋。
- **順序。**依序分解太早決定子任務的先後，當任務可以重疊時可能造成限制。

## 未解問題

- 方法能否從示範或語言中學習，使撰寫成本下降，同時保留結構？
- 當行動失敗、世界不再符合計畫時，HTN 規劃器應如何復原？

## 相關連結

SHOP2 是為規劃加入階層結構的一種方式，[規劃概述](../index.md)中把它與[STRIPS](../strips/index.md)的扁平搜尋，以及[SayCan](../saycan/index.md)的語言模型方法加以比較。階層式強化學習是其學習上的對應方法，其中的策略選擇子策略，而非人手寫的方法。

## 應用

- **遊戲 AI**，設計者編碼角色如何執行巡邏或掩護等任務。
- **物流與專案規劃**，運送貨物等任務已有標準流程。

## 參考文獻

### 開創性論文

- Nau, D. S. et al. (2003). SHOP2: An HTN Planning System. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1141 — 介紹 SHOP2，一個依序進行階層任務網路分解的規劃器，其時間與度量規劃功能使它在 2002 年競賽中獲獎。
- Fikes, R. E. & Nilsson, N. J. (1971). Strips: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(71)90010-5 — STRIPS 運算子表示法，HTN 規劃器的基本行動即採用這種形式。

### 文章與文件

- Fox, M. & Long, D. (2003). PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1129 — 定義 SHOP2 所設計處理的時間與數值規劃特性。
- Helmert, M. (2006). The Fast Downward Planning System. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1705 — 描述一個非階層式的啟發式 PDDL 規劃器，是競賽中階層分解以外的主要替代方案。
- Hoffmann, J. & Nebel, B. (2001). The FF Planning System: Fast Plan Generation Through Heuristic Search. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.855 — 說明啟發式前向搜尋，這是不依賴人手寫方法的扁平替代方案。
- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — 以原始機器人技能作為計畫中的行動，由語言模型加以組合。

[^1]: Nau et al. (2003)，見上方列表。獎項以及時間與度量特性，依該論文摘要所述。
