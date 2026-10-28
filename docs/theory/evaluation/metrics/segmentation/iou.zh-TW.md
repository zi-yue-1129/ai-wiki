---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# 交併比

交併比（IoU）又稱 Jaccard 指數，是預測區域與參考區域的重疊面積，除以兩者合起來所覆蓋的面積。它是物件偵測與分割中的標準重疊指標。

## 定義

對於預測區域 $A$ 與參考區域 $B$：

$$\text{IoU} = \frac{|A \cap B|}{|A \cup B|}$$

當兩個區域完全相同時，IoU 為 1；沒有重疊時為 0。scikit-learn 的 `jaccard_score` 對標籤集合計算同樣的量，因此對二元遮罩而言，它給出的是正例類別的 IoU（見參考文獻）。

## 解讀

由於聯集位於分母，IoU 同時懲罰遺漏的像素與多出來的像素。覆蓋了正確區域、但面積是正確的兩倍的預測，得分為 0.5，而不是 1.0。對小物件而言，邊界上幾個像素的誤差就可能大幅改變 IoU，因此小物件的結果看起來可能比模型的視覺品質差。

## 何時使用

當問題是預測區域與參考區域的吻合程度時使用 IoU，例如在偵測中以 IoU ≥ 0.5 作為正確偵測的門檻。應報告所用的門檻，以及分數是依影像、依類別還是依整個資料集平均。

## 範例

取一條 10 個像素的一維區域。預測區域涵蓋像素 1 到 6（6 個像素），參考區域涵蓋像素 4 到 7（4 個像素），兩者共享 3 個像素。聯集為 $6 + 4 - 3 = 7$，因此 IoU $= 3 / 7 \approx 0.43$。同樣的遮罩，[Dice](dice.md) 為 0.60，可見兩個指標的數值可以差距很大。

## 性質與變體

- **像素形式。** 對二元遮罩，$|A \cap B| = \mathrm{TP}$，$|A \cup B| = \mathrm{TP} + \mathrm{FP} + \mathrm{FN}$，因此 $\mathrm{IoU} = \mathrm{TP} / (\mathrm{TP} + \mathrm{FP} + \mathrm{FN})$。這就是兩個集合的 Jaccard 指數。
- **與 Dice 的關係。** $\mathrm{Dice} = 2\,\mathrm{IoU} / (1 + \mathrm{IoU})$。兩者互為單調函數，因此對單一區域的模型排序相同。
- **平均 IoU。** 各類別的平均（mIoU）是多類別分割常用的摘要。逐類別的數值可顯示稀有類別是否表現不佳。
- **邊界框變體。** 廣義 IoU 會扣除一個依最小包圍框計算的懲罰項。在邊界框不重疊時，它仍能提供有用的訊號，而一般 IoU 對這些配對都是零。
- **限制。** 小或細長的物體面積小，少數邊界像素就可能大幅改變 IoU。

## 常見陷阱

- **平均方式。** 依類別或影像取平均的 mean IoU，可能掩蓋在稀有或小物件上的糟糕表現。應報告各類別的數值。
- **門檻選擇。** 在 IoU 0.5 下算為正確的偵測，在 0.75 下可能是錯的。應說明使用的門檻。

## 相關指標

[Dice](dice.md)是分母不同的相關重疊指標。家族概述見[分割指標](index.md)。

## 參考文獻

### 文章與文件

- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API 參考，給出標籤集合交併比的定義，並附有二元與多標籤的範例。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類式比較可用的評分器概述。

### 補充來源

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- Rezatofighi, H. et al. (2019). Generalized intersection over union: a metric and a loss for bounding box regression. CVPR 2019. https://arxiv.org/abs/1902.09630 — 擴充 IoU，使其在邊界框不重疊時仍能提供資訊。
- Cordts, M. et al. (2016). The Cityscapes dataset for semantic urban scene understanding. CVPR 2016. https://arxiv.org/abs/1604.01685 — 基準資料集，其評估以各類別的交集除以聯集報告結果。
