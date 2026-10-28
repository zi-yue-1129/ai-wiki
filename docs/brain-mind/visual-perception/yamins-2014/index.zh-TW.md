---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/cnn
tags:
- neuroscience
- perception
aliases:
  - Yamins 2014
  - 效能最佳化的階層模型
  - Performance-optimised hierarchical models
---

# 效能最佳化的網路預測 IT 皮質（Yamins 等人，2014）

Yamins 等人（2014）探問：在物體辨識上表現良好的神經網路，是否也能解釋高階視覺皮質神經元的反應？他們報告的答案是肯定的，而且這種吻合來自效能本身，而不是把網路擬合到神經資料上。這篇論文是 [NeuroAI](../../neuroai/index.md) 的里程碑，也確立了後來基準研究所遵循的模式。

本頁是[知覺與視覺系統](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

靈長類的物體辨識依賴下顳葉（IT）皮質，那是腹側視覺路徑的最高區域。它的反應很難以簡單模型解釋。為分類而訓練的卷積網路是一個候選，但分類得好的網路，未必與大腦共享相同的運算。問題在於：單靠任務效能，是否就能挑出與 IT 吻合的網路。

## 方法

作者定義了一大族階層式卷積網路，它們在深度、濾波器大小與連接方式上各不相同。他們在物體辨識任務上訓練每個網路並為其效能評分，接著測試每個模型對神經反應的預測能力。

步驟如下：

1. 定義一族階層式網路，改變深度、濾波器大小與連接方式。
2. 在物體辨識任務上訓練每個網路，並為其效能評分。
3. 挑出辨識效能高的網路；被選中的模型在數項辨識測試上達到人類水準。
4. 從模型各層到記錄下來的 IT 與 V4 反應，在保留的自然影像上做線性迴歸，並測量模型對每個記錄位點的預測能力。

關鍵在於：挑選網路的步驟從不使用神經資料，只有最後的迴歸才用到。

## 結果

摘要報告三項發現：

- 在這一族網路中，分類效能與網路預測 IT 反應的能力高度相關。
- 被選中的網路在數項辨識任務上達到人類水準，它預測了 IT 對自然影像的脈衝反應，無論是單一位點還是群體層級。
- 它的中間層能預測 V4 的反應，V4 是 IT 之前的區域。

摘要沒有給出數值化的相關係數或可解釋變異，因此本頁不引用任何數字。

## 限制

- 比較只用了有限的影像與記錄位點。線性擬合良好並不代表模型使用與大腦相同的運算。
- 在保留影像上的預測成功，並不能證明模型能推廣到其他刺激、物種或任務。
- 後續的基準研究比較了更多模型與神經資料。這種預測力能否跨刺激與物種轉移，仍是開放問題。

## 與其他主題的關聯

- **方法家族**：挑選模型依任務效能、再於神經資料上檢驗的邏輯，也是後來視覺基準研究的基礎。架構家族見 [CNN](../../../theory/models/cnn/index.md)。
- **形狀偏好**：關於這些網路實際學到什麼的相關問題，見 [CNN 的形狀偏好（Geirhos 等人，2019）](../geirhos-2019/index.md)。
- **神經科學背景**：論文所依賴的皮質階層與感受野，見[神經科學基礎](../../neuroscience/index.md)。

## 開放問題

- **吻合能延伸多遠？** 論文只測試了視覺類別與有限的位點。這種吻合能否延伸到其他感覺系統與任務，仍待確認。
- **效能是正確的挑選依據嗎？** 以效能挑選在這裡有效，但其他挑選標準可能找出不同的模型。

## 參考文獻

### 開創性論文

- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J.（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*。https://doi.org/10.1073/pnas.1403112111 — 顯示物體辨識效能能預測網路對 IT 反應的解釋力。
- Krizhevsky, A., Sutskever, I. & Hinton, G. E.（2012）。ImageNet Classification with Deep Convolutional Neural Networks. *NeurIPS*。https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，也是 2014 年研究所檢驗的那類網路。
- Hubel, D. H. & Wiesel, T. N.（1962）。Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*。https://doi.org/10.1113/jphysiol.1962.sp006837 — 網路所模仿的階層背後的感受野研究。（此參考文獻沿用自神經科學基礎頁面，本頁未重新檢驗。）

### 綜述與回顧

- Lindsay, G. W.（2021）。Convolutional Neural Networks as a Model of the Visual System: Past, Present, and Future. *Journal of Cognitive Neuroscience*。https://doi.org/10.1162/jocn_a_01544 — 回顧 CNN 作為視覺系統模型的用法，以及它能解釋與無法解釋的部分。
- Kriegeskorte, N.（2015）。Deep neural networks: a new framework for modelling biological vision and brain information processing. bioRxiv 預印本。https://doi.org/10.1101/029876 — 主張以深度網路作為大腦資訊處理的候選模型，並討論此類模型應如何評估。
