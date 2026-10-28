---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# MMLU

MMLU（Massive Multitask Language Understanding）以選擇題測量知識與問題解決能力，涵蓋 57 個科目，包括國中程度的數學、美國歷史、電腦科學與法律（Hendrycks et al., 2021）。

## 任務與資料

每題有四個選項，模型要選出一個。科目涵蓋理工、人文、社會科學與專業領域。好的表現需要豐富的世界知識，也需要解題能力（Hendrycks et al., 2021）。

## 協定與指標

指標是所有題目的**準確率**，通常也會報告各科目的平均。結果多半是在提示詞中附上少數範例後取得。提示詞的細微變動，或作答字母的擷取方式，都可能改變分數，因此必須報告協定。指標說明見[準確率](../../metrics/classification/accuracy.md)。

## 它能說明什麼

發表時，多數模型的分數接近隨機猜測。最大的 GPT-3 平均比隨機猜測高出近 20 個百分點，但在每個科目上仍遠低於專家的準確率。作者也發現，模型常常不知道自己答錯了（Hendrycks et al., 2021）。

## 限制

- **飽和。** 現在模型在 MMLU 上的分數已超過 90%，因此它對前沿進展的衡量能力有限（Phan et al., 2025）。
- **標籤錯誤。** Gema et al.（2024）指出部分題目有錯誤或含義模糊，因此低於 100% 的上限不一定反映模型能力。
- **選擇題格式。** 四個選項意味著猜中的機率為四分之一，這種格式獎勵辨認而非生成。

## 後繼基準

[人類的最後考試](hle.md) 被設計為更困難的封閉式後繼基準。[GPQA](gpqa.md) 則針對研究所程度的科學題目，這些題目難以靠搜尋回答。

## 相關

- [語言家族概述](index.md) 比較各語言基準。
- [準確率](../../metrics/classification/accuracy.md) 是此基準使用的指標。

## 參考文獻

### 開創性論文

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — 介紹 57 科目的測試，並報告其第一批結果。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 介紹用於在 MMLU 上評估大型模型的少樣本提示設定。

### 文章與文件

- Gema, A. P. et al. (2024). *Are We Done with MMLU?* arXiv. https://arxiv.org/abs/2406.04127 — 審視此基準，並報告其中部分題目的錯誤與含義模糊。
- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — 指出模型在 MMLU 上已超過 90%，這也促成了它的後繼基準。

### 補充來源

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 廣泛的基準集合，把 MMLU 與其他語言任務並列。
