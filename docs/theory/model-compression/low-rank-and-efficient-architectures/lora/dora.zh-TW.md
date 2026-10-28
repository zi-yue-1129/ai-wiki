---
translation_reviewed: 2026-10-28
---

# DoRA

DoRA，即權重分解低秩適應（Weight-Decomposed Low-Rank Adaptation），是 [LoRA](index.zh-TW.md) 的一種變體。它把每個預訓練權重矩陣拆成大小與方向兩部分。低秩更新只套用在方向上，大小則直接訓練。Liu 等人（2024）報告，DoRA 在常識推理上優於 LoRA，而且把更新合併回原始權重後，推論時沒有額外延遲。它屬於 LoRA 家族，因為它保留同樣的低秩更新，只是改變了更新的套用方式。

## 問題

LoRA 在凍結的權重 \(W_0\) 上加入低秩更新 \(BA\)，訓練與儲存的成本都很低。論文比較完整微調與 LoRA 如何改變權重，發現兩者的行為不同。以 VL-BART 的查詢與值矩陣為例，LoRA 對大小與方向的改變是同步移動的，完整微調則不然。作者推測，LoRA 無法同時做到方向上的小幅改變與大小上的大幅改變（或反過來），而這限制了它的準確度。

## 關鍵概念

- **大小：** 權重矩陣每一欄的範數。在 DoRA 中，它是一個獨立的可訓練向量 \(m\)。
- **方向：** 每一欄除以其範數後的結果。低秩更新就套用在這部分。
- **權重分解：** 論文把權重寫成 \(W = m \cdot V / \lVert V \rVert_c\)，其中 \(V\) 是方向矩陣，\(\lVert \cdot \rVert_c\) 是逐欄的範數。

## 運作方式

DoRA 把 \(V\) 初始化為 \(W_0\)，並把大小向量 \(m\) 保留為可訓練參數。LoRA 的乘積 \(BA\) 更新方向，因此調整後的權重為

\[
W' = m \cdot \frac{W_0 + BA}{\lVert W_0 + BA \rVert_c}
\]

訓練後，結果可合併成單一權重矩陣，因此推論成本與原模型相同。

## 結果

在 LLaMA-7B 的常識推理上，論文的表格列出 LoRA 平均 74.7、DoRA 平均 78.4，相差 3.7 分。秩減半的變體達到 77.5。這些數字取自 ICML 2024 會議論文集版本，其他版本的預印本數字可能不同。

## 限制

- **證據範圍窄。** 作者計畫把 DoRA 測試到語言與視覺以外的領域，特別是音訊，因此它在其他領域的表現尚未得到展示。
- **完整微調較差時，增益較小。** 在 LLaVA-1.5-7B 上，完整微調的表現不如 LoRA，此時 DoRA 相對 LoRA 的優勢也較小。
- **省記憶體的變體。** 用來節省記憶體的梯度修改，會帶來小幅的準確度差異，在 LLaMA 上約為 0.2。
- **繼承 LoRA 的選擇。** 秩與要適應的矩陣仍需調整，與 LoRA 相同。

## 開放問題

- **分解為何有幫助。** 論文以觀察到的權重變化差異來說明分解的動機，但為何分開大小與方向會有幫助，完整的解釋仍是開放問題。
- **與量化的互動。** DoRA 如何與量化的基底模型（例如 [QLoRA](qlora.zh-TW.md)）結合，是實務上的問題，論文並未解決。

## 相關連結

DoRA 與 [QLoRA](qlora.zh-TW.md) 同屬 LoRA 家族，QLoRA 量化的是凍結的基底。兩者都是[微調與適應](../../../paradigms/transfer/fine-tuning-and-adaptation/index.md)中描述的參數高效微調方法。使用這些方法微調大型模型的實務，見[訓練與微調](../../../../engineering/training/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Liu, S.-Y., 等人 (2024). *DoRA: Weight-Decomposed Low-Rank Adaptation*. ICML 2024, arXiv:2402.09353. https://arxiv.org/abs/2402.09353 — 把每個預訓練權重分解為大小與方向，只把 LoRA 套用在方向上，並報告相對 LoRA 的增益且不增加推論延遲。
- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — DoRA 所修改的低秩更新，包含凍結的基底與推論時的合併。
- Dettmers, T., Pagnoni, A., Holtzman, A., Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — 把 LoRA 適配器套用在 4 位元凍結基底上，是同一家族中的量化版本。
- Houlsby, N., 等人 (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — 提出適配器，是與低秩更新相對的加層方法。
- Liu, H., 等人 (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — 顯示參數高效微調在準確度與運算成本上，都優於少樣本的上下文學習。
