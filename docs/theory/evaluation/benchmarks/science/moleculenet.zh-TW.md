---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - science
---

# MoleculeNet

MoleculeNet 是分子機器學習的基準。它收集用於預測分子性質的公開資料集，並固定共用的切分與指標，使新方法能在相同資料上比較（Wu et al., 2018）。

## 任務與資料

模型接收一個分子，通常以圖或指紋表示，並預測一項性質。這些性質涵蓋量子力學、物理化學、生物物理與生理學。各資料集的大小與標籤類型不同，從二元類別到連續數值都有。

## 協定與指標

分類任務以 ROC-AUC 評分，迴歸任務以 RMSE 或 MAE 等誤差指標評分，各資料集的定義由基準決定。基準採用骨架切分，把具有不同核心結構的分子分別放入訓練與測試集，因此測試衡量的是對新化學結構的泛化，而非近似重複的分子（Wu et al., 2018）。

## 它能說明什麼

它顯示學到的表徵能否泛化到新分子，以及哪種特徵化方式適合哪類性質。論文報告，可學習的表徵整體表現良好，但在資料稀少與類別高度不平衡時仍有困難；對量子與生物物理資料集而言，考慮物理的特徵化可能比學習演算法的選擇更重要（Wu et al., 2018）。

## 限制

- **資料品質。** 標籤來自不同來源，因此各任務的雜訊不同。
- **切分選擇。** 分數取決於切分方式，隨機切分會高估對新化學結構的表現。
- **重疊。** 同一分子可能出現在多個公開資料集中，若未去除重複，會使結果膨脹。

## 相關

- [科學概述](index.md) 說明科學基準。
- [ROC-AUC](../../metrics/classification/roc-auc.md) 是此處使用的分類指標。
- [RMSE](../../metrics/regression/rmse.md) 是迴歸任務的誤差指標。

## 參考文獻

### 開創性論文

- Wu, Z. et al. (2018). *MoleculeNet: a benchmark for molecular machine learning*. Chemical Science. https://doi.org/10.1039/C7SC02664A — 介紹整理過的資料集、共用切分與指標。

### 文章與文件

- Gilmer, J. et al. (2017). *Neural Message Passing for Quantum Chemistry*. arXiv. https://arxiv.org/abs/1704.01212 — 在分子性質預測上評估訊息傳遞網路。

### 補充來源

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，揭露其取捨。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
