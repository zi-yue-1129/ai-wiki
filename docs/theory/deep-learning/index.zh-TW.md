---
translation_reviewed: 2026-10-28
---

# 深度學習

## 直覺

深度學習把**許多層可微分函數**組合起來，直接從原始資料（像素、文字、波形）學習有用的**表徵**。早期的層學習邊緣或音素，較深的層學習物件與意義。這種階層與靈長類的視覺路徑（V1 → V2 → V4 → IT）驚人地相似；見 [NeuroAI](../../brain-mind/neuroai/index.md)。

## 人工神經元

\[
y = \sigma\Big(\sum_i w_i x_i + b\Big)
\]

| 生物神經元 | 人工神經元 |
|---|---|
| 樹突接收輸入 | 輸入 \(x_i\) |
| 突觸強度 | 權重 \(w_i\) |
| 胞體整合 | 加權和 |
| 超過閾值時發出動作電位 | 非線性激活 \(\sigma\) |
| 以脈衝頻率與時序編碼 | 輸出實數（脈衝式版本：[SNN](../../brain-mind/snn-neuromorphic/index.md)） |

!!! warning "類比的限制"
    真實的樹突本身就會進行非線性運算；要模擬單一皮質錐體神經元的輸入—輸出行為，可能需要一個 5–8 層的深度網路（Beniaguev et al., 2021）。人工神經元是一種極端的抽象。

### 激活函數

| 函數 | 公式 | 說明 |
|---|---|---|
| Sigmoid | \(1/(1+e^{-x})\) | 早期的預設選擇；容易飽和 → 梯度消失 |
| Tanh | \(\tanh x\) | 以零為中心 |
| ReLU | \(\max(0,x)\) | 簡單且有效；CNN 的預設選擇 |
| GELU／SiLU | \(x\Phi(x)\) ／ \(x\sigma(x)\) | 在 Transformer 中常見 |
| SwiGLU | 門控變體 | 在現代 LLM 中常見 |

## 訓練：反向傳播與梯度下降

1. **前向傳播**：逐層計算預測值。
2. **損失**：與目標值比較（交叉熵、均方誤差）。
3. **反向傳播**：從輸出到輸入套用鏈式法則，得到每個參數的梯度。
4. **更新**：最佳化器（SGD、AdamW）沿著梯度的反方向調整參數。

![神經網路訓練動畫：前向傳播、計算損失、反向傳播梯度、更新參數。](../../assets/concept-animations/backpropagation.gif)

*神經網路單次訓練步驟的概念動畫（原創，CC BY-SA 4.0）。* 動畫依序呈現**前向傳播、損失、反向傳播、參數更新**。藍色表示前向啟動訊號，紅色表示反向梯度資訊，青綠色表示權重更新；這些僅為教學示意，並非實際模型的數值或完整架構。

!!! question "大腦會做反向傳播嗎？"
    精確的反向傳播需要對稱的回饋權重，以及分開的前向與反向階段——這在生物上不太可能。可能的替代方案包括：回饋對齊、預測編碼網路、平衡傳播、樹突誤差計算、依賴爆發的可塑性，以及前向—前向演算法（forward-forward）。見 [NeuroAI](../../brain-mind/neuroai/index.md)。

## 架構

| 架構 | 歸納偏誤 | 典型用途 | 參見 |
|---|---|---|---|
| 多層感知器 | 無特定偏誤 | 表格資料、Transformer 內部 | — |
| 卷積網路（CNN） | 局部性、平移等變性 | 影像、音訊 | [電腦視覺](../models/computer-vision/index.md) |
| 循環網路（RNN／LSTM／GRU） | 序列順序、循環狀態 | 序列、時間序列 | [NLP](../models/nlp/index.md) |
| Transformer | 全域注意力、排列等變性（加上位置） | 幾乎所有模態 | [Transformer](../models/transformer/index.md) |
| 狀態空間模型（S4、Mamba） | 線性循環，能有效處理長序列 | 長序列、音訊、基因組學 | [Transformer](../models/transformer/index.md) |
| 圖神經網路 | 圖結構、排列不變性 | 分子、社會網路 | [GNN](../models/gnn/index.md) |
| 自編碼器／VAE | 瓶頸式壓縮 | 表徵學習、生成 | [生成模型](../models/generative/index.md) |
| 擴散模型 | 迭代去噪 | 影像、影片、分子 | [生成模型](../models/generative/index.md) |

## 讓深度網路能被訓練的技巧

- **初始化**：Xavier／Glorot、He
- **正規化**：BatchNorm、LayerNorm、RMSNorm
- **殘差連接**（ResNet）：讓梯度能流經數百層
- **Dropout**、權重衰減、資料增強
- **最佳化**：AdamW、預熱加餘弦衰減、梯度裁剪
- **混合精度**：BF16／FP16／FP8
- **分散式訓練**：資料、張量與管線平行；ZeRO／FSDP

## 表徵學習與自監督

深度學習真正的威力在於**學習表徵**。近年最大的轉變是[自監督學習](../paradigms/self-supervised/index.md)：從未標註的資料中建立訓練訊號——遮罩預測（BERT、MAE）、下一個 token 預測（GPT）、對比學習（SimCLR、CLIP）、聯合嵌入預測（JEPA）。

這呼應了大腦的**預測處理**理論：皮質持續預測其輸入，並從預測誤差中學習（見[認知科學](../../brain-mind/cognitive-science/index.md)）。

## 縮放定律

Kaplan et al.（2020）與 Hoffmann et al.（2022，「Chinchilla」）發現，語言模型的損失會依參數量、資料量與運算量呈**冪次定律**下降。Chinchilla 指出，在固定的運算預算下，參數量與訓練 token 數應該同步成長（大約每個參數 20 個 token）。實務上，為了讓推論更便宜，模型往往會被訓練到遠超過這個比例。

自 2024 年起，**測試時運算的縮放**——讓模型在回答前想得更久（長思維鏈、搜尋、取樣與投票）——已成為推理能力的第二條可靠的改進軸線。

## 開放的理論問題

- 為什麼過參數化的網路能夠泛化？（隱式正規化、平坦極小值、神經正切核）
- **頓悟（grokking）**：訓練損失早已收斂之後，突然出現的泛化
- **湧現能力**：是真正的相變，還是不連續指標造成的假象？（Schaeffer et al., 2023）
- **表徵收斂**：不同的模型與模態，是否會收斂到相似的世界表徵？（Huh et al., 2024，「柏拉圖表徵假說」）

## 關鍵方法

### AlexNet（Krizhevsky、Sutskever 與 Hinton，2012）

- **問題：** 將 130 萬張高解析度的 ImageNet 影像分為 1,000 類，當時既有系統的表現遠遠不足。
- **核心想法：** 在 GPU 上訓練的大型深度卷積網路。使用非飽和神經元加速訓練，並為全連接層加入新的正則化方法以減少過擬合。
- **架構：** 五個卷積層（部分後接最大池化）與兩個全連接層，最後是 1,000 類的 softmax，約有 6,000 萬個參數。
- **結果：** 在 LSVRC-2010 測試資料上，top-1 與 top-5 錯誤率分別為 39.7% 與 18.9%，作者認為明顯優於先前的最佳結果。
- **限制：** 證據來自單一網路與 2010 年的基準資料集。訓練依賴大量的標註資料與 GPU 算力，這在當時並不普遍。

### 殘差網路（He 等人，2015）

- **問題：** 非常深的網路難以最佳化，因此增加層數反而不再有幫助。
- **核心想法：** 每個區塊學習輸入的殘差函數，並透過捷徑把輸入加回去。讓訊號原樣通過因此容易學習。
- **方程式：** 對輸入 \(x\) 的區塊，

\[
y = \mathcal{F}(x, \{W_i\}) + x
\]

- **結果：** 網路深度最多 152 層，約為 VGG 網路的八倍，且複雜度較低。這些網路組成的集成模型在 ImageNet 測試集上達到 3.57% 錯誤率，並在 ILSVRC 2015 分類任務中獲得第一名。
- **限制：** 3.57% 來自集成模型，而非單一網路。恆等捷徑是論文所主張的設計選擇，並未證明它是最佳的。

## 學習資源

- [Dive into Deep Learning](https://d2l.ai/)（CC BY-SA 4.0；強烈推薦）
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/)（免費 PDF）
- Andrej Karpathy，*Neural Networks: Zero to Hero*
- Stanford CS231n（視覺）、CS224n（NLP）
- fast.ai，*Practical Deep Learning for Coders*

## 參考文獻

### 開創性論文

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，其在 ImageNet 上的成果開啟了現代深度學習時代。
- He, K., et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — 殘差連接，使極深的網路得以訓練。
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. arXiv. https://arxiv.org/abs/1412.6980 — Adam 最佳化器，至今仍是訓練許多神經網路的預設選擇。
- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — 顯示網路可以擬合隨機標籤，挑戰了深度模型如何泛化的古典解釋。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 深度學習數學與實務的標準教科書，可免費線上閱讀。
- Zhang, A., Lipton, Z. C., Li, M. & Smola, A. J. *Dive into Deep Learning*. https://d2l.ai/ — 附有可執行程式碼的互動式線上教科書，適合實作練習。
