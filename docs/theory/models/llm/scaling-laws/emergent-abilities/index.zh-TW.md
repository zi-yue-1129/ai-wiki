---
translation_reviewed: 2026-10-28
---

# 大型語言模型的湧現能力（Wei 等人，2022）

Wei et al. 將湧現能力定義為：小型語言模型沒有、大型模型才有的能力，並主張這類能力無法從小模型的表現外推得出。整體主題見上層頁面[縮放定律與湧現能力](../index.md)。

## 概述

語言模型的規模擴大，已被證明能在許多任務上可預測地提升表現與樣本效率。Wei et al.（2022）描述了另一種模式。對某些任務而言，一個模型家族在較小的尺寸上表現接近隨機猜測，然後在較大的尺寸上明顯超過隨機水準。他們稱此現象為湧現，並推論：進一步擴大規模，可能會以平滑外推無法揭示的方式拓展模型的能力。


## 關鍵概念

- **湧現能力**：依論文的定義，是指小模型沒有、大模型才有的能力，因此無法由小模型外推得出。
- **少樣本提示**：任務由提示中的幾個已解答範例來指定，不需更新權重。使這種做法變得實用的方法，見 [GPT-3 少樣本學習](../../gpt-3-few-shot/index.md)。
- **隨機水準**：猜測所能得到的分數。對於選擇題，它由選項數量決定。在各種大小下都停留在隨機水準的任務，代表模型尚未具備該能力。
- **門檻規模**：表現開始上升的模型大小或運算量。其數值取決於所測試的規模。

## 運作方式

論文的分析遵循一個簡單的程序，沒有單一支配性的方程式：

1. 選擇一項任務，以及數個各有多種大小的模型家族。
2. 以相同的少樣本提示格式評估每個模型，使得唯一的變因是模型本身。
3. 以表現對規模作圖，橫軸使用參數數量或訓練運算量。
4. 找出對較小的模型而言表現停留在基準附近、到某個門檻後才明顯上升的任務。
5. 將這類任務歸為湧現。論點是：僅看平坦區域無法預見之後的上升，因此從小模型外推會漏掉這個躍升。

Ganguli et al.（2022）描述了相近的想法：可預測的損失，與不可預測的特定能力並存。

## 結果

論文報告，在數個模型家族中，許多少樣本任務都呈現先平坦、後上升的模式，而且上升只出現在某個規模之上。作者由此預期，進一步的擴大規模可能會解鎖尚未出現的能力。論文摘要陳述了這項主張與定義；各項任務的具體基準與門檻規模，則載於全文中。本頁撰寫時並未檢視全文，因此其中的例子此處不再重複。

Srivastava et al.（2022）介紹了 BIG-bench 基準，並以「數量上的進步，加上新的質性能力」描述同樣的模式。

## 限制

- **依賴所取樣的規模。** 門檻只能在所測試的尺寸之間被看到。若尺寸太少，平緩的上升可能看起來像躍升。
- **依賴指標。** 完全比對或其他不連續的分數，可能讓平緩的變化看起來很突然。Schaeffer et al.（2023）後來的批評正是以此點為基礎。
- **描述而非機制。** 論文記錄了湧現出現的位置，但沒有解釋能力為何會在特定規模開啟。

## 開放問題

- 湧現能力是模型的性質，還是測量方式的性質？Schaeffer et al.（2023）主張許多情況屬於後者，而 Berti et al.（2025）的綜述回顧了此項分歧。
- 能否在訓練之前預測某項能力會在哪個規模出現？本論文的定義排除了簡單的外推，因此需要另一種預測工具。

## 相關連結

- 上層主題：[縮放定律與湧現能力](../index.md)。對它的批評見[湧現是海市蜃樓](../emergence-mirage/index.md)。
- 以提示為基礎的推理，是湧現爭論最常被套用的能力之一。見[思維鏈](../../../reasoning/chain-of-thought.md)與[推理模型](../../../reasoning/index.md)。
- 本文所對照的平滑損失定律，見 [Kaplan 縮放定律](../kaplan-scaling-laws/index.md)。
- 人類發展也呈現能力分階段出現的現象。見[發展認知](../../../../../brain-mind/developmental-cognition/index.md)。

## 參考文獻

### 開創性論文

- Wei, J., et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — 論文本身：定義湧現能力，並主張這類能力無法由小模型外推。
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示在足夠大的語言模型中，透過中間步驟的提示會出現推理能力。
- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 論文，使少樣本提示成為湧現通常被測量的情境。
- Schaeffer, R., Miranda, B. & Koyejo, S. (2023). *Are Emergent Abilities of Large Language Models a Mirage?* arXiv. https://arxiv.org/abs/2304.15004 — 對湧現主張的主要批評，主張不連續的指標會產生表觀的躍升。

### 綜述與教科書

- Berti, L., Giorgi, F. & Kasneci, G. (2025). *Emergent Abilities in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2503.05788 — 回顧湧現的文獻，以及關於這些能力是否真正湧現的爭論。

### 文章與文件

- Srivastava, A., et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — BIG-bench 基準，是研究縮放與湧現時許多任務的來源。
- Ganguli, D., et al. (2022). *Predictability and Surprise in Large Generative Models*. arXiv. https://arxiv.org/abs/2202.07785 — 討論大型生成模型中，可預測的損失與不可預測的特定能力並存的現象。
