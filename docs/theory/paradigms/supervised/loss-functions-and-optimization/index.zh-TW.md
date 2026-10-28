---
tags:
  - supervised learning
  - optimization
  - loss functions
---

# 損失函數、正規化與最佳化

學習器如何被告知什麼叫「錯誤」、如何避免死記硬背，以及它的參數究竟如何被找到。

## 損失函數

| 任務 | 損失 | 說明 |
|---|---|---|
| 迴歸 | 平方誤差 | 最佳預測子是條件平均值；對離群值敏感 |
| 迴歸 | 絕對誤差／Huber | 類似中位數；較穩健 |
| 分類 | 交叉熵 $-\log p_\theta(y\mid x)$ | 最大概似；能給出機率 |
| 分類 | Hinge | 基於間隔，SVM 使用 |
| 類別不平衡 | Focal loss、類別權重 | 降低容易的多數類樣本之權重 |
| 排序 | 成對／列表式（RankNet、LambdaRank） | 最佳化順序，而非數值 |
| 分割 | Dice、IoU 損失 | 處理區域的重疊 |

**代理損失**以可處理的凸上界取代難解的 0–1 損失；具有分類校準性的代理損失（Bartlett, Jordan & McAuliffe, 2006）能保留最佳分類器。

## 正規化

任何限制假說空間、使泛化更好的做法：權重懲罰（$\ell_1$、$\ell_2$）、dropout、早停、資料增強、標籤平滑、mixup，以及限制模型大小。其中許多方法都可以用貝氏觀點解讀為先驗。以 SGD 訓練的大型網路也會展現**隱式正規化**：最佳化器本身就偏好較簡單的解。

## 最佳化

訓練會最小化經驗風險 $\hat R(\theta)=\frac1n\sum_i L(f_\theta(x_i),y_i)$。

- **梯度下降**：$\theta\leftarrow\theta-\eta\nabla\hat R(\theta)$。**隨機／小批次**版本在子集上使用帶有雜訊的梯度，成本較低，也有助於逃離尖銳的極小值。
- **動量、RMSProp、Adam**（Kingma & Ba, 2015, arXiv:1412.6980）會自適應地調整步伐方向與大小。
- **學習率排程**（預熱、餘弦衰減）與最佳化器的選擇同樣重要。
- 凸問題（線性模型、SVM）只有一個全域最優解；深度網路則不然，但 SGD 的效果出乎意料地好。

## 類別不平衡

處理類別不平衡的兩種方式，一種改變訓練損失，另一種改變決策規則：

- [類別平衡損失](class-balanced-loss.md)：依有效樣本數為各類別加權。
- [邏輯調整](logit-adjustment.md)：依類別先驗調整分數，可在訓練後套用，也可加入損失。

## 與其他概念的連結

同樣的目標也是[自監督](../../self-supervised/index.md)預訓練的基礎；差別只在於標籤的來源。反向傳播的內容見[深度學習](../../../deep-learning/index.md)，完整的最佳化頁面則列於路線圖中。

## 參考文獻

### 開創性論文

- Bartlett, Jordan & McAuliffe (2006), "Convexity, classification, and risk bounds", *JASA* 101(473), 138–156. https://doi.org/10.1198/016214505000000907 — 說明哪些凸代理損失仍能得到良好的分類器。
- Lin et al. (2017), "Focal loss for dense object detection", ICCV, arXiv:1708.02002 — 在交叉熵中降低容易樣本的權重，有助於處理類別不平衡。
- Kingma & Ba (2015), "Adam: a method for stochastic optimization", ICLR, arXiv:1412.6980 — Adam 最佳化器，具有每個參數自適應的步長。
- Loshchilov & Hutter (2019), "Decoupled weight decay regularization", ICLR, arXiv:1711.05101 — 提出 AdamW，把權重衰減與梯度更新分開套用。

### 綜述與教科書

- Ruder (2016), "An overview of gradient descent optimization algorithms", arXiv:1609.04747 — 梯度下降變體的綜述，清楚解說動量與自適應方法。

### 講座與影片

（本頁未查核任何講座或影片。）

### 文章與文件

（除上列項目外，無其他參考。）
