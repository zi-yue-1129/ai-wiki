---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - ESM-2
  - ESMFold
  - ESM Metagenomic Atlas
  - ESM-2 與 ESMFold
---

# ESM-2 與 ESMFold（Lin 等人，2023）

ESM-2 與 ESMFold 是一個蛋白質語言模型，以及建立在它之上的結構預測器。ESM-2 只從蛋白質序列學習，ESMFold 則加上一個摺疊頭，把它的表徵轉換為三維座標。它們是[生命科學](../index.md)概覽中以序列為基礎的模型，各自有獨立的頁面。

## 概況

蛋白質的序列遠比其結構容易取得。ESM 的做法是直接從序列本身學習，語言模型的訓練不使用結構作為標籤。ESMFold 則從單一序列預測結構，不需要 [AlphaFold 2](../alphafold-2.md) 所用的比對步驟。

## 關鍵方法

這個家族包含兩種方法，各自連結到自己的頁面。

- [ESM-2](esm-2.md)：以遮罩詞元目標、在蛋白質序列上訓練的 Transformer 語言模型。它本身不預測座標。
- [ESMFold](esmfold.md)：建立在 ESM-2 之上的結構預測器。它以一條序列為輸入，輸出座標與信心分數，預印本報告其推論速度遠快於依賴比對的預測器。

## 相關連結

- [AlphaFold 2](../alphafold-2.md)：這個家族通常拿來比較的、依賴比對的結構預測器。
- [Transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md)：兩個模型都使用的架構。
- [RFdiffusion](../rfdiffusion/index.md)：建立在結構預測器（而非語言模型）之上的設計工具。

## 應用

最大規模的應用是 ESM Metagenomic Atlas，這是一個針對宏基因組序列蛋白質的預測結構資料庫。詳見 [ESMFold](esmfold.md)。

## 參考文獻

### 開創性論文

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — 正式發表版本，介紹 ESM-2 與 ESMFold。
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — 本頁摘要所依據的預印本。
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — 較早的 ESM 工作，顯示以序列進行語言模型訓練會浮現與結構相關的資訊。
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2，參照用的結構預測器。
- Vaswani et al. (2017). Attention Is All You Need. NeurIPS 2017. https://proceedings.neurips.cc/paper/7181-attention-is-all-you-need — 提出 ESM-2 所建立於其上的 Transformer 架構。
