---
translation_reviewed: 2026-10-28
---

# 模型壓縮

模型壓縮能減少已訓練模型所需的記憶體、運算量、能耗或延遲，同時盡量保留它的行為。它之所以重要，是因為在資料中心裡準確的模型，可能大到無法放進手機，慢到無法跑在汽車的控制迴圈裡，或貴到無法服務數百萬使用者。

## 概述

訓練好的網路通常是過度參數化的。許多權重對輸出的貢獻很小，許多數值的儲存精度也超過任務所需。壓縮主要利用這種冗餘，分成四個方向：

| 類別 | 減少的對象 | 典型取捨 | 頁面 |
|---|---|---|---|
| 量化 | 每個數值的位元數（權重、激活值、快取） | 捨入誤差；需要校準 | [量化](quantisation/index.zh-TW.md) |
| 剪枝 | 權重、通道或注意力頭的數量 | 稀疏度高時準確度下降；加速效果取決於硬體 | [剪枝](pruning/index.zh-TW.md) |
| 知識蒸餾 | 模型本身的大小 | 學生模型的品質受教師與資料限制 | [知識蒸餾](knowledge-distillation/index.zh-TW.md) |
| 低秩分解 | 大型矩陣中的參數 | 權重矩陣的有效秩高時會有損失 | [低秩分解與高效架構](low-rank-and-efficient-architectures/index.zh-TW.md) |

壓縮通常在訓練**之後**進行，稱為訓練後壓縮。感知訓練的方法，例如量化感知訓練或蒸餾，會改變訓練過程本身，通常能在相同大小下保留更多品質。高效架構設計是相關但不同的策略：它在訓練前選擇一個小模型，而不是縮小一個大模型。

## 關鍵概念

- **壓縮比**：原始大小除以壓縮後大小。報告的壓縮比只有搭配它所保留的準確度才有意義。
- **準確度與大小的前緣**：無法再縮小而不損失準確度的模型集合。論文通常以方法能把這個前緣推多遠來比較方法。
- **結構化與非結構化**：非結構化方法移除個別數值，留下不規則的稀疏性；結構化方法移除整個通道、注意力頭或區塊，密集硬體可以直接利用。
- **硬體相依**：90% 稀疏的矩陣只有在硬體與軟體能跳過零值時才會變快。參數減少與延遲降低是不同的數字。
- **校準資料**：訓練後方法用一小批輸入估計統計量，其大小與和部署資料的相似度都會影響結果。
- **組合使用**：多種方法可以合併。Han 等人（2016）把剪枝、量化與熵編碼串成同一條流程。

## 運作方式

大多數方法都遵循同一個循環：評估模型每個部分的重要性，移除或捨入最不重要的部分，然後修補造成的損傷。修補步驟是區分能在高壓縮率下運作的方法與無法運作的方法的關鍵。它可能是用標記資料微調、在一小批校準資料上重建每層的輸出，或直接從原始模型進行蒸餾。

### 低秩分解

截斷 SVD、低秩濾波器展開與 LoRA 的方法頁面，都在[低秩分解與高效架構](low-rank-and-efficient-architectures/index.zh-TW.md)之下。

權重矩陣 \(W \in \mathbb{R}^{m \times n}\) 可以用兩個較細矩陣的乘積來近似，即 \(W \approx UV\)，其中 \(U \in \mathbb{R}^{m \times r}\)、\(V \in \mathbb{R}^{r \times n}\)。截斷的奇異值分解給出弗羅貝尼烏斯範數下最好的秩 \(r\) 近似。參數數量從 \(mn\) 降到 \(r(m+n)\)，只要 \(r\) 相對於維度夠小，就能節省空間。

低秩壓縮只在矩陣接近低秩時有效。許多訓練後的層確實如此，但對最重要的層來說，近似誤差可能迅速增大。低秩適應（LoRA）在微調時使用相同的數學，學習凍結權重上的小型更新 \(BA\)。LoRA 並不壓縮基礎模型，相關內容見[訓練與微調](../../engineering/training/index.zh-TW.md)。

### 高效架構

有些模型從一開始就設計成小型。MobileNet 以深度可分離卷積取代標準卷積。多查詢與分組查詢注意力讓多個注意力頭共享鍵與值，以縮小 [KV 快取](../../theory/models/transformer/kv-cache/index.zh-TW.md)。專家混合層保持總參數量龐大，但每個 token 只啟用少數專家。這些屬於架構選擇，因此放在[模型](../models/index.zh-TW.md)下的各個架構家族中。

## 組合式流程

方法常常會組合在同一條流程中。[深度壓縮](deep-compression/index.zh-TW.md)串接了剪枝、碼本量化與霍夫曼編碼，其頁面說明各階段、儲存空間的結果與其限制。

## 相關連結

壓縮與 [MLOps 與部署](../../engineering/mlops/index.zh-TW.md)相關，服務成本與量化模型在實務上在那裡決定；也與 [AI 硬體](../../engineering/hardware/index.zh-TW.md)相關，因為晶片支援的精度格式與稀疏模式，決定了哪些方法值得使用。[KV 快取](../../theory/models/transformer/kv-cache/index.zh-TW.md)也會用到許多相同的想法。

大腦提供了一個類比。發育中的神經系統先產生比保留下來還多的突觸，接著消除許多突觸；大腦運作所用的元件也有雜訊且精度低。這些事實是否能解釋生物運算為何有效率，仍是開放問題；見[神經科學](../../brain-mind/neuroscience/index.zh-TW.md)，以及[資訊理論](../../theory/information-theory/index.zh-TW.md)中的高效編碼觀點。

## 應用

- **裝置端模型**：量化後的語言與視覺模型可在筆電與手機上執行，這些裝置的記憶體與電力都有限。
- **大規模服務**：供應商透過低位元權重、稀疏核心與簡單請求改用蒸餾模型，以較低成本服務大型模型。
- **嵌入式與機器人系統**：感知模型在車輛與無人機的電力與延遲預算內運作。
- **科學計算**：替代模型經過壓縮，使模擬能在一般硬體上執行。

## 開放問題

- **超越困惑度的評估**：壓縮後的模型可能保住困惑度，卻失去推理、長脈絡檢索或校準能力。能衡量這些能力的基準仍然有限。
- **推理模型的壓縮**：長串推理在量化或剪枝後能保留多少，目前衡量不足。
- **方法組合**：量化、剪枝與蒸餾的最佳順序與交互作用，大多仍靠經驗。
- **硬體支援**：非結構化稀疏能大幅減少參數，但在現有加速器上幾乎無法加速。

## 參考文獻

### 開創性論文

- Han, S., Mao, H., Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR. https://arxiv.org/abs/1510.00149 — 結合剪枝、碼本量化與霍夫曼編碼，報告儲存空間減少 35 至 49 倍。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 提出以大模型的軟輸出訓練小模型。
- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 量化感知訓練與純整數推論，是許多部署流程的基礎。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 涵蓋訓練與推論稀疏化方法的廣泛綜述。
- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧精度降低方法及其取捨。
- Gou, J., 等人 (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 依知識類型、訓練方式與應用綜述知識蒸餾。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 顯示在大型任務上，簡單的量值剪枝與更複雜的稀疏方法相當或更好。
- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS. https://arxiv.org/abs/2208.07339 — 大型語言模型的混合精度 8 位元推論，詳見量化頁。
