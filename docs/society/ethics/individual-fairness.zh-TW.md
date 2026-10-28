---
status: draft
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

個體公平要求相似的個體獲得相似的結果。Dwork 等人（2012）將它作為群體準則的替代方案提出，個體之間的相似度由任務專屬的度量定義。

## 問題

群體準則比較的是各群體之間的平均值，因此即使滿足它，相似的人仍可能受到非常不同的對待。問題是在個體層次陳述公平性要求，並使其成為分類器上一個明確、可檢驗的條件。

## 核心想法

定義一個度量 \(d\)，用來衡量兩個個體在當前任務上有多相似。分類器必須把相似的個體映射到相似的輸出分布。此要求是相似的個體應被相似地對待，而度量則使「相似」一詞精確化。

## 公式

若 \(M(x)\) 是個體 \(x\) 的輸出分布，且 \(D\) 衡量分布之間的距離，則 Lipschitz 條件為

\[
D\bigl(M(x), M(y)\bigr) \le d(x, y) \quad \text{對所有個體 } x, y.
\]

## 結果

論文提出一個公平分類的框架，將相似度度量與在公平性限制下最大化效用的演算法結合。其主要貢獻是此框架；它並未主張某個特定度量適用於某個特定應用。

## 限制

- **度量的選擇。** 此準則的公平程度取決於度量，而度量必須由某人設計。框架假設任務專屬的相似度度量可用，因此選擇度量正是核心困難。
- **規模。** 對資料集中每一對個體檢查此條件，計算成本很高，因此實際版本通常只能近似。
- **代理變數。** 即使度量忽略了敏感屬性，分類器仍可能透過相關的特徵而產生歧視。

## 參考文獻

### 開創性論文

- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — 將個體公平引入為任務專屬相似度度量上的 Lipschitz 條件。
- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1703.06856 — 以因果推理為基礎的個體層次準則，以不同方式處理度量的選擇問題。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 個體公平常與之對照的群體準則。

### 綜述與教科書

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — 如其標題所述，這是一篇包含個體公平的公平性定義綜述。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 免費教科書，涵蓋個體公平與群體公平。
