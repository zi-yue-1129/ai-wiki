---
translation_reviewed: 2026-10-28
---

# BERT：雙向編碼器預訓練（Devlin et al., 2018）

BERT 是一個僅編碼器的 Transformer，預訓練時從左右兩側的脈絡恢復被遮住的詞，之後再加上一個輸出層進行微調。它是 [Transformer 架構家族](../index.md)中具代表性的僅編碼器模型。

## 概觀

在 BERT 之前，預訓練語言模型不是基於特徵的，就是從左到右的。ELMo（Peters et al., 2018）分別運行從左到右與從右到左的兩個 LSTM，並把它們的輸出當作額外特徵使用。OpenAI GPT 則對整個從左到右的 Transformer 進行微調。BERT 的作者主張，從左到右的限制對詞元層級的任務有害，例如問答，因為答案取決於兩側的脈絡。

BERT 保留了編碼器的雙向自注意力，並以遮罩目標取代下一個 token 預測來進行預訓練。之後，同一個網路會在每個下游任務上進行微調。

BERT 是[架構家族](../index.md)中的一員，與僅解碼器的 [GPT-3](../../../llm/gpt-3-few-shot/index.md) 以及編碼器—解碼器的 [T5](../t5/index.md) 並列。遮罩目標是[遮罩預測](../../../../paradigms/self-supervised/masked-prediction/index.md)的一個特例，[DistilBERT](../../../../model-compression/knowledge-distillation/response-based/distilbert/index.md) 則示範如何縮小它。更大的脈絡見 [Transformers & Attention](../../index.md)。

## 關鍵概念

- **WordPiece token。** 文字被切成次詞單位。每個輸入開頭都有特殊的 `[CLS]` token，兩個句子打包成同一序列時，中間以 `[SEP]` 分隔。
- **遮罩語言模型（MLM）。** 隱藏部分 token，並要求模型恢復它們的預訓練目標。
- **下一句預測（NSP）。** 針對句子對的二元任務：句子 B 是語料中 A 之後的句子，還是隨機選取的句子？
- **微調。** 在預訓練網路上加一個輸出層，並在標註資料上訓練所有權重。

## 運作方式

依 Devlin et al.（2018）所述的預訓練程序：

1. 以兩段文字 A 與 B 建立每個訓練樣本。一半時候 B 是真正的下一句，另一半時候是隨機句子。
2. 隨機選出 15% 的 token 位置。其中 80% 替換為 `[MASK]`，10% 替換為隨機 token，其餘 10% 保持不變。
3. 讓序列通過雙向 Transformer。MLM 損失使用被選中位置的隱藏向量，NSP 損失使用 `[CLS]` 的向量。
4. 最小化兩個損失的總和：

$$
\mathcal{L} = \mathcal{L}_{\text{MLM}} + \mathcal{L}_{\text{NSP}}
$$

5. 微調時，加上一個輸出層（句子層級任務接在 `[CLS]` 上，標註與問答等任務則接在每個 token 上），並訓練所有權重。

論文中的兩種模型尺寸為：BERT-Base，12 層、隱藏維度 768、12 個注意力頭，共 1.1 億參數；BERT-Large，24 層、隱藏維度 1024、16 個注意力頭，共 3.4 億參數。

## 結果

論文的主要結果來自 BERT-Large。摘要中，BERT 把 GLUE 分數推到 80.5%、MultiNLI 準確率推到 86.7%、SQuAD v1.1 測試集 F1 推到 93.2、SQuAD v2.0 測試集 F1 推到 83.1，每一項都明顯超過先前的最佳結果。

開發集上的消融實驗（論文表 5，BERT-Base）分離出兩項設計的效果。把目標從雙向 MLM 改為沒有 NSP 的從左到右語言模型，會使 MRPC 準確率從 86.7 降到 77.5，SQuAD F1 從 88.5 降到 77.8。只移除 NSP 時，SQuAD F1 從 88.5 降到 87.9，MNLI 準確率從 84.4 降到 83.9。

## 限制

- **訓練與測試不一致。** 微調時從不出現 `[MASK]` token。10% 的隨機替換與 10% 的原樣保留能減輕、但無法消除這個落差。
- **每個 token 的訊號較少。** 每個樣本中只有約 15% 的位置提供訓練訊號，使預訓練成本偏高。後續研究直接處理這點：ELECTRA（Clark et al., 2020）訓練一個判別器去偵測被替換的 token，並報告較佳的樣本效率。
- **不是生成器。** 雙向編碼器不會由左至右產生文字，因此不用於開放式生成。
- **預訓練配方不足。** RoBERTa（Liu et al., 2019）重新檢視了 BERT 的預訓練選擇，包括訓練預算，並報告 BERT 訓練嚴重不足。

## 未解問題

- 遮罩預測是理解文字的最佳目標嗎？還是在相同運算量下，判別式目標表現更好？
- NSP 的貢獻有多大？在上述消融中，移除它使每個開發任務的分數都下降，其中 QNLI 的下降幅度最大，而後續的復現研究重新檢視了整個預訓練配方（Liu et al., 2019）。
- 遮罩詞模型與人類語言處理有多相似？Caucheteux 與 King（2022）顯示的是相關性，而非共享的機制。

## 參考文獻

### 開創性論文

- Devlin, J., et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv；NAACL 2019. https://arxiv.org/abs/1810.04805 — 原始論文，提出遮罩語言模型、下一句預測與微調的配方。
- Peters, M. E., et al. (2018). *Deep contextualized word representations*. arXiv；NAACL 2018. https://arxiv.org/abs/1802.05365 — ELMo，基於特徵的雙向語言模型，BERT 的作者以它作為對照。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — BERT 所堆疊並以雙向方式訓練的 Transformer 編碼器。

### 綜述與教科書

- Liu, Y., et al. (2019). *RoBERTa: A Robustly Optimized BERT Pretraining Approach*. arXiv. https://arxiv.org/abs/1907.11692 — 對 BERT 預訓練的復現研究，衡量超參數與資料量的影響。

### 文章與文件

- Clark, K., et al. (2020). *ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators*. arXiv；ICLR 2020. https://arxiv.org/abs/2003.10555 — 遮罩建模的替代方案，訓練判別器去偵測被替換的 token，樣本效率較高。
- Caucheteux, C. & King, J.-R. (2022). Brains and algorithms partially converge in natural language processing. *Communications Biology*. https://doi.org/10.1038/s42003-022-03036-1 — 把包括遮罩詞模型在內的深度語言模型與大腦反應做比較，發現預測能力推動了相似性。
