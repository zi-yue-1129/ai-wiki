---
translation_reviewed: 2026-10-28
tags:
  - transformer
  - attention
  - normalisation
  - training stability
aliases:
  - QK-norm
  - QK normalisation
  - QK 正規化
---

# QK 正規化

QK 正規化在每個注意力頭做內積之前，先對其查詢（query）與鍵（key）套用層正規化。不論產生 \(Q\) 與 \(K\) 的權重範數有多大，它都能限制注意力的 logit。Dehghani 等人（2023）在訓練 220 億參數的視覺 Transformer（ViT-22B）時，用它來防止注意力 logit 失控增長所造成的發散。上層概述是[Transformer 與注意力](index.md)，更廣泛的範數增長問題見[權重範數動態](../../optimization/weight-norm-dynamics/index.md)頁面。

## 概述

在標準的縮放點積注意力中，logit 為 \(QK^\top/\sqrt{d_k}\)。若產生 \(Q\) 與 \(K\) 的權重變大，logit 也會跟著變大，softmax 可能變得幾乎是一個 one-hot 分布。一旦如此，注意力參數的梯度會變得非常小或非常不穩定。QK 正規化在 \(Q\) 與 \(K\) 上插入正規化，使 logit 取決於向量的方向，而非長度。

## 問題

注意力 logit 的增長是大型 Transformer 訓練不穩定的來源之一。Wortsman 等人（2023）列舉了這一點，並引用先前在大規模上的報告（Dehghani 等人，2023）。logit 增長時，softmax 會集中在少數位置上，訓練可能發散。

## 核心想法

在每個頭的內積之前，對其查詢與鍵向量套用層正規化，使注意力為 \(\text{softmax}\!\left(\text{LN}(Q)\,\text{LN}(K)^\top/\sqrt{d_k}\right)\)。正規化把 \(Q\) 與 \(K\) 的尺度從 logit 中移除，因此 logit 不再隨產生它們的權重範數增長。

## 運作方式

1. 照常把輸入投影為查詢、鍵與值。
2. 對每個頭的查詢與鍵分別套用層正規化，各自有可學習的增益與偏置。
3. 計算正規化後查詢與鍵的縮放點積，再做 softmax，與標準注意力相同。
4. 值的投影與區塊的其餘部分維持不變。

這項修改只限於注意力內部，代價是每個頭對查詢與鍵各多一次正規化。

## 結果

Wortsman 等人（2023）在小規模上重現注意力 logit 的增長，並測試查詢與鍵的層正規化作為補救。他們報告，在所測的模型規模上，它能防止發散，而學習率敏感度仍隨模型規模增加。輸出 logit 的發散是另一種不穩定，他們以 z-loss 處理，而非這種正規化。確切數字應以論文為準。

## 限制

- QK 正規化限制了注意力 logit，但沒有限制輸出投影或前饋層的範數。Wortsman 等人（2023）報告，即使使用它，學習率敏感度仍隨模型規模增長；其他層的範數仍可能持續增長，權重範數分析說明了原因。
- 它限制的是 logit 的尺度，注意力仍可能在秩或熵上崩潰。Zhai 等人（2023）把熵崩潰連結到注意力 logit 的譜範數，Noci 等人（2022）則把秩崩潰連結到 token 表示。
- 論文報告的主要效益是訓練穩定性。關於最終準確率的主張取決於各論文的實驗，應在論文中核對。

## 相關主題

- [Transformer 與注意力](index.md) 描述 QK 正規化所改變的注意力區塊。
- [σReparam](sigma-reparam.md) 是另一種方案，以譜範數對每個線性層做重參數化。
- [權重範數動態](../../optimization/weight-norm-dynamics/index.md) 說明 QK 正規化本身無法解決的範數增長。
- [注意力變體](attention-variants/index.md) 涵蓋為了效率而對注意力運算所做的改動。

## 開放問題

- 在超長上下文的模型中，查詢鍵正規化是否足夠，因為 logit 要對更多位置加總。
- 這個正規化如何與旋轉位置編碼互動，因為後者作用於同樣的查詢與鍵向量。

## 參考文獻

- Dehghani, M., Djolonga, J., Mustafa, B., et al. (2023). *Scaling Vision Transformers to 22 Billion Parameters*. ICML 2023, PMLR 202:7480–7512. https://proceedings.mlr.press/v202/dehghani23a.html — 在訓練 ViT-22B（一個 220 億參數的視覺 Transformer）時，以查詢鍵層正規化防止注意力 logit 失控增長所造成的發散。
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — 在小規模上重現注意力 logit 與輸出 logit 的不穩定，並測試查詢鍵層正規化與 z-loss 作為補救。
- Zhai, S., Likhomanenko, T., Littwin, E., et al. (2023). *Stabilizing Transformer Training by Preventing Attention Entropy Collapse*. ICML 2023, PMLR 202:40770–40803. https://proceedings.mlr.press/v202/zhai23a.html — 把注意力熵崩潰連結到注意力 logit 的譜範數。
- Noci, L., Anagnostidis, S., Biggio, L., et al. (2022). *Signal Propagation in Transformers: Theoretical Perspectives and the Role of Rank Collapse*. arXiv:2206.03126. https://arxiv.org/abs/2206.03126 — 分析堆疊注意力中的秩崩潰及其對梯度的影響。
- Xiong, R., Yang, Y., He, D., et al. (2020). *On Layer Normalization in the Transformer Architecture*. ICML 2020. https://arxiv.org/abs/2002.04745 — 研究 Transformer 區塊中正規化的位置。
