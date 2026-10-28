---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - How false news spreads
  - 假新聞傳播
---

# 假新聞如何傳播

!!! info "屬於不實資訊與深偽"
    本方法頁隸屬於[不實資訊與深偽](index.md)。它詳細說明一項研究；上層頁面則將它與其他研究並列比較。

Vosoughi、Roy 與 Aral（2018）以大量經事實查核判定過的謠言轉推串，衡量真實與虛假故事在 Twitter 上的傳播方式。他們的主要發現是：假新聞比真新聞傳播得更遠、更快、更深、更廣，而造成差異的主因是人類而非自動化帳號。

## 問題

不實資訊常被歸咎於機器人或排序內容的演算法。如果這是對的，介入措施就應該針對機器。問題在於：假新聞的傳播方式是否與真新聞不同？如果是，自動化帳號能否解釋這種差異？

## 核心想法

把每則故事的傳播重建為轉推串，然後以相同的指標比較真假轉推串：觸及多少人、傳播多快、轉傳鏈有多深，以及擴散到多少不同的社群。另外單獨量測自動化帳號對每一類故事的貢獻。

## 方法如何運作

1. **收集並標示。** 收集經事實查核機構查核的謠言故事，並依判定結果標示為真或假。
2. **重建轉推串。** 對每則故事，追蹤轉推，建立傳遞該故事的人所構成的轉推串。
3. **依四項指標比較。** 比較真假轉推串的觸及、深度、廣度與速度。
4. **區分人類與機器人。** 量測自動化帳號的影響，並比較它們如何傳播真假故事。

此方法屬於觀察性研究。它記錄平台上實際發生的事，並未對使用者進行受控實驗。

## 結果

摘要指出，約 12.6 萬則故事，由約 300 萬人轉推了逾 450 萬次，結果顯示假新聞在所有資訊類別中都比真新聞傳播得更遠、更快、更深、更廣。政治類假新聞的效應最為明顯。機器人加速真假新聞傳播的速度相同，因此作者的結論是：假新聞傳播得更多，是因為人類比較可能分享它。

## 限制

- **單一平台與單一時期。** 結果來自 Twitter 與資料所涵蓋的年份，未必適用於其他平台或之後的時期。
- **觀察性資料。** 研究顯示人們分享了什麼，但無法說明他們為何分享，因此無法確立動機。
- **依賴事實查核。** 標籤來自事實查核的判定，因此研究的品質受限於那些判定與所涵蓋的故事。
- **類別範圍。** 摘要指出政治類新聞的效應最強，這使結果較難推廣到其他主題。

## 與其他主題的連結

- 同樣的傳播問題也適用於合成媒體，其內容可能是假的卻很逼真。偵測的一面見[FaceForensics++](facial-manipulation-detection.md)。
- 懷疑所造成的共同證據受損，見[不實資訊與深偽](index.md)概述中的說謊者紅利一節。
- 關於錯誤說法為何持續存在的心理學研究，見[心理學與 AI](../../brain-mind/psychology/index.md)。

## 開放問題

- 當平台改變排序與標示方式時，傳播差異有多少能維持？
- 同樣的模式是否適用於合成媒體，而後者的內容可能更具說服力？
- 如何讓更正的傳播範圍，能與最初的假消息一樣遠？

## 參考資料

### 開創性論文

- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://www.media.mit.edu/publications/the-spread-of-true-and-false-news-online/ — 本頁所述的研究，比較真假故事在 Twitter 上的傳播。
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — 深偽危害的法律分析，包括說謊者紅利，而此紅利取決於懷疑在假貨變普遍時的擴散。
- Rössler, A. et al. (2019). FaceForensics++: Learning to detect manipulated facial images. *ICCV*. https://arxiv.org/abs/1901.08971 — 人臉操縱的偵測基準，另有獨立頁面說明。

### 文章與官方文件

- C2PA. *Content Credentials: C2PA Technical Specification*, version 2.0. https://c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html — 有簽章的來源標準，是事後偵測假貨的替代做法。
- EUR-Lex. *Regulation (EU) 2022/2065 (Digital Services Act)*. https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng — 《數位服務法》的官方條文。前言第 82 與第 84 點提及對公民討論的負面影響，以及不實資訊的散布。
