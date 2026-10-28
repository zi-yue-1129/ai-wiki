---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- data-free distillation
aliases:
  - 無資料蒸餾
  - 零樣本知識蒸餾
  - Data-free distillation
  - Zero-shot knowledge distillation
---

# 無資料知識蒸餾

無資料蒸餾（data-free distillation）在無法取得教師模型訓練資料的情況下壓縮教師。學生改在由教師生成的合成輸入上訓練，因此當資料具私密性、規模過大難以分享，或已不復存在時，蒸餾仍然可以進行。

## 概觀

標準的蒸餾流程假設學生可以在真實輸入上訓練。在許多實際情況中並非如此：模型可能在發布時沒有附上訓練集，或資料受到保護。無資料方法會合成教師認為具代表性的輸入，通常的做法是從隨機雜訊開始最佳化，使教師的內部統計量符合它在真實資料上會看到的結果。接著學生就以這些合成樣本照常進行蒸餾。另一類方法則完全不做合成，而是由模型發布者在釋出訓練權重時附上少量中繼資料，Lopes 等人（2017）即提出這種做法。

## 關鍵概念

- **合成樣本（synthetic samples）。** 由教師生成的輸入，而不是取自資料集。
- **教師統計量（teacher statistics）。** 例如批次正規化的移動平均與變異數，它們摘要了訓練分布，可用來引導合成。
- **替代資料（surrogate data）。** 近似訓練資料、用於蒸餾的樣本，並不重現任何真實樣本。
- **覆蓋範圍（coverage）。** 合成樣本是否涵蓋學生必須表現良好的輸入空間區域。

## 主要方法

以下兩個方法的目標都是在沒有訓練資料的情況下蒸餾，但取得替代輸入的方式不同。

- [零樣本知識蒸餾（Nayak 等人，2019）](zero-shot-kd/index.zh-TW.md)：從教師合成「資料印象（data impressions）」，不使用原始訓練集的資料或中繼資料。
- [序列層級知識蒸餾（Kim 與 Rush，2016）](../llm-distillation/sequence-level/index.zh-TW.md)：使用教師對原始來源句子的輸出。它只是部分無資料，因為資料集的來源端仍是真實的；列在此處是因為它省去了目標端的需求。

零樣本蒸餾完全不使用真實輸入。序列層級蒸餾保留真實輸入，但以教師的輸出取代參考目標。

## 取捨

- **隱私與取得性 vs. 成本。** 無資料方法免除了對資料的需求，但合成需要計算，而且替代資料可能遺漏輸入空間中的重要區域。
- **忠實度。** 合成資料可能重現教師的錯誤，學生也無法超越教師所知。
- **授權。** 以某模型的輸出訓練另一個模型，可能受其使用條款限制，各供應商的規定不同。

## 更多變體與未解問題

- **未解問題：**如何為語言模型合成資料。離散的詞元比連續的影像更難最佳化。
- **未解問題：**從合成樣本中能恢復教師多少依賴資料的行為。
- **變體：**[大型語言模型蒸餾](../llm-distillation/index.zh-TW.md)，由教師為學生生成訓練資料。

## 關聯

無資料蒸餾與隱私議題相關，相關討論見[倫理](../../../../society/ethics/index.zh-TW.md)與[治理](../../../../society/governance/index.zh-TW.md)頁面，也與[訓練與微調](../../../../engineering/training/index.zh-TW.md)的流程有關。從訓練好的網路合成輸入，隱約類似大腦在休息時重播模式的方式，相關討論見[記憶與學習](../../../../brain-mind/memory-learning/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Nayak, G. K., Mopuri, K. R., Shaj, V., Babu, R. V. & Chakraborty, A. (2019). *Zero-Shot Knowledge Distillation in Deep Networks*. arXiv:1905.08114. https://arxiv.org/abs/1905.08114 — 從教師合成「資料印象」並以此訓練學生；摘要報告在多個基準上的泛化表現與使用真實訓練資料的蒸餾相當。
- Lopes, R. G., Fenu, S. & Starner, T. (2017). *Data-Free Knowledge Distillation for Deep Neural Networks*. arXiv:1710.07535. https://arxiv.org/abs/1710.07535 — 以隨預訓練模型釋出的少量中繼資料取代訓練集，並探討不同中繼資料選擇的取捨。
- Kim, Y. & Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — 在教師自身的序列輸出上訓練；摘要報告學生的速度約為教師的 10 倍，品質損失很小。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 標準的蒸餾目標，假設有訓練集，而無資料方法即是取代它。

### 綜述與教科書

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — 回顧蒸餾的各種設定，包括沒有資料的情況。

### 講座與影片

（本頁未查核）

### 文章與文件

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 將 BERT 蒸餾為約小 40% 的模型，同時保留 97% 的語言理解能力；是語言模型蒸餾的標準參考。
