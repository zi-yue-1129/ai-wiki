---
status: draft
last_reviewed: 2026-10-28
aliases:
  - RFdiffusion
  - RoseTTAFold Diffusion
---

# RFdiffusion（Watson et al., 2023）

RFdiffusion 以擴散模型設計新的蛋白質骨架。它以 RoseTTAFold 結構預測網路為基礎，經過微調來去除蛋白質結構中的雜訊，因此能依簡單的規格生成蛋白質。它是[生命科學](../index.md)概述中的設計工具。

## 問題

深度學習的設計方法早已存在，但預印本指出，當時尚未描述能涵蓋結合子設計、對稱結構與酵素支架的通用框架。擴散模型在影像與語言上已經成功，但用於蛋白質時效果較差，可能因為骨架幾何與序列─結構之間的關係很複雜（Watson et al., 2022）。

## 核心想法

從隨機的骨架座標開始，逐步去除雜訊，把它變成合理的骨架，這與影像擴散模型把雜訊變成圖片的方式相同。去噪器是 RoseTTAFold，它原本被訓練來預測蛋白質結構，因此已經編碼了蛋白質幾何。以設計規格作為條件，可以把結果導向指定的形狀或功能。

## 方程式或演算法

RFdiffusion 遵循[去噪擴散](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)的框架（Ho et al., 2020）。前向過程對真實結構加入雜訊，學習得來的反向過程再把雜訊移除。生成時以設計任務為條件，從雜訊執行反向過程：

1. 取樣一個隨機骨架。
2. 以微調後的 RoseTTAFold 網路經過多步去噪。
3. 以實驗檢驗所得設計。

## 結果

預印本報告，在無條件與拓撲受限的單體設計、蛋白質結合子設計、對稱寡聚體設計、酵素活性中心支架與對稱基序支架上，都有很好的表現。它也報告實驗表徵了數百個新設計。

## 限制

- 本頁的結果來自預印本摘要。最終數字與各任務的成功率，應參考已發表的版本。
- 模型提出設計，哪些設計有效要由實驗決定，設計品質並不保證。
- 這個設計模型以 RoseTTAFold 為基礎，因此它在結構預測上的優點與不足也會延續下來（這是推論，並非論文的主張）。

## 關聯

- [ESM-2 與 ESMFold](../esm/index.md)：從單一序列預測結構的蛋白質語言模型。
- [去噪擴散](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)：本方法所依據的通用框架。

## 參考文獻

### 開創性論文

- Watson et al. (2023). De novo design of protein structure and function with RFdiffusion. *Nature*. https://doi.org/10.1038/s41586-023-06415-8 — 已發表的 RFdiffusion 論文，介紹此方法。
- Watson et al. (2022). Broadly applicable and accurate protein design by integrating structure prediction networks and diffusion generative models. *bioRxiv*. https://doi.org/10.1101/2022.12.09.519842 — 結果段落所摘要的預印本。
- Baek et al. (2021). Accurate prediction of protein structures and interactions using a three-track neural network. *Science*. https://doi.org/10.1126/science.abj8754 — RoseTTAFold，RFdiffusion 所微調的結構預測網路。
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2，RoseTTAFold 通常拿來比較的結構預測器。
- Ho et al. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — 本方法所依據的擴散框架。
