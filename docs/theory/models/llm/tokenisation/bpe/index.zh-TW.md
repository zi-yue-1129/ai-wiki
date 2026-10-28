---
translation_reviewed: 2026-10-28
---

# 位元組對編碼（Byte-Pair Encoding，Sennrich et al., 2016）

位元組對編碼（BPE）透過反覆合併語料中最常相鄰的一對符號，來建立子詞詞彙表。它是語言模型中使用最廣泛的分詞器方法家族。它在其他方法中的位置，已在上層主題頁[分詞](../index.md)中說明。

## 概述

BPE 最初是一種無損的資料壓縮想法：把檔案中最常見的一對位元組，替換成一個未使用的新位元組，並記錄這個替換。Sennrich、Haddow 與 Birch（2016）把它改編用於神經機器翻譯。當時的翻譯系統使用固定的單字詞彙表，因此罕見字與人名會被對映到同一個未知符號，無法翻譯。他們的提議是把這類字切分成從訓練文字學到的子詞單位，使罕見字可以由語料中常見的片段組成。

## 關鍵概念

- **符號（Symbol）**：起始單位，即一個字元或一個位元組。合併會在訓練過程中把符號組成較長的單位。
- **合併規則（Merge rule）**：一對有順序的符號，會被接成一個新符號。學到的合併清單本身就是分詞器。
- **貪婪合併（Greedy merging）**：每一步都選取目前最頻繁的一對。結果取決於合併的順序，並不保證在任何全域標準下是最佳的。

## 運作方式

訓練依下列編號步驟進行：

1. 計算語料中每個不同的字，並把每個字拆成字元，在最後一個符號後加上字尾標記。
2. 統計所有字中每一對相鄰符號的出現次數，以字的頻率加權。
3. 選出使加權計數 $f(a,b)$ 最大的一對 $(a, b)$，並建立新符號 $ab$。
4. 把詞頻表中每一處 $a\ b$ 替換為 $ab$，並記錄規則 $a + b \rightarrow ab$。
5. 重複步驟 2 至 4，直到詞彙表達到目標大小，或合併的次數預算用完為止。

編碼新的字時，從它的字元開始，依學習的順序套用已記錄的合併，直到再也沒有可套用的為止。訓練時沒見過的字仍然可以編碼，因為基礎字母表中的每個字元都有對應項目。位元組級的變體更進一步：它從 256 個位元組值開始，因此沒有任何輸入會是未知的（Wang et al., 2019）。

有兩個近親值得一提。WordPiece 在 GNMT 系統中有描述（Wu et al., 2016），它保留同樣的合併迴圈，但依合併對訓練似然度的影響來評分，而非依原始頻率。

## 結果

Sennrich et al. 在機器翻譯基準上評估 BPE 切分，並把它與以單字為單位的系統，以及處理罕見字的回退字典方法作比較。他們以 BLEU 報告翻譯品質，並得出子詞切分改善了罕見字處理的結論。確切分數見原論文，此處不重複。

## 限制

- **貪婪且依順序。** 每次合併都是局部選擇，因此最終詞彙表不一定是該語料的最佳選擇。
- **依賴語料。** 合併結果反映訓練文字。來自其他領域或文字系統的文字會被切成更多、更小的片段，而在合併資料中稀少的語言受到的影響最大。
- **每個字只有一種切法。** 確定性的切分讓模型只看到每個字的單一版本。子詞正則化（Kudo, 2018）部分就是為了解決這點而提出的。
- **預分詞與合併互相影響。** 空白與標點的邊界劃在哪裡，決定了哪些合併得以發生，因此兩個都說自己用 BPE 的系統，行為可能不同。
- **語言之間的公平性。** 正如 Petrov et al. (2023) 對多種分詞器所示，同樣的內容在不同語言中可能需要相差很大的詞元數。

## 開放問題

- 學到的合併反映的是形態還是頻率？兩者能否被乾淨地區分，目前並不清楚。
- 在資料與運算量受控制的情況下，以似然度為基礎的合併（WordPiece）或取樣切分（Kudo, 2018）在大規模時是否能產生更好的模型？

## 相關連結

- 上層主題：[分詞](../index.md)。
- 同一頁面家族中的相關方法：[SentencePiece](../sentencepiece/index.md)，它以 unigram 模型取代合併；以及 [ByT5](../byt5/index.md)，它移除了學習得來的詞彙表。

## 參考文獻

### 開創性論文

- Sennrich, R., Haddow, B. & Birch, A. (2016). *Neural Machine Translation of Rare Words with Subword Units*. ACL. https://arxiv.org/abs/1508.07909 — 為神經機器翻譯引入位元組對編碼，使罕見字與未見過的字能由已知的子詞單位組成。
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation*. arXiv. https://arxiv.org/abs/1609.08144 — 描述 GNMT 系統及其所用的 wordpiece 切分，這是一種類似 BPE、用於實際翻譯服務的子詞方法。
- Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates*. ACL. https://arxiv.org/abs/1804.10959 — 提出在訓練時，從 unigram 語言模型取樣多種切分結果。

### 綜述與教科書

- Mielke, S. J. et al. (2021). *Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP*. arXiv. https://arxiv.org/abs/2112.10508 — 回顧 NLP 如何從字走向字元與子詞，並整理每種單位的取捨。

### 文章與文件

- Wang, C., Cho, K. & Gu, J. (2019). *Neural Machine Translation with Byte-Level Subwords*. arXiv. https://arxiv.org/abs/1909.03341 — 把位元組級 BPE 應用於翻譯，使任何文字都能以 256 個位元組值組成的基礎詞彙表來編碼。
- Petrov, A. et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages*. arXiv. https://arxiv.org/abs/2305.15425 — 顯示分詞器可能讓同樣的內容在某些語言中所需的詞元數遠多於英文。
- Schmidt, C. W. et al. (2024). *Tokenization Is More Than Compression*. arXiv. https://arxiv.org/abs/2402.18376 — 主張單靠壓縮率無法預測分詞器在下游語言建模中的表現，並以其他標準比較各種分詞器。
