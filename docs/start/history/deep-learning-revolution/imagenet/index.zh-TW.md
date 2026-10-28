---
translation_reviewed: 2026-10-28
---

# ImageNet 與 ILSVRC 基準（Deng 等人，2009；Russakovsky 等人，2015）

ImageNet 是一個依名詞階層組織的大型標註影像集，而每年舉辦的 ImageNet 大規模視覺辨識挑戰賽（ILSVRC）即建立在它之上。兩者一起為深度卷積網路提供了標註資料與共同的衡量標準，使 2012 年的突破得以被量化。這是[深度學習革命](../index.md)這一章的資料里程碑。

## 概述

Deng 等人（2009）建立 ImageNet，作為物件辨識研究的大型、階層化資源。它的類別遵循 WordNet 階層，因此每個類別都位於一棵由較一般到較具體概念所構成的樹中。挑戰賽接著把這個資料集變成一場競賽。Russakovsky 等人（2015）將它描述為物件分類與偵測的基準，自 2010 年起每年舉辦，並吸引了超過五十個機構參與。

由於每支隊伍都在同一批保留的影像上接受評分，結果因此具有可比性。2012 年以深度卷積網路為基礎的參賽作品，即 [AlexNet](../../../../theory/models/cnn/backbones-and-scaling/alexnet/index.md)，贏得了這場競賽，而它之後的幾年，正是本章所描述的時期。

## 關鍵概念

- **同義詞集（synset）**：一組共享同一個意義的詞。ImageNet 的類別即是 WordNet 名詞階層中的同義詞集（Deng 等人，2009）。
- **分類與偵測**：分類是問影像包含哪一個類別；偵測則還要定位每個物件（Russakovsky 等人，2015）。
- **前五名錯誤率（top-5 error）**：測試影像中，正確標籤不在模型五個最高分預測之內的比例。
- **保留的測試集（held-out test set）**：不參與訓練而被保留下來的影像，使分數衡量的是泛化能力，而非記憶。

## 運作方式

建立資料集包含三個步驟：

1. 從 WordNet 階層中選出類別。
2. 為每個類別從網路上蒐集候選影像。
3. 由人工標註者確認哪些候選影像確實呈現該類別。

第三步最為耗費人力，Russakovsky 等人（2015）討論了大規模取得真實標註的困難。

每一輪挑戰賽都遵循同樣的程序：主辦方釋出附標籤的訓練影像，保留測試影像，並為每個參賽作品的預測評分。對於真實標籤為 $y_i$、預測前五個標籤為 $\hat{S}_i$ 的單張影像 $x_i$，前五名錯誤率為

$$
\text{top-5 error} = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}\left[\, y_i \notin \hat{S}_i \,\right].
$$

## 結果

Russakovsky 等人（2015）描述了這個基準使物件辨識得以取得的進展，並比較了電腦視覺的準確度與人類的準確度。2012 年以深度卷積網路為基礎的參賽作品改變了這場競賽，而[AlexNet](../../../../theory/models/cnn/backbones-and-scaling/alexnet/index.md)頁面涵蓋了其具體數字。

## 限制

- **標註。** 在這種規模下取得準確的標籤很困難，部分標籤可能有誤或含糊不清（Russakovsky 等人，2015）。
- **資料集偏差。** 資料集反映了蒐集時所做的選擇。Torralba 與 Efros（2011）說明了在一個影像資料集上訓練的分類器，要推廣到其他資料集有多困難。
- **對測試集過度擬合。** 經過多年重複使用，測試集可能已被擬合得過於貼近。Recht 等人（2019）建立新的測試集，以檢驗分類器是否能推廣到新的 ImageNet 式資料，並直接提出了這項疑慮。
- **目標範圍狹窄。** 基準上的準確度並不衡量穩健性，也不衡量後來的模型所被要求的其他能力。

## 開放問題

- 一旦模型在規模更大、整理程度較低的資料上訓練，基準分數究竟衡量什麼？
- 當一個基準已經飽和，應該以什麼取代它，又由誰來維護？
- 高的 ImageNet 分數，是否反映了人類所使用的相同視覺線索？[Geirhos 等人（2019）](../../../../brain-mind/visual-perception/geirhos-2019/index.md)頁面討論了 ImageNet 訓練網路中的紋理偏好。

## 關聯

這個基準把領域的資料與方法連結起來。在 ImageNet 上訓練的網路成為後續視覺系統的骨幹（參見[卷積骨幹網路](../../../../theory/models/cnn/backbones-and-scaling/index.md)）。它們也成為神經科學的工具。Yamins 等人（2014）指出，為物件辨識最佳化的階層模型，能預測高階視覺皮質的神經反應，這一連結在[效能最佳化網路](../../../../brain-mind/neuroai/performance-optimised-networks/index.md)一頁中討論。至於通往深度模型的較早途徑，參見[深度信念網路](../deep-belief-networks/index.md)頁面。

## 參考文獻

### 開創性論文

- Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K. & Fei-Fei, L. (2009). ImageNet: A large-scale hierarchical image database. *2009 IEEE Conference on Computer Vision and Pattern Recognition*. https://doi.org/10.1109/CVPR.2009.5206848 — 介紹 ImageNet，一個依 WordNet 階層組織的大型影像資料庫。
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. *Advances in Neural Information Processing Systems 25*. https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — 贏得 2012 年挑戰賽、開啟視覺領域深度學習時代的深度卷積網路。
- Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S. 等人（2015）。ImageNet Large Scale Visual Recognition Challenge. *International Journal of Computer Vision*. https://doi.org/10.1007/s11263-015-0816-y — 描述此基準的建立、它所促成的進展，以及頭幾年的經驗教訓。

### 綜述與教科書

- Sejnowski, T. J. (2018). *The Deep Learning Revolution*. MIT Press. https://doi.org/10.7551/mitpress/11474.001.0001 — 由一位親身參與其中的神經科學家所寫的深度學習革命史。

### 文章與文件

- Torralba, A. & Efros, A. A. (2011). Unbiased look at dataset bias. *CVPR 2011*. https://doi.org/10.1109/CVPR.2011.5995347 — 探討影像資料集如何產生偏差，以及在一個資料集上訓練的分類器為何難以轉移到其他資料集。
- Recht, B., Roelofs, R., Schmidt, L. & Shankar, V. (2019). Do ImageNet classifiers generalize to ImageNet? arXiv. https://arxiv.org/abs/1902.10811 — 建立新的 ImageNet 測試集，以衡量對重複使用之基準資料的過度擬合。
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識最佳化的階層模型，能預測高階視覺皮質的神經反應。
