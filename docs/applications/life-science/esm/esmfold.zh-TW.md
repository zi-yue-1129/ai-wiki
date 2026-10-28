---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/transformer
aliases:
  - ESMFold
  - ESM Metagenomic Atlas
  - 單序列結構預測
---

# ESMFold（Lin 等人，2023）

ESMFold 從單一胺基酸序列預測蛋白質的三維結構。它在 [ESM-2](esm-2.md) 之上加入一個摺疊頭，使語言模型的表徵直接輸入結構預測器，不需要比對相關序列。在[生命科學](../index.md)概覽中，它是以序列為基礎、速度快的選項。

## 概況

[AlphaFold 2](../alphafold-2.md) 等結構預測器在預測前會搜尋序列資料庫，建立多重序列比對。這個搜尋很耗時，而且在蛋白質的近親很少時會失效。ESMFold 的輸入只有一條序列，一次前向計算即可輸出座標與信心分數。

## 關鍵概念

- **單序列預測**：輸入是一條序列，不需要比對。
- **摺疊區塊**：交替更新序列表徵與殘基配對表徵的區塊。
- **循環（recycling）**：將輸出再次餵回區塊。預印本採用三次循環。
- **信心分數**：模型在輸出座標的同時，也輸出結構的預測信心。
- **結構圖譜（atlas）**：在大量序列上執行模型所建立的預測結構資料庫。

## 演算法

1. 以 [ESM-2](esm-2.md) 編碼序列，為每個殘基得到一個表徵。
2. 將表徵送入一疊摺疊區塊。每個區塊同時更新序列表徵與殘基配對表徵。
3. 將輸出送入等變的 Transformer 結構模組，產生原子座標。
4. 對摺疊主幹與結構步驟重複三次循環，然後輸出結構及其預測信心。

作者以與 AlphaFold 相同的損失函數訓練摺疊頭，因此訓練目標沿用 AlphaFold 的脈絡，而輸入與架構則不同。

## 結果

- **速度**：預印本報告指出，單純的前向推論速度比現有最佳方法快達 60 倍，並主張解析度與精確度得以維持。
- **結構圖譜**：作者摺疊了來自 MGnify90 資料庫的超過 6.17 億條序列，其中約 2.25 億筆預測為高信心。
- 基準測試集上的精確度數字見論文，這裡不再重述。

## 限制

- 速度與精確度數字來自預印本。最終數字應以正式發表於 *Science* 的版本為準。
- 結構圖譜的條目是計算預測。高信心代表模型有把握，不代表該結構已由實驗證實。
- 精確度取決於語言模型對該蛋白質學到了多少。訓練資料中近親很少的蛋白質是最困難的情況（這是推論，並非論文的結論）。

## 相關連結

- [ESM-2](esm-2.md)：ESMFold 所建立於其上的語言模型。
- [AlphaFold 2](../alphafold-2.md)：依賴比對的預測器。ESMFold 的作者將其方法描述為對現有結構預測器的簡化，並且與 AlphaFold 共用訓練損失。
- [RFdiffusion](../rfdiffusion/index.md)：使用結構預測器 RoseTTAFold（而非語言模型）的設計工具。
- 腦與心智：沒有直接關聯。此方法處理的是序列與結構，而非神經資料。

## 應用

- **宏基因組結構圖譜**：ESMFold 使得為許多來自環境序列、沒有實驗結構的蛋白質預測結構成為可能。
- **快速篩選**：在較慢的方法或實驗之前，需要先快速估計許多序列結構的情境，單序列預測器很適合。

## 開放問題

- 單序列預測對近親很少的蛋白質，以及對多鏈複合體的準確度如何。
- 如何判斷結構圖譜中哪些預測可靠到值得進行實驗驗證。

## 參考文獻

### 開創性論文

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — 正式發表版本，介紹 ESMFold 與 ESM Metagenomic Atlas。
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — 本頁速度與結構圖譜數字所依據的預印本。
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2，ESMFold 比較的依賴比對預測器。
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — 較早的 ESM 工作，探討在蛋白質序列上訓練的語言模型。
- Vaswani et al. (2017). Attention Is All You Need. NeurIPS 2017. https://proceedings.neurips.cc/paper/7181-attention-is-all-you-need — 提出此語言模型所用的 Transformer 架構。
