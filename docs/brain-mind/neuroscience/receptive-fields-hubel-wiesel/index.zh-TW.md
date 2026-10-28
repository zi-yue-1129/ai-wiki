---
translation_reviewed: 2026-10-28
---

# 單一神經元記錄與視覺皮質（Hubel & Wiesel, 1962）

貓視覺皮質的單一神經元記錄顯示，細胞對定向邊緣有反應。

## 問題

視覺皮質如何從落在視網膜上的光，建立邊緣與形狀的表徵？

## 核心想法

在麻醉貓的視覺皮質中記錄單一神經元，同時呈現不同位置與方向的光點與光條。神經元被分為簡單細胞（具有分開的亮、暗子區，對特定方向的邊緣有反應）與複雜細胞（在較大區域內任何位置的該方向邊緣都有反應）。

## 方程式或演算法


  1. 在特定位置與方向呈現刺激。
  2. 記錄神經元的放電。
  3. 根據反應繪製感受野。
  4. 依反應型態對細胞分類。

## 結果

複雜細胞似乎匯集簡單細胞的輸出，這種階層結構啟發了後來的階層式卷積視覺模型。

## 限制

實驗使用麻醉貓，所描述的階層是一種模型；後續研究發現細胞類型比這兩類更多樣。

## 連結

- 母頁：[神經科學基礎](../index.md)
- 同一主題的另一方法：[多巴胺的獎勵預測誤差](../dopamine-reward-prediction-error/index.md)

## 參考文獻

### 開創性論文

- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — 發現具方向選擇性的簡單細胞與複雜細胞，是階層式視覺模型的生物學靈感來源。
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — 顯示多巴胺神經元發出的是獎賞預測誤差訊號，將強化學習與大腦連結起來。
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2787 — 提出大腦會最小化預測誤差，為感知、行動與學習提供統一框架。
- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識訓練的深度網路，能預測高階視覺皮質的神經反應。

### 綜述與教科書

- Neuroscience Online: An Electronic Textbook for the Neurosciences. Department of Neurobiology and Anatomy, UTHealth McGovern Medical School. https://nba.uth.tmc.edu/neuroscience/ — 免費、開放取用的神經科學電子教科書。
