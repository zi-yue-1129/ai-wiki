---
translation_reviewed: 2026-10-28
---

# 神經語言模型的縮放定律（Kaplan 等人，2020）

Kaplan et al. 量測了 Transformer 語言模型的交叉熵損失，如何隨參數數量、資料量與訓練運算量增加而下降。他們利用這些冪律來決定固定運算預算應如何使用。整體主題見上層頁面[縮放定律與湧現能力](../index.md)。

## 概述

Kaplan 與同事在大範圍的模型大小、資料集大小與運算預算下，訓練一個 Transformer 語言模型家族並記錄保留文字上的損失。目標是找出能預測各項資源價值的規律。

## 關鍵概念

- **交叉熵損失**：模型對正確下一個 token 所給出的負對數機率平均值。數值越低越好，而縮放定律描述的正是這個量。
- **模型大小**：可訓練參數的數量，透過改變寬度與深度來調整。
- **資料集大小**：訓練語料中的 token 數。模型若相對於其容量訓練了過多文字，就可能過擬合；論文給出了描述此現象的簡單方程式。
- **樣本效率**：模型每使用一個訓練 token 所達到的損失下降程度。研究發現，較大的模型樣本效率較高。

## 運作方式

此程序有五個步驟：

1. 固定一個僅解碼器的 Transformer 家族，並改變其寬度、深度與參數數量。
2. 在大型文字語料上訓練每個模型，並在訓練過程中定期記錄保留文字上的損失。
3. 分別對每個變數擬合冪律：在資料量足夠大時，損失對參數數量的關係；在模型夠大時，損失對資料量的關係；以及損失對運算量的關係。
4. 擬合過擬合關係，描述訓練損失與保留損失之間的差距，如何依模型大小與資料集大小而變。
5. 對於固定的運算預算，利用擬合好的定律，選擇能使預測損失最小的模型大小與訓練量。

單變數形式為 $L(N) \propto N^{-\alpha_N}$，資料與運算量則有類似的形式。指數與常數由論文估計，此處不再重複。

## 結果

主要結果是：在參數、資料與運算量這三項資源上，損失都遵循平滑的冪律，橫跨超過七個數量級；而網路的寬度或深度等架構細節，在廣泛範圍內影響很小。作者的結論是，在固定預算下，最好的訓練方式是非常大的模型搭配相對有限的資料，並在遠未收斂前停止。這是一項關於分配的強烈主張：額外的運算應該更多地投入參數，而非資料。

Chinchilla 研究以不同的設計重新檢驗了同一個問題。Hoffmann et al.（2022）報告，當時的模型相對於其大小明顯訓練不足，並主張模型大小與訓練 token 數應同步成長。這項比較見[運算最佳化訓練](../../compute-optimal-training/index.md)頁面。

## 限制

- **擬合範圍。** 這些定律是在所測試的範圍內、以單一資料分布與固定架構家族擬合出來的。超出該範圍的外推只是一種假設。
- **損失，而非能力。** 這些定律描述的是下一個 token 的損失，並未直接說明任何特定下游任務會如何變化。這也是後續工作另外研究下游預測的原因之一（Gadre et al., 2024）。
- **分配已被修正。** Chinchilla 分析修正了模型大小與資料之間的分配，而考慮推論成本的後續研究又給出了不同的最佳點（Sardana et al., 2023）。

## 開放問題

- 同樣的冪律形式，是否適用於新的資料混合、較長的脈絡與不同的訓練目標？其他領域的後續研究發現了相似的形狀，但常數不同（Henighan et al., 2020）。
- 保留文字上的損失，與人們關心的能力（例如推理或遵循指令）之間，關聯有多緊密？
- 指數為何取這些數值？論文是以經驗方式描述它們，這個問題目前沒有公認的理論解釋。

## 相關連結

- 上層主題：[縮放定律與湧現能力](../index.md)。
- 同一主題的其他方法：[運算最佳化訓練](../../compute-optimal-training/index.md)，它修正了分配；以及[湧現能力](../emergent-abilities/index.md)，它探討平滑的損失對能力意味著什麼。
- 被縮放的模型見 [Transformer](../../../transformer/index.md)。同一家族在更大規模下的少樣本行為，見 [GPT-3 少樣本學習](../../gpt-3-few-shot/index.md)。

## 參考文獻

### 開創性論文

- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 論文本身：參數、資料與運算量上的冪律損失，以及由此推導出的分配規則。
- Hestness, J., et al. (2017). *Deep Learning Scaling is Predictable, Empirically*. arXiv. https://arxiv.org/abs/1712.00409 — 較早的證據，顯示在四個領域中，泛化誤差隨訓練集大小呈冪律下降。
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — 以超過 400 次訓練重新檢驗分配問題，並發現資料應隨模型大小成長。
- Henighan, T., et al. (2020). *Scaling Laws for Autoregressive Generative Modeling*. arXiv. https://arxiv.org/abs/2010.14701 — 將冪律縮放延伸到影像、影片、多模態與數學模型。

### 綜述與教科書

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — 對語言模型預訓練與適應的廣泛綜述，為規模驅動的進步提供背景。

### 文章與文件

- Sardana, N., et al. (2023). *Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws*. arXiv. https://arxiv.org/abs/2401.00448 — 在縮放分析中加入推論成本，改變了最佳的模型大小。
- Gadre, S. Y., et al. (2024). *Language models scale reliably with over-training and on downstream tasks*. arXiv. https://arxiv.org/abs/2403.08540 — 檢驗縮放預測在過度訓練的模型與下游任務表現上是否成立。
