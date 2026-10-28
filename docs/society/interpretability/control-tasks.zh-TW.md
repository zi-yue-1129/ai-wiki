---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - probing
  - controls
aliases:
  - 控制任務
  - 選擇性
  - Control tasks
  - Selectivity
---

# 控制任務與選擇性

!!! info "屬於探測分類器"
    本方法頁屬於[探測分類器與表徵分析](probing.md)。它詳細說明此方法；上層頁面則比較各種探測方法。

控制任務（control task）是一種探測任務，其標籤是隨機指定的，依詞彙類型分配，因此只有探測器本身能學會它們。選擇性（selectivity）是探測器在真實語言任務上的準確率，減去其在控制任務上的準確率。Hewitt 與 Liang（2019）提出這兩者，使得高探測分數可以被解讀為表徵所編碼內容的證據，而不是探測器能記住多少的證據。

## 問題

在語言任務上得分高的探測器，可能真的學會了任務，也可能是從彈性很強的分類器中記住了資訊。單看準確率無法區分這兩種情況。問題在於量測探測分數中有多少來自表徵本身。

## 核心想法

為每個詞彙類型指定一個隨機的輸出標籤，以此建立控制任務。能編碼語言性質的表徵，在真實任務上應得高分，在控制任務上應得低分。若探測器在兩者上都得高分，表示它是在記憶，而非讀取表徵。選擇性即為兩個分數之間的差距。

## 方程式

對語言任務 $T$ 與其控制 $C$，探測器的選擇性為

$$
\mathrm{Sel} = \mathrm{Acc}_T - \mathrm{Acc}_C.
$$

探測器應以選擇性而非原始準確率來比較，因為選擇性把結果放在探測器容量的脈絡中。

## 結果

Hewitt 與 Liang 主張，選擇性能把語言任務的準確率，放在探測器記住詞彙類型標籤之容量的脈絡中。他們報告，在語言任務上準確率高的探測器，也能記住控制任務中隨機的詞彙類型標籤，因此只看準確率會高估表徵所含的內容。在預設設定下，MLP 探測器的選擇性低於線性探測器。以詞性標註為例，線性探測器的選擇性為 26.0，單隱藏層 MLP 為 4.5，而兩者的語言準確率相近（97.2 對 97.3）。

## 限制

- **設計依賴。** 控制任務必須精心設計，否則可能對探測器來說太容易或太難。
- **探測器家族。** 選擇性取決於所比較的探測器家族，因此同一表徵在不同家族下可能得到不同分數。
- **範圍。** 選擇性只說明探測器是否讀出超出記憶的性質；它並不表示模型使用了該性質。

## 相關連結

控制任務是檢驗[線性探測器](linear-probes.md)的方法，凡是在[表徵相似度分析](representational-similarity-analysis.md)或其他表徵研究中以探測準確率作為證據的場合，都需要它。整個探測家族見[探測分類器](probing.md)。控制只能說明探測器是否讀出資訊；模型是否使用這些資訊，則是介入實驗的問題，見[機械式可解釋性](mechanistic-interpretability.md)。

## 應用

- 發表探測結果時，同時報告選擇性與準確率，讓讀者能判斷探測器。
- 透過檢查每種探測容量允許多少記憶，為研究選擇適當的探測容量。
- 在把模型表徵用作下游任務的特徵之前，先檢查這些表徵。

## 開放問題

- 對影像、聲音或其他非文字輸入，應如何設計控制任務？
- 是否有原則性的方法，能選擇讓選擇性有意義的探測容量？
- 報告選擇性之後，已發表的探測結果有多少會改變？

## 參考文獻

### 開創性論文

- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Introduces control tasks and selectivity to separate probe memorisation from encoded information.
- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. arXiv:1610.01644. https://arxiv.org/abs/1610.01644 — The linear-probe method on which control tasks are built.
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — A probing study that reports on syntactic structure in contextual embeddings.

### 綜述與教科書

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Reviews probing methods, including the design of controls, and their limitations.
- Li, K. et al. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — Pairs a probe with interventions, a different check on what a representation is used for.
