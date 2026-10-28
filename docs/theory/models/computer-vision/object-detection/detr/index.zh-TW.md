---
translation_reviewed: 2026-10-28
---

# DETR

DETR（DEtection TRansformer）把物件偵測視為直接的集合預測。CNN 先擷取影像特徵，再由 Transformer 編碼器與解碼器，在單次前向計算中把這些特徵轉換為一組固定數量的預測，每個學習而來的物件查詢對應一個預測。訓練時，預測與真實物件以二分匹配（bipartite matching）進行一對一配對，因此不需要錨框，也不需要非極大值抑制（NMS）。它是 [物件偵測](../index.md) 頁所列的方法之一。

## 概述

多數偵測器會以人工設計的組件編碼任務的先驗知識：錨框、提議規則，以及用來移除重複項的 NMS 門檻。DETR 論文主張，基於集合的損失函數能讓其中許多組件變得不必要。它的兩個主要組成部分，一是透過二分匹配強制產生唯一預測的全域損失；二是 Transformer 編碼器與解碼器，用以推理物件之間的關係，以及整張影像的脈絡。[^1]

論文報告，DETR 在 COCO 上的準確率與速度可與調校良好的 Faster R-CNN 相當，並且同一框架可以延伸到全景分割。[^1] 論文報告的主要成本是訓練時間，因為排程很長。

## 關鍵概念

- **集合預測（set prediction）。** 模型輸出一個無序的 N 個預測的集合，N 選擇遠高於影像中典型物件數量的值。沒有物件的槽位帶有「無物件」類別。
- **物件查詢（object queries）。** 一組固定的 N 個學習而來的嵌入向量。解碼器把每個查詢轉換為一個預測，因此每個輸出槽位都與自己的查詢綁定。主要模型使用 100 個查詢。
- **二分匹配（bipartite matching）。** 預測與真實物件之間總成本最低的一對一指派，以匈牙利演算法計算。
- **框損失（box loss）。** 對框座標的廣義 IoU 損失與 L1 損失的組合，權重分別為 2 與 5。[^2]

## 運作方式

CNN 骨幹網路產生特徵圖。一個 1×1 卷積把通道數降為寬度 256，特徵圖再攤平為序列，並加上位置編碼。編碼器對此序列套用自注意力，使每個位置都能看見整張影像。解碼器讓 N 個物件查詢經過自注意力，並對編碼器輸出進行交叉注意力。一個小型前饋網路把每個查詢的嵌入向量轉換為類別機率向量（包含「無物件」），以及一個正規化的框。

訓練時，首先透過最小化總匹配成本，找出最佳指派：

$$
\hat{\sigma} = \arg\min_{\sigma} \sum_{i=1}^{N} \mathcal{L}_{\text{match}}\big(y_i, \hat{y}_{\sigma(i)}\big)
$$

此處 \(y_i = (c_i, b_i)\) 是一個真實物件，\(\hat{y}_{\sigma(i)}\) 是指派給它的預測。匹配成本獎勵對真實類別的高機率與接近的框。接著在匹配後的配對上計算損失：

$$
\mathcal{L}_{\text{Hungarian}}(y, \hat{y}) = \sum_{i=1}^{N} \Big[-\log \hat{p}_{\hat{\sigma}(i)}(c_i) + \mathbb{1}_{\{c_i \neq \varnothing\}}\, \mathcal{L}_{\text{box}}\big(b_i, \hat{b}_{\hat{\sigma}(i)}\big)\Big]
$$

此處 \(\mathcal{L}_{\text{box}}\) 是廣義 IoU 項與 L1 項的加權和。匹配到「無物件」的預測只對分類項有貢獻。由於每個物件恰好只有一個預測，損失會抑制重複。論文指出，解碼器的自注意力讓查詢之間能夠彼此溝通，這正是消除重複預測的原因。[^3]

基準模型訓練 300 個週期，在 16 張 V100 GPU 上約需三天。與其他 Transformer 一樣，DETR 使用 Adam 與 dropout，不像 Faster R-CNN 使用 SGD。[^4]

## 結果

在 COCO 驗證集上，ResNet-50 版的 DETR 達到 42.0 AP，速度為每秒 28 幀，參數量為 4,100 萬。帶有 FPN 骨幹網路的 Faster R-CNN 在標準排程下達到 40.2 AP，速度為每秒 26 幀；若使用比較時採用的強化訓練，則達到 42.0 AP。ResNet-101 版的 DETR 達到 43.5 AP。[^5]

結果因物件大小而異。DETR 的 APS 為 20.5，帶有 FPN 的 Faster R-CNN 為 24.2；而 DETR 的 APL 為 61.1，Faster R-CNN 為 52.0。[^5] 移除編碼器會使整體 AP 下降 3.9 點，其中大物件下降最多。解碼器各層之間的 AP 則提高了 8.2 點。[^6]

## 限制

- **小物件。** 論文指出，DETR 在小物件上的準確率低於 Faster R-CNN，並期待未來工作加以改進。[^5]
- **訓練成本。** 作為比較的排程訓練 500 個週期，相較於較短的排程，增加了 1.5 AP。[^4]
- **容量固定。** N 事先設定，因此一張影像最多只能包含 N 個物件。
- **注意力成本。** 對影像特徵做完整注意力，其成本隨解析度迅速增加。Deformable DETR 把 DETR 的空間解析度受限歸因於此成本。[^7]

## 開放問題

- **收斂。** Deformable DETR 以只關注少數取樣點的注意力取代密集注意力。它報告，在訓練週期減少為十分之一的情況下，準確率仍優於 DETR，尤其是在小物件上。[^7]
- **小物件。** 集合預測偵測器在沒有多尺度設計的情況下，能否在小物件上追上卷積偵測器，仍是開放的問題。
- **匹配與重複。** 二分匹配免除了 NMS 的需要，但它對訓練穩定性與擁擠場景的影響，需要比論文提供的更多研究。

## 關聯

- **Transformer。** DETR 把 [Transformer](../../../transformer/index.md) 應用於偵測，使用的注意力機制與 [Attention Is All You Need](../../../transformer/attention-is-all-you-need/index.md) 相同。
- **注意力與競爭。** 物件查詢之間的互動，使一個查詢能夠抑制另一個查詢的重複，這是候選物件之間一種學習而來的競爭。它與 [大腦與機器中的注意力](../../../../../brain-mind/attention-brain-machine/index.md) 中視覺注意力的有偏競爭理論有鬆散的相似之處。這種類比停留在組織方式的層次，並不是共同機制的證據。
- **與雙階段的對照。** [Faster R-CNN](../faster-rcnn/index.md) 使用學習而來的提議階段與 NMS，而 DETR 兩者都移除了。

## 應用

論文在 COCO 物件偵測上評估 DETR，並顯示同一框架可以延伸到全景分割。[^1]

## 參考文獻

### 開創性論文

- Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A. & Zagoruyko, S. (2020). *End-to-End Object Detection with Transformers*. arXiv. https://arxiv.org/abs/2005.12872 — 提出 DETR，以 Transformer 的固定預測集合與二分匹配，取代錨框與 NMS。
- Zhu, X., et al. (2020). *Deformable DETR: Deformable Transformers for End-to-End Object Detection*. arXiv. https://arxiv.org/abs/2010.04159 — 以只關注少數取樣點的注意力取代密集注意力，加快收斂並有助於小物件。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — Transformer 架構，DETR 用其編碼器與解碼器進行偵測。
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — DETR 的準確率與速度所比較的雙階段偵測器，DETR 移除了它的錨框與 NMS。
- Lin, T.-Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — DETR 的結果所據以報告的 COCO 資料集與 AP 指標。

### 綜述與教科書

- Zou, Z., et al. (2019). *Object Detection in 20 Years: A Survey*. arXiv. https://arxiv.org/abs/1905.05055 — 偵測方法的綜述，包括 DETR 所取代的人工設計組件。

[^1]: Carion et al. (2020)，摘要與引言：以二分匹配為基礎的集合損失與 Transformer 編碼器—解碼器；在 COCO 上的準確率與速度可與 Faster R-CNN 相當；以及延伸到全景分割。
[^2]: Carion et al. (2020)，第 3 節與附錄中的訓練細節：框損失結合廣義 IoU 項與 L1 項，權重為 λ_iou = 2 與 λ_L1 = 5。
[^3]: Carion et al. (2020)，第 4.2 節：解碼器的自注意力減少了重複預測，消融實驗顯示移除它的影響。
[^4]: Carion et al. (2020)，第 4 節：300 個週期的基準模型在 16 張 V100 GPU 上訓練三天、500 個週期的比較排程，以及第 4.1 節中與 Faster R-CNN 的優化器比較。
[^5]: Carion et al. (2020)，表 1：Faster R-CNN 與 DETR 在 ResNet-50 與 ResNet-101 骨幹網路下，於 COCO 驗證集上的 AP、APS、APL、GFLOPS 與 FPS。
[^6]: Carion et al. (2020)，表 2 與第 4.2 節：依編碼器層數區分的 AP（0 層為 36.7，12 層為 41.6），以及解碼器各層之間的 AP 增益。
[^7]: Zhu et al. (2020)，摘要：Deformable DETR 優於 DETR，尤其在小物件上，且訓練週期減少為十分之一。
