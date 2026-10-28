---
translation_reviewed: 2026-10-28
---

# ACT-R：心智的模組化架構（Anderson 等人，2004）

獨立的模組透過緩衝區交換資訊，由產生式規則選擇下一步動作。

## 問題

檢索、決策與運動控制等認知過程，如何從同一個系統中湧現，並與人類的時間表現相符？

## 核心想法

分離的模組（視覺、運動、陳述性記憶、目標）透過緩衝區交換資訊，由產生式規則決定下一步動作。每個模組的處理時間都依人類資料設定。

## 方程式或演算法


  1. 每個模組把目前的結果放入其緩衝區。
  2. 產生式規則比對各緩衝區的內容。
  3. 符合的規則被觸發，改變緩衝區，進而決定下一步。

## 結果

論文報告，同一個架構能解釋多種任務的人類資料，且模組的時間與腦區相連。

## 限制

此架構是大量人工設計的元件，擬合資料時需要許多建模選擇。上方的記憶方程式即是其中被擬合的部分。

## 連結

- 母頁：[認知架構](../index.md)
- 同一主題的另一方法：[CoALA](../coala/index.md)

## 參考文獻

### 開創性論文

- Anderson, J. R., 等人（2004）。An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R，在單一系統中模擬記憶、目標與學習的認知架構。
- Laird, J. E., Lebiere, C. & Rosenbloom, P. S.（2017）。A Standard Model of the Mind: Toward a Common Computational Framework. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — 提出 Soar、ACT-R 與 Sigma 共通元件的社群共識。
- Lake, B. M., 等人（2017）。Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — 主張類人學習需要因果模型、直覺理論與組合性。

### 綜述與教科書

- Kotseruba, I. & Tsotsos, J. K.（2020）。40 years of cognitive architectures: core cognitive abilities and practical applications. *Artificial Intelligence Review*. https://doi.org/10.1007/s10462-018-9646-y — 依涵蓋的認知能力與實際應用，綜述各種認知架構。
- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L.（2023）。Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — 提出 CoALA，以記憶、行動與決策來組織語言代理人的框架。
