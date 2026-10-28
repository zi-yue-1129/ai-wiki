---
translation_reviewed: 2026-10-28
---

# 可微分歸納邏輯程式設計（∂ILP）

∂ILP 以梯度下降從範例學習邏輯程式，而不採用古典歸納邏輯程式設計所用的離散搜尋。Evans 與 Grefenstette 於 2017 年以預印本形式提出，並於 2018 年正式發表。它是[神經符號 AI 概述](../index.md)中可微分邏輯的代表方法：所學得的規則仍然可讀，而學習過程能容忍雜訊。

## 概述

歸納邏輯程式設計（ILP）從範例與背景知識中學習邏輯規則。例如，給定祖孫配對的範例與父母關係的事實，ILP 系統可以恢復出「祖父母是父母的父母」這條規則。它的規則可讀，所需資料也少。它的弱點在於雜訊：一個標錯的範例就可能使離散搜尋偏離方向；另一個弱點是原始輸入（例如像素），ILP 無法直接使用。

Evans 與 Grefenstette 的框架同時處理這兩個弱點。它能解決 ILP 所適合的任務，並容忍訓練資料中的雜訊。由於它以反向傳播依似然目標訓練，也能接上神經網路，處理模糊的資料。[^1]

## 關鍵概念

- **背景知識（background knowledge）**：事先提供的事實與述詞，例如描述某個領域的關係。
- **子句（clause）**：具有頭部與本體的規則，例如*祖父母(X, Z) 若 父母(X, Y) 且 父母(Y, Z)*。
- **軟性前向鏈結（soft forward chaining）**：逐步推導事實，其中每個推導出的原子從其本體計算出介於 0 與 1 之間的真值。

## 運作方式

這個方法保留了 ILP 的骨架，並讓每一步都可微分。以下步驟是此類系統的一般架構；確切的運算子與訓練安排見論文。

1. **列舉候選子句**：在背景述詞上建立可能規則的範本集合。
2. **為子句加權。** 給每個候選一個可學習的權重，使程式成為子句的加權混合，而不是單一選擇。
3. **軟性鏈結。** 以平滑的聯結詞計算每個推導原子的真值。一般形式為

$$
v(\text{body}_c) = \prod_{i} v(b_i), \qquad v(p) = 1 - \prod_{c:\,\text{head}(c)=p} \bigl(1 - w_c\, v(\text{body}_c)\bigr)
$$

其中 $w_c$ 是子句 $c$ 的權重。重複此步驟即可推導更深層的後果。

4. **依似然目標為程式評分**，比較預測的真值與觀察到的事實。被標錯的範例只會使分數略微改變，而不會直接排除一個假設。
5. **銳化並讀出。** 梯度下降把多數權重推向 0 或 1，權重最高的子句即報告為學得的程式。

## 結果

摘要報告，此框架能解決傳統 ILP 系統所適合的任務；對訓練資料中的雜訊與錯誤具有 ILP 無法達到的穩健性；並能處理 ILP 無法應用的領域，例如模糊的感知。[^1] 摘要未提供數值結果，因此本頁不引用任何數字。引用任何數據前，應先閱讀論文的實驗部分。

## 限制

- **由設計者決定的範本。** 候選子句必須事先固定，而且其數量會隨述詞與本體原子的數目迅速增加。
- **局部最優。** 在非凸的鬆弛上做梯度下降，可能收斂到一個大致符合資料、卻不是預期規則的程式。
- **依賴背景知識。** 學得的規則只能使用所提供的述詞；此方法無法憑空發明缺漏的概念。
- **近似的真值。** 經銳化後的規則，其行為可能與產生它的軟性程式不同。

## 開放問題

- 候選子句本身能否被學習，使設計者不必事先固定範本？
- 如何確認被讀出的規則，與其來源的軟性程式行為一致？
- 可微分邏輯學習器能否擴展到大型知識庫？

## 關聯

∂ILP 是[知識表示](../../knowledge-graphs/index.md)中規則式傳統在學習面上的對應，因為它學習的是知識庫所儲存的那類定子句。其他可微分邏輯包括邏輯張量網路、[^2] DeepProbLog、[^3] 邏輯神經網路[^4] 與神經邏輯機，[^5] 後者能把從小任務學得的規則推廣到較大的任務。在證明方面，[神經定理證明器](../neural-theorem-prover/index.md)採取了相近的做法。主張學習應產生可解釋的因果規則，這一論點在 [Building Machines That Learn and Think Like People](../../../../brain-mind/cognitive-science/building-machines-like-people/index.md) 中有所發展。

[^1]: Evans 與 Grefenstette（2018），見上文。研究結果的摘要取自摘要部分。
[^2]: Serafini 與 d'Avila Garcez（2016），見上文。
[^3]: Manhaeve 等人（2018），見上文。
[^4]: Riegel 等人（2020），見上文。
[^5]: Dong 等人（2019），見上文。推廣的例子取自摘要。

## 參考文獻

### 開創性論文

- Evans, R. & Grefenstette, E. (2018). *Learning Explanatory Rules from Noisy Data*. Journal of Artificial Intelligence Research. https://doi.org/10.1613/jair.5714 — 提出可微分歸納邏輯程式設計，以梯度下降學習邏輯規則，並容忍有雜訊的訓練資料。
- Serafini, L. & d'Avila Garcez, A. (2016). *Logic Tensor Networks: Deep Learning and Logical Reasoning from Data and Knowledge*. arXiv. https://arxiv.org/abs/1606.04422 — 定義真值在單位區間內的 Real Logic，並以張量網路實作。
- Manhaeve, R. et al. (2018). *DeepProbLog: Neural Probabilistic Logic Programming*. arXiv. https://arxiv.org/abs/1805.10872 — 在機率邏輯程式語言中加入神經述詞，並從範例訓練它們。
- Riegel, R. et al. (2020). *Logical Neural Networks*. arXiv. https://arxiv.org/abs/2006.13155 — 提出讓神經元承載加權實值邏輯公式意義的模型，並以懲罰矛盾的損失訓練。
- Dong, H. et al. (2019). *Neural Logic Machines*. arXiv. https://arxiv.org/abs/1904.11694 — 從小任務學習提升式（lifted）邏輯規則，並推廣到較大的實例，例如較長的陣列。

### 綜述與教科書

- Besold, T. R. et al. (2017). *Neural-Symbolic Learning and Reasoning: A Survey and Interpretation*. arXiv. https://arxiv.org/abs/1711.03902 — 綜述神經符號學習與推理，連結計算邏輯與連結主義的認知模型。
