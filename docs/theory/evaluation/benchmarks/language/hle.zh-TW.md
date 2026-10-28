---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# 人類的最後考試

人類的最後考試（HLE）是一個包含 2,500 題的基準，涵蓋數十個學科，包括數學、人文與自然科學。它是多模態的，由各領域專家撰寫，目的是隨模型進步仍能保持困難。作者把它描述為此類封閉式學術基準的最後一個（Phan et al., 2025）。

## 任務與資料

題目為選擇題或簡答題。每題都有可自動檢查的已知解答，而且設計成無法靠快速網路搜尋回答。部分題目含有影像，因此這個基準同時測試文字與多模態推理（Phan et al., 2025）。

## 協定與指標

指標是與參考答案比對後的**準確率**，採自動評分。簡答題的評分取決於比對規則，因此必須報告評分器以及任何評審模型。指標說明見[準確率](../../metrics/classification/accuracy.md)。

## 它能說明什麼

這個基準的建立，是因為模型在 MMLU 上已超過 90%（Phan et al., 2025）。它要問的是模型在專家知識邊緣的題目上表現如何，並希望比早期基準更能長期追蹤進展。

## 限制

- **發布後的污染。** 題目公開後可能進入訓練資料，因此之後的分數需要說明模型訓練時間與題目發布的先後關係。
- **自動評分。** 簡答題的檢查可能拒絕措辭不同的正確答案，也可能接受符合預期格式的錯誤答案。
- **封閉式格式。** 真正的研究問題是開放式的，無法用固定答案鍵檢查，因此 HLE 衡量的技能比研究工作狹窄。
- **專家撰寫。** 題目品質取決於貢獻者，而封閉式基準很難解決專家之間的分歧。

## 相關

- [MMLU](mmlu.md) 是 HLE 所要取代的基準。
- [GPQA](gpqa.md) 以較少的題目涵蓋研究所程度的科學。
- [語言家族概述](index.md) 比較各語言基準。

## 參考文獻

### 開創性論文

- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — 介紹 2,500 題的基準、其建構方式與評分方式。
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — 其飽和促成了 HLE 的設計。

### 文章與文件

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — 規模較小的專家程度基準，並討論了抗搜尋的題目。
- Gema, A. P. et al. (2024). *Are We Done with MMLU?* arXiv. https://arxiv.org/abs/2406.04127 — 審視已飽和的基準，並報告對後繼基準有影響的錯誤。

### 補充來源

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 描述一種在模型進步時仍能保持資訊量的基準設計方法。
