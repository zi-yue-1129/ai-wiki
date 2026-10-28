---
translation_reviewed: 2026-10-28
---

# 蒙地卡羅樹搜尋（UCT，2006）

蒙地卡羅樹搜尋是一種規劃方法，透過反覆模擬建立搜尋樹，並以賭博機規則決定下一步要探索哪個分支。它最著名的形式 UCT 讓 MCTS 在深度學習出現之前，成為圍棋的預設搜尋方法。它是[上層主題](../index.md)中的搜尋核心。

## 概述

面對龐大博弈樹、必須在多個走法之間做選擇的規劃者，面臨的取捨和賭徒在多台吃角子老虎之間選擇一樣：每台機器都可能很好，嘗試它能帶來資訊，但嘗試差的選項則浪費努力。Kocsis 與 Szepesvári（2006）把樹中的每個節點視為多臂賭博機問題，並以 UCB1 規則選擇要造訪的子節點。他們的演算法稱為 UCT，每次模擬讓樹長大一點，並把之後的模擬集中在最有希望的走法上，同時仍偶爾取樣其他走法。

這個方法不需要人工撰寫的評估函數，結果估計來自隨機推演。這也是它在難以撰寫良好靜態評估的遊戲中取得成功的原因。

## 關鍵概念

- **賭博機規則（UCB1）**：選擇「平均獎勵加上不確定性獎勵」最高的選項。嘗試次數越多，獎勵越小。
- **模擬**：沿樹向下走一次，接著進行推演並更新。
- **推演（rollout）**：從新局面玩到終局的一局遊戲，通常使用隨機或稍有引導的策略。
- **回傳（backup）**：更新路徑上每個節點的平均結果與造訪次數。

## 運作方式

演算法執行[上層主題](../index.md)中描述的四個步驟：選擇、擴展、推演與回傳。選擇步驟會挑出使下式最大的節點 $s$ 之子節點 $a$：

$$
\bar{Q}(s,a) + c\sqrt{\frac{\ln N(s)}{N(s,a)}},
$$

其中 $N(s)$ 是父節點的造訪次數，$N(s,a)$ 是子節點的造訪次數，$\bar{Q}(s,a)$ 是從目前行棋方觀點看該子節點的平均結果，$c$ 控制探索強度。

1. 從根節點開始。當目前節點的所有走法都已展開時，移動到 UCB 分數最高的子節點。
2. 在第一個有未探索走法的節點，為該走法新增一個子節點。
3. 從新節點以快速策略進行推演到終局，並記下結果 $z \in \{-1, 0, 1\}$，以移動到該節點的一方為準。
4. 沿路徑往回走。在每個節點，增加造訪次數，並把平均結果朝 $z$ 移動，觀點為該節點的行棋方。
5. 時間預算用完後，在根節點走出造訪次數最多的走法。

## 結果

Kocsis 與 Szepesvári（2006）顯示，UCT 方法在其使用的測試問題上表現良好，這些問題包括需要在寬度與深度之間取得平衡的規劃任務。這個方法最有力的證據來自 2000 年代中期的圍棋程式，它們借此達到了先前搜尋方法未曾達到的水準。Browne 等人（2012）綜述了之後出現的眾多變體與應用。此處的結果為定性描述，確切數字請見原論文。

## 限制

- **成本高**。要下得好需要大量模擬，對於推演很長的遊戲來說成本很高。
- **推演品質弱**。在位置比機率更重要的遊戲中，隨機推演可能是結果的糟糕估計，這也是後來的系統以學得的價值取代推演的原因。
- **搜尋範圍窄**。樹只會依照賭博機規則的指示成長，因此罕見但重要的路線可能始終未被探索。
- **需要模擬器**。規劃者必須能模擬下一個狀態。

## 開放問題

如何在不犧牲隨時停止搜尋之能力的前提下，以學得的評估取代或結合推演？對於各分支數值彼此相關的樹，能否改進賭博機規則？而當模擬器只能透過可能不準確的模型取得時，UCT 在語言或其他領域能擴展到什麼程度？

## 關聯

這個方法是 [AlphaGo](../alphago/index.md)、[AlphaZero](../alphazero/index.md) 與 [MuZero](../muzero/index.md) 中的搜尋步驟，在這些系統中，學得的網路取代了隨機推演，並引導樹的成長。賭博機式的探索在[探索](../../exploration/index.md)頁面中另有討論。這個搜尋也出現在語言模型中，參見 [Hao 等人（2023）](https://arxiv.org/abs/2305.14992)關於以世界模型進行推理的研究。

## 參考文獻

### 開創性論文

- Kocsis, L. & Szepesvári, C. (2006). *Bandit Based Monte-Carlo Planning*. Lecture Notes in Computer Science. https://doi.org/10.1007/11871842_29 — 把 UCB1 賭博機規則應用於蒙地卡羅規劃中樹的走法選擇，即 UCT 演算法。
- Coulom, R. (2007). *Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-540-75538-8_7 — 研究蒙地卡羅樹如何選擇要擴展的走法，以及結果如何回傳，以圍棋為測試領域。
- Silver, D. 等人 (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — AlphaGo，使用由策略與價值網路引導的蒙地卡羅樹搜尋。
- Anthony, T., Tian, Z. & Barber, D. (2017). *Thinking Fast and Slow with Deep Learning and Tree Search*. arXiv:1705.08439. https://arxiv.org/abs/1705.08439 — 專家迭代：樹搜尋改進神經策略，改進後的策略再引導之後的搜尋。

### 綜述與教科書

- Browne, C. B. 等人 (2012). *A Survey of Monte Carlo Tree Search Methods*. IEEE Transactions on Computational Intelligence and AI in Games. https://doi.org/10.1109/TCIAIG.2012.2186810 — 廣泛綜述 MCTS 的各種變體、增強技術，以及遊戲以外的應用。

### 文章與文件

- Hao, S. 等人 (2023). *Reasoning with Language Model is Planning with World Model*. arXiv:2305.14992. https://arxiv.org/abs/2305.14992 — 把語言模型當作世界模型，並以蒙地卡羅樹搜尋規劃推理步驟。
