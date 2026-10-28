---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Facial manipulation detection
  - 人臉操縱偵測
---

# 人臉操縱偵測（FaceForensics++）

!!! info "屬於不實資訊與深偽"
    本方法頁隸屬於[不實資訊與深偽](index.md)。它詳細說明一項基準；上層頁面則將它與其他因應方式並列比較。

Rössler 等人（2019）建立了 FaceForensics++，這是一個用於偵測人臉影像與影片操縱的大型基準。它涵蓋四種操縱方法，並包含不同壓縮程度的變化，讓偵測器能在接近真實條件下接受測試。這個基準使研究者能在相同的資料上比較偵測器。

## 問題

換臉與臉部重演工具能產生逼真的假影片。偵測需要大規模、多樣且有標註的資料，但要大量收集操縱影片並不容易，而且在某一組假貨上訓練的偵測器，常在其他假貨上失效。問題在於：如何建立一個能讓偵測器比較更公平的基準。

## 核心想法

以同一批來源影片，用數種方法製作操縱影片，套用真實平台所用的壓縮程度，保留一個隱藏的測試集，讓結果無法針對它調校，然後在相同的切分上訓練並比較偵測器。

## 基準如何運作

1. **操縱。** 對同一批來源影片套用四種方法：DeepFakes、Face2Face、FaceSwap 與 NeuralTextures。
2. **改變條件。** 以數種壓縮程度與多種尺寸壓縮影片，避免偵測器只在乾淨的檔案上接受測試。
3. **隱藏測試集。** 保留一個不公開的測試切分，以限制對基準的過度擬合。
4. **訓練與比較。** 在有標註的資料上訓練偵測器，並在保留的切分上報告結果，包括自動化偵測器與人類觀察者。

## 結果

摘要指出資料庫包含逾 180 萬張被操縱的影像，並表示這比可比較的公開偽造資料集大了一個數量級以上。摘要指出，利用特定領域知識的偵測器達到很高的準確度，並明顯優於人類觀察者。摘要未提供數值化的偵測準確度，因此應從論文的表格中讀取數字。

## 限制

- **四種方法。** 基準涵蓋四種操縱方法。用它訓練的偵測器，可能無法套用到較新的生成器上，而新的生成器仍在持續出現。
- **軍備競賽。** 基準固定了某個時間點的條件。新的生成方法與新的壓縮流程，可能使偵測器過時。
- **人類比較。** 偵測器優於人類觀察者的結果，並不表示偵測器已可靠到能單獨採取行動，因為誤判會傷害真實的人。

## 與其他主題的連結

- 偵測只是因應假貨的一種方式。C2PA 等來源標準採取相反的做法，在創作時就記錄真實性。見[不實資訊與深偽](index.md)。
- 假內容的傳播，是偵測無法處理的問題，見[假新聞如何傳播](spread-of-false-news.md)。
- 合成的臉孔也帶來隱私問題，見[隱私與資料保護](../privacy/index.md)。

## 開放問題

- 應如何評估偵測器在訓練資料未涵蓋的生成器上的表現？
- 偵測能否跟上生成的速度，還是來源紀錄必須承擔主要責任？
- 偵測的錯誤，應如何與把真實影片誤標為假的傷害相權衡？

## 參考資料

### 開創性論文

- Rössler, A., Cozzolino, D., Verdoliva, L., Riess, C., Thies, J. & Nießner, M. (2019). FaceForensics++: Learning to detect manipulated facial images. *ICCV*. https://arxiv.org/abs/1901.08971 — 本頁所述的基準，含四種操縱方法與隱藏測試集。
- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://politics.media.mit.edu/papers/Vosoughi_Science.pdf — 顯示假內容主要透過人類分享而廣泛傳播，單靠偵測無法阻止。
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — 深偽危害的法律分析，包括超越偵測的必要性。

### 文章與官方文件

- C2PA. *Content Credentials specification*. https://c2pa.org/ — 有簽章的來源標準，是發布後偵測的替代做法。
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — AI 法的官方條文。本頁未摘要其對合成內容的透明度規則。
