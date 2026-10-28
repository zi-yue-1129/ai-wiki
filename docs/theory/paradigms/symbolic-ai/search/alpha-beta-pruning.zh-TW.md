---
translation_reviewed: 2026-10-28
---

# α–β 剪枝

α–β 剪枝是一種計算雙人遊戲樹極小極大值的方法，它會跳過不影響結果的分支。它回傳的值與極小極大完全相同，但檢查的節點較少。本頁是[搜尋演算法](index.md)的一部分。

## 概述

在雙人零和遊戲中，一方要極大化評估值，另一方則要極小化。極小極大搜尋會評估到固定深度為止的整棵樹，並沿著極大層與極小層回推數值。α–β 在搜尋過程中維持兩個界限：\(\alpha\) 是極大方已能保證的最佳值，\(\beta\) 是極小方已能保證的最佳值。當某分支無法改善這些界限時，就被剪掉。

## 關鍵概念

- **極小極大值**：雙方在搜尋深度內都以最佳方式下棋時，該節點的值。
- **α 界限**：極大方在某節點的價值下界。
- **β 界限**：極小方在某節點的價值上界。
- **截斷**：當 \(\alpha \ge \beta\) 時停止展開該節點，因為其餘子節點不可能改變結果。

## 運作方式

搜尋採深度優先。在極大節點，每個子節點都以目前的 \(\alpha\) 與 \(\beta\) 搜尋，只要某子節點回傳較大的值，就提高 \(\alpha\)。在極小節點則以同樣方式降低 \(\beta\)。當 \(\alpha\ge\beta\) 時，剩餘子節點被剪掉。回傳的值與普通極小極大相同，因為被剪掉的分支不可能改變它。

檢查的葉節點數取決於走法排序。Knuth 與 Moore（1975）指出，在完美排序下，對分支因子 \(b\) 與深度 \(d\)，α–β 檢查的葉節點約為 \(b^{d/2}\) 個，而極小極大則為 \(b^{d}\) 個。這大約讓同樣成本下可搜尋的深度加倍。

## 變體

- **含迭代加深的 α–β** 逐步加深搜尋深度，並重用較淺搜尋得到的走法排序資訊。
- **主要變例搜尋**對第一個子節點使用完整視窗，其餘子節點使用空視窗，在排序良好時可節省工作。
- **靜態搜尋（quiescence search）**在局面不穩定時（例如西洋棋中的吃子）延伸搜尋，以減少地平線效應。

## 結果與限制

- α–β 回傳的是極小極大值，剪枝不改變答案。
- 其效益取決於走法排序。排序不佳時，省下的工作很少。
- 單純的深度限制會造成地平線效應，因此通常會加上靜態搜尋或額外搜尋。
- α–β 需要葉節點上的靜態評估函數，而設計好的評估函數是工程上的主要部分。Campbell 等人（2002）描述 Deep Blue 如何結合 α–β 搜尋、專用硬體與調校過的評估函數。

## 應用

- **西洋棋程式**：以手工設計的評估搭配 α–β，驅動了 Deep Blue（Campbell 等人，2002）。
- **棋盤遊戲**：西洋棋盤、黑白棋等分支因子適中的遊戲。
- **教學與基準**：AI 課程中對抗式搜尋的標準範例。

## 開放問題

- 學得的評估函數可以改進 α–β，但學得的評估誤差可能隨搜尋深度累積。
- 對於分支因子極大的遊戲（例如圍棋），α–β 的效果不如取樣式搜尋（Silver 等人，2016）。

## 參考文獻

### 奠基性論文

- Shannon, C. E. (1950). XXII. Programming a computer for playing chess. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science* 41(314), 256–275. https://doi.org/10.1080/14786445008521796 — 早期提出以靜態評估函數搭配極小極大搜尋來下西洋棋。
- Knuth, D. E. & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence* 6(4), 293–326. https://doi.org/10.1016/0004-3702(75)90019-3 — 分析 α–β，包括葉節點檢查數的最佳情形。

### 綜述與教科書

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 教科書中對極小極大與 α–β 的說明。
- Campbell, M., Hoane, A. J. & Hsu, F.-h. (2002). Deep Blue. *Artificial Intelligence* 134(1–2), 57–83. https://doi.org/10.1016/S0004-3702(01)00129-1 — 描述實際運作的 α–β 搜尋系統。
- Browne, C. B. et al. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games* 4(1), 1–43. https://doi.org/10.1109/TCIAIG.2012.2186810 — 比較 α–β 與取樣式搜尋在遊戲中的表現。
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529(7587), 484–489. https://doi.org/10.1038/nature16961 — 比較圍棋中的樹搜尋與學得的評估。
