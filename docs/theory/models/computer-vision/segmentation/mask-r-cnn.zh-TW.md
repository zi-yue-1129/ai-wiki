---
translation_reviewed: 2026-11-14
related:
  - theory/models/computer-vision/object-detection
---

# Mask R-CNN

Mask R-CNN 是一個實例分割框架：它偵測影像中的每個物件，並為每個物件預測一張獨立的像素遮罩。He、Gkioxari、Dollár 與 Girshick（2017）在偵測器 Faster R-CNN 上增加第三個輸出分支，與類別與框的輸出平行預測遮罩。它成為實例分割的標準基準，並在同一框架中延伸到關鍵點估計。

本頁是[影像分割](index.md)的一部分。

## 問題

[FCN](fcn.md) 等語意分割方法以類別標記每個像素，因此兩個相鄰的同類人物會合併為同一區域。實例分割除了要勾勒輪廓，還必須把物件分開。兩階段偵測器已能把每個物件找成一個框，當時的開放問題是：如何在不付出過高成本、也不犧牲框輸出準確度的前提下，為每個偵測結果加上精確的遮罩。

## 核心想法

Mask R-CNN 保留 Faster R-CNN 的兩階段結構。區域提議網路先提出候選區域，對每個區域再擷取特徵，並預測類別與修正後的框。新增的步驟是一個小型全卷積分支，為每個感興趣區域（RoI）預測二元遮罩。遮罩分支與框分支平行執行，因此遮罩預測不會改變框的找法。論文報告，此方法只為 Faster R-CNN 增加少量負擔，並以每秒 5 幀運行。

有兩個設計選擇最為重要。

- **每類別一張二元遮罩。** 遮罩頭為每個類別輸出一張二元遮罩，損失只使用 RoI 真實類別的遮罩。每個類別有自己的 sigmoid，因此遮罩之間不像 FCN 的逐像素 softmax 那樣相互競爭。分類由獨立的類別分支負責。
- **RoIAlign。** Faster R-CNN 以 RoIPool 擷取每個 RoI 的特徵，它會把 RoI 的邊界與分格取整到特徵圖的網格上。論文主張，這種錯位會對像素級精確的遮罩產生很大的負面影響。RoIAlign 去除了取整：它在每個分格內以規則間隔取樣特徵圖，並以雙線性插值合併。

## 動態示範：取整取樣與對齊取樣

<div style="max-width:100%;overflow-x:auto" role="region" tabindex="0" aria-label="RoIAlign 與 RoIPool 取樣差異的教學圖，可水平捲動">
<div style="width:800px">
<img src="../../../../assets/concept-animations/roi-align-sampling-still.svg" data-motion-src="../../../../assets/concept-animations/roi-align-sampling-motion.svg" data-still-src="../../../../assets/concept-animations/roi-align-sampling-still.svg" width="800" height="460" alt="左右並列兩張特徵網格：橘色分數取樣位置連續移動；RoIPool 的取整位置和示意取樣值跳變，RoIAlign 依雙線性插值平滑改變。">
</div>
</div>

**觀察重點：** 橘色標記在兩張人工構造的特徵網格上連續移動。左側青綠色取樣位置在格點間跳變，使下方輸出長條突然改變；右側則以連續座標取得插值，輸出長條平滑變化。此圖刻意將 RoIPool 式座標量化簡化成**單一格點取樣**，並非完整的 RoIPool 最大池化計算。實際 RoIAlign 在每個 RoI 分格內對多個位置進行**雙線性插值**並聚合特徵。畫面是教學用的一維截面示意，並非真實影像的特徵圖或 [Mask R-CNN 論文](https://arxiv.org/abs/1703.06870)的實驗數值。

GitHub 直接顯示已檢查的**靜態回退圖**；MkDocs 則提供播放／暫停按鈕（Tab、Enter 或空白鍵），並支援減少動態效果偏好。手機可聚焦圖面區域，水平捲動以保留清楚的英文標籤。

*原創教學動畫及靜態回退圖，CC BY-SA 4.0。*

## 方程式與流程

每個取樣的 RoI 帶有多任務損失

$$
\mathcal{L} = \mathcal{L}_{\text{cls}} + \mathcal{L}_{\text{box}} + \mathcal{L}_{\text{mask}},
$$

其中 $\mathcal{L}_{\text{cls}}$ 與 $\mathcal{L}_{\text{box}}$ 與 Fast R-CNN 中的分類與框回歸損失相同。遮罩損失是在逐像素 sigmoid 之後，對真實類別 $k$ 的 $m \times m$ 遮罩取平均二元交叉熵：

$$
\mathcal{L}_{\text{mask}} = -\frac{1}{m^2}\sum_{i,j}\Big[\,y_{ij}\log \hat{y}^{k}_{ij} + (1-y_{ij})\log\big(1-\hat{y}^{k}_{ij}\big)\Big],
$$

其中 $y_{ij}$ 為真實遮罩的值，$\hat{y}^{k}_{ij}$ 為類別 $k$ 的預測機率。

單張影像的流程如下：

1. 主幹網路計算特徵圖。
2. 區域提議網路提出候選框。
3. RoIAlign 為每個提議擷取固定尺寸的特徵網格。
4. 類別與框分支預測標籤與修正後的框；遮罩分支為同一 RoI 預測每類別遮罩。
5. 推論時，保留預測類別的遮罩，並縮放到框的大小。

## 結果

以下結果為論文在 COCO 基準上報告的數字。

- **實例分割。** 以 ResNet-101 與特徵金字塔網路為主幹，論文報告在 COCO test-dev 上遮罩平均精確率（mask AP）為 35.7，AP50 為 58.0，AP75 為 37.8。
- **框偵測。** 同一模型在 test-dev 上的框 AP 為 38.2，因此遮罩分支並未降低偵測準確度。
- **RoIAlign 的效果。** 在論文以 ResNet-50 C4 為主幹的消融實驗中，遮罩 AP 從 RoIPool 的 26.9 提升到 RoIAlign 的 30.3。
- **速度。** 摘要報告，主要配置以每秒 5 幀運行。

摘要也指出，同一框架在 COCO 的框偵測與人體關鍵點偵測兩個項目中也取得頂尖結果，作者以此說明該設計不限於遮罩任務。

## 限制

- **未針對速度最佳化。** 作者表示，此設計並未針對速度最佳化，可能存在更好的速度與準確度取捨。兩階段偵測比單階段設計慢。
- **較昂貴的變體。** 論文不建議在實務上使用其 ResNet-101 C4 變體，因為每張影像約需 400 毫秒。
- **失敗案例。** 作者指出，某些類別的訓練資料稀少是主要挑戰，例如 Cityscapes 資料集中的卡車、公車與火車，並在論文圖中展示了一個失敗的預測。
- **遮罩解析度。** 遮罩以每個 RoI 固定的小解析度預測，再縮放到框的大小。因此物件的細結構與細長部位只能以粗略的方式表示。

## 關聯

- Mask R-CNN 所延伸的偵測階段，見[物件偵測](../object-detection/index.md)，其中 Faster R-CNN 是兩階段家族之一。
- 作為實例方法對照點的語意分割，即全卷積網路，見 [FCN](fcn.md) 頁面。
- 不需要偵測器的可提示分割，見 [Segment Anything](segment-anything.md) 頁面。

## 參考文獻

### 開創性論文

- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. ICCV, pp. 2980–2988. doi:[10.1109/ICCV.2017.322](https://doi.org/10.1109/ICCV.2017.322)。另見 [arXiv:1703.06870](https://arxiv.org/abs/1703.06870)。 — 在 Faster R-CNN 上加入遮罩分支，為每個 RoI 預測每類別的二元遮罩，並提出 RoIAlign。
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — Mask R-CNN 所延伸的兩階段偵測器。
- Lin, T.-Y., Maire, M., Belongie, S. et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV, pp. 740–755. doi:[10.1007/978-3-319-10602-1_48](https://doi.org/10.1007/978-3-319-10602-1_48)。另見 [arXiv:1405.0312](https://arxiv.org/abs/1405.0312)。 — 含實例遮罩的基準，論文的結果即在此報告。
- Lin, T.-Y. et al. (2017). *Feature Pyramid Networks for Object Detection*. CVPR, pp. 936–944. doi:[10.1109/CVPR.2017.106](https://doi.org/10.1109/CVPR.2017.106)。 — 論文主要 ResNet-101-FPN 配置所用的特徵金字塔。
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Deep Residual Learning for Image Recognition*. CVPR, pp. 770–778. doi:[10.1109/CVPR.2016.90](https://doi.org/10.1109/CVPR.2016.90)。 — 論文評估其主幹的殘差網路（ResNet-50 與 ResNet-101）。

### 綜述與教科書

- Minaee, S., Boykov, Y., Porikli, F. et al. (2021). Image Segmentation Using Deep Learning: A Survey. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. doi:[10.1109/TPAMI.2021.3059968](https://doi.org/10.1109/TPAMI.2021.3059968)。 — 深度學習影像分割方法的綜述，適合想了解更完整脈絡的讀者。
