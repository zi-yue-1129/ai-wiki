---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Facial manipulation detection
  - 人臉操縱偵測
---

# 人臉操縱偵測（FaceForensics++）

!!! info "屬於不實資訊與深偽"
    本方法頁隸屬於[不實資訊與深偽](index.md)。它詳細說明一項基準；上層頁面則將它與其他因應方式並列比較。

Rössler 等人（2019）建立了 FaceForensics++，這是一個公開的人臉影像與影片操縱偵測基準。它涵蓋四種操縱方法，並包含不同壓縮程度的變化，讓偵測器能在接近真實條件下接受測試。測試資料的標籤保留在伺服器上，使各方能在相同的資料上公平比較。

## 概述

換臉與臉部重演工具能產生逼真的假影片。偵測研究需要大規模、多樣且有標註的資料，而且只有在共享資料上比較，結果才有意義。FaceForensics++ 同時提供兩者，並成為偵測器的常用比較標準。

## 關鍵概念

- **人臉操縱**：替換或移動影像或影片中某人臉孔的編輯，例如換臉或重演。
- **壓縮痕跡**：影片壓縮造成的失真，可能掩蓋偵測器所依賴的痕跡。
- **隱藏測試集**：標籤不公開的測試切分，使方法無法直接針對它調校。

## 問題

偵測需要大規模、多樣且有標註的資料，但要大量收集操縱影片並不容易，而且在某一組假貨上訓練的偵測器，常在其他假貨上失效。問題在於：如何建立一個能讓偵測器比較更公平的基準。

## 基準如何運作

1. **操縱。** 對同一批來源影片套用四種方法：DeepFakes、Face2Face、FaceSwap 與 NeuralTextures。
2. **改變條件。** 以隨機的壓縮程度與尺寸製作操縱影片，避免偵測器只在乾淨的檔案上接受測試。
3. **隱藏測試集。** 基準測試資料的標籤保留在伺服器上，結果需經提交而非在本地調校。
4. **訓練與比較。** 在有標註的資料上訓練偵測器，並在保留的切分上報告結果。論文將自動化偵測器與人類觀察者相比。

論文亦限制提交頻率，每位提交者每兩週只能提交一次，以減少對測試集的過度擬合。

## 核心方法

FaceForensics++ 是一個基準，而非單一偵測器，因此它的核心方法是其中包含的四種操縱技術。每種技術產生的假貨，製作方式各不相同。

- **DeepFakes、FaceSwap**：換臉方法，以另一個身分替換原本的身分。
- **Face2Face**：臉部重演，把一個人的表情轉移到另一個人身上。
- **NeuralTextures**：學習神經紋理來呈現被操縱臉孔的方法。

## 結果

摘要指出資料庫包含逾 180 萬張被操縱的影像，並表示這比可比較的公開偽造資料集大了一個數量級以上。摘要指出，利用特定領域知識的偵測器達到前所未有的準確度，並明顯優於人類觀察者。摘要並未在其中提供單一的數值化偵測準確度，因此應從論文的表格中讀取數字。

## 限制

- **四種方法。** 基準涵蓋四種操縱方法。用它訓練的偵測器，可能無法套用到較新的生成器上，而新的生成器仍在持續出現。
- **軍備競賽。** 基準固定了某個時間點的條件。新的生成方法與新的壓縮流程，可能使偵測器過時。
- **人類比較。** 偵測器優於人類觀察者的結果，並不表示偵測器已可靠到能單獨採取行動，因為誤判會傷害真實的人。

## 變體與更多變體

- **基準訓練的偵測器**：論文中的偵測器在此資料上訓練，並在其保留的切分上比較。
- **來源紀錄**：一種在創作時就記錄真實性的不同做法，例如 C2PA，見下方連結。

## 與其他主題的連結

- 偵測只是因應假貨的一種方式。C2PA 等來源標準採取相反的做法，在創作時就記錄真實性。見[不實資訊與深偽](index.md)。
- 假內容的傳播，是偵測無法處理的問題，見[假新聞如何傳播](spread-of-false-news.md)。
- 合成的臉孔也帶來隱私問題，見[隱私與資料保護](../privacy/index.md)。

## 應用

- 平台上上傳影片的篩選，被標記的案例再由人工審查。
- 研究上的基準比較，同一切分讓偵測器可以直接比較。

## 開放問題

- 應如何評估偵測器在訓練資料未涵蓋的生成器上的表現？
- 偵測能否跟上生成的速度，還是來源紀錄必須承擔主要責任？
- 偵測的錯誤，應如何與把真實影片誤標為假的傷害相權衡？

## 參考資料

### 開創性論文

- Rössler, A., Cozzolino, D., Verdoliva, L., Riess, C., Thies, J. & Nießner, M.（2019）。FaceForensics++: Learning to Detect Manipulated Facial Images. arXiv. https://arxiv.org/abs/1901.08971 — 本頁所述的基準，含四種操縱方法、壓縮變化與保留的測試切分。
- Vosoughi, S., Roy, D. & Aral, S.（2018）。The spread of true and false news online. *Science*, 359, 1146–1151. https://doi.org/10.1126/science.aap9559 — 顯示假內容主要透過人類分享而廣泛傳播，單靠偵測無法阻止。
- Chesney, B. & Citron, D.（2019）。Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — 深偽危害的法律分析，包括超越偵測的必要性。

### 文章與官方文件

- C2PA. *Content Credentials: C2PA Technical Specification*. https://spec.c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html — 有簽章來源紀錄的技術規格，是發布後偵測的替代做法。
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — AI 法的官方條文。本頁未摘要其對合成內容的透明度規則。
