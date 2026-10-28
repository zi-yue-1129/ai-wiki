---
translation_reviewed: 2026-10-28
---

# ArcFace（Deng et al., 2019）

ArcFace 是深度人臉辨識的訓練損失函數。它在 softmax 損失上加入一個加性角度間隔，使每張臉的嵌入向量在單位超球面上被拉近自己的身分、遠離其他身分。它是現代人臉比對中嵌入模型所用的訓練損失之一，而人臉比對正是[監控、人臉辨識與人權](../index.md)所討論的主題。

## 概述

人臉辨識系統把每張臉轉換成一個嵌入向量，並透過比較向量來判斷身分。良好的辨識需要同一個人的臉彼此靠近，不同人的臉彼此遠離。以標準 softmax 損失訓練的模型，對身分的區分較弱，因此過去的研究陸續加入各種間隔。

Deng et al.（2019）提出加性角度間隔損失，稱為 ArcFace。間隔有幾何上的意義：在正規化後的超球面上，它等於一張臉與其類別中心之間的測地距離。

## 關鍵概念

- **嵌入（embedding）**：網路為一張臉產生的向量。論文的實驗使用 512 個數字。
- **超球面**：高維度中單位球的表面。在這裡，分類變成比較角度的問題。
- **特徵尺度 $s$**：套用在所有餘弦對數上的固定乘數。論文使用 $s = 64$。
- **角度間隔 $m$**：訓練時加在真實類別角度上的角度，使正確的類別必須以明確的角度差勝出。論文中表現最好的值是 $m = 0.5$。

## 運作方式

Softmax 以嵌入與各類別權重的內積計算每個類別 $j$ 的對數。當向量都正規化後，對數化簡為 $s\cos\theta_j$，其中 $\theta_j$ 是嵌入與類別 $j$ 權重之間的角度。ArcFace 把間隔加在真實類別 $y_i$ 的角度上：

$$
L = -\frac{1}{N}\sum_{i=1}^{N}\log\frac{e^{s\cos(\theta_{y_i}+m)}}{e^{s\cos(\theta_{y_i}+m)}+\sum_{j\neq y_i}e^{s\cos\theta_j}}
$$

每個批次的訓練程序如下。

1. 把每個人臉嵌入 $x_i$ 與每個類別權重 $W_j$ 正規化為單位長度。
2. 對每個類別 $j$，以正規化向量的內積計算 $\cos\theta_j$。
3. 對真實類別 $y_i$，把 $\theta_{y_i}$ 換成 $\theta_{y_i}+m$。
4. 把所有餘弦乘以 $s$，套用交叉熵後進行反向傳播。

論文也提出一個子中心（sub-centre）變體：每個類別有多個中心，一張臉只需接近其中之一。它的目的是容忍網路蒐集的人臉資料集中常見的標籤雜訊。

## 結果

論文表 2 的消融實驗以 CASIA 資料集訓練，網路為 ResNet-50。下表是驗證準確度（百分比），數字取自論文的 arXiv 版本。

| 損失函數 | LFW | CFP-FP | AgeDB |
|---|---|---|---|
| Softmax | 99.08 | 94.39 | 92.33 |
| 正規化 softmax（s = 64） | 98.56 | 89.79 | 88.72 |
| CosFace（間隔 0.35） | 99.51 | 95.44 | 94.56 |
| ArcFace（間隔 0.5） | 99.53 | 95.56 | 95.15 |

間隔 0.5 的 ArcFace 位於或接近最高，而它相對於 softmax 的優勢在較困難的 CFP-FP 與 AgeDB 上最大。arXiv 版本與會議版本可能不同，引用前請核對。

## 限制

- **基準分數不等於實際部署的分數。**LFW、CFP-FP 與 AgeDB 都是經過整理的測試集。與大量陌生人的臉進行比對，也就是辨識系統的情境，難度高得多，需另外測試。
- **損失函數無法修正有偏誤的資料。**間隔改變的是類別如何區分，並不會補上缺漏的臉孔。[Gender Shades](../gender-shades/index.md) 所描述的差距，在改進損失函數後仍可能存在。Buolamwini 與 Gebru（2018）引用的估計指出，LFW 基準約為 77.5% 男性與 83.5% 白人。
- **標籤雜訊。**網路蒐集的資料集含有標錯的人臉。子中心變體有幫助，但清理效果取決於資料集本身。
- **嵌入的隱私風險。**論文也顯示，預訓練模型可被反向推導，產生保留當事人身分的臉部影像。對任何儲存嵌入的系統而言，這都是風險。

## 與其他主題的連結

- 訓練資料與損失函數同樣重要（Cao et al., 2017，見下方參考資料）。
- 以間隔為基礎的度量學習，屬於[其他學習範式](../../../theory/paradigms/other/index.md)中更廣的嵌入方法。網路架構見[電腦視覺](../../../theory/models/computer-vision/index.md)。
- 機器的臉部辨識是否也帶有人類的偏誤（例如其他種族效應），見[主題頁](../index.md)的討論。

## 開放問題

- 驗證基準上的進步，能否延續到與數百萬張臉比對的辨識情境？
- 能否設計一種損失函數，直接降低人口統計差異，還是必須從資料與評估著手？
- 既然模型可被反向推導以還原臉部影像，嵌入應如何保護？

## 參考資料

### 開創性論文

- Deng, J. et al.（2019）. ArcFace: Additive Angular Margin Loss for Deep Face Recognition. *CVPR*. https://doi.org/10.1109/CVPR.2019.00482 — 提出加性角度間隔損失，以及用於處理網路人臉雜訊的子中心變體。

### 文章與官方文件

- Buolamwini, J. & Gebru, T.（2018）. Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAT\**. https://proceedings.mlr.press/v81/buolamwini18a.html — 稽核顯示，商業性別分類器的錯誤率因膚色與性別而有明顯差異。
- Cao, Q. et al.（2017）. VGGFace2: A dataset for recognising faces across pose and age. arXiv. https://arxiv.org/abs/1710.08092 — 大規模網路蒐集的人臉資料集，會塑造辨識模型學到的內容。
- Phillips, P. J. et al.（2011）. An other-race effect for face recognition algorithms. *ACM Transactions on Applied Perception*. https://doi.org/10.1145/1870076.1870082 — 演算法與人類觀察者一樣，對資料庫中多數族群的臉孔表現較好。
- Raji, I. D. & Buolamwini, J.（2019）. Actionable Auditing. *AAAI/ACM Conference on AI, Ethics, and Society*. https://doi.org/10.1145/3306618.3314244 — 延續對商業人臉分析產品的稽核研究。
