---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - causal inference
  - counterfactuals
aliases:
  - 反事實公平
  - Counterfactual fairness
---

# 反事實公平

!!! info "屬於公平性定義"
    本方法頁屬於[公平性定義與不可能性結果](fairness-definitions.md)。它詳細說明此準則；概述頁則比較各個準則。

反事實公平詢問：若該個體屬於另一個人口群組，決定是否會相同。它使用因果推理，因此需要一個描述受保護屬性如何影響其他變數的模型。Kusner、Loftus、Russell 與 Silva（2017）以因果推論的工具引入此準則。

## 問題

群體準則比較的是統計量，它們並未說明群體身分是透過哪些特徵發揮影響的。問題是為個別決定定義公平，並將受保護屬性的效應與結果的其他成因區分開來。

## 核心想法

建立一個因果模型，描述受保護屬性如何影響其他變數。若在該模型中將屬性改設為另一個值，而與該屬性無因果關係的變數保持不變，決定仍不改變，則此決定具反事實公平性。因此此準則同時取決於資料與因果模型。

## 公式

以受保護屬性 \(A\)，若預測 \(\hat{Y}\) 對實際值 \(a\) 與反事實值 \(a'\) 滿足

\[
\Pr\bigl[\hat{Y}_{A \leftarrow a}(U) = y \mid X = x, A = a\bigr] = \Pr\bigl[\hat{Y}_{A \leftarrow a'}(U) = y \mid X = x, A = a\bigr],
\]

則具反事實公平性，其中 \(U\) 表示因果模型中未觀測的背景變數。

## 結果

論文定義了反事實公平，並將其呈現為以因果推論為基礎、用於建模公平性的框架。其主張關於此定義所捕捉的內容。實際結果取決於所用的因果模型，因此結論只在該模型正確的範圍內成立。

## 限制

- **因果模型。** 此準則需要因果圖，而這是資料本身無法驗證的假設。
- **未觀測變數。** 反事實預測取決於未觀測的背景變數，因此必須由模型推斷。
- **適用範圍窄。** 此準則處理的是受保護屬性的因果效應；它無法處理模型之外未測量因素所造成的不公平。

## 參考文獻

### 開創性論文

- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1703.06856 — 定義反事實公平，並將其呈現為以因果推論為基礎的框架。
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — 反事實公平常與之對照的個體層次準則。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 群體準則，因果方法與之形成對照。

### 綜述與教科書

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — 如其標題所述，這是一篇公平性定義的綜述。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 免費教科書，涵蓋公平性定義及其假設。
