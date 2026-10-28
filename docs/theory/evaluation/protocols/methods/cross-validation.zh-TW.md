---
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - statistics
---

# 交叉驗證

交叉驗證的做法是：在同一份資料的數種不同切分上訓練與測試模型，再把結果取平均，以估計模型的泛化能力。相較於單一的訓練與測試切分，它能更有效地運用小型資料集。它最初是為了在不把全部資料用於單一測試集的情況下，選擇並評估預測模型而提出的（Stone, 1974）。

## 程序

在 k 摺交叉驗證中，資料被分成 k 摺。每一摺輪流作為測試集，模型在其餘各摺上訓練，最後把 k 個分數取平均。分層摺會讓每一摺的類別比例相同，這在類別不平衡時很重要。分群摺則讓同一單位（例如同一位病人）的所有範例都留在同一摺。

## 選擇超參數

交叉驗證也用於選擇設定。這麼做時，外層迴圈必須與選擇設定的內層迴圈分開，否則報告的分數會過於樂觀。巢狀設計以內層迴圈做選擇，外層迴圈做最終估計。

## 報告

說明摺數、摺是分層或分群、是否打亂，並同時報告摺分數的離散程度與平均值。每一摺都有自己的變異，單看平均值無法顯示結果是否穩定。

## 限制

- **摺之間的相依性。** 分散在不同摺中的重複或相關範例會使估計膨脹。
- **時間順序。** 在預測任務中，打亂的摺無效，因為只能用較早的資料來訓練預測較晚資料的模型。
- **與訓練重疊。** 在多次比較中重複使用的摺，可能有利於曾在其上調校的方法。

## 相關

- [評估協定概述](../index.md) 更詳細地說明各種切分方式。
- [配對自助法](paired-bootstrap.md) 估計兩個方法之間差異的不確定性。

## 參考文獻

### 開創性論文

- Stone, M. (1974). *Cross-Validatory Choice and Assessment of Statistical Predictions*. Journal of the Royal Statistical Society: Series B. https://doi.org/10.1111/j.2517-6161.1974.tb00994.x — 將交叉驗證介紹為選擇與評估預測模型的方法。

### 文章與文件

- scikit-learn contributors. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — 說明 k 摺、分層、分群與時間感知的切分方式。
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，因此單一切分可能掩蓋取捨。

### 補充來源

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張在固定任務上的技能是衡量智能的弱指標。
