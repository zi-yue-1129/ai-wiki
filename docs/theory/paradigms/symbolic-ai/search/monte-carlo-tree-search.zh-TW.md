---
translation_reviewed: 2026-10-28
---

# 蒙地卡羅樹搜尋

蒙地卡羅樹搜尋（MCTS）透過重複四個步驟來建立搜尋樹：選擇、擴展、模擬與回傳。它以隨機模擬的結果估計著法價值，並由賭博機規則決定下一步要搜尋哪裡。本頁是[搜尋演算法](index.md)的一部分。

## 概述

α–β 需要好的靜態評估函數，而對圍棋等遊戲來說，這很難手工撰寫。MCTS 改由隨機對局的結果來估計價值，避開了這個難題。它在估計看好且不確定的地方擴展搜尋樹，因此搜尋會集中於有用的路線，而不必全寬度展開。

## 關鍵概念

- **模擬（playout，又稱 rollout）**：從某個局面快速進行的模擬，通常以隨機走法下到對局結束。
- **探索與利用**：在估計價值高的著法與造訪次數少的著法之間取捨。
- **UCB1 規則**：選擇子節點以最大化 \(\bar{x}_j+c\sqrt{\ln N/n_j}\)，其中 \(\bar{x}_j\) 是子節點的平均結果，\(n_j\) 是其造訪次數，\(N\) 是父節點的造訪次數。Auer 等人（2002）分析了賭博機問題的這個界限。
- **UCT**：在選擇階段走過的每個節點都套用 UCB1 的樹策略。Kocsis 與 Szepesvári（2006）為 MCTS 提出此方法。

## 運作方式

每次迭代從根節點開始，依序做四件事：

1. **選擇**：以 UCB1 規則選擇子節點往下走，直到遇到還有未探索著法的節點。
2. **擴展**：為一個未探索的著法加入一個子節點。
3. **模擬**：從新節點開始，通常以隨機著法模擬到終局，得到結果。
4. **回傳**：更新路徑上每個節點的造訪次數與平均結果。

完成預定次數的迭代後，選擇造訪次數最多（或平均結果最高）的著法。Coulom（2007）為此方法命名，並研究了圍棋中的回傳運算子。

## 變體

- **UCT** 是標準的選擇規則，大多數 MCTS 實作都採用。
- **RAVE** 在樹上不同位置出現的相同著法之間共享統計量，能在圍棋中加速學習。
- **學得的策略與價值**：AlphaGo 以神經網路引導選擇，並以價值估計取代隨機模擬（Silver 等人，2016）。

## 結果與限制

- MCTS 不需要人工撰寫的評估函數，且隨著迭代次數增加而穩定改進。
- 在單一著法就能決定勝負的遊戲中，隨機模擬可能誤導判斷，因此模擬策略很重要。
- 要得到準確估計需要許多次迭代，在時間有限的情況下成本很高。
- Browne 等人（2012）綜述了各種變體及其在不同遊戲中的表現。

## 應用

- **圍棋**：結合神經網路的 MCTS 在圍棋中達到強勁水準（Silver 等人，2016）。
- **一般遊戲對弈**：MCTS 能處理許多只需少量遊戲專屬知識的遊戲。
- **規劃**：針對分支因子很大的決策問題，採用取樣式搜尋。

## 開放問題

- 為新遊戲選擇探索常數與模擬策略，目前仍依賴調校。
- 把 MCTS 與學得的模型結合，並理解學得的價值何時有幫助、何時有害，是活躍的研究方向。
- 把 MCTS 延伸到不完全資訊與連續動作空間，比完全資訊的情形困難得多。

## 參考文獻

### 奠基性論文

- Kocsis, L. & Szepesvári, C. (2006). Bandit based Monte-Carlo planning. In *Machine Learning: ECML 2006*, Lecture Notes in Computer Science, 282–293. https://doi.org/10.1007/11871842_29 — 提出 UCT，使 MCTS 的值收斂到極小極大值。
- Coulom, R. (2007). Efficient selectivity and backup operators in Monte-Carlo tree search. In *Computers and Games*, Lecture Notes in Computer Science, 72–83. https://doi.org/10.1007/978-3-540-75538-8_7 — 為此方法命名，並研究圍棋中的回傳運算子。
- Auer, P., Cesa-Bianchi, N. & Fischer, P. (2002). Finite-time analysis of the multiarmed bandit problem. *Machine Learning* 47(2–3), 235–256. https://doi.org/10.1023/A:1013689704352 — 給出選擇規則所依據的 UCB1 界限。

### 綜述與教科書

- Browne, C. B. et al. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games* 4(1), 1–43. https://doi.org/10.1109/TCIAIG.2012.2186810 — MCTS 變體與應用的綜述。
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529(7587), 484–489. https://doi.org/10.1038/nature16961 — 把 MCTS 與深度網路結合，在圍棋中達到專家水準。
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 對抗式與取樣式搜尋的教科書背景。
