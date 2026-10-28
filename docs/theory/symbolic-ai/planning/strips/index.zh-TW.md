---
translation_reviewed: 2026-10-28
---

# STRIPS

STRIPS 是 Richard Fikes 與 Nils Nilsson 於 1971 年為史丹佛研究院的問題求解器提出的表示法與規劃方法。它以前提條件、新增的事實與刪除的事實描述每個行動，並透過搜尋這些行動產生的狀態來找出計畫。它是古典規劃形式體系的起源，也是[自動規劃概述](../index.md)中第一個具代表性的方法。

## 概述

規劃器需要一種精簡的方式來描述行動做了什麼。若為每個行動列出它對整個世界的完整影響，會非常繁瑣。STRIPS 讓描述保持精簡：行動只改變它所提到的事實，其餘事實都假設維持原狀。

這個表示法是為行動機器人設計的，它也把規劃與邏輯連結起來。[^1] 之後的 PDDL 語言把問題標準化，是在這類描述之上的延伸。[^2]

## 關鍵概念

- **運算子（行動模式）**：一個帶有參數的命名行動，例如 `move(robot, from, to)`。
- **前提條件清單**：行動執行前必須為真的事實。
- **新增清單**：行動執行後會變為真的事實。
- **刪除清單**：行動執行後不再為真的事實。
- **封閉世界假設**：狀態中沒有出現的事實都視為假。因此否定的前提條件要寫成「某事實不存在」。
- **鬆弛問題**：保留相同運算子，但移除其刪除清單。它的解的成本常被用作原問題的啟發式估計。[^3]

## 運作方式

狀態是一組基礎事實。當行動 $a$ 的前提條件都包含在狀態 $s$ 中時，它在 $s$ 上可以執行。執行後得到的後繼狀態為

$$
\mathrm{succ}(s, a) = \bigl(s \setminus \mathrm{del}(a)\bigr) \cup \mathrm{add}(a), \quad \text{若 } \mathrm{pre}(a) \subseteq s。
$$

規劃器接著執行以下程序。

1. 從初始狀態 $s_0$ 開始，並把它放入前沿。
2. 從前沿取出一個狀態 $s$。若目標事實都在 $s$ 中，就回傳通往 $s$ 的路徑上的行動序列。
3. 對每個前提條件在 $s$ 中成立的運算子，用上式計算後繼狀態，並記錄產生它的行動。
4. 依某種搜尋策略（如廣度優先搜尋，或以啟發式的 A\*）把新狀態加入前沿，然後回到第 2 步。
5. 若前沿已空，表示不存在計畫。

這個搜尋就是圖搜尋。STRIPS 的貢獻在於它提供了用來產生後繼狀態的精簡描述。之後的啟發式規劃器保留這個表示法，並改變搜尋順序。[^3]

## 結果

1971 年的論文是附有實例的方法描述，而不是基準測試。其證據是：行動描述與定理證明可以為機器人任務產生計畫。我沒有讀完全文，因此這裡不引用任何數字。之後對同一表示法的評估來自規劃競賽，其中以 STRIPS 式運算子為基礎的啟發式規劃器表現良好。[^3][^4]

## 限制

- **表達力。**基本形式無法表達條件效果、量化目標或數值量。ADL 等較豐富的語言加入了條件效果與量詞，PDDL2.1 則加入了數值與時間特性。[^2]
- **框架假設。**未提及的事實維持不變，這條規則在行動有附帶影響時必須小心處理，而基本形式無法描述這些影響。
- **搜尋成本。**沒有良好的啟發式時，狀態數會隨計畫長度呈指數成長，因此單靠表示法並不能使規劃變快。

## 未解問題

- 行動模型應如何表示不確定性、間接效果與連續量，同時保留使 STRIPS 好用的簡潔性？
- 運算子描述能否從觀察中學習，使人不必手動撰寫？

## 相關連結

STRIPS 是[基於搜尋的規劃](../../search/index.md)所建立的表示法，而其啟發式使狀態空間規劃器變得快速。規劃概述把它與[階層任務網路](../shop2/index.md)及[以語言模型為基礎的規劃](../saycan/index.md)做比較。若要了解用來探索其狀態空間的一般搜尋方法，請見 [A\*](../../search/a-star/index.md)。

## 應用

- **機器人任務規劃**，這是最初的應用，機器人必須排序移動與推動物件等行動。
- **物流與運輸**，以 PDDL 建模，運算子包括裝載、移動與卸載，並用於規劃競賽中。[^2]

## 參考文獻

### 開創性論文

- Fikes, R. E. & Nilsson, N. J. (1971). Strips: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(71)90010-5 — 提出 STRIPS 表示法，包含前提條件、新增與刪除清單，以及建立在其上的規劃器。
- Bonet, B. & Geffner, H. (2001). Planning as heuristic search. *Artificial Intelligence*. https://doi.org/10.1016/S0004-3702(01)00108-4 — 把 STRIPS 式規劃視為啟發式搜尋，並從問題的鬆弛版本導出啟發式。

### 文章與文件

- Fox, M. & Long, D. (2003). PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1129 — 定義 PDDL2.1，把 STRIPS 式運算子擴充到時間與數值規劃，並給出其語意。
- Hoffmann, J. & Nebel, B. (2001). The FF Planning System: Fast Plan Generation Through Heuristic Search. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.855 — 說明以忽略刪除清單的目標距離估計進行啟發式前向搜尋，這是對 STRIPS 運算子的一種鬆弛。
- Helmert, M. (2006). The Fast Downward Planning System. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1705 — 描述以因果圖啟發式處理 PDDL 任務的規劃器，該系統在 2004 年競賽的古典賽道中獲勝。

[^1]: Fikes and Nilsson (1971)，見上方列表。
[^2]: Fox and Long (2003)，見上方列表。
[^3]: Hoffmann and Nebel (2001)，見上方列表。鬆弛及其作為啟發式的用途，見其摘要。
[^4]: Helmert (2006)，見上方列表。競賽結果依該論文摘要所報告。
