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
  - N-gram overlap decontamination
  - 13-gram 去污染
  - n-gram 重疊去污染
---

# N-gram 重疊去污染

!!! info "屬於污染偵測"
    本方法頁隸屬於[污染偵測](contamination-detection.zh-TW.md)。它詳細說明重疊方法；上層頁面則比較各種偵測方法。

N-gram 重疊去污染會在訓練語料中搜尋與基準測試項目共享的長詞序列，並移除或標記相符的項目。它是檢查污染最直接的方法，也是 GPT-3 所用的主要方法（Brown et al., 2020）。它的弱點是只能找到逐字相同的複本。

## 問題

只有在模型沒有見過測試項目時，基準分數才能衡量能力。網路規模的訓練語料很龐大，而基準題目又會公開張貼，因此複本可能在無人選擇的情況下進入訓練資料。問題在於找出這些複本，並只在其餘項目上報告分數。

## 核心想法

把每個測試項目與每份訓練文件切成固定長度的詞序列（即 n-gram）。若某項目與訓練資料共享足夠長的 n-gram，就將它標記。被標記的項目會從基準的乾淨版本中移除，分數則在乾淨版本上報告。

## 程序

1. 選定視窗大小 n。Brown et al. (2020) 使用 13-gram：若測試項目與預訓練資料有 13-gram 重疊，即予以標記。短於 13 個詞的項目則整體比對。
2. 為訓練語料建立索引，例如對每個 n-gram 建立雜湊。
3. 對每個測試項目，檢查其中是否有任何 n-gram 出現在索引中。
4. 移除被標記的項目，或另行報告，並在乾淨子集上重新計算分數。

視窗大小需要權衡。視窗太短會標記出只是常見片語、並非真正複本的項目；視窗太長則會漏掉經過小幅修改的複本。

## 結果

Brown et al. (2020) 第 4 節描述了這個程序及其對 GPT-3 的影響。透過機器抽取讀取的論文正文報告：污染相當常見，但對多數資料集的影響很小，而且影響「並不如擔心的那樣大」。對 LAMBADA，作者報告影響可忽略；對 Winograd，影響則很小。抽取的文字未包含乾淨版與完整版的分數表，因此本頁不提供這些數字。論文也記錄了一個錯誤：它只移除了部分被偵測到的重疊，這提醒我們清理本身也需要測試。

Dodge et al. (2021) 從語料端顯示了同樣的風險。他們對 C4 語料的記錄發現，其中含有其他基準 NLP 資料集的評估範例。

## 限制

- **只能精確比對。** 改寫、翻譯或格式改變過的項目，會保留答案，卻逃過 n-gram 檢查。
- **語料未公開。** 此檢查需要訓練資料；許多供應商不釋出資料，因此只能由供應商執行，或無從執行。
- **視窗選擇。** 結果取決於 n 與斷詞方式。使用不同視窗的團隊，可能得到不同的乾淨子集。
- **無法證明不存在。** 通過檢查只表示未找到長的複本，並不表示模型從未見過該項目。

## 關聯

- 不需要語料的機率型替代方法，見 [Min-K% Prob](min-k-percent-prob.zh-TW.md)。
- 透過更換題目來避免問題的基準，見 [LiveBench](livebench.zh-TW.md)。
- 資料切分的風險與前處理的洩漏規則，見[評估協定概述](../index.zh-TW.md)。

## 開放問題

- 對於網路文本與依教科書撰寫的測試項目中常見的改寫複本，去污染應如何處理？
- 供應商不公開語料時，能否透過第三方稽核報告乾淨的分數？

## 參考文獻

### 開創性論文

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 介紹 GPT-3，並描述訓練資料與基準測試集之間的 13-gram 重疊過濾及其影響。
- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — 記錄 C4，並在語料中發現其他基準資料集的評估範例。
- Carlini, N. et al. (2021). *Extracting Training Data from Large Language Models*. arXiv. https://arxiv.org/abs/2012.07805 — 顯示語言模型會重現被記住的訓練文本，這就是測試項目完全相同的複本之所以重要的原因。
- Oren, Y. et al. (2023). *Proving Test Set Contamination in Black Box Language Models*. arXiv. https://arxiv.org/abs/2310.17623 — 提出黑箱的污染統計檢定，是無法搜尋語料時的替代方案。
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — BIG-bench 基準，其任務檔案內含用來防止網路爬取的金絲雀字串。
