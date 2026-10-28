---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
  - theory/models/cnn
  - theory/models/transformer
tags:
  - interpretability
  - explainable AI
  - attribution
aliases:
  - 特徵歸因
  - 可解釋 AI
  - 顯著性圖
  - Feature attribution
  - SHAP
  - LIME
  - Integrated gradients
  - Saliency maps
---

# 特徵歸因：SHAP、LIME 與顯著性

特徵歸因為每個輸入特徵（例如像素、詞元或表格中的欄位）指派一個分數，用來顯示它對某個特定預測的貢獻大小。它是最常見的可解釋 AI 形式，用於檢視個別決策、找出虛假相關，並支持稽核。各種歸因方法在比較的基準、是從外部探測模型還是使用其梯度，以及是否滿足基本的一致性要求上有所不同。這些差異與地圖本身同樣重要。

## 概述

給定模型 \(f\) 與輸入 \(x\)，歸因方法會回傳一個向量 \(\phi = (\phi_1, \dots, \phi_d)\)，其中 \(\phi_i\) 是歸給特徵 \(i\) 對輸出的貢獻。輸出通常是某一類別的分數或預測值。歸因值大，表示在所選的比較下，該特徵明顯改變了輸出。這句話的意義取決於所選的比較，這也是各方法結果不同的原因。

## 核心概念

- **歸因**：針對單一預測、每個特徵的分數。
- **基準**或**參考輸入**：比較的起點，例如全黑影像、平均輸入，或一組背景樣本。多數歸因值都是相對於基準的差異。
- **局部與全域**：局部方法解釋單一預測；全域方法則彙總許多預測。
- **忠實性（faithfulness）**：歸因是否反映模型實際使用的特徵。
- **可加性（additivity）**：歸因的總和是否等於預測值與基準預測值之間的差。

## 運作方式

歸因方法大致分為兩類。

**梯度與傳播方法**利用模型的內部結構。Simonyan 等人（2014）把類別分數對輸入像素的梯度當作顯著性圖。梯度可能有雜訊且會飽和，因此後來的方法改變了傳播規則。積分梯度（Sundararajan 等人，2017）沿著從基準到輸入的直線路徑對梯度取平均，得到的歸因總和等於輸出的差。DeepLIFT（Shrikumar 等人，2017）與逐層相關性傳播（Bach 等人，2015）則依據參考啟動值或輸入訊號所用的規則，將輸出分數反向分配到各層。

**擾動與賽局理論方法**把模型當作黑箱。它們改變輸入、觀察輸出，並擬合或平均其效應。LIME 在單一輸入周圍擬合一個簡單的代理模型，SHAP 則對特徵的各種聯盟，平均每個特徵的邊際貢獻。

## 主要方法

- **顯著性圖（Simonyan 等人，2014）。** 輸出對輸入的梯度。它快速且只需反向傳播，但對梯度的局部行為敏感，且不滿足可加性。
- **積分梯度（Sundararajan 等人，2017）。** 歸因為輸入減基準的差，乘以沿路徑的平均梯度。它滿足敏感性與實作不變性，但取決於基準的選擇。
- **LIME（Ribeiro 等人，2016）。** 對輸入取樣擾動版本，依接近程度加權，並擬合一個稀疏線性模型。解釋是局部的且與模型無關，但其穩定性取決於取樣與核函數的選擇。
- **SHAP（Lundberg 與 Lee，2017）。** 特徵 \(i\) 的 Shapley 值為
  \[
  \phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N|-|S|-1)!}{|N|!}\,\bigl[v(S \cup \{i\}) - v(S)\bigr],
  \]
  其中 \(N\) 是特徵集合，\(v(S)\) 是只知道 \(S\) 中特徵時模型的期望輸出。Lundberg 與 Lee 將數種既有方法統一於這個可加形式之下，並提出高效的估計器。基於 Shapley 的預測歸因更早已由 Štrumbelj 與 Kononenko（2014）用於解釋預測。

## 結果

這些方法主要以公理與健全性檢查來驗證，而非單一基準。Sundararajan 等人（2017）顯示積分梯度滿足其提出的公理；Lundberg 與 Lee（2017）顯示 SHAP 家族在可加歸因下統一了數種既有方法。Ribeiro 等人（2016）以使用者研究評估 LIME，檢驗解釋是否幫助人們決定是否信任分類器。Adebayo 等人（2018）以隨機化模型權重與資料標籤來檢驗顯著性方法：數種廣泛使用的梯度型地圖在模型為隨機時看起來相似，表示它們並不取決於模型所學到的內容。

## 限制

- **健全性。** 某些歸因地圖在很大程度上獨立於已訓練的模型，因此看起來有資訊量，卻未反映模型行為（Adebayo 等人，2018）。
- **對基準的依賴。** 積分梯度與 SHAP 取決於參考輸入或背景分布，解釋會隨此選擇而改變。
- **相關特徵。** 當特徵彼此相關時，Shapley 式的值可能歸功於模型並未使用的特徵，因為此方法會評估不太可能出現的輸入組合。
- **因果。** 高歸因表示在所選擾動下，模型輸出依賴該特徵，而非現實世界結果的因果來源。
- **過度信任。** 解釋可能使使用者更信任模型，卻未使其更準確。見[人機互動](../human-ai-interaction/index.md)。

## 關聯

歸因是[可解釋性](index.md)中的解釋工具之一，與探測及機制方法並列。它在公平性上的用途見[公平性定義](../ethics/fairness-definitions.md)，因為歸因可以顯示受保護屬性或其代理變數驅動了某個決策。顯著性圖原本為卷積網路而發展，見 [CNN](../../theory/models/cnn/index.md)，後來也延伸至 Transformer，見 [Transformer](../../theory/models/transformer/index.md)。[探測分類器](probing.md)回答的則是不同的問題：存在哪些資訊，而非哪些輸入驅動了某個決策。

## 應用

- 除錯影像分類器，檢查它們關注的是物件還是背景線索。
- 向受影響的個人解釋信貸、保險或招募決策，因為法規要求提供理由。
- 在部署前，於表格與臨床模型中找出捷徑特徵。
- 將語言模型的輸出歸因到輸入詞元，以檢視模型。

## 未解問題

- **忠實性指標。** 對所有模型類別而言，尚無一套公認的量化測試能區分忠實與不忠實的歸因。
- **基準與分布。** 如何選擇對所提問題有意義的參考。
- **生成式與推理模型的歸因。** 長篇輸出與多步驟計算使「一個輸出對應一個歸因」的框架難以套用。

## 參考文獻

### 開創性論文

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. *Proceedings of the ICLR 2014 Workshop*. https://arxiv.org/abs/1312.6034 — 為影像分類器引入基於梯度的顯著性圖。
- Bach, S., Binder, A., Montavon, G., Klauschen, F., Müller, K.-R. & Samek, W. (2015). On Pixel-Wise Explanations for Non-Linear Classifier Decisions by Layer-Wise Relevance Propagation. *PLOS ONE*, 10(7), e0130140. https://doi.org/10.1371/journal.pone.0130140 — 將相關性分數逐層反向傳播，以將預測歸因到輸入像素。
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). Learning Important Features Through Propagating Activation Differences. *Proceedings of ICML 2017*. https://arxiv.org/abs/1704.02685 — 提出 DeepLIFT，相對於參考啟動值來歸因輸出。
- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — 提出積分梯度，以及敏感性與實作不變性公理。
- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *Proceedings of KDD 2016*. https://arxiv.org/abs/1602.04938 — 提出 LIME，為任何分類器提供局部代理解釋。
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — 提出 SHAP，在 Shapley 值下統一可加特徵歸因方法。
- Štrumbelj, E. & Kononenko, I. (2014). Explaining prediction models and individual predictions with feature contributions. *Knowledge and Information Systems*, 41(3), 647–665. https://doi.org/10.1007/s10115-013-0679-x — 以 Shapley 值解釋一般模型的個別預測。
- Adebayo, J., Gilmer, J., Muelly, M., Goodfellow, I., Hardt, M. & Kim, B. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — 顯示數種顯著性方法無法通過隨機化檢驗。

### 綜述與教科書

- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — 免費線上書籍，以範例涵蓋歸因、Shapley 值與代理模型。

## 延伸學習

- [SHAP 文件](https://shap.readthedocs.io/) — 基於 Shapley 歸因的開源實作與教學。
- [Captum](https://captum.ai/) — 實作積分梯度、DeepLIFT 等方法的 PyTorch 函式庫。
