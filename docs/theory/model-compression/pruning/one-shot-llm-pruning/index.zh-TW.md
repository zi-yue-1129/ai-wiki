---
translation_reviewed: 2026-10-28
---

# 大型語言模型單次剪枝

單次剪枝是在每層只處理一次，就移除已訓練語言模型的大部分權重，不需要重新訓練。迭代剪枝加重新訓練對於數十億參數的模型成本太高，因此單次方法利用一小批校準資料，在一個步驟中決定要移除哪些權重，並決定是否調整剩餘權重。兩個主要方法是 [SparseGPT](sparsegpt/index.zh-TW.md)（會更新剩餘權重）與 [Wanda](wanda/index.zh-TW.md)（不會更新）。

## 概述

兩個方法都逐層進行。對每個線性層，它們使用校準輸入為權重評分或選擇，移除指定比例的權重，然後處理下一層。差別在於剩餘權重是否被修正以補償移除。SparseGPT 以近似二階求解器修正它們；Wanda 使用計算成本低的分數，且不做修正。

## 各方法比較

| 方法 | 移除權重的依據 | 是否修正剩餘權重 | 成本 | 頁面 |
| --- | --- | --- | --- | --- |
| SparseGPT | 二階重建誤差 | 是，分塊更新 | 較高，每層一個求解器 | [SparseGPT](sparsegpt/index.zh-TW.md) |
| Wanda | 權重量值乘以輸入激活值的範數 | 否 | 低，對校準輸入做一次計算 | [Wanda](wanda/index.zh-TW.md) |

當校準時間或工程投入最需要控制時，Wanda 是較簡單的選擇。當高稀疏度下的準確度最重要時，應選 SparseGPT，因為修正能保留更多輸出。

## 關鍵概念

- **校準集。** 一小批輸入，用來量測每個權重所乘的激活值。
- **非結構化稀疏。** 個別權重被移除，因此需要稀疏核心才能加速；若要硬體能跳過的模式，見 [N:M 稀疏](../n-m-sparsity/index.zh-TW.md)。
- **逐層目標。** 一層輸出的誤差 \(\lVert WX - \hat{W}X \rVert^2\)，而不是權重的誤差。

## 取捨

- **準確度與成本。** SparseGPT 在高稀疏度下更準確，但校準時間較長。
- **硬體支援。** 非結構化稀疏需要稀疏核心才能加速；沒有核心時，節省的只是儲存空間。
- **與量化結合。** 同一個二階框架也被 [GPTQ](../../quantisation/post-training/gptq/index.zh-TW.md) 用於捨入，兩者可以共用程式碼。

## 開放問題

- **推理與長脈絡。** 單次剪枝對多步推理的影響，比對困惑度的研究少。
- **超越困惑度。** 剪枝後模型在指令遵循與安全性上的評估仍然有限。
- **結構化的單次方法。** 一次移除整個注意力頭或通道，同時維持相近準確度，仍是待解的工程問題。

## 相關連結

單次剪枝位於[同時學習權重與連接](../learning-weights-and-connections/index.zh-TW.md)的迭代方法與[量化](../../quantisation/index.zh-TW.md)的訓練後量化之間。它產生的稀疏格式取決於執行它們的 [AI 硬體](../../../../engineering/hardware/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — 以權重重建做單次剪枝，在困惑度幾乎沒有增加的情況下達到 60% 稀疏度。
- Sun, M., 等人 (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — Wanda，一種量值乘以激活值的分數，不需要重新訓練或修正權重。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 單次方法所取代的迭代剪枝加重新訓練。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述稀疏化方法的成本與硬體取捨。
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 量值剪枝的基準，大型語言模型的單次方法都與它比較。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — 使用相同二階框架的量化方法。
