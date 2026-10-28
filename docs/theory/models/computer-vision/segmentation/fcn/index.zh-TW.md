---
translation_reviewed: 2026-10-28
---

# 全卷積網路

全卷積網路（FCN）把影像分類器轉換為逐像素的標記器。它移除全連接層，使網路能接受任意大小的影像，並輸出一個分數網格；再由學習式的上採樣層把這個網格還原為完整解析度。它使深度網路的端到端語意分割成為標準做法。它是[圖像分割](../index.md)頁所列的四種代表性方法之一。

## 概述

在這項工作之前，許多深度分割系統是逐一對影像區塊進行分類，對於彼此重疊的區塊而言，這重複了大量計算。Long、Shelhamer 與 Darrell 觀察到，只由卷積、池化與激活層組成的網路，可以對整張影像只執行一次。它的輸出因而是一張類別分數的空間圖，而非單一標籤。他們把多個同時期的分類網路改造成這種形式，並以分割資料進行微調。[^1]

## 關鍵概念

- **卷積化**：以作用於最終特徵圖的卷積取代分類器的全連接層。同一組學習到的權重，於是在每個位置都扮演分類器的角色。
- **步幅**：池化會降低解析度。在主要網路中，輸出的步幅為 32，因此原始預測在每個方向上都比影像小 32 倍。
- **學習式上採樣**：一種向後的步幅卷積，常被稱為反卷積。它以雙線性插值初始化，再依像素損失學習。
- **跳接架構**：來自較早、較細層的預測，被加到上採樣後的粗預測上，使邊緣得以還原。

## 運作方式

流程始於一個分類網路，其各層全部為卷積層。最後一層產生粗略的圖。FCN-32s 模型直接把這張圖上採樣到影像大小。FCN-16s 則先把粗圖放大一倍，並加上步幅為 16 的某一層之預測；FCN-8s 以步幅為 8 的層重複這個步驟。每個融合後的圖最後都會上採樣到輸入大小。

訓練會最小化逐像素的多項式邏輯斯損失，並對有標註的像素求和：

$$
\mathcal{L} = -\sum_{x \in \Omega} \log p_{\ell(x)}(x)
$$

這裡 \(\Omega\) 是有標註像素的集合，\(\ell(x)\) 是像素 \(x\) 的真實類別，\(p_k(x)\) 是該像素上類別 \(k\) 的 softmax 機率。被標記為模糊的像素會被忽略。

## 結果

論文以 PASCAL VOC 分割基準進行評估，指標為平均交集（mean IU）。在 VOC 2011 驗證集的一個子集上，各變體的結果為：

| 變體 | 平均 IU |
|---|---|
| FCN-32s，僅微調最後一層 | 45.4 |
| FCN-32s | 59.4 |
| FCN-16s | 62.4 |
| FCN-8s | 62.7 |

摘要報告在 PASCAL VOC 2012 測試集上達到 62.2% 的平均 IU，相對提升 20%，並指出對一張典型影像的推論約需三分之一秒。[^2] 同一網路也在 NYUDv2 與 SIFT Flow 上進行了評估。

## 限制

- **粗糙的輸出。** 即使有跳接融合，預測仍在粗糙的網格上產生，這限制了細長結構的細節。作者指出，融合步幅為 8 的層之後，收益已逐漸遞減。
- **沒有實例。** 損失以類別標記像素，因此兩個相鄰的同類物件會合併為一個區域。[Mask R-CNN](../mask-rcnn/index.md) 處理了這個問題。
- **有限的上下文。** 固定的感受野限制了每個預測能看到的全域上下文。金字塔池化網路 PSPNet 即為聚合全域上下文而提出。[^3]
- **訓練成本。** 論文指出，在一張 GPU 上微調 FCN-32s 需要三天，升級為 FCN-16s 與 FCN-8s 各約需一天。

## 開放問題

- 能否在不設置獨立跳接路徑的情況下，同時保留精細細節與寬廣的上下文？擴張卷積、金字塔池化與編碼器—解碼器設計以不同方式回應此問題。
- 增益有多少來自架構，又有多少來自在分類資料上的預訓練？論文的結果取決於該初始化。

[^1]: Long 等人（2015）摘要：數個分類網路被改造為全卷積網路，並為分割任務進行微調。
[^2]: Long 等人（2015）摘要與論文的表 2。VOC 2011 子集的數字取自論文的驗證分割，而非測試伺服器。
[^3]: Zhao 等人（2017）摘要：金字塔池化模組聚合來自不同區域的上下文，以改善場景解析。

## 參考文獻

### 開創性論文

- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR. https://arxiv.org/abs/1411.4038 — 論文本身：將分類網路改造為具有跳接融合的全卷積分割器。
- Shelhamer, E., Long, J. & Darrell, T. (2017). *Fully Convolutional Networks for Semantic Segmentation*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2016.2572683 — FCN 論文的期刊版本，方法與實驗相同。
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. MICCAI. https://doi.org/10.1007/978-3-319-24574-4_28 — 以串接取代 FCN 跳接融合的對稱編碼器—解碼器。
- Chen, L.-C., Papandreou, G., Kokkinos, I., Murphy, K. & Yuille, A. L. (2018). *DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2017.2699184 — 以擴張卷積維持高解析度，是上採樣粗圖的另一種替代方案。
- Zhao, H., Shi, J., Qi, X., Wang, X. & Jia, J. (2017). *Pyramid Scene Parsing Network*. CVPR. https://arxiv.org/abs/1612.01105 — 加入金字塔池化模組以聚合全域上下文，用於場景解析。

- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. ICCV. https://arxiv.org/abs/1703.06870 — 在偵測器上加入遮罩分支，是本方法之後的實例層級步驟。

### 綜述與教科書

- Minaee, S., Boykov, Y., Porikli, F., Plaza, A., Kehtarnavaz, N. & Terzopoulos, D. (2021). *Image Segmentation Using Deep Learning: A Survey*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3059968 — 回顧 FCN 式的像素標記網路，以及之後的編碼器—解碼器與注意力設計。
