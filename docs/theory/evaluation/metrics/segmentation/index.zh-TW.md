---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# 分割指標

分割指標把預測遮罩與參考遮罩逐像素或逐體素地比較。它們衡量的是重疊程度，而不是平均而言類別是否正確，因此當區域的位置與範圍很重要時，這些指標是自然的選擇。

## 問題

對某一類別，令 \(A\) 為預測的前景像素集合，\(B\) 為參考的前景像素集合。當 \(A = B\) 時指標應為 1，兩個區域分離時指標應下降，而且不應獎勵把所有像素都預測為前景。像素準確率在稀疏類別上無法通過最後一項測試，因為幾乎全是背景的遮罩也會得到很高的分數。

## 關鍵概念

- **重疊：** 交集 \(|A \cap B|\)，即兩個遮罩都標示為前景的像素。
- **聯集：** \(|A \cup B|\)，即任一遮罩標示為前景的像素。
- **逐類別與平均：** 指標先逐類別計算，再取平均，因此稀有類別與常見類別的權重相同。

## 關鍵方法

### 交集除以聯集（IoU）

\[
\mathrm{IoU} = \frac{|A \cap B|}{|A \cup B|} = \frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FP} + \mathrm{FN}}
\]

IoU 也稱為 Jaccard 指數。細節見 [IoU](iou.md) 頁面。它的類別平均是語意分割中常見的主要數字。PASCAL VOC 報告（Everingham 等人，2010）是基於重疊的評估的標準參考，而 Cityscapes 評估則逐類別回報交集除以聯集（Cordts 等人，2016）。

- **限制：** IoU 無法說明錯誤位於邊界何處，而且預測遮罩與參考遮罩都為空時，需要另外約定。

### Dice 係數

\[
\mathrm{Dice} = \frac{2\,\lvert A \cap B \rvert}{\lvert A \rvert + \lvert B \rvert} = \frac{2\,\mathrm{TP}}{2\,\mathrm{TP} + \mathrm{FP} + \mathrm{FN}}
\]

Dice（1945）把這個係數提出作為物種間生態關聯的量測。在像素標籤上，它與 [F1 分數](../classification/f1.md)是同一個比率。若 \(J\) 為同一對遮罩的 IoU，則 \(\mathrm{Dice} = 2J / (1 + J)\)，因此 Dice 不小於 IoU，而且對單一區域而言，兩者對模型的排序相同。細節見 [Dice](dice.md) 頁面。

- **限制：** 對高度不平衡的多類別資料，一般的 Dice 會依類別大小加權，因此需要類別加權的變體。Sudre 等人（2017）為此情況提出廣義 Dice 重疊度。

## 關聯

重疊指標無法說明預測邊界與參考邊界相距多遠，這就是分割評估常會再加入邊界距離指標的原因。同樣的重疊比率也被許多分割方法當作訓練損失使用，Sudre 等人（2017）正是在這個用途上應用廣義形式。

## 開放問題

- 如何在一個回報數字中，同時結合重疊程度與邊界準確度。
- 當預測與參考都為空時（小型結構常見的情況），應如何定義指標。

## 參考文獻

### 奠基性論文

- Dice, L. R.（1945）。Measures of the amount of ecologic association between species。*Ecology* 26(3)，297–302。https://doi.org/10.2307/1932409 — 提出現在稱為 Dice 分數的係數。
- Everingham, M. 等人（2010）。The Pascal Visual Object Classes (VOC) Challenge。*International Journal of Computer Vision* 88(2)，303–338。https://doi.org/10.1007/s11263-009-0275-4 — 標準基準報告，其評估使用基於重疊的量測。
- Sudre, C. H., Li, W., Vercauteren, T., Ourselin, S. 等人（2017）。Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations。收錄於 *Deep Learning in Medical Image Analysis and Multimodal Learning for Clinical Decision Support*（DLMIA 2017），LNCS，第 240–248 頁。https://doi.org/10.1007/978-3-319-67558-9_28 — 為高度不平衡的分割提出依類別重新加權的廣義 Dice 重疊度。

### 文章與文件

- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API 參考，將 Jaccard 指數描述為兩個標籤集合的交集大小除以聯集大小。
- scikit-learn contributors. *f1_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — API 參考，給出公式 \(2\mathrm{TP} / (2\mathrm{TP} + \mathrm{FP} + \mathrm{FN})\)，這與二元遮罩上的 Dice 係數是同一個比率。
- Cordts, M. 等人（2016）。The Cityscapes dataset for semantic urban scene understanding。CVPR 2016。https://openaccess.thecvf.com/content_cvpr_2016/html/Cordts_The_Cityscapes_Dataset_CVPR_2016_paper.html — 基準資料集，其評估逐類別回報交集除以聯集。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 可用於像素標籤比較的分類評分器概述。

### 補充來源

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
