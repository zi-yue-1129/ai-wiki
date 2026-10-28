---
translation_reviewed: 2026-10-28
---

# 適配器模組

適配器模組是插入預訓練 Transformer 中的小型瓶頸網路。每個任務只訓練適配器與層正規化的參數，原有權重保持凍結。Houlsby 等人（2019）報告，在 GLUE 上，適配器的平均分數比全參數微調低 0.4 分，而每個任務只增加 3.6% 的參數。它是最早的參數高效微調方法之一，後來的方法如 [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.zh-TW.md) 即是在此設計上做出改變。

## 問題

全參數微調會為每個任務保留一份完整的模型副本。對於數億參數的模型，服務多個任務就得儲存與載入多份副本。目標是訓練與儲存一小組任務專用的參數，同時讓所有任務共用同一個凍結的基底模型。

## 關鍵概念

- **瓶頸適配器：** 一個把隱藏激活值投影到窄寬度 \(m\)、施加非線性函數、再投影回模型寬度 \(d\) 的模組。它有內部的殘差連接，因此在初始化附近會讓輸入直接通過。
- **放置位置：** 每個 Transformer 層有兩個適配器，一個在注意力子層之後，一個在前饋子層之後。
- **可訓練參數：** 適配器權重，加上層正規化的參數，每層約增加 \(2d\) 個參數。論文報告，只訓練層正規化的效果很差。

## 運作方式

適配器權重初始化在零附近，因此每個適配器一開始接近恆等函數，訓練開始時保留預訓練網路的行為。對每個任務，訓練只在任務資料上更新適配器與層正規化，其餘保持固定。推論時，一份凍結的基底模型只需載入一次，每個任務的那一小組參數則被換入。由於每組都很小，儲存多個任務的成本幾乎只比儲存一個模型多一點。

## 結果

論文把 BERT 遷移到 26 項文字分類任務，包括 GLUE。若瓶頸寬度從 {8, 64, 256} 中依任務選擇，適配器每個任務使用約 3.6% 的參數，GLUE 平均分數為 80.0，全參數微調為 80.4。若固定瓶頸寬度為 64，每個任務使用約 2.1% 的參數，分數為 79.6。解決所有 GLUE 任務時，適配器所需參數約為 BERT 的 1.3 倍，全參數微調則約為 9 倍。

## 限制

- **額外運算。** 適配器是額外的層，因此推論時會增加運算量；適配器的設計無法像 LoRA 那樣把它們併入基底權重。
- **需修改架構。** 適配器需要修改模型的層，不同於只改變輸入的方法。
- **證據的範圍。** 論文的實驗以 BERT 與分類任務為主，因此在其他架構與生成任務上的結果，需要另行檢驗。

## 開放問題

- **放置位置與大小。** 對於特定任務，瓶頸應多寬，以及每層兩個的放置方式是否最佳，目前靠實驗選擇，而非理論。
- **與低秩更新的比較。** 瓶頸適配器與 LoRA 等低秩更新，在參數、延遲與準確度之間何者較佳，仍有爭議，且結果取決於任務。

## 相關連結

適配器是[微調與適應](index.md)中最早被廣泛使用的參數高效方法。低秩的替代方案是 [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.zh-TW.md)，其量化版本是 [QLoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.zh-TW.md)。不加層的提示式替代方案是[前綴微調](prefix-tuning.zh-TW.md)與[提示微調](prompt-tuning.zh-TW.md)。使用這些方法的訓練實務，見[訓練與微調](../../../../engineering/training/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Houlsby, N., 等人 (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — 提出瓶頸適配器，平均 GLUE 分數比全參數微調低 0.4 分，每個任務只增加 3.6% 參數。
- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 在凍結權重上學習低秩更新，作為推論時不增加額外層的替代方案。
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — 在語言模型凍結的情況下訓練一小段連續前綴，作為適配器的提示式替代方案。
- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — 在凍結模型上學習軟提示，並顯示隨著模型變大，此方法可與模型微調相當。
- Liu, H., 等人 (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — 顯示參數高效微調在準確度與運算成本上，都優於少樣本的上下文學習。
