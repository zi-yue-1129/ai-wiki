---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Training data extraction
  - 訓練資料萃取
  - 從語言模型萃取訓練資料
---

# 訓練資料萃取

!!! info "屬於隱私與資料保護"
    本方法頁隸屬於[隱私與資料保護](index.md)。它詳細說明此攻擊；上層頁面則將它與其他風險並列比較。

訓練資料萃取是一種攻擊，目的是還原語言模型在訓練時記住的文字。Carlini 等人（2021）顯示，大型語言模型在適當的取樣方式下，可以逐字輸出訓練序列。這比成員推論是更強的洩露，因為它揭露的是內容本身，而不只是某筆紀錄是否被使用。

## 問題

語言模型是在從網路收集的文字上訓練的，其中可能包含姓名、聯絡方式或私人訊息。問題在於：當外部使用者查詢模型時，這些文字能否被取出？實務上又能還原多少？

## 核心想法

從模型生成大量樣本，依照記憶的跡象排序，再把排名最高的候選與來源比對。被記住的文字，相對於參考模型通常具有異常高的似然度，並且可以透過在訓練資料或網路上搜尋來確認。

## 攻擊如何運作

1. **取樣。** 使用各種提示，或從空白提示開始，生成大量續寫。
2. **評分。** 依記憶的訊號為每個樣本排序，例如模型相對於參考模型的似然度。
3. **保留排名最高的候選。** 選出訊號最強的樣本。
4. **驗證。** 將每個候選與來源比對，確認它是被記住的文字，而不是流暢生成的內容。

論文詳細描述了評分與驗證的方式。這裡的步驟是摘要，重用前請閱讀原文。

## 結果

Carlini 等人（2021）的摘要指出，此攻擊從 GPT-2 的訓練資料中萃取出數百段逐字的文字序列。Carlini 等人（2022）發現，記憶化會隨模型大小、訓練資料中某個樣本的重複次數，以及提示所用的脈絡長度而增加。2022 年的摘要並未給出這些關係的具體數字。

## 限制

- **只針對一個模型家族。** 2021 年的研究以 GPT-2 為對象。2021 年的摘要也指出，較大的模型比小模型更容易受到攻擊，但結果不會自動套用到其他模型家族。
- **取樣成本。** 攻擊取決於攻擊者能負擔多少樣本，因此成功與否也是資源的問題。
- **驗證。** 要確認某段序列是被記住的文字，而不是常見的片語，需要可靠地與來源資料比對。
- **緩解措施會改變結果。** 去除重複與差分隱私訓練能降低萃取，但 2022 年的摘要警告，若沒有積極的緩解措施，記憶化可能隨規模增加。

## 與其他主題的連結

- 同樣的機制也適用於影像模型，訓練影像也可能被萃取，見[從擴散模型萃取訓練資料](../copyright/diffusion-extraction.md)。
- 較弱的成員身分洩露在[成員推論](membership-inference.md)頁面說明。
- 訓練時的保護是[差分隱私](differential-privacy.md)的主題。

## 開放問題

- 隨著訓練資料與模型變大，應如何可靠地量測記憶化？
- 哪些類型的個人資料風險最高，應如何過濾？
- 安全調校與遺忘學習，是移除了可萃取的文字，還是只是隱藏了它？

## 參考資料

### 開創性論文

- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — 本頁所述的研究，從 GPT-2 萃取出逐字的訓練序列。
- Carlini, N., Liu, C., Erlingsson, Ú., Kos, J. & Song, D. (2019). The secret sharer: Evaluating and testing unintended memorization in neural networks. arXiv:1802.08232. https://arxiv.org/abs/1802.08232 — 量化無意記憶風險的測試方法，針對罕見的訓練資料。
- Carlini, N. et al. (2022). Quantifying memorization across neural language models. arXiv:2202.07646. https://arxiv.org/abs/2202.07646 — 顯示記憶化隨模型大小、重複與提示脈絡而增加。
- Carlini, N. et al. (2023). Extracting training data from diffusion models. arXiv:2301.13188. https://arxiv.org/abs/2301.13188 — 同類的萃取，應用於影像模型。
- Yeom, S., Giacomelli, I., Fredrikson, M. & Jha, S. (2018). Privacy risk in machine learning: Analyzing the connection to overfitting. arXiv:1709.01604. https://arxiv.org/abs/1709.01604 — 把驅動記憶化的過擬合與隱私風險連結起來。
