---
translation_reviewed: 2026-10-28
---

# SparseGPT

SparseGPT 是針對大型 GPT 系列模型的單次剪枝方法。它逐層移除權重，並以近似的反 Hessian（來自該層的重建誤差）更新剩餘權重以作補償。它不需要重新訓練就能達到很高的非結構化稀疏度。它是 [GPTQ](../../../quantisation/post-training/gptq/index.zh-TW.md) 在剪枝方面的對應方法，後者用相同的框架做捨入。

## 問題

迭代剪枝加重新訓練對於數十億參數的模型成本太高。簡單的量值剪枝在這些模型中高稀疏度時會失效，因為移除權重而不修正其他權重，會損失太多該層的輸出。

## 核心想法

單次剪枝每一層，同時選擇要移除的權重，並更新剩餘權重，使該層的輸出維持接近原本。選擇與更新都來自重建誤差，並以二階資訊近似。

## 公式或演算法

對輸入為 \(X\) 的層，此方法在遮罩與更新後的權重 \(\hat{W}\) 上最小化 \(\lVert WX - \hat{W}X \rVert^2\)。它逐行以分塊更新的方式進行，使用由校準輸入算出的近似反 Hessian。求解器在一小批校準資料上執行。

## 結果

摘要報告，在大型 GPT 系列模型中，此方法能達到 60% 的非結構化稀疏度，困惑度幾乎沒有增加。

## 限制

非結構化稀疏需要稀疏核心才能加速。此方法需要校準資料與近似二階求解器，增加了工程複雜度。

## 開放問題與相關變體

- **結構化變體。** 把重建框架延伸到整個注意力頭或通道，不在原始方法的範圍內。
- **相關**：[Wanda](../wanda/index.zh-TW.md)使用較簡單的分數，且不更新權重。

## 相關連結

SparseGPT 與 [GPTQ](../../../quantisation/post-training/gptq/index.zh-TW.md) 共用以曲率為基礎的框架，一個用於移除，一個用於捨入。非結構化的結果需要 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)討論的稀疏格式才能加速。

## 參考文獻

### 開創性論文

- Frantar, E., Alistarh, D. (2023). *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot*. arXiv:2301.00774. https://arxiv.org/abs/2301.00774 — 以權重重建做單次剪枝，在困惑度幾乎沒有增加的情況下達到 60% 稀疏度。
- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — 使用相同二階框架的捨入對應方法。
- Sun, M., 等人 (2023). *A Simple and Effective Pruning Approach for Large Language Models*. arXiv:2306.11695. https://arxiv.org/abs/2306.11695 — 作為比較的較簡單單次分數，不做權重修正。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述基於重建的方法與其他稀疏化方法。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — SparseGPT 所比較的量值基準。
