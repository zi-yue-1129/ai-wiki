---
translation_reviewed: 2026-10-28
---

# HAWQ

HAWQ（Hessian AWare Quantization，海森感知量化）依據每一層損失的曲率，為該層選擇位元寬度。損失對擾動變化劇烈的層保留較多位元；對擾動平坦的層則給予較少位元。它是[量化](../../index.zh-TW.md)中[混合精度](../index.zh-TW.md)家族的一種方法。

## 問題

手動選擇或窮舉搜尋位元寬度很慢，而以大小為基礎的簡單規則，無法反映每層對捨入的敏感度。大小相同的兩層，對相同的捨入誤差可能反應截然不同。

## 核心想法

以損失對各層權重的 Hessian 作為敏感度的度量。最大特徵值，或整個譜的平均，表示損失在該層各方向上彎曲的程度。依此排序各層，並把更多位元分給敏感的層，直到滿足位元預算為止。

## 公式或演算法

Hessian 很大，因此只需要它的最大特徵值。方法以冪迭代估計，每次迭代使用 Hessian 向量乘積，不必形成完整矩陣，這可以用自動微分計算。每層得到一個敏感度分數，然後選擇位元寬度，使總敏感度在記憶體限制下最小。

## 結果

摘要表示，HAWQ 能依據 Hessian 譜自動選擇每層的相對量化精度。具體的準確度結果，見論文中的表格。

## 限制

Hessian 估計有雜訊，冪迭代也會在每次校準中增加計算量。此方法是為卷積網路開發的，延伸到超大型 Transformer 仍需研究。以平均值表示的敏感度，可能會掩蓋少數但重要的層。

## 開放問題與相關變體

- **預測行為**：基於 Hessian 的敏感度，是否能預測捨入對推理與長脈絡行為的影響，而不只是平均損失，目前尚不清楚。
- **相關**：[GPTQ](../../post-training/gptq/index.zh-TW.md) 使用相同的二階資訊，但用於補償層內的捨入誤差，而不是在層與層之間選擇位元寬度。

## 相關連結

HAWQ 擴展了[量化](../../index.zh-TW.md)中的均勻精度想法。它的預算由目標[硬體](../../../../../engineering/hardware/index.zh-TW.md)的記憶體與延遲限制決定。基於曲率的敏感度，也用於[剪枝](../../../pruning/index.zh-TW.md)中決定要移除哪些權重。

## 參考文獻

### 開創性論文

- Dong, Z., Yao, Z., Gholami, A., Mahoney, M., Keutzer, K. (2019). *HAWQ: Hessian AWare Quantization of Neural Networks with Mixed-Precision*. arXiv:1905.03696. https://arxiv.org/abs/1905.03696 — 依據每層的 Hessian 譜指定位元寬度。
- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — 以二階資訊補償層內捨入，是均勻精度的對應方法。
- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 均勻 8 位元整數推論，是混合精度所要改進的基準。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧混合精度方案及其使用的敏感度度量。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 把離群維度保留在 16 位元的混合精度分解，是矩陣內部的另一種位元分配方式。
