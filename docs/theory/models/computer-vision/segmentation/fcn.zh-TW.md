---
translation_reviewed: 2026-11-04
related:
  - theory/models/cnn
---

# 全卷積網路（FCN）

全卷積網路（FCN）是使深度網路能實用於語意分割的方法。Long、Shelhamer 與 Darrell（2015）展示了：把分類網路的全連接層換成卷積層後，網路便能接受任意尺寸的影像，並輸出密集的類別分數地圖，從像素到像素端到端訓練。

本頁是[影像分割](index.md)的一部分。

## 問題

當時的影像分類網路，如 AlexNet、VGG 與 GoogLeNet，最後都接全連接層。這些層會固定輸入尺寸，並捨棄最終特徵的空間佈局，因此輸出是整張影像的單一標籤。語意分割則需要每個像素一個標籤。早期做法把影像小塊逐一送進分類器，速度慢，且每個像素只擁有很小的上下文視窗。

## 核心想法

作者觀察到，全連接層等同於一個核覆蓋整個輸入的卷積。把它改寫為卷積，網路就能在任意尺寸的影像上執行，並得到一個與輸入空間佈局一致的粗略類別分數網格。論文把這種形式稱為*全卷積*形式。以預先訓練的分類器為起點，再於分割資料上微調，遠比從頭訓練分割網路便宜；作者表示，考量到學習基礎分類網路所需的時間，從頭訓練並不可行。

基本版本的粗略輸出步幅為 32 個像素，因此必須上採樣。上採樣在網路內部以可學習的反卷積（反向步幅卷積）完成。最後一層的反卷積濾波器固定為雙線性插值，中間層則以雙線性上採樣初始化，之後再學習。論文還加入*跳躍*連接：較淺層、解析度較高的預測，會在最終上採樣之前與深層預測融合。由此得到三種變體：

- **FCN-32s**：只使用最後一層的預測，上採樣 32 倍。
- **FCN-16s**：最後一層的預測上採樣 2 倍，與 pool4 層的預測融合，再上採樣 16 倍。
- **FCN-8s**：以 pool3 層重複同樣的融合，再上採樣 8 倍。

融合淺層特徵，能恢復粗糙最終層所遺失的邊界細節。

## 方程式與流程

訓練最小化輸出最終層空間維度上加總的逐像素多項式邏輯斯諦損失。設 $y_{ij}\in\{1,\dots,K\}$ 為輸出位置 $(i,j)$ 的真實類別，$f_{ij}(\mathbf{x};\theta)\in\mathbb{R}^K$ 為該處的類別分數，目標函數為

$$
\mathcal{L}(\theta) = \sum_{i,j} \ell\big(f_{ij}(\mathbf{x};\theta),\, y_{ij}\big),
\qquad
\ell(\mathbf{s}, y) = -\log \frac{\exp(s_y)}{\sum_{k=1}^{K}\exp(s_k)}.
$$

真實標註中標為模糊或困難的像素，不計入加總。論文將此流程描述為把這個損失以標準反向傳播穿過整個網路，因此分割輸出與上採樣濾波器是聯合訓練的。

推論是對影像做一次前向傳播。論文摘要報告，一張典型影像的推論約需三分之一秒。

## 結果

- **PASCAL VOC 2012。** 摘要報告，在 VOC 2012 分割測試集上達到 62.2% 的平均交併比（mean IU），摘要將其描述為相對改進 20%。
- **變體比較。** 在 VOC 2011 的驗證子集上，論文表 2 報告 FCN-32s 為 59.4 mean IU、FCN-16s 為 62.4、FCN-8s 為 62.7，因此跳躍融合使 mean IU 提升約三個點。
- **其他基準。** 摘要也報告在 NYUDv2 與 SIFT Flow 上達到最先進的結果。

論文附錄指出，mean IU 並不是衡量細尺度精度的好指標，這也是後續工作同時回報邊界敏感指標的原因之一（見[分割指標](../../../evaluation/metrics/segmentation/index.md)）。

## 限制

- **邊界粗糙。** 作者指出，最終預測層 32 像素的步幅限制了輸出的細節尺度。跳躍融合減輕但未消除這個問題。
- **無法區分實例。** 每個像素只獲得一個類別，因此同類的兩個物件會合併為一個區域。[Mask R-CNN](mask-r-cnn.md)等實例方法處理了這個問題。
- **固定尺度的上下文。** 網路的感受野由架構固定，因此非常大或非常小的結構難以被一致地標註。
- **依賴預訓練。** 論文依賴在 ImageNet 上預訓練的分類器微調。在作者的設定中，僅以分割資料從頭訓練同一架構並不可行。

之後的編碼器—解碼器設計，例如 [U-Net](../../cnn/unet/index.md)，使用對稱的解碼器與跳躍連接來恢復更細的細節。FCN 論文提出了這些設計所依據的密集預測全卷積觀點。

## 關聯

- FCN 所改編的分類網路，見[卷積神經網路](../../cnn/index.md)一節。
- FCN 之後的編碼器—解碼器家族，見 [U-Net](../../cnn/unet/index.md) 頁面。
- 在[概述](index.md)所比較的分割方法中，FCN 是從分類器通往密集地圖最簡單的路徑。

## 參考文獻

### 開創性論文

- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR, pp. 3431–3440. doi:[10.1109/CVPR.2015.7298965](https://doi.org/10.1109/CVPR.2015.7298965)。另見 [arXiv:1411.4038](https://arxiv.org/abs/1411.4038)。 — 以可學習的上採樣與跳躍融合，把分類網路轉換為全卷積網路，並端到端訓練以做密集預測。
- Shelhamer, E., Long, J. & Darrell, T. (2017). *Fully Convolutional Networks for Semantic Segmentation*. IEEE Transactions on Pattern Analysis and Machine Intelligence, pp. 640–651. doi:[10.1109/TPAMI.2016.2572683](https://doi.org/10.1109/TPAMI.2016.2572683)。 — 同一工作的期刊版本，前述會議論文為其首次發表。
- Simonyan, K. & Zisserman, A. (2014). *Very Deep Convolutional Networks for Large-Scale Image Recognition*. arXiv. https://arxiv.org/abs/1409.1556 — VGG 分類網路。FCN 論文轉換的三個網路（另外兩個是 AlexNet 與 GoogLeNet）之一。
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. Lecture Notes in Computer Science, pp. 234–241. doi:[10.1007/978-3-319-24574-4_28](https://doi.org/10.1007/978-3-319-24574-4_28)。另見 [arXiv:1505.04597](https://arxiv.org/abs/1505.04597)。 — 帶跳躍連接的編碼器—解碼器，承襲全卷積的做法，見 U-Net 頁面。

### 綜述與教科書

- Minaee, S., Boykov, Y., Porikli, F. et al. (2021). Image Segmentation Using Deep Learning: A Survey. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. doi:[10.1109/TPAMI.2021.3059968](https://doi.org/10.1109/TPAMI.2021.3059968)。 — 深度學習影像分割方法的綜述，適合想了解更完整脈絡的讀者。
