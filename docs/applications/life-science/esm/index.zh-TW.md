---
status: draft
last_reviewed: 2026-10-28
aliases:
  - ESM-2
  - ESMFold
  - ESM Metagenomic Atlas
---

# ESM-2 與 ESMFold（Lin et al., 2023）

ESM-2 是以蛋白質序列訓練的 transformer 語言模型。ESMFold 加上結構輸出頭，讓同一個模型能直接從序列預測蛋白質的三維結構。它是[生命科學](../index.md)概述中以序列為基礎的模型。

## 問題

基因定序發現的蛋白質序列，遠多於已知結構的數量，因此預測結構需要比以往快得多的方法。預印本主張，用語言模型直接從一級序列推論結構，可以在高解析度下達到數量級的加速。

## 核心想法

在數百萬條序列上訓練的語言模型，會學到演化模式。預印本報告，把模型放大之後，它能編碼足以在原子解析度下預測結構的資訊。最大的模型參數量達 150 億。

## 方程式或演算法

ESM-2 是以蛋白質序列訓練的 [transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md) 編碼器，採用遮蔽詞元的目標：序列中的部分位置被遮住，再依上下文預測（Lin et al., 2023）。ESMFold 讀取模型的內部表示，輸出三維座標：

1. 以語言模型編碼胺基酸序列。
2. 由內部表示預測三維結構。
3. 將同一流程套用到資料庫上，建立結構圖譜。

## 結果

以下來自預印本摘要：

- 結構預測比目前最佳方法快達 60 倍，「同時維持解析度與準確度」。
- ESM 宏基因組圖譜包含超過 6.17 億個預測結構，其中超過 2.25 億個是高信心預測，包括數百萬個與實驗已知結構相比為新穎的結構。

## 限制

- 這些結果來自預印本。最終數字應參考已發表的 Science 版本。
- 圖譜中的條目是計算預測。摘要將其描述為高信心預測，而非經實驗證實的結構。
- 模型從序列中的演化模式學習，因此對已知近親很少的蛋白質，它可能掌握的資訊較少（這是推論，並非論文的主張）。

## 關聯

- [RFdiffusion](../rfdiffusion/index.md)：建立在結構預測器 RoseTTAFold 之上的設計工具，而不是語言模型。
- [Transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md)：ESM-2 所用的架構。

## 參考文獻

### 開創性論文

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — 已發表的版本，介紹 ESM-2 與 ESMFold。
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — 結果段落所摘要的預印本。
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — 較早的 ESM 研究，顯示結構相關資訊會在序列的語言模型訓練中出現。
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2，參考用的結構預測器。
- Vaswani et al. (2017). Attention Is All You Need. arXiv. https://arxiv.org/abs/1706.03762 — transformer 架構。
