---
translation_reviewed: 2026-10-28
---

# 無分類器引導

無分類器引導讓條件式擴散模型更貼近其條件（例如文字提示），代價是多樣性降低。它不需要另外的分類器：同一個網路同時以有條件與無條件的方式訓練，取樣時再把兩種預測結合。它是文字生成影像擴散模型的標準條件控制方法。家族層級的全貌見[擴散模型](index.md)頁。

## 概述

Dhariwal 與 Nichol（2021）指出，用另外訓練的分類器的梯度來引導擴散模型，可以提升樣本品質，稱為分類器引導。它需要一個在含雜訊影像上訓練的額外分類器，是個麻煩的額外元件。Ho 與 Salimans（2022）去掉了分類器：讓擴散模型本身同時學會有條件與無條件的預測。

## 核心概念

- **有條件模型** \(\epsilon_\theta(x_t, t, c)\)：在給定條件 \(c\) 下預測雜訊。
- **無條件模型** \(\epsilon_\theta(x_t, t)\)：同一個網路，但條件被換成空的 token。
- **引導權重** \(w\)：取樣時條件被強調的程度。\(w = 0\) 即一般的有條件模型，數值越大越貼近提示，但多樣性越低。
- **條件丟棄**：訓練時，條件以機率 \(p_{\text{uncond}}\) 被換成空的 token。

## 運作方式

每個取樣步驟會執行兩次網路，並以下式結合預測：

\[
\tilde\epsilon = (1+w)\,\epsilon_\theta(x_t, t, c) - w\,\epsilon_\theta(x_t, t)
\]

等價地，\(\tilde\epsilon = \epsilon_\theta(x_t,t) + (1+w)\big(\epsilon_\theta(x_t,t,c) - \epsilon_\theta(x_t,t)\big)\)，可見每一步是從無條件預測朝有條件預測移動。當 \(w = 0\) 時就是一般的有條件模型。\(w\) 越大，樣本就沿著條件所增加的方向推得越遠。每步的成本因此加倍，因為需要兩次網路評估。

## 關鍵方法

### Classifier-Free Diffusion Guidance（Ho & Salimans，2022）

- **問題：** 分類器引導以多樣性換取品質，但需要在含雜訊影像上另外訓練分類器，成本高且麻煩。
- **核心想法：** 訓練一個隨機丟棄條件的擴散模型，取樣時把它的有條件與無條件預測結合。
- **公式或演算法：** 上述結合規則，引導權重 \(w\) 在取樣時選擇。
- **結果：** 在 ImageNet 64×64、\(p_{\text{uncond}} = 0.1\) 下（論文表 1），無引導模型的 FID 為 1.80、IS 為 53.71。\(w = 0.1\) 時 FID 為 1.55、IS 為 66.11。\(w = 1.0\) 時 FID 升至 12.6，IS 達 170.1；\(w = 4.0\) 時 FID 為 26.22、IS 為 260.2。在 ImageNet 128×128、256 個取樣步（表 2）中，\(w = 0.3\) 的 FID 為 2.43，無引導為 7.27；論文指出這優於 FID 為 2.97 的 ADM-G。論文未報告 CIFAR-10 結果。
- **限制：** 每步成本加倍，且在大的 \(w\) 下 FID 急遽上升（64×64 上 \(w = 4.0\) 時為 26.22），這反映了多樣性的損失。論文測試了 10%、20% 與 50% 的條件丟棄率：10% 與 20% 表現相近，50% 則一致較差。

## 關聯

- 條件通常由[潛在擴散](latent-diffusion.md)中描述的交叉注意力路徑編碼。
- 去噪器常是 [DiT](../../../../models/transformer/dit/index.md) 或 U-Net；引導與骨幹無關。
- [DDIM](ddim.md) 的較快取樣器可以與引導結合。

## 開放問題

- 引導權重應如何沿取樣軌跡變化？
- 能否讓引導比每步兩次網路評估更便宜？

## 參考文獻

### 開創性論文

- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — 以混合有條件與無條件預測的方式引入不需外部分類器的引導。短版本曾發表於 NeurIPS 2021 深度生成模型與下游應用研討會。
- Dhariwal, P. & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. NeurIPS. https://arxiv.org/abs/2105.05233 — 提出分類器引導，無分類器引導即取代了它。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 引導所套用的基礎擴散模型。

### 綜述與教科書

- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 在統一的設計框架中討論引導與取樣選擇。
- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 說明條件取樣如何引導分數函數，是無分類器引導的理論背景。

## 延伸學習

- Rogge, N. & Rasul, K.，*The Annotated Diffusion Model*。Hugging Face 部落格。https://huggingface.co/blog/annotated-diffusion — 導讀擴散取樣的流程，其中可以加入引導步驟。
