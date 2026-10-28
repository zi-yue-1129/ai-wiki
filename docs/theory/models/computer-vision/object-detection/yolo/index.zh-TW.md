---
translation_reviewed: 2026-10-28
---

# YOLO

YOLO（You Only Look Once）是一種單階段物件偵測器，把偵測表述為單一回歸問題。一個卷積網路只看整張影像一次，就同時預測邊界框、它們的信心值與類別機率。由於沒有獨立的提議階段，系統能即時執行。它是 [物件偵測](../index.md) 頁所列的方法之一。

## 概述

早期的偵測器把任務拆成數個部分來建構。滑動視窗系統以分類器為許多裁切區域評分，R-CNN 家族則在另一個方法產生的提議上執行分類器。YOLO 論文主張，先前的工作是把分類器挪用來做偵測。它的替代做法是一個單一網路，直接把像素映射為邊界框與類別機率，並且可以針對偵測表現進行端到端的最佳化。[^1] 在論文的基準上，基礎模型每秒可處理 45 幀影像，Fast YOLO 則可達每秒 155 幀；代價是小物件與精確定位的準確率較低。

## 關鍵概念

- **格子（grid）。** 影像被切分為 S×S 的格子，論文中 S = 7。包含某個物件中心的格子，負責偵測該物件。
- **邊界框與信心值。** 每個格子預測 B = 2 個框。每個框有相對於格子的中心、相對於整張影像的寬與高，以及一個信心值：物件存在的機率乘以預測框與真實框的 IoU。
- **類別機率。** 每個格子預測一組條件類別機率，對應 C = 20 個 PASCAL VOC 類別，由它的兩個框共用。
- **輸出張量。** S × S × (B·5 + C)，在 VOC 上即 7 × 7 × 30。

## 運作方式

網路包含 24 個卷積層，設計靈感來自 GoogLeNet 分類器，後接全連接層。訓練時，最佳化的是整個格子上的單一平方和誤差：

$$
\begin{aligned}
\mathcal{L} = &\; \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{obj}}_{ij} \left[(x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2\right] \\
&+ \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{obj}}_{ij} \left[(\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2\right] \\
&+ \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{obj}}_{ij} (C_i - \hat{C}_i)^2 + \lambda_{\text{noobj}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{noobj}}_{ij} (C_i - \hat{C}_i)^2 \\
&+ \sum_{i=0}^{S^2} \mathbb{1}^{\text{obj}}_{i} \sum_{c \in \text{classes}} (p_i(c) - \hat{p}_i(c))^2
\end{aligned}
$$

此處 \(\mathbb{1}^{\text{obj}}_{ij}\) 在格子 \(i\) 的第 \(j\) 個框負責某個物件時為 1，\(\mathbb{1}^{\text{noobj}}_{ij}\) 則是其互補。權重為 \(\lambda_{\text{coord}} = 5\) 與 \(\lambda_{\text{noobj}} = 0.5\)。大小項中的平方根會降低大框誤差的懲罰，使同樣的誤差對小框影響更大。\(\lambda_{\text{noobj}}\) 權重則避免大量空格子壓過信心值項。[^2]

測試時，每個框的類別特定分數，是它的類別機率乘以框的信心值。接著以非極大值抑制移除重複偵測，論文報告這使 mAP 增加 2–3%。[^2]

## 結果

在 PASCAL VOC 2007 上，以 2007 與 2012 的 trainval 集訓練，YOLO 達到 63.4% 的 mAP，速度為每秒 45 幀；Fast YOLO 達到 52.7%，速度為每秒 155 幀。論文的比較表把這些數字與其他偵測器並列。[^3]

| 偵測器（VOC 2007 測試集） | mAP | 速度 |
|---|---|---|
| 30Hz DPM | 26.1 | 30 fps |
| Fast YOLO | 52.7 | 155 fps |
| YOLO | 63.4 | 45 fps |
| Fast R-CNN | 70.0 | 0.5 fps |
| Faster R-CNN，VGG-16 | 73.2 | 7 fps |

在 VOC 2012 測試集上，YOLO 達到 57.9% 的 mAP，略低於論文表中 VGG-16 版的 R-CNN 的 59.2%。[^3]

誤差分析是論文中最清楚的結果之一。YOLO 的定位錯誤比 Fast R-CNN 多，但背景誤判（即在不含物件的區域做出偵測）少得多。用 YOLO 為 Fast R-CNN 的偵測重新評分，可使 mAP 從 71.8% 提高到 75.0%。在自然影像上訓練的 YOLO，在 Picasso 與 People-Art 資料集的藝術作品上，泛化能力也優於 DPM 與 R-CNN。[^1]

## 限制

- **定位。** YOLO 的錯誤大多來自定位，而非分類。[^3]
- **空間限制。** 每個格子只預測兩個框與一組類別機率，因此小物件或緊密排列的物件很難偵測。[^1]
- **小物件。** 論文在 VOC 2012 上指出，與最接近的競爭者相比，YOLO 對小物件有困難。[^3]

## 開放問題

- **第一版之後的設計。** 第二版 YOLO9000 改良了模型，也從分類資料中學習。後來的 YOLOv4 與 YOLOX 論文重新檢視了架構與訓練配方。原始論文並未處理這些變化。[^4]
- **速度與準確率。** 單次計算的模型能否在小物件上達到雙階段偵測器的準確率，同時又不犧牲速度，是這個家族的主要問題。

## 關聯

- **泛化。** 藝術作品實驗問的是：在自然照片上訓練的偵測器，面對統計特性不同的影像是否仍然有效。[Geirhos 等人（2019）](../../../../../brain-mind/visual-perception/geirhos-2019/index.md) 提出了同類的問題，比較人類與 CNN 如何權衡形狀與紋理。
- **與雙階段的對照。** 格子取代了 [Faster R-CNN](../faster-rcnn/index.md) 的提議步驟；後者同樣使用 CNN 骨幹網路，但在分類之前多了一個學習而來的提議階段。

## 應用

當系統必須對移動中的場景做出反應時，即時偵測就十分重要：例如[自動駕駛](../../../../../applications/autonomous-driving/index.md)中的交通與行人監測、視訊監控，以及必須在移動時追蹤物件的機器人。

## 參考文獻

### 開創性論文

- Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2015). *You Only Look Once: Unified, Real-Time Object Detection*. arXiv. https://arxiv.org/abs/1506.02640 — YOLO 原始論文，把偵測表述為格子上的單次回歸，並報告 VOC 2007 與 2012 的結果。
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — 論文用來比較速度與準確率的雙階段偵測器。
- Liu, W., et al. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — 同期的單階段偵測器，從多個特徵圖以預設框進行預測。
- Redmon, J. & Farhadi, A. (2016). *YOLO9000: Better, Faster, Stronger*. arXiv. https://arxiv.org/abs/1612.08242 — YOLO 的第二版，對設計做了改良，並以偵測與分類資料進行聯合訓練。

### 綜述與教科書

- Zou, Z., et al. (2019). *Object Detection in 20 Years: A Survey*. arXiv. https://arxiv.org/abs/1905.05055 — 將單階段與雙階段家族放在偵測歷史脈絡中的綜述。

### 文章與文件

- Bochkovskiy, A., Wang, C.-Y. & Liao, H.-Y. M. (2020). *YOLOv4: Optimal Speed and Accuracy of Object Detection*. arXiv. https://arxiv.org/abs/2004.10934 — 將許多已發表的 CNN 技術組合成一個在單一 GPU 上兼顧速度與準確率的 YOLO 偵測器。
- Ge, Z., Liu, S., Wang, F., Li, Z. & Sun, J. (2021). *YOLOX: Exceeding YOLO Series in 2021*. arXiv. https://arxiv.org/abs/2107.08430 — 把 YOLO 設計改為無錨框形式，並搭配解耦頭與新的標籤指派策略。

[^1]: Redmon et al. (2015)，摘要：偵測器是一個可端到端最佳化的單一網路，其從自然影像到藝術作品的泛化能力與 DPM 和 R-CNN 相比。
[^2]: Redmon et al. (2015)，第 2 節：格子、信心值的定義，以及 λ_coord = 5 與 λ_noobj = 0.5 的平方和損失。關於 NMS 的說明也在同一節。
[^3]: Redmon et al. (2015)，表 1 與表 3 以及第 4 節：VOC 2007 與 2012 的結果、速度比較與誤差分析。Faster R-CNN 與 Fast R-CNN 的數字是該論文所列的數值。
[^4]: Redmon and Farhadi (2016)，摘要；Bochkovskiy et al. (2020)，摘要；Ge et al. (2021)，摘要。
