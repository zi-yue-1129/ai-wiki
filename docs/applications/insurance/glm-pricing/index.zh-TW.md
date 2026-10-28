---
translation_reviewed: 2026-10-28
---

# 保險定價的廣義線性模型（Nelder & Wedderburn 1972）

廣義線性模型（GLM）透過連結函數，將某個反應變數（例如理賠件數或理賠成本）的平均數與解釋變數的加權和相連。它是保險費率的標準工具，也是父頁面[保險與精算科學](../index.md)所介紹的方法之一。

## 概述

一般的線性迴歸假設反應變數為常態分布且變異數固定。保險資料兩者皆不符合：理賠件數是整數，多數保單沒有理賠，而理賠成本為正值且偏態。Nelder 與 Wedderburn（1972）將迴歸推廣，使反應變數可以服從指數族中的任何分布，並以連結函數把其平均數與線性預測子相連。Jørgensen（1987）進一步推廣為指數離散模型，加入離散參數，並涵蓋 Tweedie 族。

在費率工作中，通常採用對數連結。此時效果會相乘，因此每個係數都成為一個相對性，即某風險相對於基準水準被定價的倍數。這種乘法結構便於向監理人員與核保人員說明，也是此方法長期延用的主要原因。[Ohlsson 與 Johansson（2010）](https://doi.org/10.1007/978-3-642-10791-7)詳細描述了整套實務。

## 關鍵概念

- **線性預測子與連結函數**：$\eta_i = x_i^\top \beta$ 與 $g(\mu_i) = \eta_i$。採用對數連結時，$\mu_i = \exp(x_i^\top \beta)$。
- **曝險偏移項**：一張只承保半年的保單，理賠件數應約為整年的一半。這是透過在線性預測子中加入 $\log v_i$ 處理，其中 $v_i$ 為曝險。
- **相對性**：$\exp(\beta_j)$，即某個費率因子水準的乘法效果。
- **Tweedie 分布**：由伽瑪分布理賠構成的複合卜瓦松和，變異數為 $\mathrm{Var}(Y) = \phi\,\mu^{p}$，且 $1 < p < 2$。它在零點有質量，正值部分為連續分布，因此可以直接適用於每張保單的總成本。
- **離散參數建模**：讓離散參數 $\phi$ 依共變量而變，如雙重廣義線性模型。

## 運作方式

對理賠件數而言，常用的模型是採對數連結與曝險偏移項的卜瓦松 GLM。其參數以最大概似估計，等價於最小化卜瓦松偏差。擬合演算法為迭代加權最小平方法，即反覆求解加權迴歸，直到係數收斂。

費率的典型工作流程如下。

1. 為價格的每個部分選擇反應分布與連結：件數用卜瓦松，成本用伽瑪，總成本用 Tweedie。
2. 加入曝險偏移項，並將類別因子編碼為虛擬變數。
3. 以迭代加權最小平方法擬合模型，並以保留的資料檢查擬合情形。
4. 逐一檢驗交互作用與平滑項，例如年齡的樣條函數。
5. 將係數轉換為相對性，並將件數與嚴重度的相對性合併成費率表。

## 結果

Nelder 與 Wedderburn 的論文屬於架構性論文。其貢獻是提出涵蓋多種標準模型的單一擬合程序，而非基準測試結果。保險專屬的證據來自後來的應用研究。Smyth 與 Jørgensen（2002）重新檢視由彙總理賠資料建立的費率。依其摘要所述，對理賠成本的離散程度與平均數同時建模，可提高所估計費率的精確度；而且即使只記錄了總理賠成本、未記錄理賠件數，此方法仍然適用。

## 限制

- **連結尺度上的線性。** 非線性效果與交互作用必須人工指定，需要時間與專業。機器學習方法可以自動找出這些效果。
- **分布假設。** 錯誤的變異數函數，或與資料不符的分布族，即使平均數結構正確，仍會產生有偏差的費率。
- **人工特徵工程。** 預測能力很大程度來自分析師的選擇，因此結果取決於團隊。
- **透明不等於公平。** GLM 可以完全透明，但仍可能透過代理變數而對受保護特徵產生差異定價。審計問題在父頁面與[公平性定義](../../../society/ethics/fairness-definitions.md)中討論。

## 未解問題

- 在具有相同特徵的標準保險資料集上，GLM 在樣本外的預測準確度，相較於提升樹與可解釋神經網路會犧牲多少？
- 能否以更豐富的結構（例如地區的隨機效果）同時建模平均數與離散程度，同時不失去讓 GLM 費率能被接受的可讀性？

## 參考文獻

### 開創性論文

- Nelder, J. A. & Wedderburn, R. W. M. (1972). Generalized Linear Models. *Journal of the Royal Statistical Society, Series A*. https://doi.org/10.2307/2344614 — 介紹廣義線性模型，具有連結函數，並以跨分布共用的擬合程序為基礎。
- Jørgensen, B. (1987). Exponential Dispersion Models. *Journal of the Royal Statistical Society, Series B*. https://doi.org/10.1111/j.2517-6161.1987.tb01685.x — 將 GLM 的誤差族推廣為指數離散模型，此族涵蓋 Tweedie 分布。
- Smyth, G. K. & Jørgensen, B. (2002). Fitting Tweedie's Compound Poisson Model to Insurance Claims Data: Dispersion Modelling. *ASTIN Bulletin*. https://doi.org/10.2143/ast.32.1.1020 — 將雙重廣義線性模型應用於 Tweedie 理賠資料，同時對離散程度與平均數建模。

### 綜述與教科書

- Ohlsson, E. & Johansson, B. (2010). *Non-Life Insurance Pricing with Generalized Linear Models*. Springer. https://doi.org/10.1007/978-3-642-10791-7 — 面向實務的教科書，說明如何以 GLM 建立非壽險費率，包括因子選擇與驗證。
- Wüthrich, M. V. & Merz, M. (2023). *Statistical Foundations of Actuarial Learning and its Applications*. Springer. https://doi.org/10.1007/978-3-031-12409-9 — 說明 GLM 與神經網路在精算資料上的應用，並介紹其背後的擬合理論。
- Wüthrich, M. V. & Buser, C. (2017). Data Analytics for Non-Life Insurance Pricing. SSRN. https://doi.org/10.2139/ssrn.2870308 — 關於非壽險定價資料、GLM 與樹模型的講義。
