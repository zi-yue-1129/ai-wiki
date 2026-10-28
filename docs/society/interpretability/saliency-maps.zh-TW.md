---
status: complete
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

顯著性圖（saliency map）顯示，每個輸入像素對網路某一類別分數的影響有多強。它由該分數對輸入的梯度計算而得，因此一次反向傳播即可完成。Simonyan、Vedaldi 與 Zisserman（2014）為影像分類器提出了這項技術。

## 問題

卷積網路會為影像標上類別，但它的決策難以檢視。決策依賴哪些像素？網路注意的是物體，還是周圍的背景？問題在於：對一張影像與一個類別，產生一張能回答這些問題的圖。

## 核心想法

對輸入影像取類別分數的梯度。在微小改變下分數變動最大的像素，最為顯著。論文描述了兩種以此梯度為基礎的視覺化技術；類別顯著性圖則針對特定影像與類別。

## 方程式

對類別 $c$、分數 $S_c(I)$ 與影像 $I$，此圖在每個像素取梯度的大小：

$$
M_c(I)_{ij} = \left|\frac{\partial S_c}{\partial I_{ij}}\right|.
$$

## 結果

論文把顯著性圖呈現為對個別影像的視覺化，每張影像只需一次反向傳播。論文也在 ILSVRC 2013 上評估了一個基於顯著性的弱監督物件定位流程，這衡量的是定位表現。定位表現與解釋忠實度是不同的問題：圖是否反映模型的計算，後續研究會直接加以檢驗（見限制）。

## 限制

- **合理性檢驗。** Adebayo 等人（2018）報告，一些既有的顯著性方法與模型及資料生成過程都無關，因此看起來合理的圖並不能證明它反映了模型學到的東西。他們的測試也顯示，把較高層權重隨機化後，Guided BackProp 仍保有大部分外觀。
- **局部斜率。** 梯度給出的是輸入處分數的斜率，而非像素的總效應。積分梯度的提出正是為了處理這一點（Sundararajan et al., 2017）。
- **以目測解讀。** 圖常以肉眼判斷，容易讀入自己預期看到的內容。

## 相關連結

顯著性圖是[特徵歸因](feature-attribution.md)中最簡單的梯度方法。[積分梯度](integrated-gradients.md)沿路徑累積梯度，以處理局部斜率的問題；DeepLIFT（Shrikumar et al., 2017）則以相對於參考激活的差值取代梯度。梯度方法需要存取模型的內部，這使它們有別於與模型無關的 [LIME](lime.md)，也有別於只需要預測結果的 Kernel SHAP（[SHAP](shap.md)）。關於這些圖最初用於的卷積架構，見[可解釋性總覽](index.md)。

## 應用

- 檢查影像分類器是看物體，還是看浮水印等背景線索。
- 在醫學影像中定位證據，供臨床醫師審閱，但須注意上述限制。
- 在同一批影像上比較兩個模型，看它們的證據是否不同。

## 開放問題

- 哪些基於梯度的圖能在不同架構與任務上通過合理性檢驗？
- 應如何在不依賴目測的情況下，以量化方式評估顯著性？
- 輸入處的梯度，在多大程度上反映模型的計算，而非局部形狀？

## 參考文獻

### 開創性論文

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. arXiv:1312.6034. https://arxiv.org/abs/1312.6034 — Introduces gradient-based visualisations, including the class saliency map.
- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — Proposes integrated gradients as a fix for the limits of plain gradients.
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). Learning Important Features Through Propagating Activation Differences. *Proceedings of ICML 2017*. https://arxiv.org/abs/1704.02685 — Proposes DeepLIFT, which propagates activation differences from a reference rather than raw gradients.

### 綜述與教科書

- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — Tests saliency methods and finds that some are independent of the model and the data.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — Places DeepLIFT and several other attribution methods in one additive framework.

## 延伸學習

- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. [免費線上書](https://christophm.github.io/interpretable-ml-book/)，其中有基於梯度的歸因方法與實例。
