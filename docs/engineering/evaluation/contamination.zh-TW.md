---
translation_reviewed: 2026-10-28
---

# 基準測試污染

基準測試污染（benchmark contamination）指測試題目，或其近似的複本，出現在模型的訓練資料中。一個已經見過答案的模型，可能靠回憶就拿到高分，因此報告中的進步，可能反映的是訓練語料，而非基準本來要衡量的能力。對封閉模型而言，這個問題很難排除，也是領域逐漸轉向動態與私有測試集的原因之一。

## 概述

語言模型以大規模網路爬取的資料訓練，而基準測試也發布在同一個網路上。測試題目會出現在論文、部落格文章與程式碼儲存庫中，每一份複本都可能被爬蟲收錄。Dodge et al. (2021) 在 Colossal Clean Crawled Corpus 中發現了其他 NLP 基準的評估範例，顯示這個問題是結構性的，而非少數粗心作者的過失。

基準分數用來排名模型、影響決策，因此被高估的分數可能讓較弱的模型排在較強的模型之前。[評估總覽](index.md)把資料污染列為常見陷阱之一；[基準測試套件](benchmark-suites.md)則討論飽和現象，在這種狀態下，即使是少量的資料外洩，也足以決定排名。

## 關鍵概念

- **資料污染（contamination）**：測試題目（逐字或換句話說）出現在訓練資料中。
- **記憶化（memorisation）**：模型重現某段訓練序列，而非從中歸納出規律。這是資料污染使分數膨脹的機制。
- **膨脹（inflation）**：模型在洩漏題目上的分數，與在難度相近的未見題目上的分數之間的差距。
- **去污染（decontamination）**：訓練前，把類似測試內容的文字從訓練資料中移除，通常透過比對詞序列來進行。
- **金絲雀字串（canary string）**：放在文件中的獨特隨機標記。它可以請爬蟲略過該文件，也可以事後揭示該文件是否被用於訓練。
- **動態基準（dynamic benchmark）**：題目會隨時間更新的測試，讓較新的模型面對它們不可能見過的題目。
- **私有基準（private benchmark）**：題目不對外公開的測試。

## 運作方式

最直接的途徑，是測試集的完整複本出現在爬取的資料中。較不明顯的途徑包括發布後被張貼的解答，以及由已見過該基準的模型所生成的合成訓練資料（見[合成資料](../synthetic-data/index.md)）。

```mermaid
flowchart LR
  A[基準發布到網路上] --> B[被收錄進網路爬取資料]
  B --> C[模型在該語料上預訓練]
  C --> D[在相同題目上評估模型]
  D --> E[分數反映的是回憶]
  E --> F[膨脹後的比較結果]
```

記憶化取決於某段文字出現的次數。Carlini et al. (2022) 發現，記憶化會隨模型規模、範例被重複的次數，以及提示所用的上下文長度而增加。 Lee et al. (2021) 則指出，常見語料中有大量近似重複的文字；移除這些重複後，模型逐字輸出的情況與訓練與測試之間的重疊都減少了。

### 資料污染如何使分數膨脹

當洩漏的題目是靠記憶而非能力作答時，資料污染就會使分數膨脹；但影響的大小因基準而異。在 GPT-3 的分析中，約四分之一的基準其潛在污染超過 50%，但在乾淨子集上，多數分數的變化很小。作者的結論是：他們保守的過濾方式可能高估了污染，或是污染本來影響就不大。[^gpt3] 其中少數幾組，例如字詞重組與閱讀理解，被標記為需要進一步檢查。

去污染也比表面上困難。GPT-3 的作者原本試圖移除重疊的文字，但因為一個程式錯誤，只有部分成功；而重新訓練的成本太高，無法再做一次（Brown et al., 2020）。沒有發現 n-gram 重疊，也不能證明基準是乾淨的（Yang et al., 2023）。因此，Sainz et al. (2023) 主張，應針對每個基準分別衡量資料污染。

## 關鍵方法

偵測方法各自需要的條件不同：有些需要訓練語料，而封閉模型通常不公開語料；另一些則只需要輸出或權杖機率。它們回答的問題也不同：某段文字是否在語料中，或是模型是否記住了它。

| 方法 | 需要什麼 | 能顯示什麼 | 主要限制 |
|---|---|---|---|
| n-gram 重疊 | 可存取語料 | 測試集與語料之間共享的詞序列 | 無法發現換句話說與翻譯後的內容（Yang et al., 2023） |
| 金絲雀字串與版權陷阱 | 能控制被植入的文字 | 植入的文字是否被學會 | 對未被標記的基準毫無說明 |
| 似然檢定 | 權杖機率 | 異常可預測的測試題目 | 在 LLM 上，成員推論的訊號幾乎不比隨機猜測好（Duan et al., 2024） |
| 順序檢定 | 打亂後題目順序的似然 | 黑箱模型中可證明的資料污染 | 需要可交換的基準，且題目數量要足夠 |
| 槽位猜測 | 提示後的輸出 | 模型補全測試題目被隱藏的部分 | 取決於模型是否願意補全該題 |

**n-gram 重疊**是最實用的方法。GPT-3 的作者以 13-gram 比對，標記出與訓練集相符的測試題目，並在移除這些題目後，重新評分一個「乾淨」子集（Brown et al., 2020）。它的弱點是只能找出共享的字串。

**金絲雀字串**是植入文件中的獨特序列。Carlini et al. (2018) 把隨機序列植入訓練資料，以衡量模型對稀有文字的記憶程度。Meeus et al. (2024) 將這個概念應用於版權，在書籍中植入虛構的條目。他們發現，中等長度、重複 100 次的陷阱無法被偵測，但較長且重複多次的序列可以，因此標記必須強到足以被記住。

**似然檢定**詢問模型是否覺得某段文字異常可預測。Li (2023) 在不取得完整語料的情況下，以困惑度估計基準的資料污染，發現閱讀理解與摘要基準中有記憶化的跡象，選擇題基準則較少。Shi et al. (2023) 提出 Min-K% Prob，觀察段落中機率最低的權杖。Duan et al. (2024) 發現，在 Pile 上訓練的模型中，成員推論的表現幾乎不比隨機猜測好，因此這類訊號仍不可靠。

**順序檢定**依據一個簡單的觀察：對於可交換的題目，乾淨的模型應認為每種順序的可能性相同；受污染的模型則傾向偏好原始順序。Oren et al. (2023) 把這點發展成一個統計檢定，只需要黑箱似然即可進行，並在五個常用的公開模型上做了審計，未發現普遍的資料污染。

**槽位猜測**會隱藏測試題目的一部分，並要求模型補上。Deng et al. (2023) 把這種做法與以檢索為基礎、搜尋預訓練語料的方法結合。若模型能正確猜出被隱藏的文字，就表示該題目可能曾被見過。

### 預防資料污染

常見的做法有三種，各有代價。

- **去污染的訓練資料**：在訓練前，把語料與已知的測試集進行過濾或去重。它只能移除已被識別的文字，效果也受比對方法的限制。
- **動態基準**：LiveCodeBench 持續收集發布時間較晚的程式設計題目，使每個模型都能在其訓練截止後才發布的題目上接受測試（Jain et al., 2024）。動態基準需要持續維護；而且不同題目集上的分數較難比較。
- **私有或加密的測試資料**：Jacovi et al. (2023) 建議以公鑰加密公開的測試資料，並以禁止衍生使用的條款授權，使題目不會以明文形式被爬取。私有測試集較不容易外洩，但外部團體無法檢視，因此會限制結果的可重現性。

## 連結

- **基準測試。** 資料污染是[評估與基準](index.md)中所討論的效度威脅之一，也適用於[基準測試套件](benchmark-suites.md)所討論的套件，例如 MMLU 與 HumanEval。
- **隱私。** 同樣的機制，也就是記憶化與似然檢定，也可以用來保護個人，而不是用來為模型評分。[成員推論](../../society/privacy/membership-inference.md)與[訓練資料萃取](../../society/privacy/training-data-extraction.md)涵蓋隱私方面的內容。
- **資料整理。** 去污染依賴網路語料中常用的近似重複偵測；見[MinHash 去重](../data/minhash-deduplication.md)。
- **代理人。** 當代理人基準的任務取自公開的儲存庫時，會面臨同樣的問題；見[SWE-bench](../agents/agent-evaluation/swe-bench/index.md)。
- **心理學。** 人類考試也有類似的問題：事先看過考題的學生，得分中有一部分反映的是對該考題的回憶。見[心理學與 AI](../../brain-mind/psychology/index.md)。

## 應用

- **報告。** 實驗室可以公布去污染的方法與乾淨子集上的分數，就像 GPT-3 所做的那樣，讓讀者判斷其影響。
- **獨立審計。** 只需要模型輸出的測試，讓外部研究者也能檢查封閉模型，如 Oren et al. (2023) 所示。
- **依時間標記的評估。** 在每個模型的截止時間之後才加入題目的基準，能降低模型見過測試題目的機會（Jain et al., 2024）。

## 開放問題

- 在大型模型上，成員推論的訊號幾乎不比隨機猜測好（Duan et al., 2024）。只憑封閉模型的輸出，能取得哪些可靠的證據？
- 偵測方法能否抵抗改寫？n-gram 與似然方法可能漏掉換句話說的內容（Yang et al., 2023）。
- 動態基準一旦發布，題目就會進入網路。一道題目要多久才會不再受到污染？

## 參考文獻

### 開創性論文

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 的論文，其評估章節標記了基準與訓練資料的重疊，並重新評分乾淨子集。
- Carlini, N. et al. (2018). *The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks*. arXiv. https://arxiv.org/abs/1802.08232 — 將稀有的隨機序列植入訓練資料，以衡量模型記住它們的程度。
- Carlini, N. et al. (2022). *Quantifying Memorization Across Neural Language Models*. arXiv. https://arxiv.org/abs/2202.07646 — 顯示記憶化會隨模型規模、重複次數與提示上下文而增加。
- Lee, K. et al. (2021). *Deduplicating Training Data Makes Language Models Better*. arXiv. https://arxiv.org/abs/2107.06499 — 顯示常見語料中的近似重複會導致逐字輸出，且訓練與測試之間的重疊在標準資料集中很常見。
- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — 為 C4 建立文件，並報告其文字中包含其他基準的評估範例。

### 相關工作

- Deng, C. et al. (2023). *Investigating Data Contamination in Modern Benchmarks for Large Language Models*. arXiv. https://arxiv.org/abs/2311.09783 — 為訓練資料不公開的模型，引入以檢索為基礎的重疊搜尋與槽位猜測協定。
- Yang, S. et al. (2023). *Rethinking Benchmark and Contamination for Language Models with Rephrased Samples*. arXiv. https://arxiv.org/abs/2311.04850 — 顯示換句話說或翻譯後的測試資料，可以繞過 n-gram 去污染。
- Oren, Y. et al. (2023). *Proving Test Set Contamination in Black Box Language Models*. arXiv. https://arxiv.org/abs/2310.17623 — 提出針對基準題目順序的可交換性檢定，並審計五個公開模型。
- Sainz, O. et al. (2023). *NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark*. arXiv. https://arxiv.org/abs/2310.18018 — 立場論文，主張應針對每個基準衡量資料污染，因為它會使分數膨脹。
- Li, Y. (2023). *Estimating Contamination via Perplexity: Quantifying Memorisation in Language Model Evaluation*. arXiv. https://arxiv.org/abs/2309.10677 — 在無法取得完整訓練集的情況下，以困惑度估計基準的資料污染。
- Shi, W. et al. (2023). *Detecting Pretraining Data from Large Language Models*. arXiv. https://arxiv.org/abs/2310.16789 — 提出 Min-K% Prob，一種不需要參考模型的預訓練資料偵測方法。
- Duan, M. et al. (2024). *Do Membership Inference Attacks Work on Large Language Models?*. arXiv. https://arxiv.org/abs/2402.07841 — 發現在 Pile 上訓練的模型中，成員推論的表現幾乎不比隨機猜測好。
- Jacovi, A. et al. (2023). *Stop Uploading Test Data in Plain Text: Practical Strategies for Mitigating Data Contamination by Evaluation Benchmarks*. arXiv. https://arxiv.org/abs/2305.10160 — 提出以加密方式公開測試資料，並以禁止衍生使用的條款授權。
- Jain, N. et al. (2024). *LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code*. arXiv. https://arxiv.org/abs/2403.07974 — 以發布時間較晚的競賽題目建立程式碼基準。
- Meeus, M. et al. (2024). *Copyright Traps for Large Language Models*. arXiv. https://arxiv.org/abs/2402.09363 — 在有版權的文字中植入虛構條目，並測試它們何時能被偵測。

[^gpt3]: Brown et al. (2020), 第 4 節，見參考文獻。論文指出，約四分之一的基準其潛在污染超過 50%。
