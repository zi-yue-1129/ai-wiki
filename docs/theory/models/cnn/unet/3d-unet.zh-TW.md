---
translation_reviewed: 2026-11-16
---

# 三維 U-Net

3D U-Net 是 [U-Net](index.zh-TW.md) 的版本，直接以三維運算分割體積影像，取代二維運算。它的設計目的是從稀疏標註學習：使用者標註少數切片，網路便產生稠密的三維分割。Çiçek 等人（2016）為生物醫學體積資料提出此方法。

## 概述

上層的 [U-Net](index.zh-TW.md) 以二維影像分割，其編碼器下採樣、解碼器上採樣，並在兩者之間有跳接連線。3D U-Net 保留這個設計，把每一個二維運算換成三維的對應運算，使濾波器同時沿深度、寬度與高度移動。

## 問題

製作稠密的三維標註成本很高：標註者必須標記每一個體素的每一個體積。許多實務任務只有少數標註切片，而逐切片套用二維網路會忽略切片之間的結構。問題在於，三維網路能否從稀疏標註學出完整的分割。

## 核心想法

把 U-Net 的所有二維運算換成三維運算，從頭端到端訓練，並以即時的彈性形變豐富訓練資料。網路因此能從稀疏標註的體積學習，並推廣到新的體積。

## 演算法

網路沿用 U-Net 的編碼器、解碼器與跳接連線。編碼器使用 $3\times3\times3$ 卷積與 $2\times2\times2$ 最大池化。解碼器沿三個空間維度上採樣，並結合編碼器相同解析度的特徵。最後以 $1\times1\times1$ 卷積產生各體素的類別分數。原始架構輸入 $132\times132\times116$ 的區塊，輸出 $44\times44\times28$ 的預測區塊，因此能使用周圍體素作為較小輸出區域的上下文。[^original]

### 從稀疏標註學習

訓練使用加權的 softmax 交叉熵。設 $\mathcal{A}$ 為輸出區塊中已標註的體素集合，$y_v$ 為已知標籤，$w_{y_v}$ 為其類別權重，$p_v(y_v)$ 為模型對該標籤預測的機率。下式列出哪些體素會計入損失。[^original]

$$
\mathcal{L}=-\sum_{v\in\mathcal{A}}w_{y_v}\log p_v(y_v).
$$

論文將未標註體素的損失權重設為零，並以類別權重平衡已標註的各類別。未標註體素與標為背景的體素扮演不同角色，只有後者會計入背景分類的誤差。網路仍使用整個輸入區塊作為上下文，並為整個輸出區塊產生分數。訓練時，影像與標籤會套用相同的彈性形變，以維持對齊。[^original]

### 評估方式

1. **半自動**。模型使用待分割體積內的標註學習。在三折評估中，作者將三個體積的 77 張已標註切片分成三組。每折將其中一組視為未標註，並保留供評估。[^original]
2. **全自動**。每折用兩個稀疏標註的體積訓練，並在第三個體積上預測。IoU 依留出體積中的已標註切片計算。這測試模型能否遷移到同一資料集中的另一個體積。[^original]

## 主要結果

研究回報三個 Xenopus 腎臟體積上的 IoU。留出切片與留出整個體積得到不同的比較結果。[^original]

| 評估方式 | 3D 無 BN | 3D 有 BN | 2D 有 BN |
| --- | --- | --- | --- |
| 留出切片（表 1） | 0.842 | 0.863 | 0.796 |
| 留出體積（表 3） | 0.723 | 0.704 | 0.547 |

在留出體積的實驗中，批次正規化（BN）提高了兩個體積的 IoU。第三個體積的 IoU 從 0.779 降至 0.554，使得使用 BN 時的三體積平均值較低。作者另在半自動實驗中改變標註量。三個正交平面各標註一張切片時，三個體積的 IoU 介於 0.331 到 0.483。採用論文所列的 5、5 和 3 張切片時，IoU 介於 0.849 到 0.872（表 2）。[^original]

## 限制

- 結果只在一種體積上回報，即 Xenopus 腎臟，因此方法的一般性尚未展示。
- 三維卷積比二維的對應運算需要更多記憶體與運算，限制了可處理的體積大小。
- 兩種評估留出的單位不同。切片留出衡量模型在部分已標註體積內補齊分割的表現，體積留出則衡量模型在三個體積之間遷移的表現。[^original]

## 關聯

- [U-Net](index.zh-TW.md)是 3D U-Net 所擴展的二維設計。
- [分割指標](../../../evaluation/metrics/segmentation/index.zh-TW.md)說明 IoU 與 Dice，這兩種重疊度量被用來評估體積分割。
- [卷積變體](../convolution-variants/index.zh-TW.md)涵蓋體積網路所依賴的三維與空洞運算。
- [全卷積網路（Long 等人，2014）](https://arxiv.org/abs/1411.4038)是 U-Net 所建立於其上的較早全卷積分割設計。

## 應用

- 從稀疏標註進行生物醫學體積分割，即論文中 Xenopus 腎臟實驗的設定。
- 半自動標註：使用者標註少數切片，網路完成體積其餘部分。

## 開放問題

- 需要多少標註切片，半自動設定才可靠？應選擇哪些切片？
- 方法能否在不從頭重訓的情況下，轉移到其他器官與影像模態？

[^original]: Çiçek 等人，[*3D U-Net*](https://arxiv.org/html/1606.06650)，第 2 至 4 節及表 1 至 3。

## 參考文獻

### 開創性論文

- Çiçek, Ö., Abdulkadir, A., Lienkamp, S. S., Brox, T. 與 Ronneberger, O.（2016）。*3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation*。arXiv。https://arxiv.org/abs/1606.06650 — 提出 3D U-Net，並在 Xenopus 腎臟體積上回報半自動與全自動設定的 IoU。
- Ronneberger, O., Fischer, P. & Brox, T.（2015）。*U-Net: Convolutional Networks for Biomedical Image Segmentation*。arXiv。https://arxiv.org/abs/1505.04597 — 3D U-Net 所擴展的、帶跳接連線的二維編碼器–解碼器。
- Milletari, F., Navab, N. & Ahmadi, S.-A.（2016）。*V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation*。arXiv。https://arxiv.org/abs/1606.04797 — 同期用於三維醫學分割的全卷積網路。
- Long, J., Shelhamer, E. & Darrell, T.（2014）。*Fully Convolutional Networks for Semantic Segmentation*。arXiv。https://arxiv.org/abs/1411.4038 — 用於稠密預測的全卷積設計。
- Sudre, C. H., 等人（2017）。*Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations*。arXiv。https://arxiv.org/abs/1707.03237 — 適用於高度不平衡分割的重疊度損失，與稀疏的體積標註相關。
