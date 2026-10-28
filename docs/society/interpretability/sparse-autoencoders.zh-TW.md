---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - dictionary learning
aliases:
  - Sparse autoencoders
  - SAE
  - Dictionary learning
  - 稀疏自編碼器
  - 字典學習
---

# 稀疏自編碼器與特徵字典

稀疏自編碼器（sparse autoencoder, SAE）是一個小型網路，經過訓練，透過一個瓶頸重建模型的內部激活；同時加上一個懲罰項，使對於任何輸入，瓶頸中的大多數單元都保持不活躍。被激活的單元於是形成一個**特徵字典**：每個單元是激活空間中的一個方向，而一個輸入被描述為它們的一小組組合。研究者使用 SAE 來找出比單一神經元更具可解釋性的特徵，主要用於大型語言模型。

## 概覽

大型網路中的神經元常是**多義的（polysemantic）**，也就是說它們會對多個不相關的概念產生反應（參見[機械式可解釋性](mechanistic-interpretability.md)）。一種解釋是疊加：網路把比神經元維度更多的特徵打包進神經元之中，因此每個神經元混合了多個特徵。如果這是對的，特徵就是激活空間中的方向，而不是單一神經元，找出方向的方法就有機會恢復這些特徵。

稀疏字典學習是這方面的經典工具。Olshausen 與 Field（1996）顯示，對自然影像區塊訓練的稀疏編碼，會產生類似初級視覺皮層細胞感受野的濾波器。把同樣的想法應用到語言模型的激活上，就是 SAE 可解釋性研究的基礎。

## 核心概念

- **編碼器與解碼器（encoder and decoder）**：編碼器把激活映射為稀疏碼，解碼器則把碼映射回激活的近似值。
- **字典（dictionary）**：解碼器的各欄，每一欄對應一個特徵。
- **稀疏性（sparsity）**：同時活躍的特徵比例。稀疏性由 L1 懲罰或明確的 top-k 規則強制執行（[Makhzani & Frey, 2014](k-sparse-autoencoders.md)）。
- **單義特徵（monosemantic feature）**：以人類可辨識的方式只對一個概念產生反應的特徵。

## 運作方式

SAE 在從模型某一層收集的大量激活上訓練。損失函數有兩項：重建誤差，使特徵忠於激活；以及稀疏項，使碼保持簡短。訓練後，逐一檢視每個特徵，看哪些輸入最強烈地激活它。當這些輸入共享一個清楚的概念時，就認為該特徵具可解釋性。接著以介入來檢驗：加入或移除某特徵的方向，應使模型的輸出依預測的方式改變。

Cunningham et al.（2023）在小型語言模型的激活上訓練 SAE，並報告在這個流程下，許多特徵都是可解釋的，且比它們所源自的神經元更具可解釋性。Bricken et al.（2023）把這個方法應用在一個單層的小型 Transformer 上，並報告許多特徵在檢視時看起來是單義的。

## 擴展

主要的問題是這個方法能否擴展。Templeton et al.（2024）在一個量產規模的模型的激活上訓練 SAE，並報告數百萬個特徵，包括具體實體的特徵與一些抽象概念的特徵，以及可用來引導行為的特徵。Gao et al.（2024）顯示，SAE 的大小與稀疏性可以依可預測的取捨來擴展，並提出一種 top-k 架構，使訓練更穩定。Lieberum et al.（2024）為一個開放的模型家族釋出一組 SAE，讓其他研究者無需自行訓練，就能研究這些特徵。[JumpReLU 稀疏自編碼器](jumprelu-sae.md)為每個特徵設定獨立閾值，以改善重建。

擴展也帶來新的問題。重建得很好的 SAE 仍可能漏掉特徵；在較小 SAE 中具可解釋性的特徵，在較大的 SAE 中可能分裂為數個特徵，因此特徵取決於字典的大小。

## 引導與應用

特徵可以用來引導模型：把它的方向加入殘差流，會改變模型對該概念的說法。Templeton et al.（2024）展示了這類示範。引導對於檢驗某特徵是否具因果性很有用，但它也可能是一種潛在的安全工具，因為與不良行為相關的特徵，原則上可以被抑制。這對真實行為是否成立，仍是開放問題。

## 已知的失效模式

- **重建良好不等於忠實。** SAE 可以重建激活得很好，但學到的特徵卻是模型沒有使用的。
- **特徵分裂與吸收。** 一個概念可能被分裂為數個特徵，或當兩個概念同時出現時，一個特徵會吸收另一個。
- **依賴字典大小。** 特徵集合隨 SAE 的大小與稀疏性而改變，因此一個特徵是某個特定字典的性質。
- **以檢視來詮釋。** 從最強激活來為特徵命名是主觀的，而自動命名可能出錯。
- **死特徵與密集特徵。** 有些字典單元從不激活，另一些則在大多數輸入上激活，這都削弱了它們的意義。

## 相關連結

稀疏編碼在神經科學中有悠久的歷史。效率編碼假說認為，感覺系統以少數活躍單元來表示輸入，這是上述影像編碼結果的一個動機，相關連結見[稀疏編碼](../../brain-mind/computational-neuroscience/sparse-coding/index.md)。SAE 方法的不同之處在於，它應用於訓練好的人工網路，並以介入加以檢驗，而這在神經科學中較難做到。關於被分析的架構，見[Transformer](../../theory/models/transformer/index.md)。

## 應用

- 為概念（例如實體或與安全相關的主題）找出特徵，用於稽核。
- 透過加入特徵方向來引導模型輸出。
- 依共享或缺少的特徵比較不同模型。

## 開放問題

- SAE 特徵是模型實際用來運算的單元，還是有用但不完整的描述？
- 能否訓練出避免特徵分裂又不失去可解釋性的字典？
- 哪些特徵與安全有關？能否可靠地找到它們，使模型可被稽核？

## 參考文獻

### 開創性論文

- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*, 381, 607–609. https://doi.org/10.1038/381607a0 — Shows that a sparse coding objective trained on natural images produces receptive-field-like filters.
- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Enforces sparsity with a top-k rule in place of an L1 penalty.
- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies sparse autoencoders to language model activations and reports interpretable features.

### 綜述與教科書

- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.

### 文章與文件

- Bricken, T. et al. (2023). *Towards Monosemanticity: Decomposing Language Models With Dictionary Learning*. Transformer Circuits Thread. https://transformer-circuits.pub/2023/monosemantic-features/index.html — Applies dictionary learning to a small transformer and reports monosemantic features.
- Templeton, A. et al. (2024). *Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet*. Transformer Circuits Thread. https://transformer-circuits.pub/2024/scaling-monosemanticity/ — Scales sparse autoencoders to a production-scale model and reports features and steering demonstrations.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of sparse autoencoders for an open model family.
- Rajamanoharan, S. et al. (2024). *Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders*. arXiv:2407.14435. https://arxiv.org/abs/2407.14435 — Introduces a sparse autoencoder with a thresholded JumpReLU activation that improves reconstruction at a given sparsity.

## 延伸學習

- [SAELens](https://github.com/decoderesearch/SAELens) — 在語言模型上訓練與分析稀疏自編碼器的開源函式庫。
