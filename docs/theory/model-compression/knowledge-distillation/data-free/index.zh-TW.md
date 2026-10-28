---
translation_reviewed: 2026-10-28
---

# 無資料知識蒸餾

無資料蒸餾在無法存取教師訓練資料的情況下壓縮教師。學生在由教師生成的合成輸入上訓練，因此即使資料是私密的、太大而無法分享，或已不再可得，蒸餾仍能進行。

## 概述

標準的蒸餾配方假設學生能在真實輸入上訓練。在許多實際情況中並非如此：模型可能在釋出時沒有附上訓練集，或資料受到保護。無資料方法會合成教師認為具代表性的輸入，通常是最佳化隨機雜訊，使教師的內部統計量符合它在真實資料上會看到的情況。學生接著在這些合成樣本上以一般方式蒸餾。

## 關鍵概念

- **合成樣本。** 由教師生成的輸入，而不是取自資料集。
- **教師統計量。** 例如批次正規化的執行平均與變異數，它們摘要了訓練分布，可以引導合成。
- **替代資料。** 為了蒸餾目的而近似訓練資料的樣本，不複製任何真實樣本。
- **覆蓋範圍。** 合成樣本是否涵蓋學生必須表現良好的輸入空間區域。

## 方法比較

| 方法 | 輸入如何取得 | 領域 | 頁面 |
| --- | --- | --- | --- |
| 零樣本 KD | 從雜訊最佳化，使教師有信心且多樣 | 影像分類 | [零樣本 KD](zero-shot-kd/index.zh-TW.md) |
| 序列層級 KD | 教師對來源句子的 beam search 輸出，來源句子仍是真實的 | 翻譯 | [序列層級 KD](../llm-distillation/sequence-level/index.zh-TW.md) |

零樣本 KD 完全不使用真實輸入，因此是完全的無資料方法。序列層級蒸餾仍需要來源句子，只是部分無資料；列在此處是因為它省去了資料集的目標端。

## 取捨

- **隱私與存取 vs. 成本。** 無資料方法不需要資料，但合成需要計算，而替代資料可能遺漏輸入空間中的重要區域。
- **保真度。** 合成資料可能重現教師的錯誤，學生也無法超越教師的知識。
- **授權。** 使用模型的輸出訓練另一個模型，可能受其使用條款限制，各供應商不同。

## 更多變體與開放問題

- **開放問題。** 如何為語言模型合成資料，因為離散的 token 比連續的影像更難最佳化。
- **開放問題。** 從合成樣本能恢復教師多少依賴資料的行為。
- **變體。** [大型語言模型蒸餾](../llm-distillation/index.zh-TW.md)，由教師為學生生成訓練資料。

## 相關連結

無資料蒸餾涉及隱私，這在[倫理](../../../../society/ethics/index.zh-TW.md)與[治理](../../../../society/governance/index.zh-TW.md)頁討論，也與[訓練與微調](../../../../engineering/training/index.zh-TW.md)的流程相關。從訓練好的網路合成輸入，類似大腦在休息時重播模式，此類比在[記憶與學習](../../../../brain-mind/memory-learning/index.zh-TW.md)中討論。

## 參考文獻

### 開創性論文

- Nayak, G. K., Mopuri, K. R., Shaj, V., Babu, R. V., Chakraborty, A. (2019). *Zero-Shot Knowledge Distillation in Deep Networks*. arXiv:1905.08114. https://arxiv.org/abs/1905.08114 — 從合成樣本蒸餾網路，表現與使用真實訓練資料具競爭力。
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — 以教師自己的序列輸出訓練，學生比教師快約 10 倍。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 標準的蒸餾目標，假設有訓練集，而無資料方法取代了它。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾設定，包括沒有資料的情況。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 從教師輸出與隱藏狀態蒸餾 BERT，是語言模型蒸餾的標準參考。
