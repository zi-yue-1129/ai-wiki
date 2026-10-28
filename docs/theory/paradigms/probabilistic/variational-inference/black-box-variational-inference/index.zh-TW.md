---
translation_reviewed: 2026-10-28
---

# 黑箱變分推論

黑箱變分推論（black-box variational inference, BBVI）由 Ranganath、Gerrish 與 Blei（2013）提出，它以蒙地卡羅梯度最大化證據下界。這些梯度只需要聯合密度，以及近似分布族中的樣本。因此，同一套演算法可以應用於許多模型，而不必針對每個模型推導。它是[變分推論](../index.md)概述中的一種方法。

## 概述

經典的變分演算法必須針對每個模型手動推導。平均場座標上升法需要條件分布的期望有閉式解，這主要適用於條件共軛模型（Blei 等人，2016）。隨機變分推論（Hoffman 等人，2012）以帶雜訊的自然梯度把這些更新擴展到大型資料集，但它仍依賴模型的指數族結構。Ranganath 等人認為，這種針對模型的工作會拖慢新模型的擬合與比較。

BBVI 不需要這項條件。它以隨機最佳化來最大化 ELBO，每個梯度都由變分分布的樣本估計，並加入通用的變異數縮減工具，使估計在實務上可用。之所以稱為「黑箱」，是因為使用者只需提供模型，就能得到一套推論程序。

## 核心概念

- **分數函數**：變分分布對數密度的梯度 \(\nabla_\lambda \log q(z\mid\lambda)\)。它在 \(q\) 下的期望為零；利用這個恆等式可以得到不偏的梯度估計。
- **拉奧–布萊克威爾化**：把抽樣得到的項換成它對其不依賴之變數的條件期望。這樣能在不引入偏誤的前提下去除變異數。
- **控制變量**：減去一個均值為零的函數 \(h\)，並乘上係數 \(a\)。最佳的 \(a\) 等於 \(\mathrm{Cov}(f,h)/\mathrm{Var}(h)\)，論文用同一批樣本估計它。
- **Robbins–Monro 步長**：一個遞減的學習率序列，使帶雜訊的梯度上升能夠收斂。

## 運作方式

ELBO 的梯度可以寫成變分分布下的期望：

\[
\nabla_\lambda \mathcal{L} = \mathbb{E}_{q}\Big[\nabla_\lambda \log q(z\mid\lambda)\big(\log p(x,z) - \log q(z\mid\lambda)\big)\Big]
\]

對 \(S\) 個樣本 \(z_s \sim q(z\mid\lambda)\) 取平均，即得到不偏估計。論文採用拉奧–布萊克威爾化的估計器，它利用平均場的因子分解，然後再減去一個由分數函數建構的控制變量。流程如下：

1. 初始化變分參數 \(\lambda\)。
2. 從 \(q(z\mid\lambda)\) 抽出 \(S\) 個樣本。
3. 形成變異數縮減後的梯度估計，其中控制變量的係數由同一批樣本估計。
4. 以 Robbins–Monro 序列中的步長 \(\rho_t\) 更新 \(\lambda\)。
5. 當 \(\lambda\) 的變化小於門檻值（論文中為 0.01）時停止。

## 實驗結果

論文在一個醫院資料集上評估 BBVI，並與一個抽樣基準比較。

- **與抽樣方法比較。** 在一個模型上，BBVI 與 Metropolis–Hastings 嵌入 Gibbs 抽樣的方法，在固定的 20 小時預算下比較。BBVI 得到較好的留出預測似然，而且更快達到。Gibbs 抽樣器約在五小時後進展明顯變慢（論文圖 1）。
- **變異數。** 拉奧–布萊克威爾化使梯度的變異數降低了數個數量級，控制變量再進一步降低。若沒有這些步驟，基本演算法在允許的時間內幾乎沒有明顯進展（論文圖 2）。
- **模型探索。** 資料來自 976 名慢性腎臟病患者，每次就診有 17 項實驗室檢驗。同一套程式碼被用來擬合四個非共軛模型。最佳模型的留出預測似然為 −32.7，最差者為 −175。論文將其差距歸因於是否納入時間結構，以及實驗室指標之間的負相關（表 1）。

## 限制

- **雜訊仍然存在。** 變異數縮減降低了梯度的雜訊，但無法消除它，因此每一步仍需要大量樣本。
- **調參。** 論文為每個模型分別設定 AdaGrad 的縮放參數，因此步長仍需調校。
- **基準偏弱。** 抽樣比較只用了一個簡單的抽樣器與一個模型。作者也指出，哈密頓蒙地卡羅法可能表現更好。
- **局部最佳解。** ELBO 一般是非凸的，因此結果取決於初始化（Blei 等人，2016）。

## 開放問題

- 在高維連續模型上，分數函數估計器與重參數化梯度相比如何？Mohamed 等人（2019）的綜述整理了不同估計器類型之間的取捨。
- 能否將步長與變異數縮減的選擇自動化，使黑箱的承諾在實務上成立？

## 參考文獻

### 開創性論文

- Ranganath, R., Gerrish, S. & Blei, D. M. (2013). *Black Box Variational Inference*. arXiv. https://arxiv.org/abs/1401.0118 — 提出附有拉奧–布萊克威爾化與控制變量的分數函數估計器，使 ELBO 能為許多模型最佳化。
- Hoffman, M. D., Blei, D. M., Wang, C. & Paisley, J. (2012). *Stochastic Variational Inference*. arXiv. https://arxiv.org/abs/1206.7051 — 在小批次上使用帶雜訊的自然梯度，讓變分推論能擴展到大型語料庫。
- Mnih, A. & Gregor, K. (2014). *Neural Variational Inference and Learning in Belief Networks*. arXiv. https://arxiv.org/abs/1402.0030 — 以分數函數估計器訓練前饋推論網路，並以數種簡單方法降低其高變異數。
- Williams, R. J. (1992). Simple statistical gradient-following algorithms for connectionist reinforcement learning. *Machine Learning*. https://doi.org/10.1007/BF00992696 — 提出 REINFORCE 系列的分數函數梯度估計器，也就是 BBVI 所用的同一恆等式。

### 綜述與教科書

- Mohamed, S., Rosca, M., Figurnov, M. & Mnih, A. (2019). *Monte Carlo Gradient Estimation in Machine Learning*. arXiv. https://arxiv.org/abs/1906.10652 — 綜述路徑式、分數函數與測度值梯度估計器，以及它們之間的關係。
- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — 綜述平均場與座標上升法，並討論 ELBO 的局部最佳解與變異數低估問題。
- Zhang, C., Butepage, J., Kjellstrom, H. & Mandt, S. (2017). *Advances in Variational Inference*. arXiv. https://arxiv.org/abs/1711.05597 — 綜述可擴展與黑箱的變分方法，以及建立在其上的彈性分布族。

### 文章與文件

- Kucukelbir, A., Tran, D., Ranganath, R., Gelman, A. & Blei, D. M. (2016). *Automatic Differentiation Variational Inference*. arXiv. https://arxiv.org/abs/1603.00788 — 只由模型自動推導變分演算法。
