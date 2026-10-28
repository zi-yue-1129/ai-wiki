---
translation_reviewed: 2026-10-28
---

# 多巴胺的獎勵預測誤差（Schultz, Dayan & Montague, 1997）

多巴胺神經元訊號的是預期獎勵與實得獎勵之間的差異。

## 問題

中腦多巴胺神經元在動物學習獎勵的過程中傳遞什麼訊號？

## 核心想法

多巴胺神經元對未預期的獎勵有反應，隨著學習進行，反應會移到最早的預測線索上。此型態符合時序差分誤差，即實際獲得的獎勵減去預測的獎勵。

## 方程式或演算法

（採用現代符號）\(\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)\)。

## 結果

在猴子身上，未預期獎勵使多巴胺放電增加；學習後，反應移到預測線索上；預期獎勵未出現時，放電下降。

## 限制

記錄來自數量有限的猴子與任務。後續研究對多巴胺是否只編碼預測誤差、還是也包含顯著性等訊號，仍有爭論。

## 連結

- 母頁：[神經科學基礎](../index.md)
- 同一主題的另一方法：[視覺皮質的感受野](../receptive-fields-hubel-wiesel/index.md)

## 參考文獻

### 開創性論文

- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — 發現具方向選擇性的簡單細胞與複雜細胞，是階層式視覺模型的生物學靈感來源。
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — 顯示多巴胺神經元發出的是獎賞預測誤差訊號，將強化學習與大腦連結起來。
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2787 — 提出大腦會最小化預測誤差，為感知、行動與學習提供統一框架。
- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識訓練的深度網路，能預測高階視覺皮質的神經反應。

### 綜述與教科書

- Neuroscience Online: An Electronic Textbook for the Neurosciences. Department of Neurobiology and Anatomy, UTHealth McGovern Medical School. https://nba.uth.tmc.edu/neuroscience/ — 免費、開放取用的神經科學電子教科書。
