---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - applications/law
tags:
  - fairness
  - bias
  - impossibility results
aliases:
  - 公平性定義
  - 公平性不可能性定理
  - Fairness definitions
  - Impossibility of fairness
---

# 公平性定義與不可能性結果

公平性定義是對分類器或分數如何公平對待群體或個人的精確數學陳述。自然的定義有好幾種，而在真實資料上，它們通常無法同時滿足。本頁比較主要的定義，說明限制這些定義的不可能性結果，並說明選擇哪一種定義既是數學問題，也是價值判斷。

## 概述

設想一個模型預測貸款是否會被償還、被告是否會再犯，或病人是否需要額外照護。模型的輸出可能因性別、種族、年齡等受保護屬性而在群體之間有所不同。公平性定義提供一種方式，精確陳述在該情境下「平等對待」應當意味著什麼。每種定義都編碼了不同的直覺，而不可能性結果顯示：只要各群體的基礎比率不同，某些直覺就會互相衝突。

## 核心概念

- **受保護屬性** \(A\)：定義所要保護的群體身分，例如性別或種族。
- **結果** \(Y\) 與**預測** \(\hat{Y}\)：真實標籤與模型的決定。
- **分數** \(S\)：在套用門檻之前的預測機率或風險值。
- **基礎比率**：某群體中正類結果的比例，即 \(\Pr[Y=1 \mid A=a]\)。基礎比率常因底層資料生成過程的差異而不同。
- **群體公平與個體公平**：群體定義比較各群體之間的統計量；個體定義則要求相似的人獲得相似的結果。

## 運作方式

下表列出主要的準則。每一項都是對 \(A\)、\(Y\)、\(\hat{Y}\) 或 \(S\) 聯合分布的限制。

| 準則 | 條件 | 直覺 |
|---|---|---|
| 人口統計均等（demographic parity） | 對所有群體 \(a\)，\(\Pr[\hat{Y}=1 \mid A=a]\) 相等 | 正向決定的比率相等 |
| 機會均等（equal opportunity） | 對所有 \(a\)，\(\Pr[\hat{Y}=1 \mid Y=1, A=a]\) 相等 | 真陽性率相等 |
| 機會均衡（equalised odds） | 對所有 \(a\)，真陽性率與偽陽性率都相等 | 兩種結果的錯誤率都相等 |
| 預測值均等（predictive parity） | 對所有 \(a\)，\(\Pr[Y=1 \mid \hat{Y}=1, A=a]\) 相等 | 正向決定的精確率相等 |
| 群體內校準（calibration within groups） | 對所有 \(a\) 與 \(s\)，\(\Pr[Y=1 \mid S=s, A=a] = s\) | 分數 \(s\) 在每個群體中代表相同風險 |
| 個體公平（individual fairness） | 相似的個體獲得相似的輸出，相似度由任務專屬的度量定義 | 同樣的情況同樣對待 |
| 反事實公平（counterfactual fairness） | 在將 \(A\) 設為另一值的模型中，預測不變，且 \(A\) 對其他變數的因果效應保持不變 | 移除 \(A\) 的因果影響 |
| 不察覺屬性（fairness through unawareness） | \(\hat{Y}\) 不直接使用 \(A\) | 移除受保護屬性 |

**個體公平。** Dwork 等人（2012）要求兩個輸出分布之間的距離，不超過兩個個體在相似度度量下的距離。度量必須由某人選定，而這正是困難所在。

**機會均衡與機會均等。** Hardt、Price 與 Srebro（2016）定義了機會均衡，以及其較弱的形式機會均等，並展示如何用對各群體套用不同門檻、作用於固定分數的後處理規則來達成。

**不察覺屬性。** 從輸入中移除 \(A\) 是最簡單的政策，但其他特徵（郵遞區號、教育程度、消費紀錄）可能充當代理變數。Hardt 等人（2016）與 Dwork 等人（2012）都指出，模型即使從未看見受保護屬性，仍可能產生歧視。

### 不可能性結果

兩項結果顯示，當基礎比率不同且預測器並非完美時，主要的群體準則會彼此衝突。

- **Kleinberg、Mullainathan 與 Raghavan（2016）** 證明三項條件無法同時成立：群體內校準、正類的平衡（真陽性在各群體的平均分數相等），以及負類的平衡。其摘要指出，除了高度受限的特殊情況外，沒有任何方法能同時滿足這三項條件。
- **Chouldechova（2017）** 在二元預測中證明：當基礎比率不同時，預測值均等、偽陽性率相等與偽陰性率相等無法同時成立。她將此結果應用於 COMPAS 爭論中研究的風險評估工具。

實務上的結論是：模型可以是校準的，同時錯誤率卻不平等；或者錯誤率相等，但正向決定的精確率不平等。在這些結果之間做選擇，是在判斷哪一種傷害更重要。

### 強制執行準則的代價

Corbett-Davies 等人（2017）研究對風險導向決策規則施加公平性限制的代價。他們將公平性重新表述為受限最佳化：在滿足公平性限制的前提下最大化公共安全，並顯示對於數種過去的公平性定義，所得演算法會對公共安全造成代價。對實務者而言，重點是：公平性限制是有可量測副作用的政策，而不是無代價的微調。

## 主要方法

上述準則已在表中比較。每一項都是用來檢驗模型的條件，而非演算法。執行這些準則的主要方式包括：

- **前處理**：對訓練資料重新加權或重新抽樣，使基礎比率或特徵分布更平衡。
- **中途處理**：在訓練目標中加入公平性懲罰項或限制式。
- **後處理**：在訓練後調整決定，通常使用各群體專屬的門檻，如 Hardt 等人（2016）所示。

每一種執行方法都會在某個準則與準確率之間，或在不同準則之間取捨，因此應先決定定義，再選方法。

## 關聯

這些定義與 [倫理與公平](index.md) 中較廣的倫理討論相連，該頁列出了偏見的來源。它們也與[偏見案例研究](bias-case-studies.md)相關，不可能性結果解釋了為何對同一系統的審計可能得出相反結論。非歧視的法律框架是以結果來定義歧視，而非數學準則，因此將法律測試轉化為這些定義之一需要判斷；見 [法律、政策與治理](../governance/index.md)。

在機器學習的一側，這些定義是 Fairlearn 與 AIF360 等公平性工具箱的目標，它們實作了數種準則與緩解方法。

## 應用

- **信貸與放款**：貸方比較各群體的錯誤率與核准率，這可能同時涉及數種準則。
- **刑事司法風險評估**：COMPAS 爭議是校準與錯誤率準則指向不同方向的標準例子。
- **健康風險分數**：目標變數的差異（以成本而非需求為代理）可能破壞機會均等準則，即使模型對其所宣稱的目標相當準確。

## 未解問題

- **應採用哪一種準則？** 不可能性結果使這成為價值選擇。法律與監管常以結果來界定歧視，這可能與任何單一統計定義都不一致。
- **如何定義個體公平的相似度度量**，以及應由誰來設定。
- **交叉群體**：對每個屬性分別滿足的準則，對其組合不一定成立。
- **測量誤差與標籤偏誤**：這些準則假設標籤正確；當標籤本身有偏誤時，相等的錯誤率可能掩蓋不平等的傷害。

## 參考文獻

### 開創性論文

- Dwork, C. et al. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — 以任務專屬相似度度量上的 Lipschitz 條件引入個體公平。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 定義機會均等與機會均衡，並給出達成它們的後處理方法。
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://arxiv.org/abs/1609.05807 — 證明當基礎比率不同時，校準與平衡條件無法同時成立。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — 以再犯預測工具為例，顯示在基礎比率不同時，預測值均等與錯誤率平衡互不相容。
- Corbett-Davies, S., Pierson, E., Feller, A. & Goel, S. (2017). Algorithmic Decision Making and the Cost of Fairness. *Proceedings of KDD 2017*. https://doi.org/10.1145/3097983.3098095 — 將公平性重新表述為以公共安全為目標的受限最佳化，並以審前羈押決策為例。

### 綜述與教科書

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — 以同一個範例綜述並比較主要的公平性定義。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 免費教科書，涵蓋這些定義、其取捨與社會脈絡。

## 延伸學習

- [Fairlearn](https://fairlearn.org/) — 開源工具箱，提供公平性指標與緩解演算法。
- [AI Fairness 360](https://aif360.res.ibm.com/) — IBM 的開源公平性指標與演算法函式庫。
