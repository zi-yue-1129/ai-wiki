---
translation_reviewed: 2026-10-28
---

# Gender Shades（Buolamwini & Gebru, 2018）

Gender Shades 是對三款商業性別分類器的分組稽核。它顯示，平均準確度很高的系統，仍可能在不同膚色與性別之間隱藏很大的錯誤率差距。本頁是[監控、人臉辨識與人權](../index.md)的方法頁。

## 概述

商業的臉部分析服務多半以整體準確度行銷。Buolamwini 與 Gebru 問的是：這個平均值對每個人都成立嗎？他們的答案是一個依性別與膚色平衡的基準資料集，以及一項稽核，它針對每個交叉子群體（例如深膚色女性）報告錯誤率，而不只是男女或淺深膚色各自的數字。稽核本身就是方法：讓外部人員在無法檢視內部運作的情況下，衡量一個系統。

## 關鍵概念

- **Fitzpatrick 膚色分類**：源自皮膚科的六級量表，描述皮膚對日曬的反應。論文把第 IV 至 VI 級歸為深膚色，第 I 至 III 級歸為淺膚色。
- **交叉子群體**：由兩個屬性同時定義的群體。論文使用四個：深膚色女性、深膚色男性、淺膚色女性與淺膚色男性。
- **錯誤率**：某子群體中被分類錯誤的影像比例，等於一減去真陽性率。
- **黑箱稽核**：只透過公開介面測試系統，無法取得其內部資料。

## 運作方式

1. **建立平衡的基準資料。**作者組成 Pilot Parliaments Benchmark（PPB），收錄來自非洲與歐洲國家的 1,270 位國會議員影像。其膚色分布比既有基準 IJB-A 與 Adience 均衡得多；後兩者的淺膚色受試者分別占 79.6% 與 86.2%，依摘要所述。
2. **為每張影像標上**性別與 Fitzpatrick 膚色。
3. **把每張影像送入**三款商業性別分類器，分別是 Microsoft、IBM 與 Face++，透過其公開介面進行。
4. **計算每個子群體的錯誤率**：

$$
\text{Error}_g = 1 - \frac{TP_g}{TP_g + FN_g}
$$

其中 $g$ 為子群體，$TP_g$ 為正確預測的正例數，$FN_g$ 為漏掉的正例數。

5. **比較每個分類器中表現最好與最差的子群體**，並將整體數字與分組數字對照。

## 結果

以下數字取自論文的表 4，基準為 PPB。

| 分類器 | 整體錯誤率 | 深膚色女性 | 淺膚色男性 |
|---|---|---|---|
| Microsoft | 6.3% | 20.8% | 0.0% |
| Face++ | 10.0% | 34.5% | 0.8% |
| IBM | 12.1% | 34.7% | 0.3% |

摘要指出，深膚色女性的錯誤率最高，最高達 34.7%；淺膚色男性的最高錯誤率則為 0.8%。三款系統在男性臉孔上的表現都優於女性臉孔，錯誤率差距為 8.1 至 20.6 個百分點；在淺膚色臉孔上的表現也都優於深膚色臉孔，差距為 11.8 至 19.2 個百分點。南非子集也呈現相同的模式。

## 限制

- **樣本小且為擺拍影像。**PPB 只有 1,270 人。國會議員肖像的姿勢相對固定，與大多數監控影像不同。
- **性別只採二元分類。**作者指出，其標籤無法涵蓋性別或跨性別身分的複雜性，因此這項稽核衡量的是一項狹窄且二元的任務。
- **只是一個時間點的快照。**稽核描述的是評估時的系統狀態。廠商之後可能已改版，論文無法說明目前的準確度。
- **分類不等於辨識。**性別分類不同於人臉辨識，後者要把臉孔與資料庫比對。論文並未直接測試辨識。

## 與其他主題的連結

- Raji 與 Buolamwini（2019）延續這項稽核，探討公開點名有偏誤結果的做法，會對相關公司造成什麼影響。
- 基準資料的問題也適用於其他人臉資料集。訓練資料的組成會影響結果，見 [ArcFace](../arcface/index.md)的討論。
- 分組評估所依賴的公平性定義，以及它們之間的張力，見[公平性定義](../../ethics/fairness-definitions.md)。

## 開放問題

- 對某一家廠商系統的稽核結果，能否推廣到其他系統，以及同一系統的後續版本？
- 當受影響的人無法像基準資料那樣被抽樣時，如何進行分組稽核？
- Kostka et al.（2021）發現大眾對人臉辨識的接受度因國家而異。稽核結果是否應改變接受度？這對規範方式有何影響？

## 參考資料

### 開創性論文

- Buolamwini, J. & Gebru, T.（2018）. Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAT\**. https://proceedings.mlr.press/v81/buolamwini18a.html — 本頁所述的稽核，包含 Pilot Parliaments Benchmark 與各子群體的錯誤率。

### 綜述與教科書

- Cao, Q. et al.（2017）. VGGFace2: A dataset for recognising faces across pose and age. arXiv. https://arxiv.org/abs/1710.08092 — 大規模網路蒐集的人臉資料集，在姿勢、年齡與族裔上有豐富變化。

### 文章與官方文件

- Raji, I. D. & Buolamwini, J.（2019）. Actionable Auditing. *AAAI/ACM Conference on AI, Ethics, and Society*. https://doi.org/10.1145/3306618.3314244 — 延續稽核研究，探討公開報告稽核結果如何影響商業 AI 產品。
- Phillips, P. J. et al.（2011）. An other-race effect for face recognition algorithms. *ACM Transactions on Applied Perception*. https://doi.org/10.1145/1870076.1870082 — 人臉辨識演算法與人類觀察者一樣，對資料庫中多數族群的臉孔表現較好。
- Kostka, G., Steinacker, L. & Meckel, M.（2021）. Between security and convenience: Facial recognition technology in the eyes of citizens in China, Germany, the United Kingdom, and the United States. *Public Understanding of Science*. https://doi.org/10.1177/09636625211001555 — 在四個國家進行的線上調查，比較大眾對人臉辨識的接受度，結果因國家而異。
