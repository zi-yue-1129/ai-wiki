---
translation_reviewed: 2026-10-28
---

# DiT：擴散 Transformer

DiT（Diffusion Transformer，擴散 Transformer）是一種擴散去噪器，它以作用於潛在影像圖塊的 Transformer 取代 U-Net。Peebles 與 Xie（2022）指出，它的品質隨運算量穩定提升，與語言模型的情況相同。家族層級的全貌見[擴散模型](../../../paradigms/unsupervised/density-and-generative-models/diffusion/index.md)頁，注意力機制見[Transformer 與注意力](../index.md)。

## 概述

早期的潛在擴散模型使用卷積 U-Net 作為去噪器，其設計（例如跳接與多解析度區塊）是人工設計的。Peebles 與 Xie 想知道：一個具備語言與視覺中有效設計的普通 Transformer，能否作為去噪器並且可預測地擴展？答案是肯定的，但基準是類別條件的影像生成。

## 核心概念

- **圖塊化**：大小為 \(I \times I \times C\) 的潛在表示被切成 \(p \times p\) 的圖塊，每個圖塊線性嵌入為一個 token。\(p\) 越小，token 越多，運算量越大。
- **自適應層正規化（adaLN）**：時間步與類別嵌入產生縮放與平移參數，用來調節每個 Transformer 區塊。
- **Gflops**：前向傳播的運算量，比較模型大小時作為橫軸。
- **模型變體**：命名的規格，例如 DiT-S、DiT-B、DiT-L、DiT-XL，再加上圖塊大小，例如 DiT-XL/2。

## 運作方式

對於時間步 \(t\) 的潛在表示 \(z_t\) 與類別標籤 \(c\)，模型從圖塊 token 預測雜訊（某些設定下也預測變異數）：

\[
\epsilon_\theta(z_t, t, c) = \mathrm{DiT}\big(\mathrm{patchify}(z_t);\ \mathrm{emb}(t) + \mathrm{emb}(c)\big)
\]

訓練使用與 [DDPM](../../../paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md) 相同的雜訊預測損失，只是套用在潛在表示上。擴展性的研究方式是改變深度、寬度與圖塊大小（這會改變 Gflops），並在每個點測量 FID。

## 關鍵方法

### Scalable Diffusion Models with Transformers（Peebles & Xie，2022/2023）

- **問題：** U-Net 去噪器是人工設計的，而且不清楚擴散模型的品質是否像 Transformer 語言模型一樣隨運算量擴展。
- **核心想法：** 在潛在擴散中以作用於潛在圖塊的 Transformer 取代 U-Net，並以前向傳播的 Gflops 衡量品質。
- **公式或演算法：** 上述圖塊化與 adaLN 條件化，搭配潛在雜訊預測損失訓練。
- **結果：** 摘要指出，來自深度、寬度或更多 token 的 Gflops 越高，模型的 FID 就持續越低。最大的模型 DiT-XL/2 在類別條件的 ImageNet 256×256 上達到 FID 2.27，超越先前的擴散模型。摘要未給出 512×512 的 FID。
- **限制：** 結果基於類別條件的 ImageNet，比文字生成影像的基準範圍窄。摘要未提供訓練運算量數字。

## 關聯

- DiT 採用[潛在擴散](../../../paradigms/unsupervised/density-and-generative-models/diffusion/latent-diffusion.md)的潛在設定，並取代其 U-Net 去噪器。
- 注意力區塊見[Transformer 與注意力](../index.md)。
- DiT 模型可以用較快的 [DDIM](../../../paradigms/unsupervised/density-and-generative-models/diffusion/ddim.md) 更新進行取樣。

## 開放問題

- 運算量與品質的擴展關係，在文字生成影像與影片上是否在相近的成本下仍然成立？
- 圖塊大小是否為高解析度影像在細節與運算量之間取捨的最佳方式？

## 參考文獻

### 開創性論文

- Peebles, W. & Xie, S. (2023). Scalable Diffusion Models with Transformers. ICCV. https://arxiv.org/abs/2212.09748 — 提出 DiT，並報告 FID 隨 Gflops 改善。
- Rombach, R. 等人 (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — DiT 取代 U-Net 的潛在擴散設定。
- Vaswani, A. 等人 (2017). Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762 — DiT 重用為去噪器的 Transformer 架構。

### 綜述與教科書

- Song, Y. 等人 (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 提供 DiT 訓練所用雜訊預測目標的連續時間背景。
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 討論適用於 DiT 訓練的前處理與設計選擇。

### 文章與文件

- Peebles, W.，*DiT* 官方程式碼庫。https://github.com/facebookresearch/DiT — 作者的 Diffusion Transformer 模型與訓練程式參考實作。
