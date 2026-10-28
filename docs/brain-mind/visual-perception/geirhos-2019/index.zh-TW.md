---
translation_reviewed: 2026-10-28
---

# CNN 中的形狀偏好（Geirhos 等人，2019）

Geirhos 等人（2019）提出一個簡單的問題，並給出明確的答案：在 ImageNet 上訓練的卷積網路，是像人一樣以形狀辨識物體，還是以紋理辨識？研究發現，標準網路主要依賴紋理；而同一架構若改在 ImageNet 的風格化版本上訓練，就會轉向依賴形狀。這篇論文對 NeuroAI 很重要，因為它提供了網路與人類之間一個具體的行為差異，也提供了一種測試方法，來檢驗訓練方式的改變能否縮小這個差異。

本頁屬於[知覺與視覺系統](../index.md)。上層頁面提供總覽，本頁則說明方法與證據。

## 問題

人主要以形狀辨識物體，即使紋理會誤導判斷，也是如此。網路可以在 ImageNet 上達到很高的準確率，卻不學習同樣的線索，因為在自然照片中，紋理往往是可靠的捷徑。如果是這樣，網路可能是因為錯誤的理由而答對，這會限制它作為人類視覺模型的可信度。

## 方法

作者製作了紋理與形狀互相衝突的影像。每張影像保留某一類物體的形狀，卻帶有另一類物體的紋理，這是透過風格轉移產生的，因此形狀與紋理指向不同的標籤。分類器的選擇，便顯示它用了哪一種線索。作者把風格化的訓練集稱為 Stylized-ImageNet（SIN）。

步驟如下：

1. 以 ImageNet 影像之間的風格轉移，製作線索衝突的影像。
2. 在這些衝突影像上測試標準的 ImageNet 訓練網路與人類受試者。
3. 以標準影像與風格化影像的混合，或只以風格化影像，訓練同一個架構（ResNet-50）。
4. 測量 ImageNet 的準確率、在 PASCAL VOC 與 MS COCO 上的物體偵測，以及對影像失真的穩健性。

第 3 步是介入。保持架構不變，就能分離出訓練資料的效果。

## 結果

研究進行了九項心理物理實驗，共 97 位受試者，合計 48,560 次試驗。主要結果如下。

- **人類**在其正確判斷中，有 95.9% 選擇形狀類別。
- **標準的 ImageNet 訓練 CNN** 多數時候選擇紋理類別。形狀判斷的比例分別為 VGG-16 17.2%、GoogLeNet 31.2%、AlexNet 42.9%、ResNet-50 22.1%。
- **以 SIN 訓練同一個 ResNet-50**，會使它轉向形狀。在線索衝突影像上，其形狀偏好從 22% 升至 81%，相較之下人類為 95.9%。

同一架構的分類與偵測結果，取自論文的表 2：

| 訓練資料 | ImageNet top-1（%） | PASCAL VOC mAP50（%） | MS COCO mAP50（%） |
|---|---|---|---|
| 僅 ImageNet | 76.13 | 70.7 | 52.3 |
| 僅 SIN | 60.18 | 70.6 | 51.9 |
| SIN + ImageNet | 74.59 | 74.0 | 53.8 |
| SIN + ImageNet，再以 ImageNet 微調（"Shape-ResNet"） | 76.72 | 75.1 | 55.2 |

形狀偏好的模型在分類上與標準模型相當或更好，在物體偵測上也更好。論文還報告，形狀偏好的網路對影像失真有更高的穩健性。

## 限制

- **只有一種介入。**風格化訓練只改變了一種捷徑。它並不能完整說明人類視覺，也不能解決人在所有任務中如何權衡形狀與紋理的問題。
- **只用 SIN 訓練的準確率代價。**僅以 SIN 訓練的網路，ImageNet top-1 只有 60.18%，低於標準模型，因此形狀偏好的表徵並非對所有用途都自動更好。
- **行為，而非機制。**證據是關於哪種線索決定標籤，並未顯示網路的內部運算與人類視覺處理相符。

## 關聯

- **模型比較：**[Yamins 等人（2014）](../yamins-2014/index.md)顯示，CNN 特徵能預測高階視覺皮層的反應。本研究則問：這些網路在分類時依賴哪一種線索。
- **CNN 架構：**這個架構家族見 [CNN](../../../theory/models/cnn/index.md)。
- **知覺：**塑造人類辨識的腹側與背側路徑，見[知覺與視覺系統](../index.md)。

## 未解問題

- **形狀偏好是否會讓網路更像大腦？**在這項測試上，它使網路更接近人類行為，但是否也符合內部的計算，尚未得到證明。
- **哪些訓練訊號會產生形狀偏好？**論文改變的是資料。目標函數、架構或類似發展過程的訓練，是否也會產生相同的偏好，仍是未解的問題。

## 參考文獻

### 開創性論文

- Geirhos, R., Rubisch, P., Michaelis, C., Bethge, M., Wichmann, F. A. & Brendel, W. (2019). ImageNet-trained CNNs are biased towards texture. *ICLR*。https://arxiv.org/abs/1811.12231 — 顯示 ImageNet 訓練的 CNN 依賴紋理；在 Stylized-ImageNet 上訓練則會產生形狀偏好，並改善偵測與穩健性。
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). ImageNet Classification with Deep Convolutional Neural Networks. *NeurIPS*。https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，使深度卷積網路成為影像辨識的標準模型。
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*。https://doi.org/10.1073/pnas.1403112111 — 顯示物件辨識的表現，可預測網路對 IT 皮層反應的解釋程度。

### 綜述與評論

- Lindsay, G. W. (2021). Convolutional Neural Networks as a Model of the Visual System: Past, Present, and Future. *Journal of Cognitive Neuroscience*。https://doi.org/10.1162/jocn_a_01544 — 回顧 CNN 如何被用作視覺系統的模型。
- Goodale, M. A. & Milner, A. D. (1992). Separate visual pathways for perception and action. *Trends in Neurosciences*。https://doi.org/10.1016/0166-2236(92)90344-8 — 提出人類視覺的腹側（知覺）與背側（動作）路徑。
