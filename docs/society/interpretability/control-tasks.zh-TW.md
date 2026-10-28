---
status: draft
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
    本方法頁屬於[探測分類器與表徵分析](probing.md)。它詳細說明此方法；概述頁則比較各種探測方法。

控制任務是一種探測任務，其標籤依詞彙類型隨機指派，因此只有探測器本身能學會它們。選擇性則是探測器在真實語言任務上的準確率，減去其在控制任務上的準確率。Hewitt 與 Liang（2019）提出這兩者，使探測分數高時，可以被解讀為表徵所編碼內容的證據，而非探測器能記住多少的證據。

## 問題

在某個語言任務上得分高的探測器，可能真的學會了該任務，也可能是從靈活的分類器中記住了資訊。單看準確率無法區分這兩者。問題是衡量探測器的得分有多少來自表徵本身。

## 核心想法

為每個詞彙類型指派一個隨機的輸出標籤，藉此建立控制任務。若表徵確實編碼了某語言性質，它在真實任務上應得高分，在控制任務上應得低分。若探測器在兩者上都得高分，表示它在記憶，而非讀取表徵。選擇性記錄的正是兩個分數之間的差距。

## 公式

對語言任務 \(T\) 與其控制 \(C\)，探測器的選擇性為

\[
\mathrm{Sel} = \mathrm{Acc}_T - \mathrm{Acc}_C.
\]

探測器以選擇性而非原始準確率來比較，如此每個結果都能放在該探測器容量的脈絡中來看。

## 結果

論文主張，選擇性能讓語言任務的準確率放在探測器記住詞彙類型標籤之能力的脈絡中。作者認為，在語言任務上報告高準確率的探測器，也可能記住了詞彙類型的標籤，因此單看準確率會高估表徵所含的內容。

## 限制

- **依賴設計。** 控制任務必須仔細建構，因為設計不當的控制可能對探測器而言太容易或太難。
- **探測器家族。** 選擇性取決於所比較的探測器家族，因此同一表徵在不同家族下可能得到不同分數。
- **適用範圍。** 選擇性說明探測器是否讀取了記憶以外的性質，但它並不能證明模型使用了該性質。

## 參考文獻

### 開創性論文

- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — 引入控制任務與選擇性，以區分探測器的記憶與被編碼的資訊。
- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — 控制任務所依據的線性探測方法。
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — 一項探測研究，報告上下文嵌入中的句法結構。

### 綜述與教科書

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — 回顧探測方法（包括控制的設計）及其限制。
- Li, K. et al. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — 將探測器與介入配對，對表徵的用途進行另一項檢查。
