---
translation_reviewed: 2026-11-17
related:
  - theory/models/recommender
---

# BPR：貝氏個人化排序（Rendle 等人，2012）

貝氏個人化排序（BPR）從隱式回饋訓練推薦模型，方法是學習使用者偏好哪些項目勝過其他項目，而不是為每筆互動擬合一個分數。它是 Top-N 排序的標準起點。

本頁是[推薦系統](index.md)的一部分。

## 問題

點擊、瀏覽與購買等隱式回饋記錄的是使用者做了什麼，而不是他不喜歡什麼。缺漏的互動可能代表「沒興趣」，也可能代表「從未看過」。矩陣分解與鄰域方法等常見模型，通常被訓練來為每筆已觀察到的紀錄預測一個值。Rendle 等人（2012）主張，這些方法都沒有直接針對推薦實際使用的排序任務進行訓練。

## 核心想法

對使用者 $u$ 而言，已觀察到的項目 $i$ 應排在未觀察到的項目 $j$ 之前。BPR 把每位使用者的歷史轉換為這類配對，並學習一個能滿足配對順序的模型。這個方法是通用的：論文把它應用於矩陣分解，也應用於適應性最近鄰模型。

## 方程式

令 $\hat{x}_{uij}$ 為使用者 $u$ 對項目 $i$ 與 $j$ 的模型分數差，即 $\hat{x}_{ui} - \hat{x}_{uj}$。使用者偏好 $i$ 勝過 $j$ 的可能性，以邏輯斯諦函數（sigmoid）建模：

$$p(i >_u j \mid \Theta) = \sigma\left(\hat{x}_{uij}(\Theta)\right), \qquad \sigma(x) = \frac{1}{1 + e^{-x}}$$

在參數 $\Theta$ 上取零均值常態先驗，論文的最大後驗估計給出 BPR-Opt 準則：

$$\text{BPR-Opt} = \sum_{(u,i,j)\in D_S} \ln \sigma\left(\hat{x}_{uij}\right) - \lambda_\Theta \lVert \Theta \rVert^2$$

其中 $D_S$ 是訓練三元組的集合，$\lambda_\Theta$ 是模型專屬的正則化參數。

### 動畫算例：單一 BPR 配對的排序更新

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/bpr-pairwise-ranking-still.svg" data-motion-src="../../../assets/concept-animations/bpr-pairwise-ranking-motion.svg" data-still-src="../../../assets/concept-animations/bpr-pairwise-ranking-still.svg" alt="BPR 梯度更新使已觀察項目與抽樣未觀察項目的分數逐漸分開，配對邏輯損失下降。" style="width:800px;min-width:800px;max-width:none;height:auto" />
</div>

[GitHub 可讀的靜態預覽](../../../assets/concept-animations/bpr-pairwise-ranking-still.svg)

以一組抽樣三元組 $(u,i,j)$ 示範，固定一維使用者因子 $p_u=1$，並設定兩個項目因子 $q_i=0.5$、$q_j=1.3$。起初，已觀察項目 $i$ 的預測分數**低於**未觀察項目 $j$。為了單獨呈現項目因子的梯度更新，此例固定 $p_u$，不加入正則化。令 $\Delta=p_u(q_i-q_j)$、$\eta=0.4$，則對 $\log\sigma(\Delta)$ 做一步梯度上升：
$$
g=\sigma(-\Delta),\qquad q_i\leftarrow q_i+\eta g p_u,\qquad q_j\leftarrow q_j-\eta g p_u.
$$
左圖顯示已觀察項目的分數上升，抽到的未觀察項目分數下降；右圖追蹤配對損失 $-\log\sigma(\Delta)$。四次更新後，分數差由 **−0.8000** 變為約 **0.8518**，損失則由 **1.1711** 降至 **0.3553**。

所有數值皆為**人工解析計算**，不是模型實測。為隔離項目梯度而固定使用者因子，與完整 BPR-MF 訓練不同；更新之間的平滑動畫只是視覺過渡，不代表連續最佳化軌跡。「未觀察項目」只是訓練用的比較對象，**不能當作已確認的負向偏好**。

在 MkDocs 網站中可使用支援鍵盤操作的**播放／暫停**控制；窄螢幕可聚焦圖像並水平捲動。GitHub 與 `prefers-reduced-motion` 模式使用靜態回退圖。原創圖像，**CC BY-SA 4.0**。

## 演算法

此準則以在抽樣三元組上的隨機梯度上升來最佳化。論文以均勻隨機方式選取三元組，並採用有放回的拔靴法（bootstrap）抽樣，因此可以在任一步停止訓練。每一步抽出一個已觀察到的配對 $(u, i)$，再隨機選一個未觀察到的項目 $j$，然後沿著使 $\ln \sigma(\hat{x}_{uij})$ 增加的方向更新參數。

## 結果

論文在兩個轉換為隱式回饋的資料集上評估。第一個是 Rossmann 線上商店的購買紀錄，含一萬名使用者、四千個項目與 426,612 次購買。第二個是 Netflix 的子樣本，含一萬名使用者、五千個項目與 565,738 筆評分行為，評分已被去除，只保留隱式回饋。精確的 AUC 數值在論文中以圖表呈現。文中報告的比較如下：

- 在兩個資料集上，BPR-MF「在排序任務上明顯優於 WR-MF」。
- 在 Netflix 上，八維的 BPR-MF 與一百二十八維的 WR-MF 品質相當。
- 兩個以 BPR 最佳化的方法，在預測品質上優於其他所有方法。
- SVD-MF 的品質隨維度增加而下降。

## 限制

- 論文聚焦於模型參數的離線學習。線上學習只被提及為可能的延伸，作者指出一種 fold-in 策略也可用於 BPR，但沒有評估。
- 作者計算了 AUC 的上界，但該上界是「非緊的」，因此無法說明各方法離最佳排序有多遠。
- 超參數第一輪以網格搜尋設定，之後的重複實驗中保持不變。
- 論文以均勻隨機方式抽取未觀察到的項目 $j$，沒有研究其他選擇負例的方式。[神經協同過濾](neural-cf.md)同樣把非均勻的負採樣留待未來研究。

## 關聯

BPR 是一種配對排序損失，與學習排序（learning to rank）中使用的排序目標相近。它的使用者與項目因子，就是[矩陣分解](matrix-factorization.md)頁面所述的那類[嵌入](../embeddings/index.md)；它也是[神經協同過濾](neural-cf.md)所比較的排序基準。

## 應用

- **商品與媒體排序**：在只有記錄下來的購買或瀏覽資料時。
- **Top-N 清單**：輸出是一份有序的短清單，順序比預測值本身更重要。

## 開放問題

- 配對訓練應抽取哪些負例？這個選擇會在多大程度上改變最終的排序？
- 當許多推薦系統已依賴序列與情境資訊時，應如何結合配對目標與這些資訊？

## 參考文獻

### 開創性論文

- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2012). *BPR: Bayesian Personalized Ranking from Implicit Feedback*. arXiv:1205.2618，首次發表於 UAI 2009。https://arxiv.org/abs/1205.2618 — 本頁的來源：BPR-Opt 準則、抽樣的訓練三元組與 AUC 比較。
- Sarwar, B., Karypis, G., Konstan, J. & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. In *Proceedings of the 10th International World Wide Web Conference (WWW10)*, pp. 285–295. https://doi.org/10.1145/371920.372071 — 項目為基礎的鄰域協同過濾基準，作為背景引用。
- Koren, Y., Bell, R. & Volinsky, C. (2009). Matrix factorization techniques for recommender systems. *Computer*, 42, pp. 30–37. https://doi.org/10.1109/MC.2009.263 — BPR-MF 以排序目標重新訓練的、基於評分的矩陣分解。
- He, X., Liao, L., Zhang, H., Nie, L., Hu, X. & Chua, T.-S. (2017). Neural collaborative filtering. In *Proceedings of the 26th International Conference on World Wide Web (WWW 2017)*, pp. 173–182. https://doi.org/10.1145/3038912.3052569 — 以 Top-N 指標評估的後續模型，並將配對學習列為未來工作。

### 綜述與教科書

- Ricci, F., Rokach, L. & Shapira, B. (eds.) (2015). *Recommender Systems Handbook*, 2nd ed. Springer. https://doi.org/10.1007/978-1-4899-7637-6 — 參考手冊，涵蓋協同式、內容式與混合式方法，以及評估。
