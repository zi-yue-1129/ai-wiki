---
translation_reviewed: 2026-10-28
---

# 極小化極大與 α-β 剪枝

極小化極大是雙人零和博弈中選擇走法的基本規則：假設每位玩家都會選擇對自己最有利的選項。α-β 剪枝能算出完全相同的答案，同時跳過不會影響答案的博弈樹部分。兩者合起來是對抗搜尋的經典方法，並在上層的[搜尋演算法概述](../index.md)中介紹。

## 概述

以西洋棋為例，搜尋者向前看幾步，且必須假設對手會以最強的反制著法回應。局面的價值在兩種選擇之間交替：搜尋者在自己的走法中取最大值，對手則在各種回應中取最小值。搜尋通常會限制在固定深度，之後以啟發式評估為局面評分。

Claude Shannon 在 1950 年為電腦西洋棋提出這種方法。之後 Knuth 與 Moore 分析了 α-β 剪枝能節省多少工作。[^1]

## 核心概念

- **博弈樹**：以局面為節點、以合法走法為邊。MAX 節點與 MIN 節點分別是搜尋者或對手要走子的局面。
- **評估函數**：在深度限制處為局面評分的啟發式。
- **α**：搜尋者在目前路徑上已能保證的最佳值。
- **β**：對手在目前路徑上已能保證的最佳值。
- **走法排序**：檢視走法的順序。它決定剪枝能去掉多少分支。

## 運作方式

單純的極小化極大以遞迴計算節點的值：

$$
V(n) =
\begin{cases}
\text{eval}(n) & \text{若 } n \text{ 是葉節點或位於深度限制}\\
\max_{c \in \text{children}(n)} V(c) & \text{若 } n \text{ 是 MAX 節點}\\
\min_{c \in \text{children}(n)} V(c) & \text{若 } n \text{ 是 MIN 節點。}
\end{cases}
$$

α-β 會把兩個界限沿樹向下傳遞，並在兩者交錯時提早停止。

1. 以 $\alpha=-\infty$ 與 $\beta=+\infty$ 對根節點呼叫此程序。
2. 若是葉節點或達到深度限制，回傳評估值。
3. 在 MAX 節點，令 $v=-\infty$。對每個子節點，令 $v=\max(v, \text{子節點結果})$ 且 $\alpha=\max(\alpha, v)$。若 $\alpha \ge \beta$，停止檢視子節點。這稱為 β 截斷。
4. 在 MIN 節點，令 $v=+\infty$。對每個子節點，令 $v=\min(v, \text{子節點結果})$ 且 $\beta=\min(\beta, v)$。若 $\alpha \ge \beta$，停止。這稱為 α 截斷。
5. 回傳 $v$。

這種截斷是安全的：一旦 $\alpha \ge \beta$，在父節點要走子的一方已在別處有同樣好或更好的選項，因此其餘子節點不可能改變根節點的值。

節省多少工作非常依賴走法排序。Knuth 與 Moore 指出，若每次都先檢視最佳走法，對一棵分支因子為 $b$、深度為 $d$ 的均勻樹，只需檢視約 $b^{\lceil d/2\rceil}+b^{\lfloor d/2\rfloor}-1$ 個葉節點，大致是單純極小化極大所檢視數量的平方根。[^2]實際程式無法做到完美排序，但簡單的排序啟發式就能回收大部分的效益。

## 結果

Shannon 1950 年的論文是提案與設計分析，而非實驗。Knuth 與 Moore 1975 年的結果屬於分析性質：它在理想排序下為所檢視的葉節點數給出界限。如常見的情況，剪枝並不改變所得的值。這個方法的主要實證證據來自西洋棋程式。Deep Blue 結合 α-β 搜尋、專用硬體與大量人工設計的評估特徵，並在 1997 年的一場比賽中擊敗了在位的世界冠軍。[^3]

後來的 AlphaZero 採取不同的路線：以學習得來的網路取代人工評估，並以蒙地卡羅樹搜尋取代 α-β。其摘要報告，從隨機下棋開始，它在 24 小時內就在西洋棋、將棋與圍棋中達到超越人類的水準。[^4]

## 限制

- **深度限制。**固定深度的搜尋可能漏看地平線外剛好出現的威脅。這就是地平線效應，即使評估很好，也可能使程式表現不佳。
- **評估品質。**結果只取決於深度限制處的評估。人工撰寫好的評估函數十分費力。
- **適用範圍。**這個方法假設資訊完全公開、雙人對弈且結果為零和。含機率的博弈（如西洋雙陸棋）或含隱藏資訊的博弈（如撲克），需要擴充（如期望極小化極大）或其他方法。

## 開放問題

- 如何最有效地結合學習得來的評估與搜尋？AlphaZero 顯示，在某些遊戲中學習得來的搜尋可以勝過人工設計的 α-β，但其在成本與通用性上的取捨仍有爭議。
- 走法排序能否學得足夠好，以接近理想情形？

## 關聯

α-β 是[遊戲](../../../../applications/games/index.md)頁面中經典博弈系統的搜尋部分。其學習型的對應方法，即蒙地卡羅樹搜尋，見[強化學習](../../../paradigms/reinforcement-learning/index.md)，整體的搜尋家族則見[上層概述](../index.md)。關於腦如何規劃未來的可能性，見[決策與獎勵](../../../../brain-mind/decision-reward/index.md)。

## 應用

- **西洋棋。**Deep Blue 及其後的程式，都以人工評估搭配 α-β 搜尋。[^3]
- **學習型方法的基準。**確定性雙人博弈的 α-β 式搜尋，是衡量學習型搜尋（如上文的 AlphaZero 工作）的參照。

[^1]: Knuth and Moore (1975)，見上方參考文獻。
[^2]: Knuth and Moore (1975)，見上方參考文獻。葉節點數是他們在理想排序下，對均勻樹所得的結果。
[^3]: Campbell, Hoane and Hsu (2002)，見上方參考文獻。
[^4]: Silver et al. (2017)，見上方參考文獻。24 小時的數字取自摘要。

## 參考文獻

### 開創性論文

- Knuth, D. E. & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(75)90019-3 — 分析 α-β 剪枝的節省量，以及在完美走法排序下的最佳情形。
- Shannon, C. E. (1950). XXII. Programming a computer for playing chess. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science*. https://doi.org/10.1080/14786445008521796 — 電腦西洋棋的早期提案，以有深度限制的搜尋搭配局面的啟發式評估。
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*. https://doi.org/10.1038/nature16961 — 結合深度神經網路與蒙地卡羅樹搜尋，即 AlphaGo 背後的系統。
- Silver, D. et al. (2017). Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm. arXiv. https://arxiv.org/abs/1712.01815 — 以單一的學習演算法取代人工評估，透過自我對弈在西洋棋、將棋與圍棋中下棋。

### 文章與文件

- Campbell, M., Hoane, A. J. & Hsu, F. (2002). Deep Blue. *Artificial Intelligence*. https://doi.org/10.1016/S0004-3702(01)00129-1 — 描述擊敗世界西洋棋冠軍之系統的設計，結合 α-β 搜尋、硬體與評估。
