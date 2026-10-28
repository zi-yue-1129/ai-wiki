---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - reinforcement learning
  - search
  - self-play
aliases:
  - Monte Carlo tree search
  - MCTS
  - 蒙地卡羅樹搜尋
---

# 蒙地卡羅樹搜尋與自我對弈

蒙地卡羅樹搜尋（Monte Carlo tree search，MCTS）是一種規劃方法，它反覆模擬可能的未來並從結果中學習，逐步建立搜尋樹。結合自我對弈（程式與自己的舊版本對弈來訓練）之後，它成為二〇一〇年代後期最強棋類程式的搜尋引擎。

## 概述

選擇一步棋，就是判斷它之後會發生什麼。在圍棋這類遊戲中，可能的局面數量遠超過窮舉搜尋的能力。MCTS 把計算集中在最有希望的路線上，並以模擬對局估計每條路線的好壞，而不是逐一分析每個分支。自我對弈則產生訓練資料，改善搜尋內部使用的評估器。

## 關鍵概念

- **樹策略（tree policy）**：在樹中的節點上，選擇要走哪個子節點的規則。
- **擴展（expansion）**：當搜尋到尚未存入樹中的局面時，把它加入樹。
- **評估（evaluation）**：估計新局面的價值，方法可以是把遊戲隨機走到結束的隨機模擬，也可以是學習得到的價值函數。
- **回傳（backup）**：把結果沿路徑往上傳回，讓路徑上的每個節點更新其平均價值與造訪次數。
- **自我對弈（self-play）**：讓程式與自己對弈以產生訓練對局，通常是與最近的自己對弈。

## 運作方式

搜尋的每一輪包含四個步驟：用樹策略從根節點選出一條路徑、擴展一個新節點、評估它，然後把結果回傳。經過許多輪之後，會走造訪次數最多的那一步。常用的樹策略是 UCT，它在每個節點上套用 UCB1 多臂老虎機規則。UCB1 在子節點的樣本平均值上加一個信心項，該項隨造訪次數增加而變小：

\[
a_t = \arg\max_a \left( \bar{X}_a + \sqrt{\frac{2 \ln N}{n_a}} \right)
\]

其中 \(\bar{X}_a\) 是經由子節點 \(a\) 的模擬平均結果，\(n_a\) 是它被造訪的次數，\(N\) 是父節點的造訪次數。Auer、Cesa-Bianchi 與 Fischer（2002）證明 UCB1 的遺憾值只隨遊戲次數以對數速度增長。Kocsis 與 Szepesvári（2006）把同一規則用於蒙地卡羅規劃，形成 UCT 演算法。

## 關鍵方法

下列各個里程碑系統的差異，在於它們的評估從何而來，以及搜尋從中學到什麼。每個系統的細節都在其獨立頁面中，只有兩個古典方法在此說明。

- **以隨機模擬評估的基本 MCTS（Coulom，2006）**：搜尋以隨機模擬評估新局面，效果取決於選擇與回傳的運算子。論文分析了用於圍棋程式的這些運算子。
- **UCT（Kocsis 與 Szepesvári，2006）**：在每個節點套用 UCB1，讓搜尋在持續探索有希望路線的同時，也嘗試其他選項。
- [AlphaGo](../alphago/index.md)（Silver 等人，2016）：以策略網路引導樹的擴展，以價值網路判斷局面，兩者都以人類棋譜起步。
- [AlphaZero](../alphazero/index.md)（Silver 等人，2018）：以單一網路引導同樣的搜尋，該網路只靠自我對弈訓練。
- [MuZero](../model-based-rl/muzero/index.md)（Schrittwieser 等人，2020）：在遊戲的學習模型上執行搜尋，而不是使用真實規則。

## 自我對弈

在自我對弈中，搜尋本身會產生訓練目標。每次搜尋的造訪次數成為走子策略的目標，最後的對局結果則成為價值的目標。由於對手是學習者自己較近期的版本，隨著學習者進步，對局的難度也會提高。把每個新版本與較早的版本對戰，可以追蹤進展，而且這個循環不需要任何人類棋譜。

## 相關連結

- [增強學習](../index.md)：從獎勵中學習的較大方法家族。樹搜尋是在決策時運用學習得到之價值或策略的一種方式。
- [模型式增強學習](../model-based-rl/index.md)：以學習得到的模型進行規劃，MuZero 把它延伸到規則不交給程式的遊戲。
- [遊戲](../../../../applications/games/index.md)：遊戲程式的歷史，這些方法是其核心。

## 應用

- **棋類遊戲**：圍棋、西洋棋與將棋程式，從 AlphaGo 到 AlphaZero。
- **以學習模型進行規劃**：MuZero 在學習得到的模型上執行同樣的搜尋，也包括 Atari 遊戲。
- **語言模型的推理**：Tree of Thoughts（Yao 等人，2023）把中間推理步驟視為一棵樹並在其中搜尋。論文摘要指出，在其 Game of 24 任務中，成功率為 74%，而 GPT-4 搭配思維鏈提示的成功率為 4%。

## 限制

- 搜尋每一步都需要大量模擬，因此強度取決於落子時可用的時間與運算資源。
- 搜尋的效果不會超過評估器。錯誤的價值估計會誤導搜尋，而自我對弈接著會把錯誤當作訓練資料。
- 若學習者長期面對相似的對手，自我對弈可能收斂到狹窄的風格。
- 在語言模型的推理中，各個思維由模型本身判斷，因此評估可能在搜尋無法察覺的地方出錯。

## 開放問題

- 當策略與價值已經很強時，落子時還值得投入多少搜尋，以及搜尋與學習之間的平衡點在哪裡。
- 對於沒有明確檢查器（例如謎題）的任務，在推理步驟上進行樹搜尋能否對語言模型穩定帶來改進。
- 如何把自我對弈延伸到具隱藏資訊的遊戲，因為在那裡無法直接複製並搜尋模擬器。

## 參考文獻

### 開創性論文

- Coulom, R. (2006). Efficient selectivity and backup operators in Monte-Carlo tree search. *Computers and Games (CG 2006)*, LNCS 4630, Springer. https://link.springer.com/doi/10.1007/978-3-540-75538-8_7 — 分析用於圍棋程式之蒙地卡羅樹搜尋的選擇與回傳運算子。
- Kocsis, L. & Szepesvári, C. (2006). Bandit based Monte-Carlo planning. *Machine Learning: ECML 2006*, LNCS 4212, Springer. https://link.springer.com/chapter/10.1007/11871842_29 — 提出 UCT，在搜尋樹的每個節點上套用 UCB1 多臂老虎機規則。
- Auer, P., Cesa-Bianchi, N. & Fischer, P. (2002). Finite-time analysis of the multiarmed bandit problem. *Machine Learning* 47(2–3), 235–256. https://homes.di.unimi.it/~cesabian/Pubblicazioni/ml-02.pdf — UCB1 規則及其對數遺憾界，取自作者本人的版本。
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529, 484–503. https://doi.org/10.1038/nature16961 — AlphaGo，結合策略網路、價值網路與樹搜尋。
- Schrittwieser, J. et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model. *Nature*. https://doi.org/10.1038/s41586-020-03051-4 — MuZero，在學習得到的模型上執行搜尋。
- Yao, S. et al. (2023). Tree of Thoughts: Deliberate problem solving with large language models. arXiv. https://arxiv.org/abs/2305.10601 — 在語言模型的中間推理步驟上套用樹搜尋。

### 綜述與教科書

- Browne, C. et al. (2012). A Survey of Monte Carlo Tree Search Methods. *IEEE Transactions on Computational Intelligence and AI in Games*. https://doi.org/10.1109/TCIAIG.2012.2186810 — 蒙地卡羅樹搜尋各種變體及其在遊戲與規劃中之應用的綜述。
