---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/methods/contamination-detection.md
tags:
  - evaluation
  - protocols
  - contamination
aliases:
  - Min-K% Prob
  - Min-K 機率
---

# Min-K% Prob

!!! info "屬於污染偵測"
    本方法頁隸屬於[污染偵測](contamination-detection.zh-TW.md)。它詳細說明以似然度為基礎的方法；上層頁面則比較各種偵測方法。

Min-K% Prob 是一種偵測方法，只利用模型的 token 機率，判斷某段文字是否曾出現在模型的預訓練資料中。它的依據是：模型見過的文字很少含有機率極低的詞，而未見過的文字通常會含有。Shi et al. (2024) 提出此方法，並報告它在 WikiMIA 基準上優於早期的似然度方法。

## 問題

重疊檢查需要訓練語料，而許多模型不公開語料。部分早期的偵測方法需要一個在相似資料上訓練的參考模型。問題在於：只能存取模型的輸出、不知道語料內容時，能否偵測預訓練資料。

## 核心想法

未見過的文字通常含有模型認為非常不可能的詞。已見過的文字則很少如此，因為訓練提高了其中各詞的機率。因此，文字的分數應由其最不可能的 token 決定，而非由平均似然度決定。Min-K% Prob 會對機率最低的 K% token 取對數機率的平均；分數高（低尾端較不令人意外）表示該文字可能在訓練資料中。

## 程序

1. 計算模型在給定前文下，候選文字每個 token 的機率。
2. 依機率排序，保留最低的 K% token。
3. 對保留的 token 取對數機率的平均，即為 Min-K% 分數。
4. 以門檻比較分數，或用來排序候選文字，並以 AUC 評估排序。

此方法不需要參考模型，也不需要訓練攻擊分類器。

## 結果

Shi et al. (2024) 的摘要報告，Min-K% Prob 在 WikiMIA 上比先前方法提升 7.4%。論文以 AUC 報告 WikiMIA 結果，表 1 中 Min-K% Prob 的平均值為 0.72。

## 限制

- **依賴基準。** 所報告的提升來自 WikiMIA。論文的評估並未顯示此方法在程式碼或其他文字類型上的表現。
- **K 的選擇。** 論文在驗證集上掃描 10 至 50 後，採用 k = 20。本頁不能說明 20 對其他語料也是最佳值。
- **判定方向。** 圖 1 表示平均對數似然度高代表屬於預訓練資料，但演算法 1 的寫法相反。重用門檻前，應先確認符號慣例。
- **是排序，不是證明。** 分數只顯示某文字很可能在訓練資料中，無法指出確切使用了哪些文件，因此它是統計訊號，不是定論。
- **模型存取。** 此方法需要模型提供 token 機率，因此無法用於不提供機率的模型。

## 關聯

- 需要語料的精確比對替代方法，見 [N-gram 重疊去污染](ngram-overlap-decontamination.zh-TW.md)。
- 隱私研究中的成員推論攻擊，也以比較模型在已見與未見資料上的行為為基礎。見[成員推論](../../../../society/privacy/membership-inference.zh-TW.md)。

## 開放問題

- 若模型以去重複後的資料訓練（重複文字的機率會降低），這個訊號是否仍然有效？
- 當基準中受污染項目的比例未知時，應如何設定門檻？

## 參考文獻

### 開創性論文

- Shi, W. et al. (2024). *Detecting Pretraining Data from Large Language Models*. arXiv. https://arxiv.org/abs/2310.16789 — 提出 Min-K% Prob，一種不需參考模型的似然度偵測器，並報告在 WikiMIA 上提升 7.4%。
- Carlini, N. et al. (2021). *Extracting Training Data from Large Language Models*. arXiv. https://arxiv.org/abs/2012.07805 — 顯示可以透過查詢模型來抽取其訓練樣本，這也說明了為何要偵測被記住的文本。
- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). *Membership Inference Attacks Against Machine Learning Models*. IEEE Symposium on Security and Privacy. https://arxiv.org/abs/1610.05820 — 研究黑箱存取下，模型是否會洩露某筆紀錄是否在其訓練資料中；似然度偵測與此類攻擊相近。
- Oren, Y. et al. (2023). *Proving Test Set Contamination in Black Box Language Models*. arXiv. https://arxiv.org/abs/2310.17623 — 提出黑箱的污染統計檢定，不需要預訓練資料或模型權重。
- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — 在 C4 網路語料中發現基準評估範例，顯示預訓練文本可能含有測試資料。
