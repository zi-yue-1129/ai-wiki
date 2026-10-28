---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - dictionary learning
aliases:
  - JumpReLU SAE
  - JumpReLU sparse autoencoder
  - JumpReLU 稀疏自編碼器
---

# JumpReLU 稀疏自編碼器

JumpReLU 稀疏自編碼器是用於語言模型激活的稀疏自編碼器，其隱藏單元使用有閾值的激活函數。每個特徵都有自己學到的閾值：編碼器的輸出只有超過該閾值才會原樣通過，否則設為零。Rajamanoharan et al.（2024）提出它，目的是在給定的稀疏程度下改善重建，並把「這個特徵是否活躍」與「活躍的強度有多大」分開處理。

## 問題

用於語言模型的稀疏自編碼器必須同時做到兩件事：忠實地重建模型的激活，以及讓大多數特徵對每個輸入都保持不活躍。常見的 ReLU 稀疏自編碼器加上 L1 懲罰，會把活躍的特徵拉向零，損害重建。top-k 自編碼器固定了稀疏程度，但每個輸入的活躍特徵數量也固定。Rajamanoharan et al. 指出以 L1 懲罰訓練有已知的限制，並以 L0 的啟用特徵計數取而代之。

## 核心想法

以 JumpReLU 取代 ReLU。每個特徵 $i$ 有一個閾值 $\theta_i > 0$。如果該特徵的編碼器輸出超過 $\theta_i$，激活就原樣通過；否則為零。由於閾值與激活值是分開的，特徵一旦開啟，網路就能保持其數值準確，而閾值決定它是否開啟。

## 方程式或演算法

令 $\pi_i(x)$ 為特徵 $i$ 的編碼器前激活，則 JumpReLU 特徵激活為

$$
f_i(x) = \mathrm{JumpReLU}_{\theta_i}\big(\pi_i(x)\big) = \pi_i(x)\,\mathbf{1}\big[\pi_i(x) > \theta_i\big]
$$

重建為 $\hat{x} = W_{\text{dec}} f(x) + b_{\text{dec}}$。訓練最小化重建誤差加上活躍特徵數量的懲罰，

$$
\mathcal{L} = \lVert x - \hat{x} \rVert^2 + \lambda \lVert f(x) \rVert_0
$$

其中 $\lVert f(x) \rVert_0$ 計算活躍特徵的數量。閾值是不連續的，因此計數懲罰對閾值的梯度幾乎處處為零。論文以直通估計器（straight-through estimator）處理這個問題，讓梯度穿過閾值，如同它是平滑函數一樣，使閾值可以被學習。

## 結果

摘要報告，在給定的稀疏程度下，其重建保真度達到當時的最先進水準，比較對象包括 Gated 與 TopK 等其他近期的稀疏自編碼器架構。實驗使用 Gemma 2 9B 語言模型的激活。摘要未給出具體的數值結果，比較數字見論文本身，此處不重複。

## 限制

- **以稀疏作為代理。** 懲罰計算的是活躍特徵的數量，這是可解釋性的代理。稀疏的字典仍可能含有難以解讀的特徵。
- **訓練複雜度。** 直通估計器與閾值增加了必須調整的超參數與訓練選擇。
- **特徵分裂仍然存在。** 和其他字典學習方法一樣，JumpReLU 字典隨規模增大時，可能把概念分散到多個特徵上。
- **證據範圍。** 報告的比較限於一個模型家族與數個稀疏程度。在其他模型上，或在電路層級的分析中，結果可能不同。

## 相關連結

JumpReLU 屬於[稀疏自編碼器](sparse-autoencoders.md)所述的家族，與[k-稀疏自編碼器](k-sparse-autoencoders.md)所述的 top-k 變體並列。把「是否開啟」與「強度多大」分開，是一項設計選擇，而不是關於神經元的主張，但它與神經元具有發放閾值的想法相呼應。JumpReLU 論文所比較的 Gated 設計，見[門控稀疏自編碼器](gated-sae.md)。關於自編碼器所讀取的 Transformer 架構，見[Transformer](../../theory/models/transformer/index.md)。

## 應用

- 為大型語言模型的可解釋性研究建立特徵字典。
- 在分析過程中以自編碼器取代模型的一部分時，改善重建。
- 在相同的稀疏程度下比較稀疏自編碼器架構。

## 開放問題

- 在重建相當的情況下，JumpReLU 特徵是否比其他架構更具可解釋性？
- 學到的閾值對訓練時程與稀疏懲罰有多敏感？
- 重建的提升，能否延續到[機械式可解釋性](mechanistic-interpretability.md)所用的因果測試？

## 參考文獻

### 開創性論文

- Rajamanoharan, S. et al. (2024). *Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders*. arXiv:2407.14435. https://arxiv.org/abs/2407.14435 — Introduces a sparse autoencoder with a thresholded JumpReLU activation that improves reconstruction at a given sparsity.
- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Introduces top-k sparsity, the main alternative to L1 penalties that JumpReLU is compared with.

### 綜述與教科書

- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies L1-penalised sparse autoencoders to language model activations, the setting in which JumpReLU is later applied.
- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of JumpReLU sparse autoencoders for Gemma 2 models.
