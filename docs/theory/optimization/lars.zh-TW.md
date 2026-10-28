---
translation_reviewed: 2026-10-28
---

# LARS

LARS（逐層自適應學習率縮放）為每一層提供各自的學習率，其值依該層權重範數與梯度範數的比例縮放。You、Gitman 與 Ginsburg（2017）提出它，使卷積網路能以 8K 與 32K 的批次大小訓練而不損失準確率。上層概述見[梯度裁剪與正規化更新](gradient-clipping-and-normalisation.md)。

## 概述

Goyal 等人（2017）所用的線性學習率縮放加預熱，只在某個範圍內有效。超過該範圍後，對早期層安全的全域學習率，可能會使其他層發散，因為不同層的梯度與權重比例各不相同。LARS 的做法是讓每一層的步長與該層權重的大小成正比。權重小的層得到小的步長，無論其梯度多大。

## 問題

摘要指出，大批次的常用做法（線性學習率縮放加預熱）不夠通用，且訓練可能發散。作者想知道，逐層的規則能否讓 AlexNet 與 ResNet-50 的大批次訓練保持穩定。

## 核心想法

為每一層計算局部學習率，其值等於全域學習率乘以信任比。信任比是該層的權重範數除以梯度範數，並包含一個小的權重衰減項，再乘上信任係數 \(\eta\)。於是每一層的步長，由其自身權重的大小決定。

## 演算法

對於權重為 \(w_\ell\)、梯度為 \(\nabla L(w_\ell)\) 的第 \(\ell\) 層，全域學習率為 \(\gamma\)，權重衰減為 \(\beta\)，信任係數為 \(\eta<1\)：

1. 計算信任比 \(\lambda_\ell = \eta\,\dfrac{\|w_\ell\|}{\|\nabla L(w_\ell)\| + \beta\|w_\ell\|}\)。
2. 更新動量 \(v_\ell \leftarrow m\, v_\ell + \gamma\,\lambda_\ell\,(\nabla L(w_\ell) + \beta w_\ell)\)，再令 \(w_\ell \leftarrow w_\ell - v_\ell\)。

信任比的定義取自論文第 6 式，動量與權重的更新則取自其演算法 1。兩者均已對照論文全文核對。

## 結果

- 摘要報告，作者將 AlexNet 擴展到批次大小 8K，ResNet-50 擴展到批次大小 32K，兩者都「沒有準確率損失」。
- 摘要沒有其他準確率或速度數字，因此本頁不引用。

## 限制

- 此方法是針對帶動量的 SGD 類更新設計的。它延伸到自適應最佳化器的做法，是 [LAMB](lamb.md) 的主題。
- 論文分別報告偏置與權重的信任比，兩者並不相同。
- 效益是在大批次下報告的。在小批次下，它可能無法勝過普通的 SGD。

## 關聯

- [梯度裁剪與正規化更新](gradient-clipping-and-normalisation.md)是上層概述，LARS 與範數裁剪、LAMB 並列於其中。
- [漸進式預熱與線性縮放](gradual-warm-up.md)是 LARS 所延伸的全域學習率做法。
- [LAMB](lamb.md)把相同的信任比想法套用到 Adam 上。
- [大批次與分散式訓練](large-batch-and-distributed.md)是此方法使用的場景。

## 開放問題

- 信任比應如何處理權重接近零的層，或由批次統計量正規化的層？
- 當批次小到全域學習率本身已經穩定時，此效益是否仍然存在？

## 參考文獻

### 開創性論文

- You, Y., Gitman, I. & Ginsburg, B. (2017). *Large Batch Training of Convolutional Networks*. arXiv. https://arxiv.org/abs/1708.03888 — 提出 LARS，並報告 AlexNet 在批次 8K、ResNet-50 在批次 32K 下，準確率沒有損失。
- You, Y., et al. (2019). *Large Batch Optimization for Deep Learning: Training BERT in 76 Minutes*. ICLR. https://arxiv.org/abs/1904.00962 — 把逐層信任比的想法透過 LAMB 延伸到 Adam。
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — LARS 所要超越的線性縮放與預熱做法。
- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). *On the Difficulty of Training Recurrent Neural Networks*. ICML. https://arxiv.org/abs/1211.5063 — 範數裁剪，是另一種在梯度大時限制步長的方式。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機梯度方法的綜述，討論大批次下的步長選擇。
