---
translation_reviewed: 2026-11-04
related:
  - theory/models/computer-vision/object-detection
---

# 分割一切（Segment Anything, SAM）

分割一切是一項可提示影像分割的任務、一個模型與一個資料集。Kirillov 等人（2023）訓練了一個模型，只要使用者以點、框或遮罩指出某個物件，它就回傳該物件的有效遮罩。模型以一個資料引擎建立，該引擎產生超過十億個遮罩，並且無需重新訓練即可遷移到新的影像分布。作者把它釋出，作為電腦視覺研究的基礎模型。

本頁是[影像分割](index.md)的一部分。

## 問題

本節[概述](index.md)中的方法都是針對固定的標籤集訓練的。[FCN](fcn.md) 與 [U-Net](../../cnn/unet/index.md) 學習其訓練資料的類別，[Mask R-CNN](mask-r-cnn.md) 則學習其資料集的物件類別。要加入新的物件種類，就需要新的標註遮罩。作者提出的問題是：單一模型能否依需求分割任何物件，讓使用者指出目標即可得到遮罩，而不需要類別清單。作者因此把這個問題同時視為資料問題與建模問題，並以一個資料引擎建立大型資料集。

## 核心想法

論文提出三個相互連結的部分。

- **任務。** 可提示分割：給定影像與指向某個物件的提示，回傳該物件至少一個有效遮罩。允許含糊，因此模型可能對同一提示回傳多個遮罩。
- **模型。** 由三個元件組成。影像編碼器對影像只計算一次特徵嵌入。提示編碼器嵌入點、框、遮罩或文字。輕量的遮罩解碼器結合兩者並快速預測遮罩，因此在一次影像嵌入之後，可以回應許多提示。
- **資料引擎。** 一個迴圈，其中當前模型協助標註者標註遮罩，新標註的遮罩再用來訓練下一個模型。此迴圈分為三個階段，詳見下文。

影像編碼器是以遮罩自編碼器（masked autoencoder）預訓練初始化的 Vision Transformer（ViT-H/16），並以最小改動調整為可處理高解析度輸入。由於沉重的編碼器只需對每張影像執行一次，解碼器便能對每個提示互動式地執行。

## 方程式與流程

遮罩以焦點損失（focal loss）與 Dice 損失的線性組合預測，焦點損失與 Dice 損失的比例為 20 比 1。另有一個獨立的頭預測每個遮罩的品質，即其與真實遮罩的 IoU，並以均方誤差訓練。設 $\mathcal{L}_{\text{focal}}$ 與 $\mathcal{L}_{\text{dice}}$ 為兩個遮罩損失，$\mathcal{L}_{\text{IoU}}$ 為品質項，則

$$
\mathcal{L} = 20\,\mathcal{L}_{\text{focal}} + \mathcal{L}_{\text{dice}} + \mathcal{L}_{\text{IoU}}.
$$

含糊性的處理方式是：對單一提示預測三個遮罩，作者將其描述為分別對應整個物件、部分與次部分。訓練時只有損失最低的遮罩接收梯度，因此每個輸出會專精於一個粒度層級。推論時，預測的 IoU 分數為三個遮罩排序。若給定多個提示，模型只回傳一個遮罩。

資料引擎分為三個階段。

1. **輔助人工。** 標註者在一個互動式模型的協助下標註遮罩，該模型在此階段中會重新訓練。論文報告此階段產生來自 120,000 張影像的 430 萬個遮罩。
2. **半自動。** 模型為它能分割的物件提出遮罩，標註者再補上其餘物件的遮罩。此階段新增來自 180,000 張影像的 590 萬個遮罩，總計 1,020 萬個。
3. **全自動。** 模型以規則的點網格作為提示，為所有影像產生遮罩。論文表示，最終遮罩中有 99.1% 是以此方式產生的。

最終的資料集 SA-1B 約有 1,100 萬張影像與約 11 億個遮罩。摘要把這些影像描述為已取得授權並尊重隱私。

## 結果

以下結果為論文所報告的數字。

- **零樣本單點分割。** 在 23 個未用於訓練的分割資料集上，該模型在其中 16 個上的結果高於 RITM（一個互動式分割基準），在某些資料集上的增益高達約 47 IoU。
- **物件提議。** 在 LVIS v1 上，該模型在 1,000 個提議下的平均召回率為 59.3，而以完全監督在該資料集上訓練的 ViTDet-H 為 63.0。論文報告，該模型在中型與大型物件，以及稀有與常見類別上都優於 ViTDet-H。
- **總體主張。** 摘要將其零樣本表現描述為，常常與既有完全監督的結果相當，甚至更優。

這些比較衡量的是未針對各基準微調的模型。它們並不表示每個分割任務都已被解決，論文也只報告其所選評估協定上的結果。

## 限制

作者提出以下限制。

- **細結構。** 模型可能遺漏細結構，有時還會幻覺出微小、不連通的成分。
- **大型編碼器的速度。** 使用沉重的影像編碼器時，整體表現並非即時。
- **文字提示。** 文字到遮罩的提示被視為初步實驗，作者表示它並非完全穩健。
- **語意與全景任務。** 論文指出，尚不清楚如何為語意與全景分割設計簡單的提示；這兩者標示的是每個區域，而非單一指定的物件。

此模型回傳的是物件的遮罩，而非類別標籤。要為物件命名，需要另一個辨識器，這正是[物件偵測](../object-detection/index.md)中所涵蓋的偵測與分類方法的任務。

## 關聯

- SAM 無法直接涵蓋的任務變體，即語意與全景分割，定義於[概述](index.md)頁面。
- 用來評分其遮罩的指標 IoU 與 Dice，見[分割指標](../../../evaluation/metrics/segmentation/index.md)頁面。
- 其可提示的設計，與 [Mask R-CNN](mask-r-cnn.md) 以偵測為先的做法形成對比；後者只為訓練過的類別預測遮罩。

## 參考文獻

### 開創性論文

- Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P. & Girshick, R. (2023). *Segment Anything*. ICCV, pp. 3992–4003. doi:[10.1109/ICCV51070.2023.00371](https://doi.org/10.1109/ICCV51070.2023.00371)。另見 [arXiv:2304.02643](https://arxiv.org/abs/2304.02643)。 — 提出可提示分割任務、SAM 模型與 SA-1B 資料集，並可零樣本遷移到新的影像分布。
- He, K., Chen, X., Xie, S., Li, Y., Dollár, P. & Girshick, R. (2022). *Masked Autoencoders Are Scalable Vision Learners*. CVPR, pp. 15979–15988. doi:[10.1109/CVPR52688.2022.01553](https://doi.org/10.1109/CVPR52688.2022.01553)。另見 [arXiv:2111.06377](https://arxiv.org/abs/2111.06377)。 — 遮罩自編碼器預訓練，用來初始化 SAM 的影像編碼器。
- Kirillov, A., He, K., Girshick, R., Rother, C. & Dollár, P. (2019). *Panoptic Segmentation*. CVPR, pp. 9396–9405. doi:[10.1109/CVPR.2019.00963](https://doi.org/10.1109/CVPR.2019.00963)。另見 [arXiv:1801.00868](https://arxiv.org/abs/1801.00868)。 — 定義全景分割任務，這是 SAM 論文討論中較難提示的變體之一。
- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv. https://arxiv.org/abs/2010.11929 — SAM 影像編碼器（ViT-H/16）所依據的 Vision Transformer 架構。
- Sofiiuk, K., Petrov, I. A. & Konushin, A. (2021). *Reviving Iterative Training with Mask Guidance for Interactive Segmentation*. arXiv. https://arxiv.org/abs/2102.06583 — RITM 互動式分割器，是論文單點比較中的基準。
- Li, Y., Mao, H., Girshick, R. & He, K. (2022). *Exploring Plain Vision Transformer Backbones for Object Detection*. arXiv. https://arxiv.org/abs/2203.16527 — ViTDet 偵測器，是論文在 LVIS 上完全監督的比較對象。

### 綜述與教科書

- Minaee, S., Boykov, Y., Porikli, F. et al. (2021). Image Segmentation Using Deep Learning: A Survey. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. doi:[10.1109/TPAMI.2021.3059968](https://doi.org/10.1109/TPAMI.2021.3059968)。 — 深度學習影像分割方法的綜述，適合想了解更完整脈絡的讀者。
