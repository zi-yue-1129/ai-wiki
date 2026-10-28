---
translation_reviewed: 2026-10-28
related:
- theory/paradigms/unsupervised/density-and-generative-models
- brain-mind/neuroimaging-methods
tags:
- neuroscience
- brain-computer interface
- generative models
aliases:
  - fMRI 影像重建
  - Image reconstruction from fMRI
  - Takagi and Nishimoto
---

# 從 fMRI 重建所見影像（Takagi & Nishimoto, 2023）

此方法從功能性磁振造影（fMRI）活動，重建一個人正在看的影像。它把 fMRI 的型態映射到預先訓練好的影像生成器——潛在擴散模型——的潛在空間，再由這個潛在表徵生成影像。輸出在內容與版面上都接近所看的影像，顯示生成器的表徵能與大腦活動連結。

本頁屬於[腦機介面與神經解碼](../index.md)。它詳細說明一種解碼方法。

## 概述

fMRI 量測神經活動之後的血氧變化，是非侵入式腦部影像最常用的工具。早期的研究可以判斷一個人正在看一組已知影像中的哪一張，但無法從腦活動產生新的影像。Takagi 與 Nishimoto 問的是：生成式影像模型能否作為橋梁——把腦部型態讀入生成器的潛在空間，再由生成器畫出影像。

## 核心概念

- **fMRI 型態（fMRI pattern）**：觀看時，視覺皮質中血氧訊號的空間分布，作為解碼器的輸入。
- **潛在擴散模型（latent diffusion model）**：在壓縮的潛在空間中透過去噪產生影像的生成器，使生成保持可行。
- **線性映射（linear mapping）**：從 fMRI 特徵到生成器潛在表徵的迴歸，每位受試者分別擬合。
- **文字條件（text conditioning）**：由腦部型態導出的文字或語意描述，引導生成器朝正確的內容生成。

## 問題

能否從 fMRI 復原所看影像的內容，並生成與之吻合的新影像？困難在於：fMRI 的空間與時間解析度都不高，而資料集中的影像數量，與可能影像的數量相比非常少。已經學會自然影像空間的生成器，提供了使問題可解的先驗。

## 核心想法

訓練一個映射，把受試者觀看影像時記錄的 fMRI 活動，映射到這些影像的兩種表徵：捕捉畫面內容的語意嵌入，以及捕捉版面與紋理的低階潛在表徵。測試時，映射出的表徵作為條件，輸入預先訓練好的潛在擴散模型，由它生成重建影像。生成器提供影像的統計特性，fMRI 則提供內容。

## 方法

1. 受試者觀看許多自然影像時，記錄視覺皮質的 fMRI 反應。
2. 以生成器自身的編碼器編碼每張所看的影像，得到目標的潛在與語意表徵。
3. 分別為每位受試者，擬合從 fMRI 特徵到這些表徵的迴歸。
4. 對新的 fMRI 型態預測表徵，並以之為條件，讓潛在擴散模型生成影像。

## 結果

論文報告，重建影像在內容與整體版面上接近所看的影像，並與早期的重建方法比較，後者產生的影像較模糊或較不具體。評估使用保留的測試影像，因此重建並非由訓練集中記憶而來。論文中的量化分數應以原論文為準。

## 限制

- **重建看起來合理，不代表準確。**生成器會產生逼真的影像，有些細節可能來自它的先驗，而非腦部訊號。
- **需要每人訓練。**映射分別為每位受試者擬合，且需要大量的掃描時間。
- **是所看的影像，不是想像的影像。**此方法重建的是人正在看的東西，而非思緒或夢境，也並非讀取私人的心理內容。

## 與其他主題的關聯

- **神經影像方法**：fMRI 訊號及其限制見[神經影像方法](../../neuroimaging-methods/index.md)，包括 [BOLD fMRI](../../neuroimaging-methods/bold-fmri/index.md)。
- **生成式模型**：生成器是潛在擴散模型，見[理論](../../../theory/paradigms/unsupervised/density-and-generative-models/index.md)中的密度與生成式模型部分。
- **母主題**：[腦機介面與神經解碼](../index.md)，其中涵蓋侵入式解碼與解碼的倫理。

## 應用

- **基礎研究**：重建顯示視覺皮質中存在哪些關於所看影像的資訊。
- **臨床溝通**：知覺解碼被研究作為無法說話或活動的人的可能輔助，但目前仍處於研究階段。

## 開放問題

- **輸出有多少來自生成器的先驗？**區分腦部訊號貢獻了什麼，與生成器加入了什麼，是核心的效度問題。
- **此方法能否用於想像，以及大腦結構不同的人？**超出觀看與掃描受試者的推廣尚未確立。
- **隱私的界線在哪裡？**解碼知覺引發了關於同意以及解碼系統能揭露什麼的問題，這些在母主題中討論。

## 參考文獻

### 開創性論文

- Takagi, Y. & Nishimoto, S.（2023）。High-resolution image reconstruction with latent diffusion models from human brain activity. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*。https://doi.org/10.1109/CVPR52729.2023.01389 — 把 fMRI 活動映射到擴散模型的潛在空間，生成所看影像的重建。
- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B.（2022）。High-Resolution Image Synthesis with Latent Diffusion Models. *CVPR*。https://arxiv.org/abs/2112.10752 — 本方法所用的生成器，即潛在擴散模型。
- Kay, K. N., Naselaris, T., Prenger, R. J. & Gallant, J. L.（2008）。Identifying natural images from human brain activity. *Nature*。https://doi.org/10.1038/nature06713 — 從 fMRI 判斷一個人正在看哪一張自然影像，是邁向重建的早期一步。
- Nishimoto, S., Vu, A. T., Naselaris, T., Benjamini, Y., Yu, B. & Gallant, J. L.（2011）。Reconstructing visual experiences from brain activity evoked by natural movies. *Current Biology*。https://doi.org/10.1016/j.cub.2011.08.031 — 以學習得來的編碼模型，從 fMRI 重建自然影片。

### 綜述與回顧

- Naselaris, T., Kay, K. N., Nishimoto, S. & Gallant, J. L.（2011）。Encoding and decoding in fMRI. *NeuroImage*。https://doi.org/10.1016/j.neuroimage.2010.05.051 — 回顧這些重建方法所用的編碼與解碼框架。
