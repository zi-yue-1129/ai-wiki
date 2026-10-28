---
translation_reviewed: 2026-10-28
---

# 保險與精算科學

保險把許多人的不確定損失集中起來，讓每個人只需支付可預期的保費。精算科學提供計算這些保費的統計基礎，以及為尚未給付的理賠所提列的準備金。機器學習如今已進入費率訂定、理賠處理與詐欺偵測，而這些用途都引發了公平性與監理審查的問題。

## 概述

保險人承諾賠付尚未發生的損失，因此其核心工作是事先估計這些損失。對單一保單而言，預期成本是理賠頻率（理賠發生的頻繁程度）乘以理賠嚴重度（每件理賠平均的金額）。保費再加上費用、利潤與資本的附加保費。另外，保險人還須為已經發生但尚未結案的損失提列準備金。

精算師用表格與迴歸來做這些估計，已超過一個世紀。古典的廣義線性模型仍是費率表的標準工具，而提升樹與神經網路正逐漸與之並行使用。保險定價比許多其他應用受到更多限制：價格必須能向監理機關與客戶說明，而且不得因受保護的特徵而產生歧視。金融背景請見[金融](../finance/index.md)。公平性的問題則連結到[倫理與公平](../../society/ethics/index.md)。

## 關鍵概念

- **純保費**：每張保單的預期理賠成本，是價格的核心，尚未加上附加保費。
- **頻率與嚴重度**：每單位曝險的理賠件數，以及每件理賠的平均成本。
- **費率因子**：用來區分不同價格的投保人或車輛特徵，例如年齡、車種或地區。
- **逆選擇與道德風險**：投保人通常比保險人更了解自身的風險，而且保障可能改變人的行為。
- **代理歧視**：即使模型從未以受保護特徵作為輸入，仍可能從相關的特徵中推斷出該特徵。
- **按用量計費保險**：部分保費依據實際測量的行為計算，通常由車聯網裝置或手機應用程式記錄。

## 運作方式

定價團隊通常分別為理賠件數與理賠成本擬合一個模型，再將兩者結合成費率表。流程如下。

```mermaid
flowchart LR
  A[保單與理賠資料] --> B[頻率模型]
  A --> C[嚴重度模型]
  B --> D[每張保單的預期理賠]
  C --> D
  D --> E[加上費用與資本的附加保費]
  E --> F[費率表、審查與核定]
```

若理賠件數與理賠成本互相獨立，純保費即等於 $\mathbb{E}[N]\,\mathbb{E}[X]$，也就是預期理賠件數乘以單件理賠的預期成本。許多保險人改為直接以 Tweedie 分布為總理賠成本建模。其在零點的質量涵蓋沒有理賠的保單，連續的正值部分則涵蓋實際發生的理賠成本。詳細說明見[廣義線性模型](glm-pricing/index.md)頁面。

理賠處理是另一條流程。損失通報後，保險人要決定快速結案、轉交專員，或是調查可能的詐欺。模型會為每件理賠評估預期成本與可疑程度，使人力投入在最需要的地方。詐欺偵測本身是一個歷史悠久的統計問題。Bolton 與 Hand 的回顧介紹了詐欺偵測所用的統計工具，並指出詐欺者具有適應性，因此偵測器必須持續更新。

## 關鍵方法

下表比較三種代表性方法，每一種都有專屬頁面。

| 方法 | 在保險中的角色 | 區別之處 |
|---|---|---|
| [廣義線性模型](glm-pricing/index.md) | 理賠件數與成本的標準費率模型 | 效果透明且為乘法形式，但只限於連結尺度上的線性項 |
| [LocalGLMnet](localglmnet/index.md) | 保留類似 GLM、可解釋形式的神經網路 | 係數隨保單而變；在一個資料集上，相較於一般神經網路，準確度略有犧牲 |
| [CARE-GNN](care-gnn/index.md) | 在評論、使用者或理賠網路上做詐欺偵測 | 學會忽略詐欺者用來偽裝的鄰居 |

## 相關連結

- **樹集成**。梯度提升樹廣泛用於保險人持有的表格資料。見[決策樹與集成方法](../../theory/paradigms/supervised/trees-and-ensembles/index.md)。Chen 與 Guestrin 的 XGBoost 論文介紹了其中最為人所知的實作之一。
- **線性模型**。廣義線性模型是傳統精算實務與現代機器學習之間的橋樑。見[線性模型與廣義線性模型](../../theory/paradigms/supervised/linear-models/index.md)。
- **可解釋性**。Rudin 主張，高風險決策應使用本身即可解釋的模型，而非事後解釋不透明的模型。見[可解釋性](../../society/interpretability/index.md)。
- **圖**。詐欺集團與共享屬性的網路都是圖，這也是[圖神經網路](../../theory/models/gnn/index.md)會出現在理賠相關段落的原因。
- **大腦與心智**。保險是人們每天在風險下做決策的場景。Kahneman 與 Tversky 的展望理論描述了偏離期望值推理的系統性現象，包括高估小機率事件。這關係到購買者如何評估小風險與保費變動。見[啟發法與偏誤](../../brain-mind/cognitive-science/heuristics-and-biases/index.md)。

## 應用

### 費率訂定

車險、房屋險與壽險長期以來都以廣義線性模型建立的費率表定價，並以保單層級的紀錄擬合，再由定價精算師審查。機器學習則用來測試並改進這些費率表，並找出人工建立的模型可能遺漏的交互作用。

### 車聯網與按用量計費保險

車聯網資料，例如里程、速度、煞車與時段，讓保險人可以依據實際測量的駕駛行為定價，而不必依賴年齡等代理變數。Huang 與 Meng 利用車聯網駕駛資料進行汽車保費的費率分級；Li 等人則將可解釋的機器學習應用於車聯網資料，以研究按用量計費保險的駕駛風險。車聯網也引發了關於持續位置資料之隱私與同意的問題。

### 理賠分流與詐欺偵測

理賠分流模型依據預期成本與可疑程度將理賠分派出去。詐欺偵測器則結合監督式分類器與網路分析，因為有組織的詐欺會在理賠人、修車廠與仲介之間形成連結。CARE-GNN 方法是在評論詐欺資料上測試，而非保險資料，因此將其用於理賠網路屬於推論延伸，並非論文中的結果。

### 公平性與反歧視限制

保險價格可能因合理的風險理由而在不同群體之間有所差異，也可能透過代理變數而產生差異。把受保護的屬性從輸入中移除，並不能消除代理效應。Lindholm 等人提出一個多任務神經網路，可產生不受代理歧視影響的價格，並且在受保護特徵只有部分紀錄的情況下也能訓練。Kleinberg 等人則指出，當各群體的基礎比率不同時，數個公平性準則無法同時成立。形式化的結果見[公平性定義](../../society/ethics/fairness-definitions.md)頁面。Charpentier 的專書則全面討論保險中的偏誤、歧視與公平性。

### 監理機關對定價模型的審查

許多司法管轄區的監理機關都會審查費率因子與定價模型。它們要求保險人為每一項差異化提出理由，並證明其不是以受保護特徵為依據。由此產生兩個張力。足以達到準確度的複雜模型，往往難以解釋；而要檢測模型是否對群體產生差異，可能需要保險人不被允許收集的受保護屬性資料。規定因國家與險種而異，因此定價團隊通常以其所面對最嚴格的當地要求作為設計依據。

## 未解問題

- 當受保護特徵缺漏時，應如何權衡準確度與公平性？Lindholm 等人的部分資訊方法是一種答案，但其成本尚未被充分衡量。
- LocalGLMnet 等可解釋架構能否在日常費率資料上達到黑箱模型的準確度，而監理機關是否會接受其解釋？
- 詐欺標籤稀少，而詐欺者會不斷調整。當錯誤指控落在誠實的理賠人身上時，應如何評估偵測器？
- 重大損失很罕見，因此其分布取決於資料很少能檢驗的尾部假設。

## 參考文獻

### 開創性論文

- Nelder, J. A. & Wedderburn, R. W. M. (1972). Generalized Linear Models. *Journal of the Royal Statistical Society, Series A*. https://doi.org/10.2307/2344614 — 介紹廣義線性模型，具有連結函數，並以跨分布共用的擬合程序為基礎，是多數保險費率的理論根據。
- Smyth, G. K. & Jørgensen, B. (2002). Fitting Tweedie's Compound Poisson Model to Insurance Claims Data: Dispersion Modelling. *ASTIN Bulletin*. https://doi.org/10.2143/ast.32.1.1020 — 將雙重廣義線性模型應用於 Tweedie 理賠資料，同時對離散程度與平均數建模。
- Richman, R. & Wüthrich, M. V. (2021). LocalGLMnet: interpretable deep learning for tabular data. arXiv. https://arxiv.org/abs/2107.11059 — 一種具有類似 GLM 加法結構的神經網路，其係數取決於輸入，並在汽車保險資料上測試。
- Lindholm, M. et al. (2022). A multi-task network approach for calculating discrimination-free insurance prices. arXiv. https://arxiv.org/abs/2207.02799 — 提出一種避免代理歧視的神經網路，可在受保護屬性部分缺漏的情況下訓練。
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2016). Inherent Trade-Offs in the Fair Determination of Risk Scores. arXiv. https://arxiv.org/abs/1609.05807 — 指出當基礎比率不同時，跨群體的校準與平衡一般無法同時成立，這是以風險為基礎之定價的核心結果。
- Dou, Y. et al. (2020). Enhancing Graph Neural Network-based Fraud Detectors against Camouflaged Fraudsters. *CIKM*. https://arxiv.org/abs/2008.08692 — 介紹 CARE-GNN，這是一種在聚合前先過濾偽裝鄰居的詐欺偵測器。
- Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *KDD*. https://arxiv.org/abs/1603.02754 — 描述一個廣泛用於表格資料的梯度提升樹系統。
- Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. *Econometrica*. https://doi.org/10.2307/1914185 — 提出人們以參考點衡量結果，並且高估小機率事件的看法。

### 綜述與教科書

- Ohlsson, E. & Johansson, B. (2010). *Non-Life Insurance Pricing with Generalized Linear Models*. Springer. https://doi.org/10.1007/978-3-642-10791-7 — 面向實務的教科書，說明如何以 GLM 建立非壽險費率。
- Wüthrich, M. V. & Merz, M. (2023). *Statistical Foundations of Actuarial Learning and its Applications*. Springer. https://doi.org/10.1007/978-3-031-12409-9 — 涵蓋精算資料的 GLM、神經網路與樹方法，並附程式碼。
- Wüthrich, M. V. & Buser, C. (2017). Data Analytics for Non-Life Insurance Pricing. SSRN. https://doi.org/10.2139/ssrn.2870308 — 關於非壽險定價資料、GLM 與樹模型的講義。
- Charpentier, A. (2024). *Insurance, Biases, Discrimination and Fairness*. Springer. https://doi.org/10.1007/978-3-031-49783-4 — 以專書篇幅說明偏誤與歧視如何在保險定價中產生，以及如何評估公平性。
- Bolton, R. J. & Hand, D. J. (2002). Statistical Fraud Detection: A Review. *Statistical Science*. https://doi.org/10.1214/ss/1042727940 — 回顧詐欺偵測的統計工具，涵蓋信用卡、電信與電腦入侵等詐欺，以及適應性詐欺者如何規避偵測器。

### 文章與文件

- Huang, Y. & Meng, S. (2019). Automobile insurance classification ratemaking based on telematics driving data. *Decision Support Systems*. https://doi.org/10.1016/j.dss.2019.113156 — 利用車聯網駕駛紀錄，為汽車保費費率分級。
- Li, H.-J. et al. (2023). Driving risk prevention in usage-based insurance services based on interpretable machine learning and telematics data. *Decision Support Systems*. https://doi.org/10.1016/j.dss.2023.113985 — 將可解釋的機器學習應用於車聯網資料，以評估按用量計費保險的駕駛風險。
- Rudin, C. (2018). Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead. arXiv. https://arxiv.org/abs/1811.10154 — 主張高風險決策應使用本身即可解釋的模型，並舉例說明刑事司法與醫療的應用。
