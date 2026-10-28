---
translation_reviewed: 2026-10-28
---

# 三維 U-Net

3D U-Net 是 [U-Net](index.md) 的版本，直接以三維運算分割體積影像，取代二維運算。它的設計目的是從稀疏標註學習：使用者標註少數切片，網路便產生稠密的三維分割。Çiçek 等人（2016）為生物醫學體積資料提出此方法。

## 概述

上層的 [U-Net](index.md) 以二維影像分割，其編碼器下採樣、解碼器上採樣，並在兩者之間有跳接連線。3D U-Net 保留這個設計，把每一個二維運算換成三維的對應運算，使濾波器同時沿深度、寬度與高度移動。

## 問題

製作稠密的三維標註成本很高：標註者必須標記每一個體素的每一個體積。許多實務任務只有少數標註切片，而逐切片套用二維網路會忽略切片之間的結構。問題在於，三維網路能否從稀疏標註學出完整的分割。

## 核心想法

把 U-Net 的所有二維運算換成三維運算，從頭端到端訓練，並以即時的彈性形變豐富訓練資料。網路因此能從稀疏標註的體積學習，並推廣到新的體積。

## 演算法

網路沿用 U-Net 的編碼器–解碼器與跳接連線。卷積、池化與上採樣都在三個空間維度上運作。訓練時對輸入體積做即時的彈性形變作為資料擴增，且不使用預訓練網路。論文評估兩種設定：

1. **半自動**：使用者標註待分割體積的部分切片，網路完成其餘分割。
2. **全自動**：假設存在一組具代表性的稀疏標註訓練集，訓練後的網路不需使用者輸入即可分割新的體積。

## 主要結果

論文在 Xenopus 腎臟體積上評估，並回報交集除以聯集（IoU）。以下數字取自其表 1 與表 3。

- **半自動**（3 折交叉驗證）：使用批次正規化時平均 IoU 為 0.863，不使用時為 0.842。二維變體為 0.796。
- **全自動**：使用批次正規化時平均 IoU 為 0.704，不使用時為 0.723。論文文字說批次正規化有幫助，但這些平均值指向相反方向。它在兩個體積上有幫助、在第三個上有害（使用時 0.554，不使用時 0.779，依論文回報）。

論文只回報 IoU，這些實驗未給出 Dice 分數或準確率。

## 限制

- 結果只在一種體積上回報，即 Xenopus 腎臟，因此方法的一般性尚未展示。
- 三維卷積比二維的對應運算需要更多記憶體與運算，限制了可處理的體積大小。
- 全自動設定中批次正規化的結果與論文自己的文字相矛盾，因此應以表格的平均值為準，而非摘要敘述。

## 關聯

- [U-Net](index.md)是 3D U-Net 所擴展的二維設計。
- [分割指標](../../../evaluation/metrics/segmentation/index.md)說明 IoU 與 Dice，這兩種重疊度量被用來評估體積分割。
- [卷積變體](../convolution-variants/index.md)涵蓋體積網路所依賴的三維與空洞運算。
- [全卷積網路（Long 等人，2014）](https://arxiv.org/abs/1411.4038)是 U-Net 所建立於其上的較早全卷積分割設計。

## 應用

- 從稀疏標註進行生物醫學體積分割，即論文中 Xenopus 腎臟實驗的設定。
- 半自動標註：使用者標註少數切片，網路完成體積其餘部分。

## 開放問題

- 需要多少標註切片，半自動設定才可靠？應選擇哪些切片？
- 方法能否在不從頭重訓的情況下，轉移到其他器官與影像模態？

## 參考文獻

### 開創性論文

- Çiçek, Ö., Abdulkadir, A., Lienkamp, S. S., Brox, T. 與 Ronneberger, O.（2016）。*3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation*。arXiv。https://arxiv.org/abs/1606.06650 — 提出 3D U-Net，並在 Xenopus 腎臟體積上回報半自動與全自動設定的 IoU。查核：arXiv metadata 與論文表 1、表 3。
- Ronneberger, O., Fischer, P. & Brox, T.（2015）。*U-Net: Convolutional Networks for Biomedical Image Segmentation*。arXiv。https://arxiv.org/abs/1505.04597 — 3D U-Net 所擴展的、帶跳接連線的二維編碼器–解碼器。查核：arXiv metadata。
- Milletari, F., Navab, N. & Ahmadi, S.-A.（2016）。*V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation*。arXiv。https://arxiv.org/abs/1606.04797 — 同期用於三維醫學分割的全卷積網路。查核：arXiv metadata。
- Long, J., Shelhamer, E. & Darrell, T.（2014）。*Fully Convolutional Networks for Semantic Segmentation*。arXiv。https://arxiv.org/abs/1411.4038 — 用於稠密預測的全卷積設計。查核：arXiv metadata。
- Sudre, C. H., 等人（2017）。*Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations*。arXiv。https://arxiv.org/abs/1707.03237 — 適用於高度不平衡分割的重疊度損失，與稀疏的體積標註相關。查核：arXiv metadata。
