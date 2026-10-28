---
translation_reviewed: 2026-10-28
---

# CoALA：語言代理人的認知架構（Sumers 等人，2023）

為語言模型設計的代理人，具有模組化記憶與一組內部動作。

## 問題

以大型語言模型為基礎的語言代理人已展現強勁的結果，但缺少系統性的框架來組織它們。

## 核心想法

將代理人描述為包含模組化記憶（工作、情節、語意與程序記憶）、一組內部行動（檢索、推理、學習）與外部行動（與環境互動的落地），以及用來選擇行動的決策循環。

## 方法

概念框架。論文用它來分類既有代理人，並提出建造新代理人的方向。

## 結果

論文沒有提出新系統或基準測試，貢獻在於分類與設計語彙。

## 限制

框架本身並非經過評估的系統，而且真實代理人不一定能整齊地歸入這些類別。

## 連結

- 母頁：[認知架構](../index.md)
- 同一主題的另一方法：[ACT-R](../act-r/index.md)

## 參考文獻

### 開創性論文

- Anderson, J. R., 等人（2004）。An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R，在單一系統中模擬記憶、目標與學習的認知架構。
- Laird, J. E., Lebiere, C. & Rosenbloom, P. S.（2017）。A Standard Model of the Mind: Toward a Common Computational Framework. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — 提出 Soar、ACT-R 與 Sigma 共通元件的社群共識。
- Lake, B. M., 等人（2017）。Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — 主張類人學習需要因果模型、直覺理論與組合性。

### 綜述與教科書

- Kotseruba, I. & Tsotsos, J. K.（2020）。40 years of cognitive architectures: core cognitive abilities and practical applications. *Artificial Intelligence Review*. https://doi.org/10.1007/s10462-018-9646-y — 依涵蓋的認知能力與實際應用，綜述各種認知架構。
- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L.（2023）。Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — 提出 CoALA，以記憶、行動與決策來組織語言代理人的框架。
