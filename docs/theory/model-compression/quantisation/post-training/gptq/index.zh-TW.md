---
translation_reviewed: 2026-10-28
---

# GPTQ

GPTQ 是一種訓練後方法，把大型語言模型的權重量化為 3 或 4 位元。它每次處理一層中的一行，捨入後再用校準資料的近似二階資訊，調整尚未量化的行，以補償捨入誤差。

## 問題

像最近捨入這樣把每個權重都四捨五入到最近的網格值，忽略了捨入對其他權重的影響。在 3 或 4 位元時，誤差會累積，品質下降。

## 核心想法

逐行量化單一層的權重。每一行捨入後，用校準輸入的近似二階資訊，更新尚未量化的行，以補償捨入誤差。

## 公式或演算法

此方法遵循最佳腦部量化（optimal brain quantisation）的框架，利用該層平方誤差 \(\lVert WX - \hat{W}X \rVert^2\) 的反 Hessian \(H^{-1}\)，決定先捨入哪個權重，以及如何更新其餘權重。GPTQ 以分塊處理與 Cholesky 分解，使數十億參數的模型也能有效率地完成。

## 結果

摘要報告，GPTQ 能在約四個 GPU 小時內量化 1750 億參數的 GPT 模型，把權重降到 3 或 4 位元。

## 限制

校準使用一小批資料，因此結果取決於它與目標領域的吻合程度。推論時要獲得加速，需要支援該打包格式的核心程式。

## 開放問題與相關變體

- **校準敏感度**：結果隨校準資料而變，對推理與長脈絡任務的影響較少被研究。
- **相關**：[AWQ](../awq/index.zh-TW.md) 透過縮放顯著通道達到相近的位元寬度，而不是補償捨入誤差。

## 相關連結

GPTQ 與[二階重建剪枝](../../../pruning/index.zh-TW.md)使用相同的曲率概念，也是[混合精度](../../mixed-precision/index.zh-TW.md)比較中常見的基準。

## 參考文獻

### 開創性論文

- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. ICLR 2023. https://arxiv.org/abs/2210.17323 — 逐層二階捨入，為 3 與 4 位元權重做誤差補償。
- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — 剪枝的對應方法，使用相同的重建框架。
- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 8 位元替代方案，把離群值保留在 16 位元。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧 GPTQ 所屬的精度降低方法。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Lin, J., 等人 (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. arXiv:2306.00978. https://arxiv.org/abs/2306.00978 — 4 位元權重的激活感知替代方法。
