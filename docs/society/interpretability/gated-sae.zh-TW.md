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
  - Gated SAE
  - Gated sparse autoencoder
  - Gated 稀疏自編碼器
  - 門控稀疏自編碼器
---

# 門控稀疏自編碼器

門控稀疏自編碼器（gated sparse autoencoder）是一種編碼器有兩條路徑的稀疏自編碼器。一個門（gate）決定哪些特徵開啟，另一條獨立的幅度路徑（magnitude path）估計每個開啟特徵的強度。只有門的路徑會接受 L1 懲罰。Rajamanoharan et al.（2024）提出這個設計，目的是減少收縮（shrinkage）：標準稀疏自編碼器中，L1 懲罰會使特徵激活被系統性地低估。

## 問題

標準的稀疏自編碼器用同一個 ReLU 編碼器完成兩項工作：判斷哪些特徵活躍，以及估計它們的激活有多大。編碼上的 L1 懲罰會把兩者都往零推。判斷特徵是否開啟需要稀疏性的壓力，但估計其大小並不需要，因此單一懲罰會同時扭曲兩項工作。結果就是收縮：重建值系統性地小於真實激活，而且懲罰越強，偏差越大。

## 核心想法

把編碼器拆成門與幅度兩條路徑。門的前激活經過 Heaviside 階躍函數，只有門的值為正時，特徵才開啟。之後由 ReLU 幅度路徑給出強度，而且只有門的路徑接受 L1 懲罰。幅度路徑重用門的方向，並加上每個特徵學得的重新縮放與自己的偏置，因此相較於標準的稀疏自編碼器，這個設計每個特徵只多兩個參數。

## 方程式或演算法

對於以 ReLU 為編碼器的基準稀疏自編碼器，特徵與損失為

$$
f(x) = \mathrm{ReLU}\big(W_{\text{enc}}(x - b_{\text{dec}}) + b_{\text{enc}}\big), \qquad \mathcal{L} = \lVert x - \hat{x}(f(x)) \rVert_2^2 + \lambda \lVert f(x) \rVert_1
$$

門控編碼器使用門的前激活 $\pi_{\text{gate}}(x) = W_{\text{gate}}(x - b_{\text{dec}}) + b_{\text{gate}}$，以及幅度的前激活 $\pi_{\text{mag}}(x) = W_{\text{mag}}(x - b_{\text{dec}}) + b_{\text{mag}}$：

$$
\tilde{f}(x) = \mathbf{1}\big[\pi_{\text{gate}}(x) > 0\big] \odot \mathrm{ReLU}\big(\pi_{\text{mag}}(x)\big)
$$

幅度權重透過逐列（row-wise）的重新縮放與門的權重綁定，即 $W_{\text{mag}} = \exp(r_{\text{mag}}) \odot W_{\text{gate}}$，其中 $r_{\text{mag}}$ 是學得的參數。訓練損失為

$$
\mathcal{L}_{\text{gated}}(x) = \lVert x - \hat{x}(\tilde{f}(x)) \rVert_2^2 + \lambda \lVert \mathrm{ReLU}(\pi_{\text{gate}}(x)) \rVert_1 + \lVert x - \hat{x}_{\text{frozen}}\big(\mathrm{ReLU}(\pi_{\text{gate}}(x))\big) \rVert_2^2
$$

最後一項是輔助重建，經過解碼器的凍結副本，因此其梯度不會回傳到解碼器。論文的消融實驗指出，凍結此副本很重要。

## 結果

- **用更少的特徵達到重建。** 在相同的訓練運算量下，論文報告其權衡優於基準。摘要的說法是：達到相當的重建保真度，所需的活躍特徵約為基準的一半。
- **收縮。** 門控重建值接近無偏，擬合出的收縮係數接近 1。基準稀疏自編碼器的係數則低於 1，且偏差隨懲罰增大而惡化。
- **可解釋性。** 在一項盲測的評分者研究中，採用 Pythia-2.8B 的 150 個特徵與 Gemma-7B 的 192 個特徵，門控特徵被評為可解釋性相當。單尾檢定的 $p = 0.060$，因此作者的結論是門控特徵至少相當，但不能確定更具可解釋性。
- **成本。** 計算損失時，每步的運算量增加約 50%，因為解碼器要執行兩次。實際訓練的牆鐘時間增加較少，因為激活生成與輸入輸出往往佔主導。

## 限制

- **仍有 L1。** 門仍接受類似 L1 的懲罰，因此稀疏性的計數仍是可解釋性的代理。
- **可解釋性優勢未確立。** 評分者研究沒有顯示明確的改進，論文也如此說明。
- **額外運算。** 輔助項的解碼器前向傳遞會增加每步的訓練成本。
- **模型範圍有限。** 報告的比較涵蓋少數模型與層，因此在其他模型上結果可能不同。

## 相關連結

門控設計是[JumpReLU 稀疏自編碼器](jumprelu-sae.md)所比較的架構之一。JumpReLU 論文報告，在給定的稀疏程度下，其方法比 Gated SAE 更忠實，而兩篇論文有幾位共同作者。兩者都屬於[稀疏自編碼器](sparse-autoencoders.md)所述的家族，與[k-稀疏自編碼器](k-sparse-autoencoders.md)中的 top-k 變體並列。門控 SAE 所修改的基準，是 Cunningham et al.（2023）使用的 L1 設計。關於這些方法所讀取激活的 Transformer 架構，見[Transformer](../../theory/models/transformer/index.md)。

## 應用

- 為語言模型激活建立特徵字典，當收縮會使後續測量產生偏差時尤其重要。
- 在活躍特徵數量相當的條件下，比較稀疏自編碼器的設計。
- 在分析中把「這個特徵是否開啟」與「它開啟的強度多大」分開處理。

## 開放問題

- 在更大規模的評分者研究中，可解釋性的優勢是否依然成立？
- 較低的收縮，能否像改善重建一樣改善因果測試（例如激活修補）？
- 凍結的輔助解碼器，對其他架構是否有同樣的幫助？

## 參考文獻

### 開創性論文

- Rajamanoharan, S. et al. (2024). *Improving Dictionary Learning with Gated Sparse Autoencoders*. arXiv:2404.16014. https://arxiv.org/abs/2404.16014 — Introduces the gated encoder, which separates feature detection from magnitude estimation to reduce shrinkage.
- Rajamanoharan, S. et al. (2024). *Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders*. arXiv:2407.14435. https://arxiv.org/abs/2407.14435 — Compares JumpReLU sparse autoencoders with Gated and TopK sparse autoencoders on Gemma 2 9B activations.
- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Introduces top-k sparsity, an alternative to the L1 penalty.

### 綜述與教科書

- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies L1-penalised sparse autoencoders to language model activations, the baseline design that gated sparse autoencoders modify.
- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of JumpReLU sparse autoencoders for Gemma 2 models.
