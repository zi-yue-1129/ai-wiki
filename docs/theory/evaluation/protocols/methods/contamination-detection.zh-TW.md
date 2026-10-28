---
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - contamination
---

# 污染偵測

污染偵測檢查基準的測試項目或其答案，是否曾出現在模型的訓練資料中。若是，分數衡量的就是記憶而非能力。方法從比對重疊文字，到只使用模型輸出的統計檢定都有（Oren et al., 2023）。

## 程序

重疊方法會把測試項目與訓練語料比對，通常使用 n-gram 比對，並標記出現在語料中的項目。成員推論方法則詢問：模型對測試文字的likelihood是否高於可比的新文字，因為被記住的文字通常會得到較高的likelihood（Carlini et al., 2021）。Oren et al.（2023）提出一種統計檢定，只需黑箱存取模型，就能利用基準範例的排列順序，證明模型見過該基準。

## 報告

說明使用的方法、執行所針對的語料或模型、標記項目的門檻，以及被標記項目的比例。若方法沒有發現重疊，並不能證明模型從未見過該基準，因為訓練資料可能未公開或經過過濾。

## 限制

- **訓練資料未公開。** 重疊檢查需要語料，而許多供應商不釋出語料。
- **改寫。** 改寫過的項目可以逃過 n-gram 比對，同時保留相同的答案。
- **誤報。** 以 likelihood 為基礎的方法可能標記出只是常見或簡單的文字。

## 相關

- [評估協定概述](../index.md) 列出切分的洩漏風險。
- [配對自助法](paired-bootstrap.md) 說明移除受污染項目後分數的不確定性。

## 參考文獻

### 開創性論文

- Carlini, N. et al. (2021). *Extracting Training Data from Large Language Models*. arXiv. https://arxiv.org/abs/2012.07805 — 顯示語言模型會記憶並重現訓練文本，這是 likelihood 檢查的基礎。
- Oren, Y. et al. (2023). *Proving Test Set Contamination in Black Box Language Models*. arXiv. https://arxiv.org/abs/2310.17623 — 提出統計檢定，只用模型輸出判斷基準是否出現在訓練中。

### 文章與文件

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，並注意測試資料的報告方式。

### 補充來源

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
