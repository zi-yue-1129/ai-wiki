---
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - human-evaluation
---

# 人工評估

人工評估請人直接判斷系統輸出，例如流暢度、正確性或偏好。它是檢驗自動指標與模型評審的參考，但只有在報告了評分者、指示與評分者之間的一致性時才有用（Gehrmann et al., 2022）。

## 程序

評分者會收到說明與評分尺度，通常附有示例，且每個項目由數人評分。成對偏好（評分者在兩個輸出之間選擇）通常比絕對尺度更可靠。抽樣的項目應代表實際用途，而非為了偏袒某個系統而挑選。

## 一致性

評分者之間的一致性顯示判斷是否足夠一致而有意義。常見統計量包括兩位評分者用的 Cohen's kappa，以及多位評分者用的 Krippendorff's alpha，報告時應附上項目數與評分者數。一致性低通常表示評分準則不清楚，而非評分者粗心。

## 報告

報告評分者是誰、如何招募，獲得什麼報酬或指示，使用的尺度與說明，項目數與評分數，一致性統計量，以及分歧如何解決。缺少這些資訊，結果就無法重現。

## 限制

- **成本。** 人工評分既慢又貴，因此樣本小、區間寬。
- **評分者效應。** 專業程度、疲勞與項目順序都可能改變判斷。
- **效度。** 評分尺度只捕捉它所詢問的內容，而流暢的答案仍可能是錯的。

## 相關

- [LLM 作為評審](llm-as-judge.md) 會以這類人工評分來檢驗。
- [Elo 評分與競技場](elo-rating.md) 彙總人類的成對偏好。

## 參考文獻

### 開創性論文

- Gehrmann, S. et al. (2022). *Repairing the Cracked Foundation: A Survey of Obstacles in Evaluation Practices for Generated Text*. arXiv. https://arxiv.org/abs/2202.06935 — 調查生成文本的評估實務，包括人工評估的報告問題。

### 文章與文件

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，並將人工判斷與自動指標並列。
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. arXiv. https://arxiv.org/abs/2306.05685 — 比較以模型為基礎的評審與人類偏好。

### 補充來源

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
