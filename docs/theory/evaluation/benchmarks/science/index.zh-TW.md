---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - science
---

# 科學基準

科學基準測試模型能否預測自然系統的量測性質，例如分子的性質。由於每個資料集有自己的標籤，只有在資料集、切分與指標相同時，分數才可比較。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [MoleculeNet](moleculenet.md) | 跨多個資料集預測分子性質 | 分類用 ROC-AUC，迴歸用誤差指標 |

## 常見問題

- **切分方式。** 隨機切分會把近似重複的分子放入訓練與測試集，因而高估泛化能力。骨架切分則測試全新的核心結構。
- **標籤雜訊。** 標籤來自不同的實驗與來源，因此各任務的雜訊程度不同（Wu et al., 2018）。
- **資料稀少。** 當標籤很少或類別高度不平衡時，學習到的表徵可能表現不佳（Wu et al., 2018）。

## 相關

- [基準測試概述](../index.md) 列出所有家族。
- [指標](../../metrics/index.md) 說明 ROC-AUC 與誤差指標。
- [協定](../../protocols/index.md) 說明切分與報告方式。

## 參考文獻

### 開創性論文

- Wu, Z. et al. (2018). *MoleculeNet: a benchmark for molecular machine learning*. Chemical Science. https://doi.org/10.1039/C7SC02664A — 介紹整理過的資料集、共用切分與指標。

### 文章與文件

- Gilmer, J. et al. (2017). *Neural Message Passing for Quantum Chemistry*. arXiv. https://arxiv.org/abs/1704.01212 — 在分子性質預測上評估訊息傳遞網路。

### 補充來源

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，揭露其取捨。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
