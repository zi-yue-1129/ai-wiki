---
translation_reviewed: 2026-10-28
---

# 低秩分解與高效架構

這個家族在不改變數值精度、也不使用非結構化稀疏的情況下，減少模型的參數或計算量。它包含兩個部分：把大型權重矩陣分解為較瘦矩陣的乘積，以及選擇本身就很小的架構。低秩適應（LoRA）也在此討論，因為它使用相同的數學，但不壓縮它所適應的模型。

## 概述

低秩分解通常在訓練後，把一個大型權重矩陣改寫為兩個較瘦矩陣的乘積。高效架構則做相反的選擇：模型在訓練前就設計得很小。兩者的差別在於決定的時機。分解是縮小一個既有模型，而高效架構是從一開始就訓練另一個較小的模型。

## 方法比較

| 方法 | 套用時機 | 減少的內容 | 典型取捨 | 頁面 |
| --- | --- | --- | --- | --- |
| 截斷 SVD | 訓練後 | 稠密層與卷積層的參數與乘加運算 | 層的有效秩高時，誤差會增大 | [截斷 SVD](truncated-svd/index.zh-TW.md) |
| 低秩濾波器展開 | 訓練後，通常搭配微調 | 卷積層的乘加運算 | 壓縮越多，準確度損失越大，且每層需要各自的秩 | [低秩濾波器展開](low-rank-filter-expansion/index.zh-TW.md) |
| LoRA | 微調期間 | 可訓練參數，而非基礎模型的大小 | 推論時會增加一個更新項，除非先合併 | [LoRA](lora/index.zh-TW.md) |
| 高效架構 | 訓練前 | 依設計而定的參數與計算量 | 模型由設計固定，準確度取決於設計 | 見下文 |

前兩個方法壓縮的是已訓練的模型，因此結果取決於每一層接近低秩的程度。LoRA 讓基礎模型維持原來的大小，只學習一個小的更新。高效架構則完全避開這個問題，直接訓練一個小模型。

## 高效架構

高效架構的運作方式，在模型頁面中說明，本頁連結過去而不重複內容。

- **深度可分離卷積**被 MobileNet 採用，它以逐通道的濾波器加上一個 \(1 \times 1\) 的混合步驟，取代標準卷積。見[深度可分離卷積](../../models/cnn/convolution-variants/depthwise-separable-convolution/index.zh-TW.md)。
- **共享的鍵與值**出現在多查詢與分組查詢注意力中，在解碼時縮小鍵值快取。見[注意力變體](../../models/transformer/attention-variants/index.zh-TW.md)與[KV 快取](../../models/transformer/kv-cache/index.zh-TW.md)。
- **專家混合**讓總參數量維持很大，同時每個 token 只啟用少數專家。見 [Transformer](../../models/transformer/index.zh-TW.md) 頁面中對該層的說明。

## 取捨

- **壓縮或設計。** 壓縮已訓練的模型，能保留原有準確度作為起點，但不能在不損失準確度的情況下大幅縮小。設計一個小模型可以達到更好的準確度與大小的邊界，但必須重新訓練。
- **參數與速度。** 較低的秩或較小的架構能節省參數，但速度提升取決於硬體能否有效執行這些較小的運算。
- **適應器與壓縮。** LoRA 減少的是每個任務需要訓練與儲存的量，而不是推論時需要服務的量。兩者混淆會導致對推論記憶體用量的估計錯誤。

## 更多變體與開放問題

- **秩的選擇。** 每一層的秩通常靠搜尋或量測權重的頻譜來決定，目前沒有通用規則。
- **分解後的微調。** 分解後的模型在微調後，是否比一次性分解恢復得更好，取決於各層，最佳做法仍需依經驗決定。
- **高效注意力。** 共享鍵與值在非常長的上下文中是否仍然有效，是活躍的研究問題；見注意力變體頁面的開放問題。

## 相關連結

分解矩陣是找出其本質方向的方法，與[線性代數](../../math/index.zh-TW.md)以及學習表徵的譜觀點相連。有時人們把大腦的效率歸因於稀疏、低維的編碼，比較見[神經科學](../../../brain-mind/neuroscience/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Denton, R., Zaremba, W., Bruna, J., LeCun, Y., Fergus, R. (2014). *Exploiting Linear Structure Within Convolutional Networks for Efficient Evaluation*. arXiv:1404.0736. https://arxiv.org/abs/1404.0736 — 對卷積濾波器做低秩近似，速度約提升 2 倍，且準確度維持在 1% 以內。
- Jaderberg, M., Vedaldi, A., Zisserman, A. (2014). *Speeding up Convolutional Neural Networks with Low Rank Expansions*. arXiv:1405.3866. https://arxiv.org/abs/1405.3866 — 卷積層的低秩展開，在文字辨識網路上最多提速 4.5 倍。
- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 在凍結權重上訓練低秩更新，把 GPT-3 175B 的可訓練參數減少至多 10,000 倍。
- Howard, A. G., 等人 (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — 深度可分離卷積，用於小型快速的視覺模型，並以寬度與解析度乘數權衡延遲與準確度。
- Shazeer, N., 等人 (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. https://arxiv.org/abs/1701.06538 — 稀疏閘控的專家層，以很小的效率代價把容量提高超過 1000 倍。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 廣泛綜述訓練與推論的高效架構與稀疏方法。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Ainslie, J., 等人 (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. arXiv:2305.13245. https://arxiv.org/abs/2305.13245 — 分組查詢注意力，品質接近多頭注意力，速度接近多查詢注意力。
