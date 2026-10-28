---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/governance
  - applications/creative
  - applications/cybersecurity
  - applications/social-science
tags:
  - misinformation
  - deepfakes
aliases:
  - Misinformation
  - 假訊息
  - 深偽
  - Deepfake
  - Disinformation
---

# 不實資訊與深偽

生成式 AI 讓製作有說服力的文字、影像、音訊與影片變得很便宜。這降低了假內容的製作成本，也改變了人們判斷真假的方式。本頁說明不實資訊如何傳播、AI 如何改變這個過程，以及可以採取哪些因應措施。

## 概述

不實資訊（misinformation）是在沒有欺騙意圖的情況下分享的錯誤或誤導性資訊。錯假資訊（disinformation）則是刻意分享的假資訊。**深偽（deepfake）**是合成的媒體，通常是影片或音訊，顯示真實的人做了或說了他們並未做過或說過的事。在生成式 AI 出現之前，製作以假亂真的媒體需要技術與時間。如今，一個人使用消費級工具，就能產生看起來像新聞照片、新聞影片，或家人語音訊息的內容。

最重要的效應有兩個。第一，假內容製作與散布的規模變得容易。第二，逼真的假貨存在本身，就讓人能把真實的證據說成是假的。第二種效應有時被稱為**說謊者紅利（liar's dividend）**。

## 關鍵概念

- **合成媒體（synthetic media）**：由模型生成或大幅修改的文字、影像、音訊或影片。
- **來源紀錄（provenance）**：附在檔案上的紀錄，說明內容從何而來，以及經過哪些編輯。
- **浮水印（watermarking）**：嵌入生成內容中的訊號，用來標示來源。它可能被移除或減弱。
- **偵測（detection）**：把內容分類為被操縱或由模型生成。偵測器與生成器之間存在軍備競賽。
- **說謊者紅利（liar's dividend）**：當事人藉由宣稱真實證據是假的，來否認該證據的能力。

## 運作方式

有三個過程決定了危害的樣貌。

1. **傳播。** 內容透過社群網路擴散，而且通常比更正還快。帶有強烈情緒、又新奇的說法傳播得最遠。大部分的傳播是由真人推動，而非自動化帳號（見[關鍵方法](#關鍵方法)）。
2. **製作。** 生成模型降低了製作假貨所需的技能。文字可以大量生成、針對讀者個人化，並從許多帳號發布。語音複製與換臉工具被用於詐騙與冒充（見[資安](../../applications/cybersecurity/index.md)）。
3. **懷疑。** 當假貨普遍時，人們對所見的事物就越不信任。即使內容是真的，共同的證據基礎也會遭到侵蝕。

偵測只是防線之一。偵測器會尋找生成器留下的痕跡，例如光線不一致、眨眼異常或壓縮痕跡，但遇到未曾用於訓練的生成器時，效果往往會下降。來源紀錄系統則採取相反的做法：在拍攝或建立內容時就記錄其真實性，而不是事後去猜測。

## 關鍵方法

每個方法都有自己的頁面，說明問題、方法、結果與限制。下表做簡要比較。

| 方法 | 所問的問題 | 主要結果（依摘要） | 延伸閱讀 |
|---|---|---|---|
| 真假新聞的傳播（Vosoughi 等人，2018） | 真假故事的傳播方式是否不同？自動化帳號能否解釋差異？ | 假新聞傳播得更遠、更快、更深、更廣；差異主要來自人類而非機器人 | [假新聞如何傳播](spread-of-false-news.zh-TW.md) |
| 人臉操縱偵測（Rössler 等人，2019） | 能否大規模且可靠地偵測被操縱的人臉？ | 逾 180 萬張被操縱影像的基準；摘要未提供數值化準確度 | [FaceForensics++](facial-manipulation-detection.zh-TW.md) |

## 因應措施

| 做法 | 作用 | 限制 |
|---|---|---|
| 來源紀錄（例如 [C2PA Content Credentials](https://c2pa.org/)） | 在有簽章的中繼資料中記錄拍攝與編輯歷程 | 必須整條鏈都採用才有效；中繼資料可能被移除 |
| 生成輸出加上浮水印 | 在生成時標記模型輸出 | 可能被移除或減弱；必須能跨平台保持穩健 |
| 偵測 | 在發布後標記可能的假貨 | 遇到新的生成器會失效；誤判會傷害真實的人 |
| 平台規則與標示 | 降低排序、加上標示或移除內容 | 與言論自由之間有取捨；難以大規模一致地執行 |
| 媒體素養 | 幫助人們檢查來源、辨識操縱 | 見效慢；效果難以衡量 |

法規也在同步推進。歐盟 AI 法對 AI 生成內容設有透明度義務；《數位服務法》（Digital Services Act）則要求超大型線上平台評估並降低系統性風險，包括不實資訊。其他司法管轄區的做法，請見[法律、政策與治理](../governance/index.md)。

## 與其他主題的連結

- 關於重複、情緒與信任的心理學研究，解釋了為何錯誤說法會持續存在（見[心理學與 AI](../../brain-mind/psychology/index.md)）。
- 不實資訊與[倫理與公平](../ethics/index.md)有所重疊，後者將其視為對共同資訊環境的傷害。
- 合成媒體在創作與政治上的用途，分別見於[創作與 AI](../../applications/creative/index.md)與[社會科學](../../applications/social-science/index.md)。

## 應用

- **事實查核支援**：模型協助找出值得查核的主張，並檢索先前的查核結果，最終仍由人來判斷。
- **相機、編輯軟體與新聞出版中的來源紀錄工具**。
- **防詐騙**：銀行與客服中心以語音與影像驗證防範冒充。

## 開放問題

- 偵測能否跟上生成的速度，還是來源紀錄必須承擔主要責任？
- 與人類製作的內容相比，AI 生成的不實資訊在現實世界中的影響有多大？
- 平台應如何在標示、移除與言論自由之間取得平衡？
- 如何因應說謊者紅利，又不致讓虛假的否認獲得掩護？

## 參考資料

### 開創性論文

- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://politics.media.mit.edu/papers/Vosoughi_Science.pdf — 比較 Twitter 上真假故事的傳播，發現假新聞傳播得更遠、更快，且主要是由人類分享造成。
- Rössler, A. et al. (2019). FaceForensics++: Learning to detect manipulated facial images. *ICCV*. https://arxiv.org/abs/1901.08971 — 含壓縮變化與隱藏測試集的人臉操縱基準，用於訓練與評估偵測器。
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — 深偽危害的法律分析，包括說謊者紅利。

### 文章與官方文件

- C2PA. *Content Credentials specification*. https://c2pa.org/ — 有簽章來源中繼資料的開放標準，由科技與媒體公司組成的指導委員會支持。
- EUR-Lex. *Regulation (EU) 2022/2065 (Digital Services Act)*. https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng — 《數位服務法》的官方條文，為超大型線上平台設定系統性風險的義務。
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — 歐盟 AI 法的官方條文，包括 AI 生成內容的透明度規則。
