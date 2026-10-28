---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Data replication
  - 擴散模型資料重現
---

# 擴散模型中的資料重現

!!! info "屬於著作權與智慧財產權"
    本方法頁隸屬於[著作權與智慧財產權](index.md)。它詳細說明一項研究；上層頁面則將它與其他研究並列比較。

Somepalli 等人（2022）探討影像擴散模型是會複製訓練影像，還是能從中泛化。他們的答案是：某些模型在特定情況下會複製，而複製的程度取決於訓練上的選擇，例如訓練集的大小與資料重複的程度。這項研究對著作權很重要，因為直接複製受保護的影像，是產生侵權輸出最明顯的途徑。

## 問題

擴散模型在大量的影像與標題配對上訓練，學會依文字提示生成新影像。它的訓練資料常包含受著作權保護的美術作品與照片。問題在於：模型產生的新影像，是反映了一般的風格與內容，還是把特定的訓練影像複製得夠接近、以致構成複製？

## 核心想法

以與訓練標題相符的提示生成影像，然後在訓練集中搜尋與每張生成影像極為相似的影像。如果某張生成影像在訓練資料中有近乎相同的配對，就表示模型複製了該訓練影像。這個方法把「會不會複製」這個模糊的疑慮，轉化為可以量測的搜尋問題。

## 方法如何運作

1. **選擇提示。** 使用訓練資料中的標題，讓模型生成它學過的內容。
2. **生成。** 對每個提示從模型取樣影像。
3. **檢索。** 對每張生成影像，在特徵空間中以相似度度量找出最相似的訓練影像。
4. **檢視。** 檢查最接近的配對，區分真正的複製與僅是大致相似。
5. **改變設定。** 研究重現程度如何隨訓練集的大小與圖像重複次數而改變。

摘要並未交代第 3 至 5 步的全部細節。在重用此流程前，請先閱讀原文。

## 結果

摘要指出，包括 Stable Diffusion 在內的某些擴散模型，在特定情況下會「明顯地複製」訓練資料；重現程度也取決於訓練集大小與資料重複等因素。摘要沒有給出任何模型的整體重現率，因此不應把這項研究解讀為實際中複製發生頻率的量測。

## 限制

- **沒有整體比率。** 摘要沒有量化重現發生的頻率，因此無法說明在所有輸出中的問題規模。
- **範圍有限。** 摘要列出了所用的資料集（包括 Oxford flowers、CelebA、ImageNet 與 LAION 的子集）。結果未必能推廣到其他模型、資料集或提示方式。
- **比對是一種判斷。** 判定兩張影像是否為複製，取決於相似度門檻與人工檢視，這可能與法律上判斷複製的標準不一致。

## 與其他主題的連結

- 相對的研究是從已訓練模型中萃取訓練影像，見[從擴散模型萃取訓練資料](diffusion-extraction.md)。
- 訓練資料的記憶化是引發隱私問題的同一機制，見[隱私與資料保護](../privacy/index.md)。
- 重現也牽涉到訓練與輸出的法律問題，見[法律、政策與治理](../governance/index.md)。

## 開放問題

- 應如何量測重現率，才能讓不同模型之間的結果可以比較？
- 在法律上，重現某張訓練影像是否一律構成複製，還是要視個案事實而定？
- 去除訓練資料中的重複，能否在不降低模型品質的前提下減少重現？

## 參考資料

### 開創性論文

- Somepalli, G., Singla, V., Goldblum, M., Geiping, J. & Goldstein, T. (2022). Diffusion art or digital forgery? Investigating data replication in diffusion models. arXiv:2212.03860. https://arxiv.org/abs/2212.03860 — 本頁所述的研究，包含直接複製的例子，以及訓練集大小與資料重複的影響。
- Carlini, N. et al. (2023). Extracting training data from diffusion models. arXiv:2301.13188. https://arxiv.org/abs/2301.13188 — 相關研究，顯示可以從已訓練的擴散模型中萃取出訓練影像。
- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). High-resolution image synthesis with latent diffusion models. *CVPR*. https://arxiv.org/abs/2112.10752 — Stable Diffusion 所依據的潛在擴散方法，在壓縮的影像表示上進行擴散。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising diffusion probabilistic models. arXiv:2006.11239. https://arxiv.org/abs/2006.11239 — 多數影像擴散模型所依據的去噪擴散公式。
- Schuhmann, C. et al. (2022). LAION-5B: An open large-scale dataset for training next generation image-text models. arXiv:2210.08402. https://arxiv.org/abs/2210.08402 — 公開的資料集，含 58.5 億組影像與文字配對，是訓練影像模型的來源之一。

### 文章與官方文件

- EUR-Lex. *Directive (EU) 2019/790 on copyright and related rights in the Digital Single Market*. https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng — 第 3 條與第 4 條規定文字與資料探勘的例外，以及權利保留，這決定了何種訓練複製是被允許的。
