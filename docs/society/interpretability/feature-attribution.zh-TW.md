---
translation_reviewed: 2026-10-28
---

# 特徵歸因：SHAP、LIME 與顯著性

特徵歸因方法會為每個輸入特徵給出一個分數，表示它對某一次預測貢獻了多少。這一族方法包括以梯度為基礎的顯著性圖、積分梯度、LIME 等擾動方法，以及 SHAP 等 Shapley 值方法。它們的輸出容易閱讀，但其中數種方法已被證明未能通過基本檢驗。

## 概述

以一個訓練好的模型與一筆輸入為例。歸因方法會為每個輸入特徵（一個像素、一個詞元 或表格中的一欄）回傳一個數字，說明該特徵相對於某個參照，把輸出推向預測類別的程度。歸因是局部的：它解釋的是單一決策，而不是整個模型。它屬於[可解釋 AI](index.md)的範疇；而[機械式可解釋性](mechanistic-interpretability.md)中的電路研究，則是在問哪些內部單元負責執行計算。

兩大家族佔據主流。梯度方法問的是，輸入稍微移動時輸出如何改變；擾動與賽局理論方法問的是，移除或平均掉某些特徵時輸出如何改變。

## 核心概念

- **基線（參照輸入）**：對一個特徵而言「不存在」是什麼意思，例如全黑的影像或零向量的嵌入。多數歸因值都是相對於它來衡量的。
- **完備性**：各項分數加總後，等於輸入的輸出與基線的輸出之差。積分梯度與 Shapley 值具有此性質；單純的梯度圖則沒有。
- **Shapley 值**：一個特徵對其他特徵所有子集合的平均邊際貢獻，源自合作賽局理論（Shapley, 1953）。

## 運作方式

**梯度。** Simonyan et al. (2013) 以類別分數對輸入的梯度（取絕對值）作為顯著性圖。Grad-CAM 則將最後一個卷積層的梯度依通道在空間上取平均，產生粗略的熱圖（Selvaraju et al., 2017）。

**積分梯度。** Sundararajan et al. (2017) 沿著從基線 $x'$ 到輸入 $x$ 的直線路徑對梯度積分：

$$\mathrm{IG}_i(x) = (x_i - x'_i)\int_0^1 \frac{\partial F\big(x' + \alpha(x - x')\big)}{\partial x_i}\,d\alpha$$

各項歸因加總為 $F(x) - F(x')$，因此基線的選擇決定了結果的意義。

**LIME。** Ribeiro et al. (2016) 對輸入取樣出擾動後的版本（例如移除部分詞語的句子），依其與原始輸入的相似度加權，並把一個稀疏線性模型 $g$ 擬合到黑箱的輸出上：

$$\xi(x) = \arg\min_{g \in G}\; \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

其中 $\pi_x$ 衡量鄰近程度，$\Omega$ 懲罰複雜度。$g$ 的係數即為解釋。

**Shapley 值（SHAP）。** 特徵 $i$ 的 Shapley 值為

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N|-|S|-1)!}{|N|!}\,\big[v(S \cup \{i\}) - v(S)\big]$$

Lundberg & Lee (2017) 證明，LIME、DeepLIFT 及相關方法都是可加性的特徵歸因，而且在這類方法中，只有 Shapley 值同時滿足局部準確性、缺失性與一致性。精確的加總包含指數多項。TreeSHAP 能在多項式時間內為樹集成精確計算它（Lundberg et al., 2020）。

## 關鍵方法

下表比較主要方法。每種方法都有已知的弱點。

| 方法 | 想法 | 已知弱點 |
|---|---|---|
| 梯度顯著性（Simonyan et al., 2013） | 類別分數對輸入的梯度 | 雜訊多，且對輸入的微小變化敏感 |
| Grad-CAM（Selvaraju et al., 2017） | 卷積層上依類別加權的激活圖 | 解析度粗；只定義於卷積網路 |
| DeepLIFT（Shrikumar et al., 2017） | 由參照激活向後傳播激活差異 | 結果取決於參照激活 |
| 積分梯度（Sundararajan et al., 2017） | 沿著從基線出發的路徑平均梯度 | 取決於基線與路徑 |
| LIME（Ribeiro et al., 2016） | 擬合到擾動樣本上的局部稀疏線性替代模型 | 結果隨取樣而變，且可能被操縱（Slack et al., 2020） |
| SHAP（Lundberg & Lee, 2017） | 某個價值函數的 Shapley 值 | 精確計算成本呈指數增長；必須選定價值函數 |

**合理性檢查。** Adebayo et al. (2018) 詢問顯著性圖是否取決於模型學到了什麼。當訓練好的權重被逐層換成隨機權重時，數種常用方法產生的圖幾乎沒有改變。Hooker et al. (2019) 移除每種方法排名最高的特徵後重新訓練，發現許多方法的表現不比隨機排序好。

**Transformer。** 注意力權重常被當作解釋來讀，但 Jain & Wallace (2019) 發現，學到的注意力權重常與以梯度為基礎的重要性無關，而且不同的注意力分布可能得出相同的預測。Chefer et al. (2021) 則改為將相關性傳播穿過視覺 Transformer 的注意力層。對語言模型而言，以詞元嵌入為對象的梯度歸因相當普遍（Zhao et al., 2023）。

## 連結

- **腦與心智。** [基於顯著性的視覺注意力](../../brain-mind/attention-brain-machine/saliency-map/index.md)模型依特徵對比為影像位置評分，不需要梯度，也不需要訓練好的網路。兩者共用的名稱，掩蓋了兩條各自發展的脈絡。
- **梯度。** 梯度方法依賴[自動微分](../../theory/math/automatic-differentiation/index.md)來計算輸入的梯度。
- **機械式研究。** 歸因說明哪些輸入發揮了作用；[機械式可解釋性](mechanistic-interpretability.md)則說明哪些電路攜帶了這些資訊。

## 應用

- **除錯。** 歸因圖可能顯示模型依賴的是浮水印，而非物件本身。
- **表格式決策。** TreeSHAP 讓樹集成的精確 Shapley 歸因變得實用；樹集成常見於信用與臨床風險模型（Lundberg et al., 2020）。
- **醫學影像。** 展示給臨床人員的顯著性圖，需要先經過驗證，因為數種方法未能通過基本檢驗（Adebayo et al., 2018）。

## 開放問題

- **基準真相。** 對於一項預測，並不存在公認正確的歸因。合理性檢查與移除式基準只能檢驗部分性質，無法決定哪種方法才是對的。
- **參照的選擇。** Janzing et al. (2020) 主張，被移除的特徵應以無條件期望值取代，而這項選擇會改變歸因結果。
- **操縱。** 可以把有偏見的分類器包裝起來，使 LIME 與 SHAP 的解釋看起來不帶偏見（Slack et al., 2020）。稽核必須檢驗模型本身，而不能只看解釋。
- **因果意涵。** 歸因顯示的是模型用了什麼，而非世界中什麼導致了結果。

## 參考文獻

### 開創性論文

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2013). *Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps*. arXiv. https://arxiv.org/abs/1312.6034 — 為影像分類器定義以梯度為基礎的類別顯著性圖。
- Sundararajan, M., Taly, A. & Yan, Q. (2017). *Axiomatic Attribution for Deep Networks*. ICML. https://arxiv.org/abs/1703.01365 — 提出積分梯度，其推導來自兩條歸因公理。
- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). *"Why Should I Trust You?": Explaining the Predictions of Any Classifier*. KDD. https://arxiv.org/abs/1602.04938 — 提出 LIME，一種擬合到擾動樣本上的局部稀疏線性替代模型。
- Lundberg, S. M. & Lee, S.-I. (2017). *A Unified Approach to Interpreting Model Predictions*. NeurIPS. https://arxiv.org/abs/1705.07874 — 把 LIME、DeepLIFT 等方法統一為可加性歸因，並提出 SHAP 值。
- Selvaraju, R. R., et al. (2017). *Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization*. ICCV. https://arxiv.org/abs/1610.02391 — 利用最後一個卷積層的梯度，產生特定類別的定位圖。
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). *Learning Important Features Through Propagating Activation Differences*. ICML. https://arxiv.org/abs/1704.02685 — 提出 DeepLIFT，將每個神經元的激活與參照激活相比較。
- Shapley, L. S. (1953). *A Value for n-Person Games*. In Kuhn & Tucker (eds.), *Contributions to the Theory of Games II*. Princeton University Press. https://doi.org/10.1515/9781400881970-018 — Shapley 值的原始定義，後來被應用於模型特徵。
- Adebayo, J., et al. (2018). *Sanity Checks for Saliency Maps*. NeurIPS. https://arxiv.org/abs/1810.03292 — 提出隨機化檢驗，顯示數種顯著性方法無法通過。
- Hooker, S., et al. (2019). *A Benchmark for Interpretability Methods in Deep Neural Networks*. NeurIPS. https://arxiv.org/abs/1806.10758 — 提出以移除特徵為基礎的基準，發現許多特徵重要性方法不比隨機好。
- Slack, D., et al. (2020). *Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods*. AIES. https://arxiv.org/abs/1911.02508 — 顯示有偏見的分類器如何被包裝，以通過 LIME 與 SHAP 的解釋。
- Janzing, D., Minorics, L. & Blöbaum, P. (2020). *Feature relevance quantification in explainable AI: A causal problem*. AISTATS. https://arxiv.org/abs/1910.13413 — 主張被移除的特徵應以無條件期望值取代，而非條件期望值。
- Chefer, H., Gur, S. & Wolf, L. (2021). *Transformer Interpretability Beyond Attention Visualization*. CVPR. https://arxiv.org/abs/2012.09838 — 透過注意力層計算 Transformer 的相關性，而非視覺化注意力權重。
- Jain, S. & Wallace, B. C. (2019). *Attention is not Explanation*. NAACL. https://arxiv.org/abs/1902.10186 — 發現學到的注意力權重常與以梯度為基礎的重要性量度無關。
- Lundberg, S. M., et al. (2020). *From local explanations to global understanding with explainable AI for trees*. Nature Machine Intelligence. https://doi.org/10.1038/s42256-019-0138-9 — 提出 TreeSHAP，一種針對樹集成、可在多項式時間內精確計算的方法。

### 綜述與教科書

- Zhao, H., et al. (2023). *Explainability for Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2309.01029 — 為基於 Transformer 的語言模型整理可解釋性技術的分類。
