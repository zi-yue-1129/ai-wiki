---
translation_reviewed: 2026-10-28
---

# 混合精度量化

混合精度量化讓不同層，或同一層的不同部分，使用不同的位元數。網路中有些部分對捨入很敏感，應保留較多位元；有些則容忍很少的位元。問題在於，在總記憶體或延遲的預算下，如何分配位元。它是均勻[量化](../index.zh-TW.md)的改進。

## 概述

均勻方案在所有地方使用相同位元數，會在不敏感的層上浪費位元，又在敏感的層上損失準確度。混合精度尋找一種分配方式，在滿足預算的同時使損失維持很小。搜尋需要一個敏感度的度量。簡單的啟發式方法使用層的大小，或捨入後的輸出誤差。較有原則的方法則使用損失的曲率，以 Hessian 近似。

## 關鍵概念

- **位元分配**：為每層指定位元寬度，通常從 4、8、16 位元等小集合中選擇。
- **敏感度**：一層被捨入時，損失變化多少。敏感度取決於層以及位元寬度。
- **預算**：目標大小或延遲，使位元分配成為有約束的最佳化問題。
- **混合精度分解**：在一次矩陣乘法內，把需要保留高精度的離群維度分開，如 [LLM.int8()](../index.zh-TW.md)。

## 重要方法

### HAWQ（Dong 等人，2019）

- **問題：** 手動或窮舉搜尋位元寬度很慢，而以大小為基礎的簡單規則無法反映每層對捨入的敏感度。
- **核心想法：** 使用每層的 Hessian 譜，也就是損失在該層各方向上的彎曲程度，來排序各層的敏感度。最大特徵值大的層分配較多位元。
- **公式或演算法：** 每層的敏感度由損失對該層權重的 Hessian 估計，以 Hessian 向量乘積的冪迭代計算。之後分配位元以滿足預算。
- **結果：** 摘要表示，HAWQ 能依據 Hessian 譜自動選擇每層的相對量化精度。具體的準確度結果應查閱論文中的圖表。
- **限制：** Hessian 估計有雜訊，計算成本也較高。方法是為卷積網路開發的，延伸到超大型 Transformer 仍需研究。

## 取捨

- **固定預算下的準確度**：混合精度通常在相同平均寬度下優於均勻精度，但增益取決於敏感度估計的好壞。
- **硬體支援**：混合位元寬度會使核心程式變複雜。只提供少數格式的硬體，會限制可用的分配。
- **搜尋成本**：在進行任何壓縮之前，敏感度估計需要額外的校準時間。

## 更多變體與開放問題

- **變體**：每個區塊帶指數的浮點格式，例如近期加速器支援的 FP8 與 FP4 格式，這使混合精度與數字格式設計的界線變得模糊；見 [AI 硬體](../../../../engineering/hardware/index.zh-TW.md)。
- **開放問題**：基於 Hessian 的敏感度，是否能預測捨入對推理與長脈絡行為的影響，而不只是平均損失。
- **開放問題**：如何將位元分配與剪枝聯合進行；[剪枝](../../pruning/index.zh-TW.md)只部分涵蓋這種組合。

## 相關連結

混合精度直接回應上層[量化](../index.zh-TW.md)頁所討論的離群值問題，並使用 [GPTQ](../index.zh-TW.md) 補償捨入誤差所用的相同曲率概念。它所針對的記憶體預算，由目標裝置的[記憶體層級](../../../../engineering/hardware/index.zh-TW.md)決定。

## 參考文獻

### 開創性論文

- Dong, Z., Yao, Z., Gholami, A., Mahoney, M., Keutzer, K. (2019). *HAWQ: Hessian AWare Quantization of Neural Networks with Mixed-Precision*. arXiv:1905.03696. https://arxiv.org/abs/1905.03696 — 依據每層的 Hessian 譜分配位元寬度。
- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — 以二階資訊補償 3 與 4 位元的捨入，是大型語言模型的均勻精度基準。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧精度降低方法，包括混合精度方案。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 以 16 位元保留離群維度的混合精度分解。
- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 均勻 8 位元整數推論，是混合精度所要改進的基準。
