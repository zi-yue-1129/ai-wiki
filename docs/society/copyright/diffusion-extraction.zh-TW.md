---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Training data extraction
  - 從擴散模型萃取訓練資料
---

# 從擴散模型萃取訓練資料

!!! info "屬於著作權與智慧財產權"
    本方法頁隸屬於[著作權與智慧財產權](index.md)。它詳細說明一項研究；上層頁面則將它與其他研究並列比較。

Carlini 等人（2023）顯示，可以從已訓練的擴散模型中萃取出訓練影像。他們的流程從最先進的模型中產生了逾一千個訓練樣本。論文以此說明影像模型的記憶化是在規模上發生的，並牽涉到著作權與隱私。

## 問題

擴散模型在大量影像上訓練，其中可能包含私人照片與受著作權保護的作品。如果模型儲存了足夠多的訓練資料，外部使用者或許能透過查詢模型把這些資料還原出來。問題在於：這在實務上是否做得到，而且規模是否足以產生影響。

## 核心想法

採用先生成、再過濾的流程。大量從模型生成影像，然後只保留看起來像訓練影像副本的輸出。過濾在生成之後進行，因此成本取決於生成了多少影像，以及有多少候選需要與訓練資料比對。

## 方法如何運作

1. **生成。** 從模型取樣大量影像。
2. **過濾。** 依每張生成影像與已知訓練資料的相似程度評分，保留分數最高的候選。
3. **驗證。** 將每個候選與訓練資料比對，確認它是副本，而非僅是大致相似。

摘要把做法描述為先生成、再過濾。具體的評分與驗證步驟見原文，重用前請先閱讀。

## 結果

摘要指出，此流程從最先進的模型中萃取出「逾一千個訓練樣本」。摘要沒有分別列出各模型的數字，也沒有說明審查了多少張生成影像。因此，這個數字顯示萃取在規模上確實發生，但無法得出可以在不同模型或設定之間比較的比率。摘要還指出，作者在各種設定下訓練了數百個擴散模型，以檢驗建模與資料選擇如何影響隱私，並指出擴散模型的隱私保護程度遠低於先前的生成模型，例如 GAN。

## 限制

- **沒有各模型的細分。** 摘要只給出跨模型的總數，因此僅憑摘要無法把結果歸因於特定系統。
- **分母未知。** 若不知道審查了多少張生成影像，萃取率就無從得知。
- **過濾的選擇。** 結果取決於過濾條件。不同的門檻或驗證規則，會改變什麼算是萃取成功。

## 與其他主題的連結

- 關於視覺相似度複製的相關研究，見[擴散模型中的資料重現](data-replication.md)。
- 文字模型中也有相同的記憶化機制，文字模型研究與作為防禦的差分隱私，見[隱私與資料保護](../privacy/index.md)。
- 萃取受著作權保護的作品，是[著作權與智慧財產權](index.md)與[法律、政策與治理](../governance/index.md)中的問題之一。

## 開放問題

- 需要審查多少張生成影像，才能估計出可在不同模型之間比較的萃取率？
- 哪些訓練影像風險最高？重複是否能解釋大部分的風險？
- 去重複或差分隱私等防禦，是消除萃取，還是只是降低萃取？

## 參考資料

### 開創性論文

- Carlini, N. et al. (2023). Extracting training data from diffusion models. arXiv:2301.13188. https://arxiv.org/abs/2301.13188 — 本頁所述的研究，以先生成、再過濾的流程萃取出逾一千個訓練樣本。
- Somepalli, G., Singla, V., Goldblum, M., Geiping, J. & Goldstein, T. (2022). Diffusion art or digital forgery? Investigating data replication in diffusion models. arXiv:2212.03860. https://arxiv.org/abs/2212.03860 — 關於擴散模型資料重現的相關研究，並說明了其結論的限制。
- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — 文字模型的對應研究，顯示被記住的訓練序列可以被逐字萃取。
- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). High-resolution image synthesis with latent diffusion models. *CVPR*. https://arxiv.org/abs/2112.10752 — Stable Diffusion 所依據的潛在擴散方法，本頁所述的研究對象之一。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising diffusion probabilistic models. arXiv:2006.11239. https://arxiv.org/abs/2006.11239 — 本頁所述模型所依據的去噪擴散公式。

### 文章與官方文件

- EUR-Lex. *Directive (EU) 2019/790 on copyright and related rights in the Digital Single Market*. https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng — 第 3 條與第 4 條規定文字與資料探勘的例外，以及權利保留，這決定了何種訓練複製是被允許的。
