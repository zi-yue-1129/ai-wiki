---
translation_reviewed: 2026-10-28
---

# LoRA

低秩適應（LoRA）在凍結的權重上學習低秩更新，以微調大型模型。Hu 等人報告，對 GPT-3 175B 而言，LoRA 能把可訓練參數減少至多 10,000 倍，GPU 記憶體約減少為三分之一，而模型品質與完整微調相當或更好。LoRA 使用與[壓縮](../index.zh-TW.md)相同的低秩數學，但它並不讓基礎模型變小，因此在本家族中只作為對照。

## 問題

為每個任務適應一個大型預訓練模型，意味著為每個任務儲存一份完整的權重副本，而訓練所有權重需要大量記憶體。需要一種只改變模型一小部分的方法，使同一個基礎模型能服務多個任務。

## 核心想法

凍結預訓練權重矩陣 \(W_0\)，並學習更新 \(\Delta W = BA\)，其中 \(B\) 與 \(A\) 是秩為 \(r\) 的瘦矩陣。每個任務只訓練並儲存 \(A\) 與 \(B\)，所有任務共用同一個基礎模型。

![LoRA 動態示意圖：保留凍結的完整權重矩陣，以小型 A、B 因子矩陣學習低秩更新，訓練後可合併回基礎權重。](../../../../assets/concept-animations/lora-low-rank-update.gif)

*原創概念動畫，CC BY-SA 4.0。* 預訓練矩陣 \(W_0\) 保持凍結，輸入依序經過可訓練的 \(A\) 與 \(B\)，形成秩至多為 \(r\) 的 \(\Delta W=BA\)。LoRA 通常把 \(B\) 初始化為零，因此初始更新為零；微調後可將 \(W_0+BA\) 合併用於推論。**LoRA 並未壓縮凍結的基礎權重**。矩陣顏色、脈衝位置與尺寸皆為機制示意，不代表實際訓練量測值。參見 [Hu 等人（2021）](https://arxiv.org/abs/2106.09685)。

## 公式或演算法

該層計算 \(h = W_0 x + BA x\)。若 \(W_0 \in \mathbb{R}^{m \times n}\)，更新的參數數量為 \(r(m+n)\)，當 \(r\) 很小時遠少於 \(mn\)。Hu 等人將 \(B\) 初始化為零，因此訓練從預訓練模型開始。訓練後，\(BA\) 可以合併進 \(W_0\)，使推論時沒有額外成本。

## 結果

摘要報告，與以 Adam 適應的 GPT-3 175B 相比，LoRA 能把可訓練參數減少至多 10,000 倍，GPU 記憶體約減少為三倍。在 RoBERTa、DeBERTa、GPT-2 與 GPT-3 上，其表現與微調相當或更好；合併後推論沒有額外延遲。

## 限制

LoRA 減少的是訓練與儲存任務專屬權重的成本，而不是必須服務的基礎模型大小。秩的選擇以及要適應哪些矩陣都會影響品質，而在差異很大的任務上，它相對於完整微調的優勢則較不明確。

## 開放問題與相關變體

- **秩的選擇。** 秩應如何依任務與層而變，尚無定論，通常靠實驗調整。
- **相關：** [截斷 SVD](../truncated-svd/index.zh-TW.md)使用相同的低秩結構來壓縮已訓練的矩陣，而不是用來適應。
- **組合。** LoRA 更新能否與量化的基礎模型結合而不損失準確度，是活躍的實務問題。[QLoRA](qlora.zh-TW.md) 針對 4 位元基底回答了這個問題，並報告在其測試的基準上與 16 位元 LoRA 相當。

## 相關連結

LoRA 是一種訓練方法，因此與[訓練](../../../../engineering/training/index.zh-TW.md)中描述的微調實務相關。它常與基礎模型的量化一起使用，而量化是另一個獨立步驟，見[量化](../../quantisation/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 在凍結權重上學習低秩更新，把 GPT-3 175B 的可訓練參數減少至多 10,000 倍。
- Denton, R., Zaremba, W., Bruna, J., LeCun, Y., Fergus, R. (2014). *Exploiting Linear Structure Within Convolutional Networks for Efficient Evaluation*. arXiv:1404.0736. https://arxiv.org/abs/1404.0736 — 把低秩結構用於壓縮，與用於適應的 LoRA 形成對照。
- Jaderberg, M., Vedaldi, A., Zisserman, A. (2014). *Speeding up Convolutional Neural Networks with Low Rank Expansions*. arXiv:1405.3866. https://arxiv.org/abs/1405.3866 — 壓縮已訓練卷積網路的低秩展開。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 綜述訓練期與推論期的效率方法。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Ainslie, J., 等人 (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. arXiv:2305.13245. https://arxiv.org/abs/2305.13245 — 一種同樣會改變推論成本的高效注意力設計。
