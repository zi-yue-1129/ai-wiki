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
  - LiveBench
  - 持續更新的基準
  - 抗污染基準
---

# LiveBench 與持續更新的基準

!!! info "屬於污染偵測"
    本方法頁隸屬於[污染偵測](contamination-detection.zh-TW.md)。它詳細說明持續更新基準的做法；上層頁面則比較各種偵測方法。

持續更新的基準透過隨時間更換題目來避免污染，使新的測試項目來自模型訓練截止後才發表的來源。LiveBench 就是以此設計的基準：White et al. (2024) 每月新增並更新題目，題目取自近期的材料，並以自動方式計分。與私有測試集不同，LiveBench 會釋出所有題目。

## 問題

靜態基準一旦題目公開，就會開始受到污染。題目進入網路爬取的資料後，之後的模型可能學到這些題目，分數便衡量的是記憶。偵測方法可以事後標出受損的部分，但無法讓一個固定的基準重新變乾淨。問題在於：一開始就讓測試項目不進入訓練資料。

## 核心想法

使用模型訓練時尚未存在的測試項目。題目取自近期來源，並依固定時程持續新增，使每次發布的題目都晚於所比較模型的訓練截止時間。答案以客觀的標準答案計分，而非以 LLM 評審計分，使計分不會因評審模型改變而漂移。

## 程序

依 White et al. (2024) 描述的設計，LiveBench 的一次發布是這樣產生的：

1. 每月從近期的數學競賽、arXiv 論文、新聞文章與資料集中蒐集新題目。
2. 加入較難、用來限制污染的舊任務版本，例如 Big-Bench Hard、AMPS 與 IFEval。
3. 以客觀的標準答案自動為每個答案計分。
4. 公開題目、程式碼與模型答案，使他人能重新執行該基準。

## 結果

White et al. (2024) 的摘要描述了設計與目標；它沒有報告任何模型的代表性分數，本頁也不提供。摘要指出，題目會「每月新增與更新」，且所有題目、程式碼與模型答案都會釋出。

## 限制

- **截止時間未公開。** 持續更新的基準假設最新題目晚於各模型的訓練資料，但對截止時間未知的模型，這個假設無法驗證。
- **維護成本。** 每月蒐集需要人力或流程，而舊版本的題目仍可能被複製。
- **來源範圍窄。** 來自競賽、論文與新聞的題目，較適合某些能力而非其他能力。
- **公開釋出。** 釋出所有題目意味著題目一旦公開，對之後訓練的模型就不再乾淨。這是刻意的設計，但也限制了舊版本與新版本分數的可比性。

## 關聯

- 偵測靜態基準污染的方法，見 [N-gram 重疊去污染](ngram-overlap-decontamination.zh-TW.md) 與 [Min-K% Prob](min-k-percent-prob.zh-TW.md)。
- 私有測試集是另一種保持題目隱藏的做法，它以開放性換取對誰能看到題目的控制。
- 採用此設計的基準家族，列在[評估](../../../../theory/evaluation/index.zh-TW.md)之下。

## 開放問題

- 隨著訓練語料變大，基準需要多久更新一次，才能維持乾淨？
- 能否使新題目與舊題目可比，以便長期追蹤分數？

## 參考文獻

### 開創性論文

- White, C. et al. (2024). *LiveBench: A Challenging, Contamination-Limited LLM Benchmark*. arXiv. https://arxiv.org/abs/2406.19314 — 描述每月更新、以客觀計分設計、用來限制測試集污染的基準。
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 大型靜態基準，其任務檔案內含防止網路爬取的金絲雀字串，是解決同一問題的另一種做法。
- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — 顯示基準範例可能出現在網路語料中，這也是持續更新基準存在的原因。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 報告 13-gram 重疊分析，推動了對基準的仔細清理。
