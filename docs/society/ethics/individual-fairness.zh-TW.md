---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - individual fairness
  - similarity metrics
aliases:
  - 個體公平
  - Individual fairness
  - Fairness through awareness
---

# 個體公平

!!! info "屬於公平性定義"
    本方法頁屬於[公平性定義與不可能性結果](fairness-definitions.md)。它詳細說明此準則；概述頁則比較各個準則。

個體公平要求相似的個人得到相似的結果。Dwork、Hardt、Pitassi、Reingold 與 Zemel（2012）將它作為群體準則的替代方案提出，個人之間的相似度由與任務相關的度量定義。

## 問題

群體準則比較各群體的平均值，它們可能在滿足時，仍然對相似的人給予非常不同的待遇。問題是在個人層級陳述公平性要求，並把它變成分類器上明確、可檢驗的條件。

## 核心想法

定義一個度量 \(d\)，用來衡量兩個個人在當前任務中有多相似。分類器必須把相似的個人映射到相似的輸出分布。要求是相似的個人應被相似地對待，而度量則使「相似」得以精確定義。論文的分類器是隨機化的：它把每個個人映射到結果上的一個分布。

## 公式

若 \(M(x)\) 是個人 \(x\) 的輸出分布，\(D\) 衡量分布之間的距離，則 Lipschitz 條件為

\[
D\bigl(M(x), M(y)\bigr) \le d(x, y) \quad \text{對所有個人 } x, y \text{ 成立}
\]

論文採用全變差距離與最大散度作為 \(D\) 的選擇。

## 結果

論文屬於理論性質，未報告任何實驗。主要結果如下：

- **最佳化。** 在 Lipschitz 條件下最小化期望損失，對論文考慮的兩種距離選擇，都可以寫成線性規劃問題。
- **與群體公平的關係。** 論文以地球移動距離（earth mover's distance）衡量，給出 Lipschitz 條件與統計均等之間的界限。
- **非唯一性。** 同一個度量下有許多分類器都與之相容，因此度量本身無法決定分類器。

論文將度量描述為假設性的，並未在真實資料上評估某個具體的度量。

## 限制

- **度量的選擇。** 此準則的公平程度取決於度量，而度量必須由人設計。此框架假設存在與任務相關的相似度量，因此選擇度量是最核心的困難。
- **規模。** Lipschitz 條件必須對每一對個人成立，因此直接檢驗在大型資料集上成本高昂。
- **代理變數。** 忽略敏感屬性的度量，仍可能讓分類器透過相關特徵產生歧視。

## 參考文獻

### 開創性論文

- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*, 214–226. https://doi.org/10.1145/2090236.2090255 — 將個體公平引入為任務相關相似度量上的 Lipschitz 條件。
- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1703.06856 — 以因果推理為基礎的個體層級準則，以不同方式處理度量的選擇問題。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 個體公平常與之對照的群體準則。

### 綜述與教科書

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — 綜述機器學習中偏誤的來源，以及用來衡量偏誤的公平性定義。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 可免費線上閱讀的教科書，涵蓋個體與群體公平。
