---
translation_reviewed: 2026-10-28
---

# 漸進式剪枝

漸進式剪枝在訓練期間平滑地提高網路的稀疏度，而不是一次剪掉。Zhu 與 Gupta 以它比較大型稀疏網路與小型稠密網路，發現稀疏網路始終較好。它是疊加在[幅度剪枝](../index.zh-TW.md)之上的一種排程。

## 問題

剪枝論文把剪枝後的網路與其來源的稠密網路作比較。對於固定的預算，剪枝是否比一開始就訓練較小的稠密網路更好，並不清楚。

## 核心想法

在大小相當的條件下比較大型稀疏模型與小型稠密模型，並在訓練期間逐步剪大型模型。網路能適應每次小幅度的剪除，因此漸進式排程比一次剪到相同稀疏度能恢復更多準確率。

## 公式或演算法

稀疏度沿著三次方排程，從初始值 \(s_i\)（通常為零）上升到最終目標 \(s_f\)：

\[
s_t = s_f + (s_i - s_f)\left(1 - \frac{t - t_0}{n\,\Delta t}\right)^3
\]

其中 \(t \in \{t_0, t_0 + \Delta t, \dots, t_0 + n\,\Delta t\}\)。\(t_0\) 是開始剪枝的訓練步數，\(n\) 是剪枝步數，\(\Delta t\) 是剪枝頻率（以訓練步數計）。每個剪枝步驟會遮罩幅度最小的權重，直到達到當前稀疏度，然後在剩下的權重上繼續訓練。三次方的形式在網路冗餘最多的初期剪得較快，接近目標時則放慢。

## 結果

論文摘要報告，大型稀疏模型始終優於小型稠密模型。部分實驗在非零參數數量相等的條件下比較；另一些實驗則在記憶體佔用相當的條件下比較，並把稀疏儲存的額外開銷算進去。實驗的最終稀疏度從 50% 到 97.5% 不等。

## 限制

漸進式排程會增加訓練步數，並有自己的超參數：起始步數、步數與頻率。參數數量相等不等於運算量相等，因為稀疏層在稠密硬體上不一定跑得更快。

## 未解問題與相關變體

- **排程遷移。** 為某一架構調好的排程，能否不經重新調校地用於另一架構，尚無定論。
- **相關。** [彩票](../../lottery-ticket/lottery-ticket-hypothesis/index.zh-TW.md)程序也是迭代式剪枝，但它把存活的權重倒回訓練早期的某一點。

## 與其他主題的連結

漸進式排程是[同時學習權重與連接](../../learning-weights-and-connections/index.zh-TW.md)中迭代剪枝的改良。把幅度剪枝與其他方法並列比較的基準，見[稀疏性現況](../state-of-sparsity/index.zh-TW.md)。

## 參考文獻

### 奠基性論文

- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — 提出三次方的漸進排程，並顯示大型稀疏模型始終優於小型稠密模型。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 漸進排程所改良的迭代式剪枝再訓練流程。
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 把漸進式幅度剪枝與其他稀疏化方法作基準比較。

### 綜述與教科書

- Hoefler, T., Alistarh, D., Ben-Nun, T., Dryden, N., Peste, A. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述訓練期間的稀疏排程。

### 講座與影片

（本頁未檢核任何項目）

### 文章與文件

- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — 漸進排程的倒回再訓練替代方案。
