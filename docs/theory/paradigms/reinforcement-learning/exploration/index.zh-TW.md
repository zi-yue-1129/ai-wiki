---
related:
- theory/paradigms/online
- brain-mind/neuroscience
aliases:
  - Exploration
  - Exploration–Exploitation
  - Intrinsic Motivation
  - 探索
  - 探索與利用
  - 內在動機
tags:
  - reinforcement learning
  - exploration
  - intrinsic motivation
translation_reviewed: 2026-10-28
---

# 探索

代理人只能學到自己嘗試過的動作，因此必須在利用已知與探索未知之間做選擇。在強化學習中，這個取捨決定代理人能否找到罕見的獎勵。當獎勵密集時，簡單的隨機探索就夠用；但在困難的問題中，代理人需要一長串特定的動作才會看到第一個獎勵，隨機探索就會失敗。因此，多數探索方法都是在獎勵之外加上一個「獎勵加成」（bonus），或設計一種機制，讓較少造訪或較不了解的狀態變得有吸引力。探索是每個[價值導向](../value-based-methods/index.md)與[策略梯度](../policy-gradient-and-actor-critic/index.md)方法的組件，也和[多臂吃角子老虎機](../../online/stochastic-bandits/index.md)問題密切相關。

## 概觀

探索方法的差別在於它們在獎勵之外加上什麼訊號：

- **無方向的雜訊**會擾動動作或參數，不考慮已經看過什麼。
- **計數式獎勵加成**會獎勵造訪次數少的狀態。
- **預測誤差式獎勵加成**會獎勵代理人還無法預測的狀態，它借助學到的模型。
- **後驗或集成方法**保留多個假說，並依其中一個行動。
- **歸檔式方法**保存有潛力的狀態，並回到這些狀態。

## 做法

| 家族 | 想法 | 關鍵論文 |
|---|---|---|
| 隨機動作雜訊 | ε-greedy 或 softmax 動作選擇 | Sutton & Barto (2018) |
| 偽計數獎勵 | 用密度模型估計狀態造訪，並加上隨造訪次數遞減的獎勵 | Bellemare et al. (2016), arXiv:1606.01868 |
| 好奇心模組（ICM） | 獎勵是前向模型在學到的特徵空間中的誤差 | Pathak et al. (2017), arXiv:1705.05363 |
| 隨機網路蒸餾 | 獎勵是一個預測器模仿固定隨機網路時的誤差 | Burda et al. (2018), arXiv:1810.12894 |
| 雜訊網路 | 學習網路權重上雜訊的尺度，讓探索在訓練中自我調整 | Fortunato et al. (2017), arXiv:1706.10295 |
| Bootstrapped DQN | 共用網路上有多個價值頭；每回合由抽中的一個頭引導行動 | Osband et al. (2016), arXiv:1602.04621 |
| Go-Explore | 保存已造訪狀態的歸檔，回到有潛力的狀態，再從那裡探索 | Ecoffet et al. (2019), arXiv:1901.10995 |

### 計數與預測式獎勵

計數獎勵會隨造訪次數遞減，鼓勵覆蓋整個狀態空間。在高維觀測中無法精確計數，因此改用密度模型估計偽計數。預測誤差式獎勵則把學到的預測器的誤差當作新奇度。好奇心模組預測動作的後果，但使用的特徵空間會忽略代理人無法控制的東西。隨機網路蒸餾則不學特徵空間，而是預測一個固定隨機網路的輸出。

### 參數雜訊與集成

雜訊網路在權重上加入學到的雜訊，因此代理人會隨學習而變得較不隨機。Bootstrapped DQN 保留多個頭，每個頭都在資料的不同 bootstrap 樣本上訓練。在整個回合中只用一個抽中的頭行動，會產生一致、深入的探索行為，而不是來回搖擺，因此常被稱為深度探索（deep exploration）。

### 歸檔式探索

Go-Explore 把問題拆成兩部分：回到先前找過的狀態，然後從那裡探索。它保存一份不同狀態的歸檔，挑選其中一個，回到它，再探索。能夠回到已知狀態，是因為模擬器可以重設到保存的狀態。在 Atari 上，對於獎勵極為稀疏的遊戲（例如 Montezuma's Revenge），它的分數遠超過先前的方法。

## 取捨

- **獎勵加成會改變目標。** 獎勵加成會加到任務獎勵上，因此代理人在任務已解決後仍可能持續追求新奇；除非加成會遞減，否則最終策略可能不是最優。
- **隨機干擾。** 不可預測的雜訊來源會造成持續的預測誤差。由預測誤差驅動的代理人可能會無止境地盯著它，這稱為「雜訊電視」問題（noisy-TV problem）。
- **超參數敏感。** 獎勵加成相對於任務獎勵的尺度，往往是最重要的設定，而合適的值因任務而異。
- **重設需求。** 歸檔方法假設環境可以還原到保存的狀態，但許多真實系統並非如此。

## 相關連結

在多臂問題中，探索有以遺憾界（regret bound）為基礎的長期理論，見[線上學習](../../online/index.md)。這些結果能指引價值導向方法，但很少能直接搬到深度網路上。探索也與[經驗回放](../experience-replay/index.md)緊密耦合，因為代理人保留的資料決定了它能從罕見事件中學到什麼。

心理學與神經科學區分了人類選擇中的兩種探索。Wilson et al.（2014）發現，人們會把一個有方向的成分（偏好不確定性或資訊價值高的選項）與一個隨機成分（加入選擇雜訊）結合在一起。多巴胺與去甲腎上腺素系統常被與探索相連，雖然對應關係仍有爭議。更廣的背景見[神經科學](../../../../brain-mind/neuroscience/index.md)。

## 未解問題與更多變體

- **擴展計數與新奇度。** 在非常大的觀測空間中，偽計數與預測誤差變得不可靠，哪一種新奇度量最能擴展尚不清楚。
- **區分可學習與不可學習的新奇。** 忽略隨機雜訊的方法仍然只是近似，有用與無用好奇心之間的界線也沒有形式化。
- **語言與生成模型中的探索。** 在強化學習式回饋訓練中取樣多樣的輸出，可以視為一種探索。它與經典獎勵加成的關係大多尚未研究。
- **稀疏、長視野的任務。** 歸檔與子目標方法有幫助，但它們需要一個進度的概念，而這通常是人工設計的。
- **探索時的安全。** 在實體系統中，探索性動作可能不安全。受約束的探索與安全後備策略是活躍的研究方向。
- **評估。** Montezuma's Revenge 等困難探索基準常用來比較方法，但結果對隨機種子與實作細節很敏感。

## 參考文獻

### 開創性論文

- Bellemare, M. G., et al. (2016). "Unifying Count-Based Exploration and Intrinsic Motivation". arXiv:1606.01868 — 從密度模型的偽計數推導出計數式獎勵加成。
- Pathak, D., et al. (2017). "Curiosity-driven Exploration by Self-supervised Prediction". arXiv:1705.05363 — 以學到的特徵空間中的前向模型預測誤差作為獎勵加成。
- Burda, Y., et al. (2018). "Exploration by Random Network Distillation". arXiv:1810.12894 — 以模仿固定隨機網路的預測器誤差作為新奇獎勵。
- Osband, I., et al. (2016). "Deep Exploration via Bootstrapped DQN". arXiv:1602.04621 — 以價值頭的集成達成一致、深入的探索。
- Ecoffet, A., et al. (2019). "Go-Explore: a New Approach for Hard-Exploration Problems". arXiv:1901.10995 — 歸檔有潛力的狀態，探索前先回到這些狀態。

### 綜述與教科書

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — 涵蓋 ε-greedy 動作選擇與探索–利用取捨。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Wilson, R. C., et al. (2014). "Humans use directed and random exploration to solve the explore–exploit dilemma". *Journal of Experimental Psychology: General* 143(6). https://doi.org/10.1037/a0038199 — 行為證據顯示人們同時使用依不確定性導向的探索與隨機探索。
- Fortunato, M., et al. (2017). "Noisy Networks for Exploration". arXiv:1706.10295 — 學習網路權重雜訊的尺度，讓代理人在有把握之處減少探索。
