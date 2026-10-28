---
translation_reviewed: 2026-10-28
---

# OpenScholar（Asai 等人，2024）

OpenScholar 是一個檢索增強的語言模型，用來回答有關科學文獻的問題。它會搜尋一個包含 4,500 萬篇開放取用論文的資料庫，並撰寫附帶引用的長篇答案。Akari Asai 及其同事於 2024 年發表此方法。它是父頁面[AI 用於 AI 研究](../index.md)中的文獻回顧方法。

## 概述

綜整一個領域的文獻既費時，語言模型又常常捏造參考文獻。作者報告，在他們的實驗中，GPT-4o 捏造引用的比例為 78% 至 90%（Asai 等人，2024）。較早的系統也曾嘗試回答關於論文的問題，PaperQA（Lála 等人，2023）便是一例；而讓生成文字以檢索到的來源為依據的廣義做法，稱為[檢索增強生成](../../../engineering/rag/index.md)（Lewis 等人，2020）。將生成文字的引用品質視為可量測的性質，則是 Gao 等人（2023）的研究。

OpenScholar 的答案由檢索到的段落組成，因此每一項主張都能指向系統實際找到的來源。這與一般的[搜尋與資訊檢索](../../search-and-information-retrieval/index.md)問題不同，因為它的輸出是綜整後的答案，而不是排序後的文件清單。

## 關鍵概念

- **資料庫**：包含 4,500 萬篇開放取用論文的集合，已建立索引以便搜尋。
- **檢索器**：負責為問題找出候選段落的元件。
- **引用準確度**：每一段被引用的文字，是否支持其所附的句子。[RAG](../../../engineering/rag/index.md) 系統通常以此評判。
- **自我回饋迴圈**：模型審視自己的草稿，並可能在修訂答案前檢索更多證據。
- **ScholarQABench**：作者為測試文獻搜尋與綜整而建立的基準測試。

## 運作方式

系統遵循「檢索、起草、修訂」的循環：

1. 問題送交檢索器，後者從資料庫中回傳候選段落。
2. 語言模型閱讀這些段落並起草答案，將每一項主張附上對應的段落。
3. 在自我回饋步驟中，模型審視其草稿，並可能檢索更多段落來強化薄弱的主張。
4. 修訂後的答案連同其引用一併回傳。

作者將檢索器、資料庫與回饋迴圈合稱為一個推論迴圈。他們也顯示，同一個迴圈可以改進既有的模型：OpenScholar-GPT4o 使 GPT-4o 的正確率提升了 12%（Asai 等人，2024）。

## 結果

在 ScholarQABench 上，該基準包含 2,967 條由專家撰寫的查詢與 208 則長篇答案，涵蓋電腦科學、物理、神經科學與生物醫學。OpenScholar-8B 在正確率上勝過 GPT-4o 5%，勝過 PaperQA2 7%。作者指出，OpenScholar-8B 是一個較小的開源模型。其引用準確度與人類專家相當。

在人工評估中，專家認為 OpenScholar-8B 的回應優於專家撰寫的答案的比例為 51%，認為 OpenScholar-GPT4o 的回應較優的比例為 70%。GPT-4o 的相應數字為 32%。

## 限制

- **開放取用的涵蓋範圍。** 資料庫只包含開放取用的論文，因此付費牆後的著作不在綜整之中。讀者應檢查被省略的著作是否會改變整體圖像。
- **引用不等於正確。** 正確的引用只表示一段文字支持某句話，並不表示被引用的研究穩健、具代表性或仍然有效。
- **基準的適配性。** 查詢由專家為基準而撰寫，可能與特定研究者實際提出的問題不符。
- **平衡性取決於文獻。** 綜整反映的是已發表並被索引的內容。若某領域存在發表偏誤，答案也會繼承這種偏誤。

## 開放問題

- 這類系統能否權衡相互衝突的研究，而不只是引用它們？
- 隨著文獻增長，資料庫應如何保持更新？
- 依賴經綜整的回顧，是否會減少研究者閱讀原始文獻的頻率？Messeri 與 Crockett（2024）對 AI 輔助科學整體提出了這項疑慮。

## 參考文獻

### 開創性論文

- Asai, A. 等人（2024）。OpenScholar: Synthesizing Scientific Literature with Retrieval-augmented LMs。arXiv。https://arxiv.org/abs/2411.14199 — 檢索增強模型，從 4,500 萬篇開放取用論文中撰寫附帶引用的答案，並附有新的基準測試。
- Lewis, P. 等人（2020）。Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks。arXiv。https://arxiv.org/abs/2005.11401 — 提出檢索增強生成，讓生成器可以利用檢索器取得的文件。

### 文章與文件

- Gao, T. 等人（2023）。Enabling Large Language Models to Generate Text with Citations。arXiv。https://arxiv.org/abs/2305.14627 — 研究如何讓語言模型的輸出引用支持性證據，以及如何衡量引用品質。
- Lála, J. 等人（2023）。PaperQA: Retrieval-Augmented Generative Agent for Scientific Research。arXiv。https://arxiv.org/abs/2312.07559 — 代理人會檢索並評估全文科學文章，以附帶引用的方式回答問題。
- Messeri, L. & Crockett, M. J.（2024）。Artificial intelligence and illusions of understanding in scientific research。*Nature*。https://doi.org/10.1038/s41586-024-07146-0 — 評論文章，探討 AI 工具如何讓研究者產生理解的錯覺，與信任綜整文獻的問題相關。
