---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
  - applications/science
tags:
  - evaluation
  - benchmarks
  - science
aliases:
  - Science benchmarks
  - 科學基準
---

# 科學基準

科學基準測試模型能否預測自然系統的實測性質，例如分子的性質。每個資料集都有自己的標籤，而每個標籤來自特定的實驗或計算，因此只有在資料集、切分與指標都相同時，分數才可以比較。

## 概述

分子機器學習長期缺乏共享的基準。多數新方法都在不同的資料集上測試，因此很難判斷哪種方法比較好。MoleculeNet 的解法是整理多個公開資料集、定義評估指標，並在 DeepChem 函式庫中提供特徵化與學習方法的開源實作（Wu et al., 2018）。作者報告，可學習的表徵非常有力，整體上提供最佳表現，但仍有附帶條件：在資料稀少與類別高度不平衡的複雜任務上，它們仍然吃力。

這個基準是科學領域一個普遍模式的早期例子：預測模型所提供的資訊，取決於區分訓練分子與測試分子的切分方式。隨機切分會把近親分子同時放進兩個集合，而骨架切分（scaffold split）會依分子的核心結構分組，用以測試模型能否推廣到新的化學結構。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [MoleculeNet](moleculenet.md) | 跨多個資料集預測分子性質 | 分類用 ROC-AUC，迴歸用誤差量測 |

目前 MoleculeNet 是此家族中唯一的基準，因此比較的是它內部的各項任務，而非不同基準之間。它的資料集涵蓋不同的性質與不同的標籤來源，因此跨任務的平均會掩蓋彼此之間的大差異。

## 關鍵概念

- **骨架（scaffold）**：分子的核心環狀與連接結構，去除側鏈後的部分。骨架切分會讓每個骨架只出現在一個集合中。
- **ROC-AUC**：接收者操作特徵曲線下的面積，是不依賴單一決策門檻的分類分數。
- **特徵化**：把分子轉換成數字的步驟，例如指紋或圖形。可學習的特徵化以訓練後的網路取代它。

## 運作方式

模型在某資料集的訓練切分上訓練，並以該資料集的指標在保留的測試切分上評分。分類任務使用 ROC-AUC，迴歸任務使用誤差量測。結果通常會跨任務與多次執行取平均。由於切分會改變結果，必須報告所用的切分方式；同一個模型在隨機切分與骨架切分下，數字可能差異很大。

## 常見問題

- **切分選擇。** 隨機切分會把幾乎相同的分子放進訓練與測試，使泛化能力被高估。骨架切分則測試新的核心結構。
- **標籤雜訊。** 標籤來自不同的檢測方法與來源，因此各任務的雜訊程度不同。
- **資料稀少與不平衡。** 當標籤很少或類別高度不平衡時，可學習的表徵可能表現不佳（Wu et al., 2018）。

## 相關連結

- [圖神經網路](../../../models/gnn/index.md) 是分子常用的模型家族，因為分子自然地是由原子與鍵構成的圖（Gilmer et al., 2017）。
- [指標](../../metrics/index.md) 說明 ROC-AUC 與各種誤差量測。
- [科學應用](../../../../applications/science/index.md) 涵蓋這些基準所要支持的科學用途。

## 開放問題

- 固定的分子資料集基準能否跟上新方法所應用的化學領域。
- 如何報告不確定性，使方法之間的小幅進步能與切分及種子之間的變異相比較。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [協定](../../protocols/index.md) 涵蓋切分與報告方式。

## 參考文獻

### 開創性論文

- Wu, Z. et al. (2018). *MoleculeNet: a benchmark for molecular machine learning*. Chemical Science, 513–530. https://doi.org/10.1039/C7SC02664A — 介紹整理後的資料集、指標與此基準的開源實作。
- Gilmer, J. et al. (2017). *Neural Message Passing for Quantum Chemistry*. arXiv. https://arxiv.org/abs/1704.01212 — 提出從圖形預測分子性質的訊息傳遞框架。

### 文章與文件

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，以揭示取捨，此方法也適用於科學基準。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新收集的測試集能揭露對原資料集的擬合，這對任何固定基準都是風險。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 檢視基準的建構效度，以及廣泛宣稱的限制。
