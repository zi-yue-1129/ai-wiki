---
translation_reviewed: 2026-10-28
---

# STRIPS

STRIPS 是古典規劃的一種表示法，每個動作有前置條件列表、新增列表與刪除列表。狀態是事實的集合，動作在其前置條件都位於狀態中時才能套用。本頁是[自動規劃](index.md)的一部分。

## 概述

在 STRIPS 之前，規劃系統多依賴邏輯上的定理證明，既慢又難以控制。Fikes 與 Nilsson（1971）以受限的形式表示動作，使規劃成為對事實集合的搜尋。這種表示法夠小而有效率，也夠清楚而能被重複使用，之後成為包括 PDDL 在內的多種建模語言的基礎。

## 關鍵概念

- **前置條件**：動作套用前必須成立的事實。
- **新增列表**：動作之後會成立的事實。
- **刪除列表**：動作之後會不成立的事實。未被提及的事實假設不變，這就是封閉世界與框架假設。
- **動作模式**：帶有變數的動作，由問題中的物件實例化。

## 運作方式

設 \(s\) 為狀態（事實的集合），動作 \(a\) 有前置條件 \(\mathrm{pre}(a)\)、新增列表 \(\mathrm{add}(a)\) 與刪除列表 \(\mathrm{del}(a)\)。當 \(\mathrm{pre}(a)\subseteq s\) 時，動作在 \(s\) 中可以套用。其後繼狀態為

\[
\gamma(s,a) = \left(s\setminus \mathrm{del}(a)\right)\cup \mathrm{add}(a).
\]

計畫是一串可套用的動作，能從初始狀態導向包含目標事實的狀態。前向規劃器從初始狀態套用此規則，後向規劃器則透過動作對目標進行回推。兩者通常都由啟發式引導。

## 變體

- **命題式 STRIPS** 只使用基底事實，是最簡單的形式。
- **ADL**（動作描述語言）允許條件效果與量化的前置條件，表達力比 STRIPS 強。
- **PDDL** 在 STRIPS 的想法上擴充了有型別的物件、數值流（fluent）與持續性動作，並用於規劃競賽。

## 結果與限制

- 此表示法易於閱讀與實作，並支援由問題的鬆弛版本導出的通用啟發式（Bonet 與 Geffner，2001）。
- 封閉世界假設意味著狀態中沒有的事實都為假，這適用於某些領域，但不適用於知識不完整的領域。
- 基本 STRIPS 不包含否定的前置條件與條件效果，因此某些領域需要擴充。
- 一般而言計畫的存在性本身就很難判定，搜尋成本取決於所用的啟發式。

## 應用

- **機器人任務規劃**：STRIPS 為 Shakey 機器人而發展，用來規劃它在房間之間移動與推動物體的動作順序。
- **規劃基準**：多數規劃競賽使用 PDDL，它源自 STRIPS；Fast Downward 等規劃器以啟發式搜尋解這些基準（Helmert，2006）。
- **教學**：AI 課程中規劃的標準入門表示法。

## 開放問題

- 把 STRIPS 擴展到不確定性、數值與時間，只在某些情況下能保持可處理性。
- 從觀察中自動學得動作模型，使表示法不必手工撰寫，目前仍難以可靠地做到。

## 參考文獻

### 奠基性論文

- Fikes, R. E. & Nilsson, N. J. (1971). STRIPS: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence* 2(3–4), 189–208. https://doi.org/10.1016/0004-3702(71)90010-5 — 提出 STRIPS 表示法及其規劃器。
- Bonet, B. & Geffner, H. (2001). Planning as heuristic search. *Artificial Intelligence* 129(1–2), 5–33. https://doi.org/10.1016/S0004-3702(01)00108-4 — 說明如何由鬆弛問題計算 STRIPS 式問題的啟發式。
- Blum, A. L. & Furst, M. L. (1997). Fast planning through planning graph analysis. *Artificial Intelligence* 90(1–2), 281–300. https://doi.org/10.1016/S0004-3702(96)00047-1 — 以規劃圖為 STRIPS 式問題規劃，作為前向搜尋的替代方案。

### 綜述與教科書

- Helmert, M. (2006). The Fast Downward planning system. *Journal of Artificial Intelligence Research* 26, 191–246. https://doi.org/10.1613/jair.1705 — 處理 STRIPS 式與 PDDL 問題的規劃器，建立於啟發式搜尋之上。
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 教科書對 STRIPS 動作與規劃問題的說明。
- Kaelbling, L. P., Littman, M. L. & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence* 101(1–2), 99–134. https://doi.org/10.1016/S0004-3702(98)00023-X — 說明 STRIPS 式動作在部分可觀測下規劃時會有哪些改變。
