---
translation_reviewed: 2026-11-14
related:
  - theory/models/recommender
---

# 矩陣分解（Koren 等人，2009）

矩陣分解以每位使用者與每個項目各一個短向量，來預測使用者對項目的評分。這個方法成為大型評分預測問題的標準做法，也是之後許多推薦系統研究的基礎。

本頁是[推薦系統](index.md)的一部分。

## 問題

使用者—項目評分矩陣非常稀疏。一位使用者只會評分一小部分的項目，任務則是把缺漏的評分填補到足以排序或預測的程度。鄰域方法直接比較使用者或項目，在稀疏資料中很難找到好的配對，而且模型也不夠精簡。Koren、Bell 與 Volinsky（2009）描述了一種潛在因子模型，能從已觀察到的評分中學出精簡的表示。

## 核心想法

使用者與項目被映射到共享的 *f* 維空間。每個項目有一個因子向量 $q_i$，每位使用者有一個因子向量 $p_u$，兩者的內積即為評分的估計。評分的大部分變異來自使用者與項目本身的傾向，因此模型還加入全域平均 $\mu$ 與偏差項 $b_u$、$b_i$。

## 方程式

預測式為

$$\hat{r}_{ui} = \mu + b_i + b_u + q_i^{\top} p_u$$

參數只在已知評分 $\kappa$ 上擬合，並加上懲罰項以降低過度擬合：

$$\min_{q, p, b} \sum_{(u,i)\in\kappa} \left[ \left(r_{ui} - \hat{r}_{ui}\right)^2 + \lambda \left(\lVert q_i \rVert^2 + \lVert p_u \rVert^2 + b_u^2 + b_i^2\right) \right]$

常數 $\lambda$ 控制懲罰的強度，通常以交叉驗證選定。

## 學習演算法

論文描述了兩種最小化目標函數的方法。

1. **隨機梯度下降（SGD）。** 逐一走過每個已知評分，計算預測誤差，並沿損失函數梯度的反方向移動使用者與項目向量。論文認為它簡單且相對快速。
2. **交替最小平方（ALS）。** 目標函數聯合上不是凸的，但固定其中一組向量時就是二次函數。ALS 交替求解所有項目向量與所有使用者向量。論文指出，當計算可以平行化時，以及在隱式回饋資料上，ALS 較為合適，因為每個向量都可以獨立求解。

## 隱式回饋的延伸

論文也把模型延伸到隱式訊號。使用者互動過的項目，以及人口統計等使用者屬性，會為使用者的向量增加額外的因子向量。作者給出三個理由：明確評分稀疏；購買與瀏覽等隱式行為不需要使用者額外付出；額外的使用者資訊在冷啟動情況下有幫助。信心權重則讓一次性事件的分量低於重複出現的行為。

## 結果

論文在 Netflix Prize 資料上評估：超過一億筆評分，來自約五十萬名匿名顧客，涵蓋一萬七千多部電影；測試集約三百萬筆評分，以均方根誤差（RMSE）計分。Netflix 自己的系統在此資料上達到 0.9514 的 RMSE，大獎門檻為 0.8563。作者報告，他們在 2007 年進步獎中的參賽作品相較於 Netflix 的演算法提升了 8.43%；其 2008 年進步獎的參賽作品則提升了 9.46%。該參賽作品結合了一百多個預測器，其中多數是分解模型。

## 限制

- 論文的主要目標是評分預測，而多數實際系統需要從隱式回饋中排出一份短清單。為此設計的排序目標是 [BPR](bpr.md)。
- 聯合目標函數是非凸的，因此 ALS 與 SGD 只能找到局部解，結果取決於起始點與正則化。
- 模型是兩個向量之間的線性互動。[神經協同過濾](neural-cf.md)主張學得的互動函數更有彈性，並在 Top-N 評估中報告了進步。
- 向量只從互動資料描述使用者與項目，因此新使用者與新項目需要附加資訊。

## 關聯

使用者與項目向量就是嵌入，同樣的概念也是推薦的[嵌入](../embeddings/index.md)觀點的基礎。矩陣分解所比較的鄰域方法，則在[推薦系統](index.md)概述中說明。

## 應用

- **評分與排序服務**：以潛在向量預測使用者對未見過項目的評分。
- **檢索系統**：將項目向量建立索引，以便快速的最近鄰搜尋。

## 開放問題

- 當目標函數與資料都與任務相配時，更豐富的互動函數能帶來多少幫助？
- 當資料隨時間改變時，應如何選擇正則化與維度？

## 參考文獻

### 開創性論文

- Koren, Y., Bell, R. & Volinsky, C. (2009). Matrix factorization techniques for recommender systems. *Computer*, 42, pp. 30–37. https://doi.org/10.1109/MC.2009.263 — 本頁的來源：含偏差項的潛在因子模型，以 SGD 或 ALS 對評分擬合。
- Sarwar, B., Karypis, G., Konstan, J. & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. In *Proceedings of the 10th International World Wide Web Conference (WWW10)*, pp. 285–295. https://doi.org/10.1145/371920.372071 — 分解方法所比較的鄰域方法。
- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2012). *BPR: Bayesian Personalized Ranking from Implicit Feedback*. arXiv:1205.2618，首次發表於 UAI 2009。https://arxiv.org/abs/1205.2618 — 將配對排序目標應用於隱式回饋的矩陣分解。
- He, X., Liao, L., Zhang, H., Nie, L., Hu, X. & Chua, T.-S. (2017). Neural collaborative filtering. In *Proceedings of the 26th International Conference on World Wide Web (WWW 2017)*, pp. 173–182. https://doi.org/10.1145/3038912.3052569 — 主張矩陣分解的內積可以由學得的網路取代。

### 綜述與教科書

- Ricci, F., Rokach, L. & Shapira, B. (eds.) (2015). *Recommender Systems Handbook*, 2nd ed. Springer. https://doi.org/10.1007/978-1-4899-7637-6 — 參考手冊，涵蓋協同式、內容式與混合式方法，以及評估。
