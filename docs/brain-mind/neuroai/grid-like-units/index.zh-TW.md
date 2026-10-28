---
translation_reviewed: 2026-10-28
---

# 導航網路中的格狀單元（Banino 等人，2018）

經過訓練導航的循環代理人，會發展出格狀單元。

## 問題

大腦用來表示位置的格狀表徵，是否會在網路只被訓練去導航時自然出現？

## 核心想法

以強化學習訓練一個遞迴式代理在虛擬環境中導航到目標，輸入為速度與視覺。論文指出，格狀單元會在代理的隱藏層中自然出現，而非預先設定，且有助於以向量方式導航。

## 方程式或演算法


  1. 給代理速度與視覺輸入。
  2. 以強化學習訓練它抵達目標。
  3. 檢查其隱藏單元是否出現六角形的放電型態。

## 限制

代理與環境都很簡單且是人工的。上表中關於設計選擇的警語也適用於此結果。

## 連結

- 母頁：[NeuroAI：大腦與 AI 的雙向啟發](../index.md)
- 同一主題的另一方法：[以效能最佳化的網路預測視覺皮質](../performance-optimised-networks/index.md)

## 參考文獻

### 開創性論文

- Yamins, D. L. K., 等人（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — 顯示針對物件辨識訓練的深度網路能預測高階視覺皮質的神經反應。
- Banino, A., 等人（2018）。Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — 顯示在訓練導航的遞迴代理中會出現格狀單元。
- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M.（2017）。Neuroscience-Inspired Artificial Intelligence. *Neuron*. https://doi.org/10.1016/j.neuron.2017.06.011 — 關於神經科學如何啟發 AI、以及 AI 如何檢驗大腦假說的經典綜述。
- Richards, B. A., 等人（2019）。A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — 主張以目標函數、學習規則與架構來研究大腦。

### 綜述與教科書

- Schrimpf, M., 等人（2021）。The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — 顯示預測下一個詞的語言模型能預測語言網路的大腦反應，且預測越好，與大腦越吻合。
