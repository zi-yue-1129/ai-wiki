---
translation_reviewed: 2026-10-28
---

# 影片擴散模型

影片擴散模型透過在所有影格上同時逆轉加噪過程來生成影片片段。Ho 等人（2022）顯示，以三維 U-Net 作為去噪器的標準影像擴散公式能產生時間上連貫的影片，而同時在影像與影片上訓練則有所助益。它是[影片理解與生成](../index.md)頁所列的方法之一。

## 概述

[擴散模型](../../../../generative/diffusion/index.md)的做法用於影片時幾乎不需改動。影片片段被視為一個張量，網路學習從中去除雜訊。主要困難在於記憶體，因為每個影格都必須同時通過網路；另一是跨影格的連貫性。論文主張，對影像架構做自然的延伸，即可同時處理這兩個問題。[^1]

## 關鍵概念

- **時空 U-Net。** 一種 [U-Net](../../segmentation/unet/index.md)，其區塊包含空間層與時間注意力，注意力經過分解，使空間與時間分別處理。[^1]
- **影像與影片聯合訓練。** 把獨立的影像附加到每段影片之後，並遮罩時間注意力，使影像不與影格相互混合。作者回報，這能降低小批次梯度的變異數。[^1]
- **重建引導。** 以已知影格作為條件進行取樣，使片段得以在時間上延長，或提高解析度。

## 運作方式

前向過程加入高斯雜訊，$q(z_t \mid x) = \mathcal{N}(z_t;\,\alpha_t x,\ \sigma_t^2 I)$。網路 $\hat x_\theta(z_t)$ 負責還原乾淨的片段，訓練時在均勻抽樣的時間上使用加權的均方誤差：[^1]

$$
\mathcal{L}(\theta) = \mathbb{E}_{x,\,t}\left[\, w(\lambda_t)\,\lVert \hat x_\theta(z_t) - x\rVert_2^2 \,\right].
$$

取樣從高斯雜訊開始，逐步套用學得的去噪器，可採用祖先取樣器，或加入朗之萬步的預測—校正取樣器。

超過固定影格數的片段以自迴歸方式生成：以第一段的結尾為條件，再取樣第二段。論文發現，常用的替換方法所產生的片段與上下文不吻合，因此重建引導改為調整去噪預測，使其重建已知的影格。[^1]

## 結果

論文涵蓋無條件生成、影片預測與文字條件生成。

- **UCF-101，無條件，16 影格、64×64。** 模型達到 Fréchet Inception Distance（FID）295，以 C3D 特徵計算。[^2] 論文表中 64×64 最佳的先前結果為 3431。[^1]
- **機器人推球的影片預測。** 模型在 512 步祖先取樣下達到 Fréchet 影片距離（FVD）68.2，在 256 步朗之萬取樣下為 66.9；相比之下，兩個較早的影片模型分別為 86.9 與 103.3。FVD 以 [I3D](../i3d/index.md) 特徵計算。[^1]
- **文字條件生成。** 論文在 1,000 萬段附有字幕的影片上訓練，並首次展示此任務的結果。其證據大多是質性的。[^1]

## 限制

- **解析度。** 無條件模型以 64×64 運作，作者承認這可能使它處於劣勢。[^1]
- **長度固定，成本高。** 基礎模型生成固定數量的影格，並需要數百個取樣步驟。
- **分數敏感。** 在一個 600 類的動作基準上，以放回抽樣的方式抽取測試影片（一些早期論文採用此法），會使論文的 FVD 從 16.2 升至 16.9。[^1]

## 開放問題

- 影像的做法能否擴展到長篇、高解析度的影片？[Align your Latents](https://arxiv.org/abs/2304.08818) 與 [Stable Video Diffusion](https://arxiv.org/abs/2311.15127) 在壓縮後的潛在空間中去噪以降低成本，後者並強調資料篩選的重要性。[^3]
- 對影片而言，U-Net 還是 Transformer 是較好的去噪器？[Diffusion Transformers](https://arxiv.org/abs/2212.09748) 在影像上以作用於潛在圖塊的 Transformer 取代 U-Net，影片方面的答案仍未定。[^4]

[^1]: Ho 等人（2022）：摘要、第 2 至 4 節，以及表 1 至表 3，包括影片預測段落中的取樣說明。
[^2]: Ho 等人（2022）第 4.1 節：UCF-101 的 FID 以 C3D 特徵計算，影片預測的 FVD 以 I3D 特徵計算。
[^3]: Blattmann 等人（2023）：兩篇摘要，分別描述在潛在影像模型上加入時間層，以及對訓練階段與資料篩選的研究。
[^4]: Peebles 與 Xie（2022）：Transformer 去噪器作用於潛在圖塊。

## 參考文獻

### 開創性論文

- Ho, J., Salimans, T., Gritsenko, A., Chan, W., Norouzi, M. & Fleet, D. J. (2022). *Video Diffusion Models*. arXiv. https://arxiv.org/abs/2204.03458 — 第一個用於影片的擴散模型，採用時空 U-Net。
- Carreira, J. & Zisserman, A. (2017). *Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset*. arXiv. https://arxiv.org/abs/1705.07750 — 提出 I3D，其特徵是 FVD 的基礎。
- Tran, D., et al. (2014). *Learning Spatiotemporal Features with 3D Convolutional Networks*. arXiv. https://arxiv.org/abs/1412.0767 — C3D 網路，此處的 FID 以其特徵計算。
- Soomro, K., Zamir, A. R. & Shah, M. (2012). *UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild*. arXiv. https://arxiv.org/abs/1212.0402 — 無條件訓練所用的動作資料集。
- Heusel, M., et al. (2017). *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*. arXiv. https://arxiv.org/abs/1706.08500 — 定義 Fréchet Inception Distance。
- Unterthiner, T., et al. (2018). *Towards Accurate Generative Models of Video: A New Metric & Challenges*. arXiv. https://arxiv.org/abs/1812.01717 — 提出 Fréchet 影片距離。
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. arXiv. https://arxiv.org/abs/1505.04597 — 帶有跳躍連接的編碼器—解碼器，此處延伸到時空。
- Blattmann, A., et al. (2023). *Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models*. arXiv. https://arxiv.org/abs/2304.08818 — 為潛在影像擴散模型加入時間層。
- Blattmann, A., et al. (2023). *Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets*. arXiv. https://arxiv.org/abs/2311.15127 — 研究訓練階段與資料篩選。
- Peebles, W. & Xie, S. (2022). *Scalable Diffusion Models with Transformers*. arXiv. https://arxiv.org/abs/2212.09748 — 以作用於潛在圖塊的 Transformer 取代 U-Net 去噪器。
