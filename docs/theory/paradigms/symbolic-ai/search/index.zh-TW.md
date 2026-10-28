---
translation_reviewed: 2026-10-28
---

# 搜尋演算法

搜尋演算法尋找一串能到達目標的動作或狀態，或是遊戲中的最佳著法。智能體探索狀態空間，並由成本函數引導，有時也依靠啟發式的估計。本頁是[符號 AI、搜尋與規劃](../index.md)的一部分。

## 概述

許多 AI 問題都可以描述為搜尋。路線規劃是圖上的搜尋，西洋棋的局面則是遊戲樹中的一個節點，其分支是合法的著法。主要困難來自組合爆炸：狀態數隨深度呈指數成長，因此演算法必須剪除搜尋空間，或利用知識來引導搜尋。

搜尋方法可分為下表的幾類。凡被列為具名方法者，都另有詳細頁面。

| 類別 | 想法 | 例子 |
|---|---|---|
| 無資訊搜尋 | 不借助額外知識展開狀態 | 廣度優先、深度優先、迭代加深 |
| 啟發式搜尋 | 利用剩餘成本的估計 | 貪婪最佳優先、[A\*](a-star.md)、IDA\* |
| 對抗式搜尋 | 搜尋雙人遊戲樹 | 含 [α–β 剪枝](alpha-beta-pruning.md)的極小極大搜尋 |
| 取樣式搜尋 | 以隨機模擬估計價值 | [蒙地卡羅樹搜尋](monte-carlo-tree-search.md) |

## 關鍵概念

- **狀態空間與後繼函數**：狀態，以及從一個狀態轉到另一個狀態的動作。
- **可容許啟發式**：估計值 \(h(n)\) 永不高估真正的剩餘成本。使用可容許的啟發式時，A\* 會回傳最佳路徑。
- **分支因子與深度**：每個節點的後繼數，以及目標所在的深度。兩者共同決定搜尋樹的大小。
- **剪枝**：捨棄不會改變答案的搜尋樹部分。α–β 剪枝即用於遊戲。

## 運作方式

在啟發式搜尋中，節點保存在前緣集合中，並依某個評估函數的順序展開。貪婪最佳優先使用 \(f(n)=h(n)\)，速度快但不保證最佳。A\* 則使用 \(f(n)=g(n)+h(n)\)，其中 \(g(n)\) 為目前已花費的成本。對抗式搜尋在極大化與極小化兩方之間交替，葉節點的值來自靜態評估函數。蒙地卡羅方法則以隨機模擬的平均結果取代靜態評估。

## 主要方法

- [A\* 搜尋](a-star.md)：以 \(f=g+h\) 排序的最佳優先搜尋。在可容許的啟發式下是最佳的。
- [α–β 剪枝](alpha-beta-pruning.md)：含剪枝的極小極大搜尋。它回傳與極小極大相同的值，但檢查的節點較少。
- [蒙地卡羅樹搜尋](monte-carlo-tree-search.md)：以隨機模擬建立搜尋樹，並以賭博機規則選擇要展開的分支。它是 AlphaGo 等圍棋程式的核心。

## 與其他頁面的連結

- [符號 AI、搜尋與規劃](../index.md)說明搜尋在古典 AI 工具中的位置。
- [自動規劃](../planning/index.md)在規劃問題的狀態上使用啟發式搜尋。
- [強化學習](../../reinforcement-learning/index.md)與搜尋同樣要在探索與利用之間取捨，學得的價值函數也可以取代人工設計的評估函數。

## 應用

- **路線規劃與導航**：A\* 及其變體用於道路網路與格狀地圖。
- **雙人遊戲**：以手工調校評估函數搭配 α–β 搜尋的系統，驅動了西洋棋程式 Deep Blue（Campbell 等人，2002）。
- **圍棋與其他大型遊戲**：結合神經網路的 MCTS 在圍棋上達到專家水準（Silver 等人，2016）。

## 開放問題

- 啟發式搜尋需要好的啟發式函數。從資料學得可容許或接近可容許的啟發式，仍難以保證。
- 搜尋成本隨深度呈指數成長，目前沒有通用的方法能消除這種依賴。
- 把搜尋與學得的模型結合（例如以學得的評估或策略引導搜尋），會引出精確度問題，以及誤差如何隨深度累積的問題。

## 參考文獻

### 奠基性論文

- Hart, P. E., Nilsson, N. J. & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics* 4(2), 100–107. https://doi.org/10.1109/TSSC.1968.300136 — 定義 A\*，並證明可容許啟發式下的最佳性。
- Knuth, D. E. & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence* 6(4), 293–326. https://doi.org/10.1016/0004-3702(75)90019-3 — 分析遊戲樹上 α–β 剪枝的成本。
- Shannon, C. E. (1950). XXII. Programming a computer for playing chess. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science* 41(314), 256–275. https://doi.org/10.1080/14786445008521796 — 早期提出以靜態評估函數搭配極小極大搜尋來下西洋棋。

### 綜述與教科書

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 涵蓋無資訊、啟發式與對抗式搜尋的標準教科書。
- Browne, C. B. et al. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games* 4(1), 1–43. https://doi.org/10.1109/TCIAIG.2012.2186810 — MCTS 變體與應用的綜述。
- Campbell, M., Hoane, A. J. & Hsu, F.-h. (2002). Deep Blue. *Artificial Intelligence* 134(1–2), 57–83. https://doi.org/10.1016/S0004-3702(01)00129-1 — 描述西洋棋系統 Deep Blue 的搜尋與評估設計。
