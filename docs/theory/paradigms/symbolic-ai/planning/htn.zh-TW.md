---
translation_reviewed: 2026-11-04
---

# 階層任務網路規劃

階層任務網路（HTN）規劃透過領域專屬的方法，反覆把高層任務分解為子任務，直到只剩下基本動作，從而找出計畫。本頁是[自動規劃](index.md)的一部分。

## 概述

像 [STRIPS](strips.md) 中的古典規劃器，只用基本動作在狀態上搜尋。HTN 規劃器則加入如何完成任務的知識。領域專家撰寫方法，也就是完成任務的食譜，規劃器再把它們展開。由於這些食譜使搜尋範圍大幅縮小，這種做法在實用系統中很常見。Georgievski 與 Aiello（2015）比較了 HTN 的各種形式化與規劃器。Ghallab 等人（2004）給出標準的表述。

## 關鍵概念

- **基本任務**：可直接執行的動作，其前置條件與效果與 STRIPS 相同。
- **複合任務**：不能直接執行，必須由方法分解的任務。
- **方法**：在特定條件下，把複合任務替換為子任務的規則。
- **任務網路**：一組帶有順序限制的任務，每個計畫都必須遵守這些限制。

## 運作方式

規劃器維護一個待處理的任務清單。它取出第一個複合任務，並選擇一個在目前狀態下條件成立的方法。它把該任務替換為方法的子任務，然後繼續。當只剩基本任務時，規劃器沿著順序檢查它們的前置條件。若檢查失敗，就回溯並嘗試另一個方法。

作為示意例子，「把包裹從 A 運到 C」這個任務可以有一個直接開車的方法，其子任務為裝貨、從 A 開到 C、卸貨。第二個方法在直達路線封閉時使用，可把任務拆成從 A 到 B 的運送，與從 B 到 C 的運送。規劃器會選擇適用的方法。

有些 HTN 規劃器以固定順序分解任務，這使得在分解過程中檢查狀態變得容易。SHOP2 是這類有序規劃器之一（Nau 等人，2003）。其他規劃器允許偏序的任務網路，較為彈性，但搜尋較困難。

## 主要方法

- [STRIPS](strips.md)：HTN 規劃器所依賴的基本動作模型。HTN 並不取代它。
- [GraphPlan](graphplan.md)：不做分解的古典規劃，可用來對照方法提供了多少知識。

## 結果與限制

- 方法編碼了領域知識，因此在符合分解方式的問題上，規劃可以很快。代價是這些知識必須撰寫與維護（Nau 等人，2003）。
- 不完整或錯誤的方法可能使規劃器漏掉解。完備性取決於方法函式庫。
- 各種 HTN 形式化在表達力與計算複雜度上有所不同。Georgievski 與 Aiello（2015）比較了這些取捨，而它們取決於所選的形式化。

## 應用

- **物流與運輸**：搬運貨物的標準程序可寫成方法。
- **遊戲 AI 與機器人**：「清空房間」這類任務食譜很自然。
- **商業與工業流程**：規劃依循既有的文件化程序。

## 與其他頁面的連結

- [自動規劃](index.md)提供較廣的脈絡，包括古典與不確定規劃。
- [搜尋演算法](../search/index.md)：HTN 規劃器會搜尋任務分解的各種方式。
- [強化學習](../../reinforcement-learning/index.md)與 HTN 共享把長任務分解為子任務的想法，透過階層式方法實現。

## 開放問題

- 撰寫好的方法很費工。從計畫軌跡中學習方法是活躍但困難的問題。
- 把 HTN 分解與學得的模型、以及在真實環境中的行動結合，仍是研究問題（Ghallab 等人，2016）。

## 參考文獻

### 奠基性論文

- Nau, D. S., Au, T.-C., Ilghami, O., Kuter, U., Murdock, J. W., Wu, D. & Yaman, F. (2003). SHOP2: an HTN planning system. *Journal of Artificial Intelligence Research* 20, 379–404. https://doi.org/10.1613/jair.1141 — 介紹 SHOP2，一種依計畫順序分解任務的有序 HTN 規劃器。
- Ghallab, M., Nau, D. & Traverso, P. (2004). Hierarchical task network planning. In *Automated Planning: Theory and Practice*, 229–261. https://doi.org/10.1016/b978-155860856-6/50017-x — HTN 規劃形式定義的標準章節。

### 綜述與教科書

- Georgievski, I. & Aiello, M. (2015). HTN planning: overview, comparison, and beyond. *Artificial Intelligence* 222, 124–156. https://doi.org/10.1016/j.artint.2015.02.002 — HTN 形式化與規劃器的綜述與比較。
- Ghallab, M., Nau, D. & Traverso, P. (2016). *Automated Planning and Acting*. Cambridge University Press. https://doi.org/10.1017/CBO9781139583923 — 教科書，涵蓋 HTN 規劃與行動執行。
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 關於規劃與任務分解的教科書背景。
