---
translation_reviewed: 2026-10-28
---

# 公平性定義與不可能性結果

公平性定義是一條精確的規則，用來說明分類器或分數何時對人是公平的。當所比較的群體基礎比率不同時，幾個自然的定義無法同時成立，因此選擇其中一個，既是價值判斷，也是技術決定。

## 概述

在診斷出偏見之後（見[倫理與公平](index.md)），開發者仍須以公式說明「公平」的意思。已提出的答案常常彼此衝突。2016 與 2017 年的結果顯示，這種分歧不只是品味的問題：在常見條件下，主要的準則在數學上互不相容。

這些定義建立在[評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)中的錯誤率與校準度量之上。它們在刑事司法、信貸、醫療與招聘中的風險分數上最為重要。

## 關鍵概念

- **受保護屬性**（$A$）：例如種族或性別等特徵，在許多情境中決策不得依此區分。
- **結果**（$Y$）、**預測**（$\hat{Y}$）與**分數**（$S$）：真實目標、所做的決策，以及決策所依據的風險值。
- **基礎比率**：某群體中陽性案例所佔的比例，即 $P(Y=1 \mid A=a)$。
- **真陽性率與偽陽性率**：實際為陽性者被正確標記的比例，以及實際為陰性者被誤標為陽性的比例。
- **校準**：分數為 $s$ 時，無論此人屬於哪個群體，對應的陽性結果機率都相同。

## 運作方式

每個定義都是對受保護屬性、預測或分數，以及真實結果之間聯合分布的一項限制。多數定義描述的是群體之間的統計量，因此系統可能符合某項定義，卻仍然對特定的人不公平。這正是個體層級定義存在的原因。

限制通常可以在訓練之後施加。Hardt、Price 與 Srebro（2016）說明如何調整已學成的預測器，以滿足他們提出的準則。Corbett-Davies 等人（2017）發現，對於數種定義，最佳規則會對每個群體使用不同的門檻，且要付出公共安全上的代價。

### 不可能性結果

Kleinberg、Mullainathan 與 Raghavan（2016）將分數的三個條件形式化：各群體內的校準，以及陽性類與陰性類的平衡。他們證明，除了高度受限的特殊情況（即基礎比率相等，或預測器完美）之外，這三個條件無法同時成立。Chouldechova（2017）以偽陽性率（FPR）、偽陰性率（FNR）與陽性預測值（PPV）得到平行的結果。對任一群體而言，這三者由以下恆等式連結：

$$\mathrm{FPR} = \frac{p}{1-p}\cdot\frac{1-\mathrm{PPV}}{\mathrm{PPV}}\cdot(1-\mathrm{FNR})$$

其中 $p$ 為該群體的基礎比率。若兩個群體的 PPV 與 FNR 相等，但 $p$ 不同，則它們的偽陽性率必然不同。這正是 COMPAS 再犯預測工具公共辯論的形式核心：同一組分數分別以不同準則被辯護與批評。

## 關鍵方法

下表比較主要的定義。每一項都是一條限制，也各有其典型的弱點。

| 定義 | 要求 | 主要弱點 |
|---|---|---|
| 人口統計均等 | 每個群體的 $P(\hat{Y}=1 \mid A=a)$ 相同 | 忽略真實結果，因此可能迫使某一群體出現額外的偽陽性 |
| 機會平等（Hardt 等人，2016） | 真陽性率相等，即 $P(\hat{Y}=1 \mid Y=1, A=a)$ | 對偽陽性不加限制 |
| 機會均等化（Hardt 等人，2016） | 各群體的真陽性率與偽陽性率皆相等 | 當基礎比率不同時，與校準不相容 |
| 校準與預測均等 | $P(Y=1 \mid S=s, A=a) = s$，或 PPV 相等 | 當基礎比率不同時，與錯誤率相等不相容 |
| 個體公平（Dwork 等人，2012） | 相似的個體獲得相似的結果，依據某個相似度量 | 度量本身包含價值選擇 |
| 反事實公平（Kusner 等人，2017） | 在 $A$ 不同的反事實世界中，決策不變 | 依賴必須加以論證的因果模型 |

當分類器具有一定的判別能力，且基礎比率不同時，人口統計均等與機會均等化也會互相衝突：錯誤率相等時，群體之間陽性預測率的差距會與基礎比率的差距成比例。

### 以「不察覺」達成公平

把受保護屬性從輸入中移除，是最簡單的規則，也是實務上最常被提出的做法。但它往往不足夠，因為其他特徵（例如郵遞區號）可能帶有相同的資訊。Lipton、Chouldechova 與 McAuley（2018）指出，當其他特徵與群體歸屬相關時，即使學習過程在測試時對受保護屬性視而不見，仍可能實際造成待遇差異。反事實公平則透過詢問「若該屬性不同，決策會如何改變」來處理這個問題。

### 在定義之間做選擇

沒有任何定義是中立的。選擇首先取決於什麼算是傷害：某人被錯誤拒絕、某人被錯誤標記，還是分數對不同群體意義不同。基礎比率從何而來也很重要。若它們反映的是過去的歧視，等同的結果與等同的錯誤可能會彼此分離。Friedler、Scheidegger 與 Venkatasubramanian（2021）主張，適當的機制取決於其背後所採用的價值體系。Mitchell 等人（2021）則列出以預測為基礎的決策通常隱藏的各種假設。較務實的做法是：先說明傷害為何，挑選與之相符的準則，衡量其成本，並記錄所做的決定，以便日後受到質疑時可被檢視。

## 與其他主題的連結

- **評估。** 這些公平性準則，是[評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)中錯誤率與校準度量依群體切分後的條件。
- **倫理。** 偏見的來源，例如代理目標與歷史資料，見[倫理與公平](index.md)。本頁討論的是同一問題的形式面。
- **隱私。** 進行公平性稽核需要受保護屬性，但隱私規範可能限制其蒐集。見[隱私與資料保護](../privacy/index.md)。
- **腦與心智。** 基礎比率忽視，即在判斷某個案例時低估某類別有多常見，是人類判斷中的經典偏誤，因此人類決策者同樣面臨基礎比率的問題。見[捷思與偏誤](../../brain-mind/cognitive-science/heuristics-and-biases/index.md)。

## 應用

- **刑事司法。** 風險評估是研究最多的案例。Chouldechova（2017）說明，為何同一組分數可能符合某項準則，卻在另一項準則下失敗。Corbett-Davies 等人（2017）則研究這些限制的成本。
- **醫療。** Obermeyer 等人（2019）發現，一套廣泛使用的演算法會把與健康狀況較差的白人相同的風險等級給予黑人患者。問題出在其代理目標，即過去的醫療支出。
- **法律。** 數個法律體系區分有意針對某群體的差別待遇，以及在中立規則下結果對群體造成的不均等影響。上述統計定義與後者關係較為密切。見[法律](../../applications/law/index.md)。

## 開放問題

- 單一定義能否適用於所有決策，還是準則應依情境與所涉的傷害而定？
- 基礎比率若反映過去的不公義，應視為預測的依據，還是應加以修正的結果？
- 稽核需要受保護屬性，但隱私規範往往限制其蒐集。

## 參考資料

### 開創性論文

- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). *Fairness Through Awareness*. arXiv 預印本. https://arxiv.org/abs/1104.3913 — 透過任務相關的相似度量定義個體公平，並將統計均等與平權行動相連結。
- Hardt, M., Price, E. & Srebro, N. (2016). *Equality of Opportunity in Supervised Learning*. arXiv 預印本. https://arxiv.org/abs/1610.02413 — 提出機會平等與機會均等化，並說明如何調整預測器以滿足兩者。
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2016). *Inherent Trade-Offs in the Fair Determination of Risk Scores*. arXiv 預印本. https://arxiv.org/abs/1609.05807 — 證明除特殊情況外，校準與兩項平衡條件無法同時成立。
- Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. *Big Data*. https://doi.org/10.1089/big.2016.0047 — 以再犯分數說明，當盛行率不同時，偽陽性率、偽陰性率與陽性預測值無法在各群體間全部相等。
- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). *Counterfactual Fairness*. arXiv 預印本. https://arxiv.org/abs/1703.06856 — 以因果推論定義反事實公平，比較實際世界與反事實世界中的決策。
- Lipton, Z. C., Chouldechova, A. & McAuley, J. (2018). *Does mitigating ML's impact disparity require treatment disparity?* arXiv 預印本. https://arxiv.org/abs/1711.07076 — 指出當其他特徵與群體歸屬相關時，對群體視而不見的學習仍可能造成待遇差異。
- Corbett-Davies, S., Pierson, E., Feller, A., Goel, S. & Huq, A. (2017). Algorithmic decision making and the cost of fairness. arXiv 預印本. https://arxiv.org/abs/1701.08230 — 指出數種公平性限制需要依種族設定的門檻，且會犧牲公共安全。
- Obermeyer, Z., Powers, B., Vogeli, C. & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*. https://doi.org/10.1126/science.aax2342 — 將一套醫療管理演算法中的種族偏見，追溯至其所選用的代理目標。

### 綜述與教科書

- Mitchell, S., Potash, E., Barocas, S., D'Amour, A. & Lum, K. (2021). Algorithmic Fairness: Choices, Assumptions, and Definitions. *Annual Review of Statistics and Its Application*. https://doi.org/10.1146/annurev-statistics-042720-125902 — 整理各種公平性定義，以及以預測為基礎的決策背後的各項假設。
- Friedler, S. A., Scheidegger, C. & Venkatasubramanian, S. (2021). The (Im)possibility of fairness. *Communications of the ACM*. https://doi.org/10.1145/3433949 — 主張適當的公平性機制取決於所採用的價值體系。
