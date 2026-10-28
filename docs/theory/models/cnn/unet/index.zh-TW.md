---
translation_reviewed: 2026-10-28
related:
  - theory/models/cnn
  - theory/paradigms/unsupervised/density-and-generative-models
  - brain-mind/neuroai
tags:
  - 卷積網路
  - 影像分割
  - 架構
aliases:
  - U-Net
  - U 型網路
  - 編碼器–解碼器卷積網路
---

# U-Net

U-Net 是一種帶有跳接連線的卷積編碼器–解碼器。它為生物醫學影像分割而設計，此領域的標註影像稀少，而每個輸出像素都需要同時具備上下文與精細的定位。它對稱的形狀，即一條捕捉上下文的收縮路徑，加上一條恢復解析度的擴張路徑，成為密集預測的預設骨幹。它也是影像擴散模型中常用的去噪器。家族概覽見[卷積網路](../index.md)頁。

## 概覽

Ronneberger、Fischer 與 Brox（2015）結合了兩個想法。卷積網路在低解析度下已能很好地捕捉上下文，而擴張路徑則透過串接來自編碼器的高解析度特徵，恢復精細的定位。搭配大量的資料擴增，此架構能以極少的標註影像訓練。它在 2015 年 ISBI 細胞追蹤挑戰賽的兩個類別中獲勝，論文並報告它在電子顯微鏡分割上優於先前的滑動視窗方法。

## 關鍵概念

- **收縮路徑**：重複的卷積對接上池化，使解析度減半、通道數加倍。
- **擴張路徑**：上卷積使解析度加倍、通道數減半。
- **跳接連線**：把編碼器的特徵圖與同一解析度的解碼器特徵圖串接，使精細細節跨越瓶頸層傳遞。
- **重疊切片策略**：以重疊的切片預測大型影像，使每個輸出像素都能看到完整的上下文視窗。
- **權重圖**：逐像素的損失權重，強調相鄰物件之間細窄的分隔邊界。

## 運作方式

網路是一個對稱的 U 形。收縮路徑的每一層套用兩次無填充的 3×3 卷積與 ReLU，接著以步幅 2 的 2×2 最大池化。在最底層，表徵具有最大的感受野與最多的通道。擴張路徑的每一層套用 2×2 上卷積，串接同一層裁切後的編碼器特徵，再套用兩次 3×3 卷積與 ReLU。最後以 1×1 卷積產生逐像素的類別分數。論文版本共有 23 個卷積層。

訓練使用帶權重圖的逐像素交叉熵。論文採用具大動量的隨機梯度下降，並以彈性形變擴增少量的訓練影像，用以模擬自然組織的變異。

## 關鍵方法

U-Net 是此處的里程碑式架構。它的變體改變維度或區塊設計；每一種變體都有待撰寫的獨立頁面。

- **U-Net（Ronneberger 等人，2015）**：上述架構，以跳接連線進行密集預測。
- **3D U-Net 與 V-Net**：相同的設計用於體積醫學影像。方法頁仍待撰寫。
- **殘差與注意力 U-Net**：在跳接路徑上加入殘差區塊或注意力閘門。方法頁仍待撰寫。

### U-Net：用於生物醫學影像分割的卷積網路（Ronneberger 等人，2015）

- **問題：** 在只有少量標註範例的情況下，對生物醫學影像做密集分割，且相鄰物件必須被精確地分開。
- **核心想法：** 對稱的編碼器–解碼器，跳接連線把高解析度特徵送到解碼器，並搭配重疊切片推論與彈性形變擴增。
- **公式或演算法：** 即上述架構。損失為逐像素交叉熵，並以權重圖提升細窄分隔邊界的權重。
- **結果：** 摘要報告網路能以極少的影像端到端訓練，並在 ISBI 電子顯微鏡神經結構分割挑戰賽上，優於先前最好的滑動視窗卷積方法。它也在 ISBI 2015 細胞追蹤挑戰賽的相位對比與 DIC 類別中獲勝，並報告在近期 GPU 上一秒內可分割 512×512 的影像。
- **限制：** 論文的設計針對二維影像，而重疊切片策略增加推論開銷。填充方式的選擇很重要，且架構的深度固定，因此非常大或非常小的輸入需要調整。

## 關聯

- U-Net 是大多數像素空間影像擴散模型的去噪器。Dhariwal 與 Nichol（2021）使用改良的 U-Net，見 [DDPM](../../../paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)；以 Transformer 取代它的是 [DiT](../../transformer/dit/index.md)，屬於 [Transformer](../../transformer/index.md) 家族。
- U 形跳接的想法與全卷積網路（Long 等人，2015）密切相關，後者用於密集預測，而 U-Net 以對稱的解碼器加以擴展。
- 編碼器–解碼器的模式也出現在 [VAE](../../../paradigms/unsupervised/density-and-generative-models/vae/index.md) 中，編碼器與解碼器在機率模型中扮演同樣的角色。
- 具跳接樣連線的階層式處理，與皮質路徑只有鬆散的類比，見 [NeuroAI](../../../../brain-mind/neuroai/index.md)。

## 應用

細胞、胞器與組織的生物醫學分割；衛星與遙測影像分割；影像擴散模型的去噪骨幹；以及深度與光流估計等密集預測任務。

## 開放問題

- 跳接連線是否為結合不同尺度的最佳方式，或注意力與 Transformer 會在大規模下取代它們。
- 在非常大量的資料上訓練後，U 形結構還有多大的重要性。
- 在記憶體有限的情況下，把此設計推廣到三維與影片資料。

## 參考文獻

### 開創性論文

- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. MICCAI（arXiv）. https://arxiv.org/abs/1505.04597 — 提出具跳接連線、重疊切片推論與加權損失的編碼器–解碼器架構。
- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR（arXiv）. https://arxiv.org/abs/1411.4038 — 證明卷積網路可以端到端訓練用於密集預測，並在不同尺度之間使用跳接連線。
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. NeurIPS（arXiv）. https://arxiv.org/abs/2006.11239 — 以帶時間步條件的 U-Net 作為影像擴散的去噪器。
- Dhariwal, P. & Nichol, A. (2021). *Diffusion Models Beat GANs on Image Synthesis*. NeurIPS（arXiv）. https://arxiv.org/abs/2105.05233 — 改良擴散模型所用的 U-Net 去噪器，並報告其在影像合成上超越 GAN。
