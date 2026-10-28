---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - attribution
aliases:
  - 顯著性圖
  - 梯度顯著性
  - Saliency maps
  - Gradient-based saliency
---

# 顯著性圖

!!! info "屬於特徵歸因"
    本方法頁屬於[特徵歸因](feature-attribution.md)。它詳細說明此方法；概述頁則比較各種方法。

顯著性圖顯示每個輸入像素對網路某一類別分數的影響強度。它由該分數對輸入的梯度計算而得，因此只需一次反向傳播。Simonyan、Vedaldi 與 Zisserman（2014）為影像分類器引入這項技術。

## 問題

卷積網路會為一張影像貼上標籤，但其決定很難檢視。決定依賴哪些像素？網路是在看物體，還是在看周圍的背景？問題在於對單一影像與單一類別，產生能回答此問題的圖。

## 核心想法

取類別分數對輸入影像的梯度。在小幅改變時會使分數變動最大的像素，就是最顯著的像素。論文描述兩種基於此梯度的視覺化技術；類別顯著性圖則針對特定影像與特定類別。

## 公式

對類別 \(c\)、分數 \(S_c(I)\) 與影像 \(I\)，此圖在每個像素取梯度的大小：

\[
M_c(I)_{ij} = \left|\frac{\partial S_c}{\partial I_{ij}}\right|.
\]

## 結果

論文將顯著性圖呈現為單一影像的視覺化，而非基準測試。圖是否忠實反映模型，是另一個問題，後續研究直接加以檢驗（見限制）。

## 限制

- **健全性。** Adebayo 等人（2018）報告，部分既有顯著性方法與模型及資料生成過程皆無關，因此看起來合理的圖並不能證明它反映了模型所學到的內容。
- **局部斜率。** 梯度只給出輸入處分數的斜率，而非像素對分數的總效應。積分梯度正是為了處理此問題而提出（Sundararajan 等人，2017）。
- **以視覺判讀。** 圖常憑肉眼判斷，容易讀出自己預期看到的內容。

## 參考文獻

### 開創性論文

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. *ICLR 2014 Workshop*. https://arxiv.org/abs/1312.6034 — 引入基於梯度的視覺化，包括類別顯著性圖。
- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — 提出積分梯度，修正純梯度的限制。
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). Learning Important Features Through Propagating Activation Differences. *Proceedings of ICML 2017*. https://arxiv.org/abs/1704.02685 — 提出 DeepLIFT，從參考啟動值傳播啟動差異，而非使用原始梯度。

### 綜述與教科書

- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — 測試顯著性方法，發現部分方法與模型及資料無關。
- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — 免費線上書籍，涵蓋基於梯度與其他歸因方法。
