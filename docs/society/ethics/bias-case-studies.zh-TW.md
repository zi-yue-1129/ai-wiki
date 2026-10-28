---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - applications/healthcare
  - applications/law
tags:
  - bias
  - fairness
  - audits
  - case studies
aliases:
  - 演算法偏見案例
  - 算法偏見案例研究
  - Algorithmic bias case studies
  - COMPAS
  - Gender Shades
---

# 演算法偏見案例研究

已有數個已部署的系統被仔細研究，足以顯示偏見如何產生、如何被量測，以及量測方式本身如何受到爭議。本頁回顧四個有完整記錄的案例，其中一個涉及語言模型。對每個案例，我們都問：量測了什麼、爭議的焦點為何、這個案例教會了領域什麼。案例之所以有用，是因為它們具體；公平性的數學則在[公平性定義](fairness-definitions.md)中討論。

## 概述

偏見案例有共同的結構。某系統被設計來預測或排序某事，訓練資料反映了過去的決策或取樣不均，然後系統以一個無法反映某些群體所受傷害的指標來評估。事後的爭議往往不只是關於系統，也關於指標。因此，案例研究要問兩個問題：系統對誰、在什麼地方出錯，以及用什麼標準來判斷。

## 核心概念

- **各群體錯誤率差異**：模型對某一群體犯的錯比另一群體多，這未必等同於不平等對待。
- **代理目標**：用來替代所關心量的可量測變數。當代理變數在不同群體中的意義不同，模型就會繼承這種差異。
- **稽核**：由外部方對已部署系統所做的評估，使用一組定義好的群體與指標。稽核取決於取得的存取權限，以及所選的群體。

## 案例一：再犯風險分數（COMPAS）

COMPAS 是一套商業工具，用來估計被告再次遭逮捕的風險，曾在美國數個司法管轄區用來輔助保釋與量刑決定。2016 年，記者以佛羅里達州布勞沃德郡兩年的結果分析其分數，並報導黑人被告的偽陽性率高於白人被告。開發者對此分析提出異議。

Chouldechova（2017）以形式化方式分析這類工具。她證明，當各群體的再犯基礎比率不同時，這些公平性準則無法同時被滿足，並將此結果應用於相關的再犯風險工具。因此，這場爭議未必是任一方分析的單純錯誤。雙方各自選擇了不同的公平性準則，而這些準則無法全部成立。這是本案例的主要教訓，也是[公平性定義](fairness-definitions.md)在實務中重要的原因。

## 案例二：性別辨識（Gender Shades）

Buolamwini 與 Gebru（2018）建立了一個在膚色與性別上平衡的基準資料集，並用它測試三個商業性別辨識系統。摘要報告，膚色較深的女性錯誤率高達 34.7%，而膚色較淺的男性最大錯誤率為 0.8%。

後續研究 Raji 與 Buolamwini（2019）探討公開點名商業 AI 產品有偏見的效能結果所產生的影響，這正是本案例提出的後續問題。

## 案例三：健康風險分數

Obermeyer 等人（2019）研究美國醫療體系廣泛使用的一套演算法，該演算法用來決定哪些病人應獲得額外照護。該演算法預測未來的醫療成本，並以成本作為健康需求的代理變數。由於相同病況的黑人病患在過去花費的醫療資源較少，在相同的風險分數下，黑人病患的病情明顯比白人病患嚴重。作者報告，重新設計演算法使其不再以成本作為需求的代理變數，可降低種族偏見。

這個案例顯示，模型對其宣稱目標可以相當準確，卻仍然有偏見，因為目標本身帶有就醫機會不平等的歷史。它屬於量測偏誤的案例，而不是資料量不足的案例。

## 案例四：語言模型的刻板印象與方言偏見

大型語言模型會重現訓練文本中存在的刻板印象。Bender 等人（2021）討論極大型語言模型所帶來的風險，如其標題所示。Hofmann 等人（2024）研究方言。其預印本報告，語言模型對非裔美國英語使用者持有隱性刻板印象，其負面程度超過實驗中記錄到的任何人類刻板印象，並將此與就業能力及犯罪判斷等決策連結起來。

## 本案例教會我們什麼

- **依群體量測，並說明是哪些群體。** 整體準確率會掩蓋真正重要的失敗。
- **檢查目標。** 代理標籤可能編碼了模型本應避免的不平等。
- **預期指標會衝突。** 不同立場可能各自對於不同的準則是正確的。
- **公開點名是問責的一種機制。** 公開有偏見的結果是否促成改變，是 Raji 與 Buolamwini（2019）探討的問題。

## 關聯

本案例使用[公平性定義](fairness-definitions.md)中的公平性準則，以及[倫理與公平](index.md)中列出的偏見來源。稽核的一面在[演算法稽核與影響評估](algorithmic-auditing.md)中進一步討論。醫療與法律的應用見[醫療](../../applications/healthcare/index.md)與[法律](../../applications/law/index.md)。

## 應用

- 在部署前後稽核商業系統。
- 在採購系統時選擇評估群體與指標。
- 為方言與語言變體設計基準資料集。

## 未解問題

- **由誰決定目標與群體？** 多數案例的關鍵都在於開發者或稽核者所做的選擇，而這些選擇並不中立。
- **語言模型的偏見能否推廣？** 隱性方言偏見已在特定模型與任務上被證明；這個結果能延伸到多廣的系統範圍，仍是活躍的問題。
- **稽核能改變行為到什麼程度？** Raji 與 Buolamwini（2019）探討公開點名有偏見結果的影響；稽核更廣泛的效果仍是未解的問題。

## 參考文獻

### 開創性論文

- Buolamwini, J. & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *Proceedings of the 1st Conference on Fairness, Accountability and Transparency (PMLR 81)*. https://proceedings.mlr.press/v81/buolamwini18a.html — 稽核三個商業性別分類器，依膚色與性別檢視，並報告錯誤率的大幅差距。
- Raji, I. D. & Buolamwini, J. (2019). Actionable Auditing: Investigating the Impact of Publicly Naming Biased Performance Results of Commercial AI Products. *Proceedings of AIES 2019*. https://doi.org/10.1145/3306618.3314244 — 探討公開點名商業 AI 產品有偏見的效能結果所產生的影響。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — 顯示在再犯盛行率因群體而異時，這些公平性準則無法同時被滿足。
- Obermeyer, Z., Powers, B., Vogeli, C. & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*, 366, 447–453. https://doi.org/10.1126/science.aax2342 — 顯示以成本為代理目標的健康管理演算法產生種族偏見，而改變目標可降低此偏見。
- Bender, E. M., Gebru, T., McMillan-Major, A. & Shmitchell, S. (2021). On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? *Proceedings of FAccT 2021*. https://doi.org/10.1145/3442188.3445922 — 討論超大型語言模型所帶來的風險，如其標題所示。
- Hofmann, V., Kalluri, P. R., Jurafsky, D. & King, S. (2024). AI generates covertly racist decisions about people based on their dialect. *Nature*, 633, 147–154. https://doi.org/10.1038/s41586-024-07856-5 — 報告語言模型中的隱性方言偏見，其刻板印象比記錄到的人類刻板印象更負面。

### 綜述與教科書

- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 免費教科書，以上述案例為範例說明這些公平性準則。

## 延伸學習

- Angwin, J. et al. (2016). Machine Bias. *ProPublica*. https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing — 對 COMPAS 分析與公司回應的新聞報導；建議與 Chouldechova（2017）一併閱讀。
