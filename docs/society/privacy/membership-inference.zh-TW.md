---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Membership inference attack
  - 成員推論攻擊
  - Membership inference
---

# 成員推論

!!! info "屬於隱私與資料保護"
    本方法頁隸屬於[隱私與資料保護](index.md)。它詳細說明此攻擊；上層頁面則將它與其他風險並列比較。

成員推論攻擊要判斷某筆特定紀錄是否在模型的訓練集中。它只需要能夠查詢模型，是訓練好的模型洩露其資料中人物資訊最簡單的方式之一。Shokri 等人（2017）展示了對機器學習服務的這種攻擊，後續研究則說明了攻擊何時會成功。

## 問題

模型應該描述群體，而不應揭露某個特定的人的紀錄是否被用於訓練。成員身分本身就可能敏感：知道某人的病歷在某種疾病患者的訓練集中，就等於揭露了健康狀況。問題在於：攻擊者只能依靠模型的輸出，能多準確地分辨成員與非成員？

## 核心想法

訓練攻擊者去辨認模型對成員與非成員的反應差異。模型對訓練過的樣本，通常會給出更有把握或損失更低的輸出。攻擊分類器從攻擊者自行建立、用來模仿目標的模型中，學到這種模式。

## 攻擊如何運作

1. **建立影子模型。** 在攻擊者掌控的資料上訓練模型，設定與目標相近。
2. **收集輸出。** 記錄每個模型對已知為成員與非成員的樣本所給出的輸出。
3. **訓練攻擊模型。** 學習一個分類器，輸入為輸出向量，預測「成員」或「非成員」。
4. **套用到目標。** 查詢目標模型中的該筆紀錄，並套用攻擊模型。

Shokri 等人（2017）描述了這種黑箱設定。Yeom 等人（2018）顯示過擬合足以支持這種攻擊。Carlini 等人（2022）主張，常用的平均準確度評估可能掩蓋攻擊的真實威力，因此提議在極低的偽陽性率下評估。

## 結果

Shokri 等人（2017）的摘要指出，商業機器學習服務所提供的模型可能受到成員推論的攻擊，摘要未提供準確度數字。Carlini 等人（2022）的摘要指出，他們的攻擊 LiRA 在低偽陽性率（例如低於 0.1%）時，威力約為先前攻擊的十倍。因此，攻擊的強度很大程度取決於評分的方式。

## 限制

- **取決於設定。** 結果依模型、訓練方式與過擬合程度而定。經過良好正則化的模型，暴露程度可能低很多。
- **評估方式。** 平均準確度可能使攻擊看起來很弱，即使它能可靠地辨認出部分成員，而這才是隱私上真正重要的。
- **不只這一種洩露。** 成員身分只是一種洩露。屬性推論與萃取可能揭露更多，針對成員推論的防禦並不涵蓋它們。

## 與其他主題的連結

- 訓練時的主要防禦是差分隱私，見[差分隱私](differential-privacy.md)。
- 萃取訓練文字是比是非判斷更強的洩露，見[訓練資料萃取](training-data-extraction.md)。
- 同樣的風險也出現在訓練影像上，見[著作權與智慧財產權](../copyright/index.md)中的相關頁面。

## 開放問題

- 哪些訓練做法能在不大量損失準確度的情況下，最有效地降低成員風險？
- 模型的隱私評估是否應以低偽陽性率作為標準量測？
- 當某人的資料在訓練集中時，應如何向他們說明成員風險？

## 參考資料

### 開創性論文

- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *IEEE Symposium on Security and Privacy*. https://arxiv.org/abs/1610.05820 — 提出影子模型攻擊，並展示其對商業機器學習服務的效果。
- Yeom, S., Giacomelli, I., Fredrikson, M. & Jha, S. (2018). Privacy risk in machine learning: Analyzing the connection to overfitting. arXiv:1709.01604. https://arxiv.org/abs/1709.01604 — 顯示過擬合足以進行成員推論。
- Carlini, N. et al. (2022). Membership inference attacks from first principles. arXiv:2112.03570. https://arxiv.org/abs/2112.03570 — 主張在低偽陽性率下進行評估，並提出 LiRA 攻擊。
- Carlini, N. et al. (2022). Quantifying memorization across neural language models. arXiv:2202.07646. https://arxiv.org/abs/2202.07646 — 顯示記憶化隨模型大小、資料重複與提示脈絡而增加。
- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — 顯示被記住的訓練文字可以被萃取，這比成員身分本身是更強的洩露。
