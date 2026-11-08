---
related:
  - theory/paradigms/imitation
  - theory/paradigms/reinforcement-learning
  - applications/robotics
tags:
  - imitation learning
  - behavioural cloning
  - inverse reinforcement learning
  - survey
aliases:
  - An Algorithmic Perspective on Imitation Learning
  - Osa et al. survey
  - 模仿學習的演算法觀點
translation_reviewed: 2026-11-01
---

# 模仿學習的演算法觀點

Osa 等人（2018）是一本從演算法角度綜述模仿學習的專書。它同時為機器學習研究者與機器人學者而寫，並以兩大家族組織這個領域：行為複製，直接從觀測學習到動作的映射；以及逆強化學習，推論專家似乎在最佳化的獎勵。本書是這個領域很好的地圖，家族層級的比較見[模仿學習](index.md)頁面。

## 概述

模仿學習從示範而非獎勵訊號建構策略。專書把這個領域視為一組設計選擇，包括示範長什麼樣子、學習者能否觀測到專家所觀測的東西、策略如何表示，以及如何訓練。每個選擇都會改變適用的演算法，因此綜述以這些選擇來組織各種方法。

## 範圍與結構

專書共五章。

- **第 2 章，設計選擇：** 可觀測性、策略抽象、行為描述子，以及資訊理論分析。
- **第 3 章，行為複製：** 從示範中以監督式學習動作或軌跡。涵蓋含神經網路（包括循環網路）的動作-狀態模型、教師-學生互動、以動作基元進行的軌跡學習、任務層級規劃，以及以模型為基礎的方法。
- **第 4 章，逆強化學習：** 以模型為基礎的方法，如最大間隔規劃與最大熵逆強化學習；以及無模型方法，如相對熵逆強化學習與生成對抗模仿學習（GAIL）。
- **第 5 章，挑戰：** 行為複製與逆強化學習的關係，以及關於資料、設計選擇、演算法與評估的未解問題。

DAgger 等互動式方法被放在第 3 章的教師-學生互動之下。GAIL 則在第 4.5.2 節處理，而非獨立的對抗章節。

## 核心問題

專書把行為複製的核心困難解釋為分布偏移：學習者常會到達專家從未造訪過的狀態，因此早期的小錯誤可能導致之後的不良行為。互動式方法被視為回應，因為它們讓學習者自己經過的狀態得到標註。綜述也指出，最大似然複製在許多應用中可能效果不佳，並把學習者軌跡分布與專家軌跡分布的匹配寫成一個 KL 散度目標（第 2.7.2 節）。

## 未解挑戰

專書列出幾個仍未解決的困難。

- **投影。** 作者指出，沒有任何現有模仿方法能精確執行 I 投影，並稱基於 I 投影的方法是有趣的研究方向。
- **模型學習。** 對某些任務而言，學習動力學很困難，例如可變形物體之間的接觸。
- **專家與學習者的不匹配。** 當兩者觀測的資訊或身體不同時，專家示範對學習者可能是次佳的。
- **階層。** 同時學習高層與低層策略被描述為並非易事。
- **資料成本。** 示範與推演都很昂貴，近期方法常需要大量資料。

## 關聯

- 互動式方法是 [DAgger](interactive-imitation/index.md)，它處理綜述所描述的分布偏移問題。
- 逆強化學習章節所涵蓋的家族見[逆強化學習](inverse-reinforcement-learning/index.md)。
- 模仿可以取代或輔助的強化學習方法，見[強化學習](../reinforcement-learning/index.md)頁面。

## 未解問題

- 不使用互動式專家，能解決多少分布偏移問題？
- 逆強化學習恢復的獎勵，能否轉移到新的身體構造上？
- 什麼樣的評估協定能證明模仿策略是在推廣，而不只是重現示範？

## 參考文獻

### 奠基論文

- Osa, T., Pajarinen, J., Neumann, G., Bagnell, J. A., Abbeel, P. & Peters, J. (2018). An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics, 7(1–2), 1–179. [DOI 10.1561/2300000053](https://doi.org/10.1561/2300000053) — 本頁所摘要的專書，涵蓋行為複製、逆強化學習與未解挑戰。
- Ross, S., Gordon, G. J. & Bagnell, J. A. (2010). A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — 提出 DAgger，處理分布偏移的互動式方法。
- Ho, J. & Ermon, S. (2016). Generative Adversarial Imitation Learning. [arXiv:1606.03476](https://arxiv.org/abs/1606.03476) — GAIL，即綜述第 4.5.2 節處理的對抗式方法。
- Argall, B. D. 等人（2009）。A survey of robot learning from demonstration. Robotics and Autonomous Systems, 57, 469–483. [DOI 10.1016/j.robot.2008.10.024](https://doi.org/10.1016/j.robot.2008.10.024) — 較早從機器人學角度綜述示範學習的文獻。

### 綜述與教科書

- Goodfellow, I. J. 等人（2014）。Generative Adversarial Networks. [arXiv:1406.2661](https://arxiv.org/abs/1406.2661) — GAIL 所改編的對抗訓練框架。

### 講座與影片

（本頁未核對）

### 文章與文件

（本頁未核對）
