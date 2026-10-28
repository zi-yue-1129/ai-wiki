---
translation_reviewed: 2026-10-28
---

# 無分類器引導

無分類器引導讓條件式擴散模型更貼近其條件（例如文字提示），代價是多樣性降低。它不需要另外的分類器：同一個網路同時以有條件與無條件的方式訓練，取樣時再把兩種預測結合。它是文字生成影像擴散模型的標準條件控制方法。家族層級的全貌見[擴散模型](index.md)頁。

## 概述

Dhariwal 與 Nichol（2021）指出，用另外訓練的分類器的梯度來引導擴散模型，可以提升樣本品質，稱為分類器引導。它需要一個在含雜訊影像上訓練的額外分類器，是個麻煩的額外元件。Ho 與 Salimans（2022）去掉了分類器：讓擴散模型本身同時學會有條件與無條件的預測。

## 核心概念

- **有條件模型** \(\epsilon_\theta(x_t, t, c)\)：在給定條件 \(c\) 下預測雜訊。
- **無條件模型** \(\epsilon_\theta(x_t, t, \varnothing)\)：同一個網路，但移除條件。
- **引導比例** \(w\)：取樣時條件被強調的程度。數值越大，越貼近提示，但多樣性越低。
- **條件丟棄**：訓練時，條件以某個機率（常見約 10%）被換成空的 token。

## 運作方式

每個取樣步驟會執行兩次網路，並以下式結合預測：

\[
\tilde\epsilon = \epsilon_\theta(x_t, t, \varnothing) + w\,\big(\epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \varnothing)\big)
\]

當 \(w = 1\) 時就是一般的有條件模型。\(w\) 越大，樣本就沿著條件所增加的方向推得越遠。每步的成本因此加倍，因為需要兩次網路評估。

## 關鍵方法

### Classifier-Free Diffusion Guidance（Ho & Salimans，2022）

- **問題：** 分類器引導以多樣性換取品質，但需要在含雜訊影像上另外訓練分類器，成本高且麻煩。
- **核心想法：** 訓練一個隨機丟棄條件的擴散模型，取樣時把它的有條件與無條件分數估計混合。
- **公式或演算法：** 上述結合規則，引導比例 \(w\) 在取樣時選擇。
- **結果：** 摘要指出，引導可以由純粹的生成模型完成，不需要分類器，而且混合方法達到的品質與多樣性取捨與分類器引導相當。摘要未給出數字。
- **限制：** 每步成本加倍，且在高引導比例下多樣性下降，這兩點都仍然存在。摘要未量化任一項。

## 關聯

- 條件通常由[潛在擴散](latent-diffusion.md)中描述的交叉注意力路徑編碼。
- 去噪器常是 [DiT](../../../../models/transformer/dit/index.md) 或 U-Net；引導與骨幹無關。
- [DDIM](ddim.md) 的較快取樣器可以與引導結合。

## 開放問題

- 引導比例應如何沿取樣軌跡變化？
- 能否讓引導比每步兩次網路評估更便宜？

## 參考文獻

### 開創性論文

- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. https://arxiv.org/abs/2207.12598 — 以混合有條件與無條件預測的方式引入不需外部分類器的引導。
- Dhariwal, P. & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. NeurIPS. https://arxiv.org/abs/2105.05233 — 提出分類器引導，無分類器引導即取代了它。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 引導所套用的基礎擴散模型。

### 綜述與教科書

- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 在統一的設計框架中討論引導與取樣選擇。
- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 說明條件取樣如何引導分數函數，是無分類器引導的理論背景。

### 文章與文件

## 延伸學習

- Rogge, N. & Rasul, K.，*The Annotated Diffusion Model*。Hugging Face 部落格。https://huggingface.co/blog/annotated-diffusion — 導讀擴散取樣的流程，其中可以加入引導步驟。
