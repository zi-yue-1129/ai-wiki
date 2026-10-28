---
translation_reviewed: 2026-10-28
status: draft
last_reviewed: 2026-10-28
tags:
- reinforcement learning
- neuroscience
- representation learning
- navigation
aliases:
  - 後繼表徵
  - Successor representation
  - SR
---

# 後繼表徵（Dayan，1993）

後繼表徵（SR）用智慧體從某狀態出發、預期會到達的未來狀態來描述該狀態。價值再由這張預測地圖與各狀態的獎勵結合而得。由於這張地圖不依賴獎勵，獎勵改變時仍能使用同一張地圖。Gershman（2018）回顧其計算邏輯與神經證據。

本頁屬於[空間導航與認知地圖](../index.md)。它詳細說明一種方法。此想法在海馬迴的部分見[位置細胞頁面](../place-cells/index.md)。

## 概述

設想一隻老鼠走過迷宮去找食物。它對每個位置的價值估計取決於兩件事：從該處出發，它多常能到達食物；以及食物有多少。SR 把第一部分保存為儲存的預測。食物的數量改變時，只需更新第二部分。

## 關鍵概念

- **佔據**：未來某狀態被造訪的頻率，並按造訪的遠近加權。越遠的造訪權重越低，由折扣因子決定。
- **後繼表徵**：對每個狀態，從該起點出發，所有狀態期望折扣佔據值組成的向量。
- **獎勵向量**：每個狀態所附的獎勵。改變它不會改變 SR。
- **時序差分（TD）學習**：從經驗中一步一步學習 SR 的方法。

## 問題

時序差分學習從經驗估計價值。Dayan（1993）主張，用來做這些估計的表徵很重要。摘要中說，狀態之間適當的泛化取決於它們後繼狀態的相似程度，因此表徵應該反映這種相似性。一般的狀態價值估計並不記錄這種結構，而獎勵改變時就必須重新建立。

## 核心想法

Dayan（1993）把 SR 定義為：從當前狀態出發，每個狀態的預測未來佔據值所組成的向量。它與價值估計一樣，用 TD 機制學習。學成之後，某狀態的價值就是其 SR 以獎勵加權後的總和。因此 SR 把任務的兩個部分分開：哪些狀態通往哪些狀態的時間結構，以及各狀態所附的獎勵。論文指出，SR 排除了任務中的時間成分，使學習變成較簡單的估計問題。

## 方程式或演算法

令 \(M(s, s')\) 為從狀態 \(s\) 出發，對狀態 \(s'\) 的期望折扣造訪次數，令 \(R(s')\) 為 \(s'\) 的獎勵。則

\(M(s, s') = \mathbb{E}\left[\sum_{t \ge 0} \gamma^{t}\, \mathbf{1}[s_t = s'] \,\middle|\, s_0 = s\right]\)，且 \(V(s) = \sum_{s'} M(s, s')\, R(s')\)

其中 \(\gamma\) 為折扣因子。觀察到從 \(s\) 轉移到 \(s'\) 之後，列 \(M(s, \cdot)\) 以一步 TD 更新：

\(M(s,\cdot) \leftarrow M(s,\cdot) + \alpha\,[\mathbf{1}_{s} + \gamma\, M(s',\cdot) - M(s,\cdot)]\)

其中 \(\alpha\) 為學習率。獎勵權重 \(R\) 則另外從各狀態觀察到的獎勵中估計。由於 \(M\) 由智慧體的策略定義，改變策略就會改變 \(M\)。

## 結果

Dayan（1993）以一個導航任務說明此方法，摘要指出，結果在各狀態之間的分布方式反映了它們的後繼狀態。論文所提的證據就是這個單一的示範任務，因此它本身並不足以確立這個解釋適用於大腦。

後來的研究把此想法應用於人類選擇（Momennejad 等人，2017），並把它與海馬迴位置細胞相連（Stachenfeld 等人，2017）。這些在相關頁面中討論。

## 限制

- **轉移改變時必須重新學習。** Dayan（1993）指出，在任務改變後修正 SR，需要重新學習受影響的預測。當只有獎勵改變時，SR 不必重新學習，但狀態之間的路徑改變時仍需要。
- **儲存。** SR 是以狀態為索引的矩陣。狀態空間很大時，儲存與學習都很昂貴。
- **依賴策略。** SR 是在特定策略下定義的，不同的行動方式會產生不同的 SR。
- **依賴表徵。** 它的效用取決於狀態如何定義，而這個方法本身不解決此問題。

## 關聯

- **多巴胺與 TD 學習**：SR 以與多巴胺被認為傳遞的訊號同類的時序差分更新來學習。見[多巴胺的獎勵預測誤差](../../neuroscience/dopamine-reward-prediction-error/index.md)。
- **有模型與無模型控制**：SR 儲存關於未來的預測，但不需要完整的獎勵模型，因此常被視為兩者之間的折衷。見[有模型與無模型控制](../../decision-reward/model-based-vs-model-free/index.md)。
- **位置細胞**：海馬迴中的預測地圖可以被讀為空間上的 SR。見[位置細胞與認知地圖假說](../place-cells/index.md)。
- **AI 中的強化學習**：SR 是[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)中研究的表徵之一，與[有模型的強化學習](../../../theory/paradigms/reinforcement-learning/model-based-rl/index.md)密切相關。

## 應用

- **模擬人類學習**：Momennejad 等人（2017）把 SR 應用於人類強化學習，檢驗人類的學習是否符合這種預測式解釋。
- **解讀海馬迴**：Stachenfeld 等人（2017）提出海馬迴是一張與 SR 相關的預測地圖，把此方法與空間記憶連在一起。
- **任務之間的轉移**：由於 SR 不依賴獎勵，獎勵改變時仍可重用，這正是 SR 定義所帶來的特性。

## 未解問題

- **SR 在哪裡計算？** 大腦是在海馬迴、皮質或其他地方計算 SR，仍在研究中。
- **在豐富的狀態空間中如何學習 SR？** 原論文的表格式情形不能直接套用到學習得來或高維的表徵。
- **它能解釋多少行為？** SR 可能解釋某些選擇而非其他，它與有模型控制如何互動，仍有爭議。

## 參考文獻

### 開創性論文

- Dayan, P.（1993）。Improving generalization for temporal difference learning: the successor representation。*Neural Computation*。https://doi.org/10.1162/neco.1993.5.4.613 — 定義後繼表徵，並說明時序差分學習如何學到它。論文以一個導航任務示範此結果。
- Stachenfeld, K. L.、Botvinick, M. M. 與 Gershman, S. J.（2017）。The hippocampus as a predictive map。*Nature Neuroscience*。https://doi.org/10.1038/nn.4650 — 提出海馬迴位置細胞編碼與後繼表徵相關的預測地圖。

### 綜論與回顧

- Gershman, S. J.（2018）。The Successor Representation: Its Computational Logic and Neural Substrates。*Journal of Neuroscience*。https://doi.org/10.1523/JNEUROSCI.0151-18.2018 — 回顧後繼表徵的計算邏輯與大腦中的證據。

### 文章與應用

- Momennejad, I. 等人（2017）。The successor representation in human reinforcement learning。*Nature Human Behaviour*。https://doi.org/10.1038/s41562-017-0180-8 — 把後繼表徵應用於人類強化學習。
