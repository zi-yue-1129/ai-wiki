# 搜尋與資訊檢索

搜尋引擎決定在數十億項內容中，哪幾項會先被使用者看到。機器學習現在負責這個決策的大部分階段，而生成式模型又帶來一種新的搜尋產品：不只回傳連結，而是直接寫出答案。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 查詢理解 | 拼字校正、查詢分類、以語言模型改寫查詢 | 查詢通常很短且含糊 |
| 候選檢索 | 以 BM25 為基礎的倒排索引；以雙編碼器做的密集檢索；近似最近鄰搜尋 | 必須在毫秒內回傳候選 |
| 排序 | 以梯度提升樹做學習排序；神經交叉編碼器（BERT 類重排序器） | 通常只套用在前幾百個候選上 |
| 個人化與廣告排序 | 點擊率模型、使用者嵌入 | 與推薦系統共用同一套機制 |
| 生成式搜尋與答案引擎 | 附行內引用的檢索增強生成 | 引用不準確是主要的失敗模式 |
| 評估 | 人工相關性判斷、NDCG、線上 A/B 測試 | 點擊紀錄會受位置偏誤影響 |

## 現代搜尋系統如何組合

典型的系統分階段運作。一個成本低的檢索器（稀疏索引、密集向量索引，或兩者並用）挑出數百個候選。接著由學習式排序器重新排列，通常分兩輪，第二輪使用較昂貴的神經模型。最後的後處理層會去除重複內容、套用政策規則；在答案引擎中，還會請語言模型根據前幾份文件，附上引用進行摘要。

## 為什麼困難

- **有偏差的回饋**：使用者只會點擊被展示的結果，因此原始點擊紀錄同時混入了相關性與位置效應。Joachims（2002）展示了如何用點擊資料訓練排序器，而偏誤問題此後一直是核心議題。
- **延遲預算**：準確但慢的神經模型，只能處理較少的候選。
- **長尾查詢**：大多數查詢很少見，因此從紀錄中學習的模型很少見過它們。
- **新鮮度**：索引必須能吸收新文件，而不必整批重建。

## 關鍵方法

有四種方法能解釋目前大部分的技術堆疊。每一項都連到解說它的頁面。

- [Dense Passage Retrieval](../../engineering/vector-databases/dense-passage-retrieval.md)：以兩組獨立的編碼器把查詢與段落映射到同一向量空間，使檢索化為最近鄰搜尋。
- [ColBERT](../../engineering/vector-databases/colbert.md)：為每個詞元保留一個向量，以遲後互動（late interaction）計算查詢與段落的分數，以儲存空間換取準確度。
- [HNSW](../../engineering/vector-databases/hnsw.md)：一種圖結構索引，使近似最近鄰搜尋快到足以用於候選檢索。
- [檢索增強生成](../../engineering/rag/index.md)：把檢索到的文件餵給生成器，是答案引擎的基礎。

神經重排序器通常是針對查詢–段落配對微調過的 [Transformer](../../theory/models/transformer/index.md)（Nogueira & Cho, 2019）。

## 相關連結

- 建構組件（向量資料庫、RAG 流程）見[向量資料庫與語意搜尋](../../engineering/vector-databases/index.md)與[檢索增強生成](../../engineering/rag/index.md)。本頁談的是網路規模的排序，以及建立在其上的產品。
- 排序中的探索（系統必須展示新項目才能學到它們）是一個多臂拉霸機問題，見[上下文多臂拉霸機](../../theory/paradigms/online/contextual-bandits/index.md)。
- 人類記憶部分是依線索進行的檢索，這個類比在[記憶與學習](../../brain-mind/memory-learning/index.md)章節中有所討論。

## 應用

- 網路搜尋與答案引擎
- 企業與文件搜尋，包括法律文件探索（見[法律](../law/index.md)）
- 電子商務商品排序
- 廣告與資訊流排序，與搜尋共用排序模型

## 風險與限制

- **無依據的答案**：Liu 等人（2023）發現，生成式搜尋回應中有許多句子並未被其引用的來源完全支持。
- **回饋迴圈**：若排序器以自身過去的點擊來訓練，會使使用者看到的內容越來越窄。
- **操弄**：搜尋引擎最佳化與 AI 生成內容直接鎖定排序訊號。
- **出版者與流量效應**：答案引擎可能減少來源仰賴的點擊。

## 開放問題

- 在使用者常常只讀答案、不再點進來源的情況下，如何評估答案引擎，而不只看點擊指標。
- 當來源內容被用於生成答案時，如何標示出處並給予補償。

## 參考文獻

### 開創性論文

- Joachims, T. (2002). Optimizing search engines using clickthrough data. *Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/775047.775067 — 展示如何以點擊紀錄作為隱性相關性回饋來訓練排序函數。
- Karpukhin, V. et al. (2020). Dense Passage Retrieval for Open-Domain Question Answering. *EMNLP*. https://arxiv.org/abs/2004.04906 — 分別訓練問題與段落編碼器，使檢索化為密集向量上的最近鄰搜尋。
- Khattab, O. & Zaharia, M. (2020). ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. *SIGIR*. https://arxiv.org/abs/2004.12832 — 以逐詞元方式對查詢與段落評分，兼顧交叉編碼器的準確度與雙編碼器的速度。
- Nogueira, R. & Cho, K. (2019). Passage Re-ranking with BERT. arXiv. https://arxiv.org/abs/1901.04085 — 將 BERT 用作已檢索段落的重排序器，並在段落檢索基準上取得大幅進步。
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS*. https://arxiv.org/abs/2005.11401 — 將檢索器與序列生成器結合，使答案能參考檢索到的文件。

### 綜述與教科書

- Liu, T.-Y. (2009). Learning to Rank for Information Retrieval. *Foundations and Trends in Information Retrieval*. https://doi.org/10.1561/1500000016 — 綜述逐點、逐對與逐列三種學習排序方法。
- Robertson, S. & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*. https://doi.org/10.1561/1500000019 — 說明大多數搜尋引擎仍用於候選生成的稀疏檢索評分函數 BM25 家族。
- Johnson, J., Douze, M. & Jégou, H. (2021). Billion-Scale Similarity Search with GPUs. *IEEE Transactions on Big Data*. https://doi.org/10.1109/TBDATA.2019.2921572 — 介紹 FAISS 函式庫，用 GPU 搜尋極大規模的密集向量集合。

### 文章與文件

- Liu, N. F. et al. (2023). Evaluating Verifiability in Generative Search Engines. arXiv. https://arxiv.org/abs/2304.09848 — 衡量生成式搜尋引擎給出的引用，是否真的支持所附的句子。
