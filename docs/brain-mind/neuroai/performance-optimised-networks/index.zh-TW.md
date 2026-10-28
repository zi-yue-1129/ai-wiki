---
translation_reviewed: 2026-10-28
---

# 以效能最佳化的網路預測視覺皮質（Yamins 等人，2014）

為物體辨識最佳化的網路，能預測視覺皮質的神經反應。

## 問題

哪一種計算模型最能預測腹側視覺路徑高階皮質的神經反應？

## 核心想法

將深度卷積網路針對物件辨識做最佳化，再測試其特徵對 V4 與 IT 記錄到的反應有多少預測力。步驟與上方的任務最佳化範式相同。

## 結果

論文指出，各模型的物件辨識表現與其預測 IT 反應的能力相符；表現最好的模型，預測也比較早期、未最佳化的模型更好。

## 限制

預測分數不等於機制。測試使用固定的刺激與記錄位置，上方的警語同樣適用。

## 連結

- 母頁：[NeuroAI：大腦與 AI 的雙向啟發](../index.md)
- 同一主題的另一方法：[導航網路中的格狀單元](../grid-like-units/index.md)

## 參考文獻

### 開創性論文

- Yamins, D. L. K., 等人（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — 顯示針對物件辨識訓練的深度網路能預測高階視覺皮質的神經反應。
- Banino, A., 等人（2018）。Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — 顯示在訓練導航的遞迴代理中會出現格狀單元。
- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M.（2017）。Neuroscience-Inspired Artificial Intelligence. *Neuron*. https://doi.org/10.1016/j.neuron.2017.06.011 — 關於神經科學如何啟發 AI、以及 AI 如何檢驗大腦假說的經典綜述。
- Richards, B. A., 等人（2019）。A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — 主張以目標函數、學習規則與架構來研究大腦。

### 綜述與教科書

- Schrimpf, M., 等人（2021）。The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — 顯示預測下一個詞的語言模型能預測語言網路的大腦反應，且預測越好，與大腦越吻合。
