---
translation_reviewed: 2026-10-28
---

# 蒙地卡羅樹搜尋與自我對弈

蒙地卡羅樹搜尋（Monte Carlo tree search，MCTS）是一種規劃方法，透過反覆模擬可能的未來逐步長出搜尋樹，並把計算重心放在看起來最有希望的走法上。自我對弈（self-play）則是讓代理人與自己對弈來訓練，使對手隨著代理人一起變強，訓練資料因此源源不絕。兩者結合於 AlphaZero 等系統，產生了當時最強的遊戲程式之一，如今也開始被用於語言模型的推理。

## 概述

本頁涵蓋兩個核心想法。第一是**搜尋**：當問題的規則已知時，代理人可以先在腦中模擬走法，再決定實際要走哪一步。圍棋的每個局面都有遠多於電腦能窮舉的後續變化，因此完整前瞻不可能實現；MCTS 改為取樣，把模擬集中在最重要的地方。第二是**從自己產生的經驗中學習**：程式和自己下棋，就能產生自己的訓練棋譜，資料品質隨實力提升，也不需要人類棋譜。

早期的遊戲程式各只用到其中一個想法。1990 年代的西洋棋引擎主要依靠搜尋，加上人工撰寫的評估函數；TD-Gammon 則以自我對弈學習西洋雙陸棋，但幾乎沒有深度前瞻。這個領域真正的突破，是把兩者連成一個循環：搜尋借助學習得到的網路決定往哪裡看，而搜尋的結果又成為訓練網路的目標。兩部分彼此增強。[應用](../../../../applications/games/index.md)中的遊戲頁面追溯了這些程式的歷史，本頁則說明方法本身。

## 關鍵概念

- **博弈樹**：節點是局面，邊是走法。搜尋的目標是找出從目前局面（根節點）出發的最佳走法。
- **模擬（推演，rollout）**：從某個局面一路玩到終局的一局遊戲，最初以快速的隨機或簡單啟發式策略進行。
- **價值**：對某個局面最終結果的期望估計。學習得到的價值函數可以取代推演，也可以與推演並用。
- **先驗策略**：對各走法的學習機率分布，指出哪些走法值得先檢查。
- **探索獎勵**：偏袒嘗試次數較少之走法的一項。在 UCT 中，它來自處理賭博機問題的 UCB1 規則，詳見 [MCTS 方法頁](monte-carlo-tree-search/index.md)。
- **自我對弈**：代理人與自己的複本或過去的版本對弈，每一局都成為訓練資料。
- **課程（curriculum）**：把訓練任務由易到難排序。自我對弈會自動產生這樣的課程，因為雙方的對手會隨訓練而變強。
- **搜尋即策略改進**：搜尋後的造訪次數，比網路的原始輸出更銳利，可作為更好的訓練目標，因為搜尋已經檢驗過每個選項的後果。

## 運作方式

每一次 MCTS 模擬都重複四個步驟：

1. **選擇**。從根節點出發，挑選一個子走法，在它迄今的平均結果與嘗試次數不足之間取得平衡。
2. **擴展**。當走訪抵達尚未在樹中的局面時，把它加入樹中。
3. **評估**。估計新局面的結果，可以用一局推演到終局，也可以用學習得到的價值函數。
4. **回傳**。把結果沿路徑往上傳，更新路徑上每個走法的平均值。

完成大量模擬後，在根節點造訪次數最多的走法被實際走出。在 UCT 中，選擇規則為

$$
a^\ast = \arg\max_a \left( \bar{Q}(s,a) + c \sqrt{\frac{\ln N(s)}{N(s,a)}} \right),
$$

其中 $\bar{Q}$ 是走法 $a$ 的平均結果，$N(s)$ 與 $N(s,a)$ 是造訪次數，$c$ 決定探索的強度。

自我對弈接著形成一個循環：

```mermaid
flowchart LR
  N[網路：先驗與價值] --> S[從目前局面進行 MCTS]
  S --> M[走出造訪次數最多的走法]
  M --> G[完成的一局]
  G --> D[訓練資料：造訪次數與結果]
  D --> T[更新網路]
  T --> N
```

網路提出走法與價值估計，搜尋加以檢驗，訓練步驟則讓下一輪的提議更準確。

## 關鍵方法

本頁涵蓋四個里程碑式的方法，各有專頁。它們的差異主要在於學習什麼，以及搜尋可以知道遊戲規則到什麼程度。

| 方法 | 年份 | 搜尋 | 學習的內容 | 是否需要規則 |
|---|---|---|---|---|
| [附 UCT 的 MCTS](monte-carlo-tree-search/index.md) | 2006 | 隨機推演 | 無；僅有搜尋 | 需要，作為模擬器 |
| [AlphaGo](alphago/index.md) | 2016 | 由網路引導的 MCTS | 策略網路與價值網路，先用人類棋譜，再用自我對弈 | 需要 |
| [AlphaZero](alphazero/index.md) | 2017 | 由單一網路引導的 MCTS | 策略與價值，僅來自自我對弈 | 需要 |
| [MuZero](muzero/index.md) | 2019 | 在學得模型中進行的 MCTS | 表徵、動態、策略與價值 | 不需要；學習動態 |

## 關聯

這個方法屬於更廣的[模型式強化學習](../model-based-rl/index.md)家族：MuZero 是在學得模型中規劃的最清楚例子。引導搜尋的學得價值，正是[價值基礎方法](../value-based-methods/index.md)所研究的量；負責提議走法的策略網路，則是[策略梯度與 Actor-Critic](../policy-gradient-and-actor-critic/index.md)意義下的 actor。

大腦的關聯有啟發性，但尚未獲得證實。多巴胺訊號反映的是價值函數所學習的獎勵預測誤差，參見[決策、多巴胺與獎勵](../../../../brain-mind/decision-reward/index.md)。人類選擇的研究區分了習慣（類似快取的價值）與目標導向的選擇（類似用模型規劃），參見[模型基礎與無模型控制](../../../../brain-mind/decision-reward/model-based-vs-model-free/index.md)。Pfeiffer 與 Foster（2013）在大鼠身上記錄到海馬迴位置細胞的序列，這些序列會沿著通往目標的未來路徑向前延伸。這與基於模擬的前瞻相似，但並不表示大腦執行的是 UCT 或任何特定的樹搜尋。

## 應用

- **棋類遊戲**。AlphaZero 僅憑規則就學會西洋棋、將棋與圍棋。同一系列的後續程式成為這些遊戲的參考棋手。
- **單一代理人的規劃**。MuZero 把同樣的搜尋用於 Atari 遊戲，搜尋過程中不給定規則。
- **語言模型的推理**。Hao 等人（2023）把語言模型同時當作推理代理人與世界模型，並以 MCTS 在候選推理步驟上進行規劃。Feng 等人（2023）使用類似 AlphaZero 的樹搜尋，搭配學得的價值函數來引導解碼並在訓練時改進模型。Zhang 等人（2024）則用樹搜尋收集品質更高的推理軌跡，並為每一步產生價值標籤，用於自我訓練。
- **測試時運算**。Snell 等人（2024）研究在推論時花費更多運算（包括對過程式驗證器進行搜尋），與單純使用更大模型相比，表現會如何改變。[測試時擴展](../../../models/reasoning/test-time-scaling.md)頁面對此有更詳細的說明。

## 開放問題

- **沒有模擬器的領域**。MCTS 需要一種模擬結果的方式。MuZero 顯示學得的模型也可以勝任，但長時間搜尋中模型誤差會累積，而且這種做法能推廣到多雜亂的真實任務，目前並不清楚。
- **自我對弈課程**。自我對弈可以產生有用的課程，但也可能收斂到狹隘的策略，或在幾種策略之間循環。Sukhbaatar 等人（2017）顯示，不對稱的自我對弈可以在沒有外部獎勵的情況下驅動探索，但自我對弈何時能為一般任務提供正確的課程，仍是開放問題。
- **語言推理**。西洋棋有明確的勝負，推理鏈卻沒有同樣清楚的獎勵。以語言模型進行樹搜尋，取決於驗證器或價值估計的品質，而且每一步搜尋的成本很高。
- **運算取捨**。在固定的運算預算下，搜尋是否勝過更大的單次推論，取決於問題與模型，目前尚無定論。

## 參考文獻

### 開創性論文

- Kocsis, L. & Szepesvári, C. (2006). *Bandit Based Monte-Carlo Planning*. Lecture Notes in Computer Science. https://doi.org/10.1007/11871842_29 — 把 UCB1 賭博機規則應用於蒙地卡羅規劃中樹的走法選擇，即 UCT 演算法。
- Coulom, R. (2007). *Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-540-75538-8_7 — 研究蒙地卡羅樹如何選擇要擴展的走法，以及結果如何回傳，以圍棋為測試領域。
- Tesauro, G. (1995). *Temporal difference learning and TD-Gammon*. Communications of the ACM. https://doi.org/10.1145/203330.203343 — 介紹 TD-Gammon，一個透過自我對弈學習神經網路評估函數的西洋雙陸棋程式。
- Silver, D. 等人 (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — AlphaGo，結合策略與價值網路和蒙地卡羅樹搜尋。
- Silver, D. 等人 (2017). *Mastering the game of Go without human knowledge*. Nature. https://doi.org/10.1038/nature24270 — AlphaGo Zero，從隨機對弈開始、不使用人類棋譜、以自我對弈學習圍棋。
- Silver, D. 等人 (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — AlphaZero，單一套自我對弈演算法僅憑規則即可學會三種棋類。
- Schrittwieser, J. 等人 (2020). *Mastering Atari, Go, chess and shogi by planning with a learned model*. Nature. https://doi.org/10.1038/s41586-020-03051-4 — MuZero，在自己學得的模型中以搜尋進行規劃，不需要給定規則。
- Anthony, T., Tian, Z. & Barber, D. (2017). *Thinking Fast and Slow with Deep Learning and Tree Search*. arXiv:1705.08439. https://arxiv.org/abs/1705.08439 — 專家迭代（expert iteration）：樹搜尋改進神經策略，改進後的策略再引導之後的搜尋。
- Sukhbaatar, S. 等人 (2017). *Intrinsic Motivation and Automatic Curricula via Asymmetric Self-Play*. arXiv:1703.05407. https://arxiv.org/abs/1703.05407 — 兩個代理人互相提出並完成任務，在沒有外部獎勵的情況下自動產生課程。
- Pfeiffer, B. E. & Foster, D. J. (2013). *Hippocampal place-cell sequences depict future paths to remembered goals*. Nature. https://doi.org/10.1038/nature12112 — 記錄大鼠海馬迴位置細胞序列，這些序列會沿著通往目標的路徑向前延伸，是前瞻的一種神經對應。

### 綜述與教科書

- Browne, C. B. 等人 (2012). *A Survey of Monte Carlo Tree Search Methods*. IEEE Transactions on Computational Intelligence and AI in Games. https://doi.org/10.1109/TCIAIG.2012.2186810 — 廣泛綜述 MCTS 的各種變體、增強技術，以及遊戲以外的應用。

### 文章與文件

- Hao, S. 等人 (2023). *Reasoning with Language Model is Planning with World Model*. arXiv:2305.14992. https://arxiv.org/abs/2305.14992 — 把語言模型當作世界模型，並以蒙地卡羅樹搜尋規劃推理步驟。
- Feng, X. 等人 (2023). *Alphazero-like Tree-Search can Guide Large Language Model Decoding and Training*. arXiv:2309.17179. https://arxiv.org/abs/2309.17179 — 以學得的價值函數，將類似 AlphaZero 的樹搜尋應用於語言模型的解碼與訓練。
- Snell, C. 等人 (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv:2408.03314. https://arxiv.org/abs/2408.03314 — 研究增加推論運算（包括對驗證器進行搜尋）對表現的影響。
- Zhang, D. 等人 (2024). *ReST-MCTS\*: LLM Self-Training via Process Reward Guided Tree Search*. arXiv:2406.03816. https://arxiv.org/abs/2406.03816 — 以樹搜尋收集推理軌跡與逐步價值，用於語言模型的自我訓練。
