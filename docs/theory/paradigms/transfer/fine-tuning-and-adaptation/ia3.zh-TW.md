---
translation_reviewed: 2026-10-28
---

# (IA)³ 微調

(IA)³ 是一種參數高效的微調方法，它以學習得到的向量重新縮放凍結語言模型的內部激活值，以進行適應。Liu 等人（2022）主張，參數高效微調在準確度與成本上都優於少樣本的上下文學習；後者在每次預測時都必須重新處理所有範例。他們並結合此方法提出訓練配方 T-Few，在 RAFT 基準上達到超越人類的表現。它屬於[微調與適應](index.md)的範圍，是一種只加入極少參數、且不改變模型結構的方法。

## 問題

上下文學習的做法是把少數標註範例放進輸入，不更新任何權重。這很方便，但它有可觀的運算、記憶體與儲存成本，因為每次預測都要重新處理所有範例。全參數微調準確，但每個任務需要一份完整的模型副本。因此需要一種訓練與儲存都便宜、又能與兩者競爭的方法。

## 關鍵概念

- **激活縮放：** 以學習得到的向量逐元素地乘上激活值。這些向量初始為全 1，因此初始化時模型行為不變。
- **縮放的位置：** 每個 Transformer 區塊中，自注意力與編碼器—解碼器注意力中的鍵與值，以及前饋網路的中間激活值。
- **凍結模型：** 預訓練權重保持固定，只訓練縮放向量。

## 運作方式

對每個任務，縮放向量在該任務的標註範例上訓練，模型權重保持固定。推論時，激活值乘上這些向量。由於這是逐元素的縮放，它增加的運算很少，而且每個任務只需儲存一小組向量。

T-Few 是圍繞此方法建立的配方。它以 T0 模型為骨幹，並把三種損失加總：標準語言建模損失、unlikelihood 損失，以及長度正規化損失。論文在 T0-3B 上的設計實驗顯示，長度正規化把準確度從 60.7% 提高到 62.7%，再加上 unlikelihood 損失後達到 63.3%。

## 結果

論文指出，(IA)³ 更新的參數最多比全參數微調少 10,000 倍，其表格列出 T0-3B 約增加 54 萬個參數。在 RAFT（一組未見任務的基準）上，T-Few 達到 75.8%，人類基準為 73.5%；論文稱之為首次達到超越人類的表現。表中排名第二的 PET 得分為 69.6%。

## 限制

- **只限分類任務。** 作者表示，他們的實驗全部是分類任務，而摘要與問答等生成式任務留待未來研究。
- **以 FLOPs 作為代理指標。** 成本比較使用 FLOPs，它與硬體無關，因此無法衡量實際的延遲或功耗。
- **基準數字是轉抄的。** GPT-3 的數字取自 Brown 等人，而不是重新執行。
- **配方的影響。** 報告的 RAFT 結果是 T-Few 整體的表現，它結合了此方法與預訓練及額外損失，因此激活縮放本身的效果需要另外的消融實驗。

## 開放問題

- **生成式任務。** 相同的增益能否延伸到生成任務，論文留待未來研究，仍是開放問題。
- **與低秩更新的比較。** 在相同任務上，激活縮放與 [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.zh-TW.md) 在準確度與推論成本上的比較，仍是開放的實務問題。

## 相關連結

(IA)³ 與[適配器](adapters.zh-TW.md)（加入小型層）及 [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.zh-TW.md)（加入低秩更新）同屬參數高效方法。與上下文學習的比較，對[訓練與微調](../../../../engineering/training/index.zh-TW.md)實務很重要，因為少樣本提示是那裡常用的替代方案。

## 參考文獻

### 開創性論文

- Liu, H., 等人 (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — 提出 (IA)³ 與 T-Few 配方，並顯示參數高效微調在準確度與成本上都優於少樣本的上下文學習。
- Houlsby, N., 等人 (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — 提出適配器，是同一家族中加入小型層的參數高效方法。
- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 在凍結權重上學習低秩更新，另一種參數高效方法，合併後不增加推論延遲。
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — 在語言模型凍結時訓練一段連續前綴，是通往同一目標的提示式路線。
- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — 在凍結模型上學習軟提示，並顯示隨模型變大，它可與模型微調相當。
