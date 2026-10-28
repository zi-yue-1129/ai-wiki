---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - Differential privacy
  - DP-SGD
  - 差分隱私
---

# 差分隱私

!!! info "屬於隱私與資料保護"
    本方法頁隸屬於[隱私與資料保護](index.md)。它詳細說明此方法；上層頁面則將它與其他保護措施並列比較。

差分隱私是資料分析中隱私的形式化定義。它保證：當任一個人的紀錄被加入或移除時，分析的輸出只會略有改變。Dwork 等人（2006）提出了這個定義，以及實現它的基於雜訊的機制。在機器學習中，同樣的概念被應用於訓練過程，用來限制任何單一樣本對模型的影響。

## 問題

即使分析或模型的目的是描述群體，它仍可能洩露個人的資訊。匿名化紀錄並不足夠，因為統計結果本身仍可能暴露某個人。問題在於：如何發布有用的結果，並提供一種不依賴攻擊者既有知識的保證。

## 核心想法

在輸出中加入隨機雜訊，雜訊的大小取決於單一紀錄最多能改變答案多少。如果某人是否被納入資料，答案幾乎不變，那麼觀察者就幾乎學不到關於這個人的資訊。雜訊的大小由兩個數字決定：隱私參數 ε（越小表示隱私越強），以及寬鬆版本中的 δ。

## 運作方式

**定義。** 若對於每一對只差一筆紀錄的資料集 \(D\) 與 \(D'\)，以及所有輸出集合 \(S\)，都有

\[
\Pr[M(D)\in S] \le e^{\varepsilon}\,\Pr[M(D')\in S],
\]

則隨機化機制 \(M\) 滿足 \(\varepsilon\)-差分隱私。

**拉普拉斯機制。** 對敏感度為 \(\Delta f\) 的數值查詢，機制回傳 \(f(D)\) 加上尺度為 \(\Delta f / \varepsilon\) 的拉普拉斯雜訊。

**訓練中（DP-SGD）。** Abadi 等人（2016）把這個概念用於隨機梯度下降：限制每個樣本梯度的大小，並在每次更新前對合併後的梯度加入雜訊。隱私會計器再追蹤所有訓練步驟的總隱私成本。

## 結果

Dwork 等人（2006）提供形式化的保證與校準雜訊的方法，而非實證的基準測試。Abadi 等人（2016）顯示，深度網路可以用 DP-SGD 訓練，並追蹤整個訓練過程的隱私成本。準確度的實際取捨取決於任務、資料集與隱私預算，因此比較時應以具體的論文為準。

## 限制

- **準確度成本。** 雜訊會降低準確度。損失通常在小群體上最大，這會引發公平性的問題（見[倫理與公平](../ethics/index.md)）。
- **預算耗用。** 每次發布都會消耗一部分隱私預算，因此若不追蹤預算，重複查詢會削弱保證。
- **適用範圍。** 保證涵蓋的是資料集中的紀錄。它無法阻止模型學到一般性的事實，也無法單獨阻止公開資料在受保護的資料集之外被記住。
- **ε 的選擇。** 定義本身並未說明可接受的 ε 值，這是政策上的選擇。

## 與其他主題的連結

- 成員推論是差分隱私所要限制的攻擊，見[成員推論](membership-inference.md)。
- 訓練文字的記憶化是 DP-SGD 所能降低的風險，見[訓練資料萃取](training-data-extraction.md)。
- 聯邦學習常結合安全聚合與差分隱私，見[聯邦與隱私保護學習](../../theory/paradigms/federated/index.md)。

## 開放問題

- 隱私預算應如何選擇，又應如何告知其資料被使用的人？
- 對於大型語言模型，DP 訓練能否在合理成本下接近非私密訓練的準確度？
- 當受保護的單位是個人，而模型同時也從公開文字學習時，應如何說明這項保證？

## 參考資料

### 開創性論文

- Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *Theory of Cryptography Conference (TCC)*. https://doi.org/10.1007/11681878_14 — 提出差分隱私與領域廣泛使用的雜訊校準框架。
- Abadi, M. et al. (2016). Deep learning with differential privacy. *ACM CCS*. https://arxiv.org/abs/1607.00133 — DP-SGD，以差分隱私保證訓練深度模型的方法。
- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *IEEE Symposium on Security and Privacy*. https://arxiv.org/abs/1610.05820 — 差分隱私所要限制的攻擊。
- Yeom, S., Giacomelli, I., Fredrikson, M. & Jha, S. (2018). Privacy risk in machine learning: Analyzing the connection to overfitting. arXiv:1709.01604. https://arxiv.org/abs/1709.01604 — 顯示單靠過擬合就足以進行成員推論，因此限制記憶化十分重要。

### 綜述與教科書

- Dwork, C. & Roth, A. (2014). *The Algorithmic Foundations of Differential Privacy*. Foundations and Trends in Theoretical Computer Science, 9(3–4). https://doi.org/10.1561/0400000042 — 標準教科書，完整收錄機制與證明。
