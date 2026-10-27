# 深度學習

## 直覺

深度學習用**多層可微分函數**組成的網路，從原始資料（像素、文字、聲波）自動學出有用的**表徵**。淺層學到邊緣、音素等低階特徵，深層學到物體、語意等高階概念。這種階層結構與靈長類視覺皮質（V1 → V2 → V4 → IT）有驚人的相似，見 [NeuroAI](../brain-mind/neuroai.md)。

## 人工神經元

\[
y = \sigma\Big(\sum_i w_i x_i + b\Big)
\]

| 生物神經元 | 人工神經元 |
|---|---|
| 樹突接收訊號 | 輸入 \(x_i\) |
| 突觸強度 | 權重 \(w_i\) |
| 細胞體整合 | 加權和 |
| 達閾值發出動作電位 | 非線性啟動函數 \(\sigma\) |
| 以脈衝頻率與時序編碼 | 以實數值輸出（脈衝版本見 [SNN](../brain-mind/snn-neuromorphic.md)） |

!!! warning "類比的限制"
    真實神經元的樹突本身能做非線性運算，單一皮質神經元可能需要一個 5–8 層的深度網路才能模擬（Beniaguev et al., 2021）。人工神經元是極度簡化的抽象。

### 啟動函數

| 函數 | 公式 | 特點 |
|---|---|---|
| Sigmoid | \(1/(1+e^{-x})\) | 早期常用，飽和導致梯度消失 |
| Tanh | \(\tanh x\) | 零中心 |
| ReLU | \(\max(0,x)\) | 簡單有效，現代 CNN 標配 |
| GELU / SiLU | \(x\Phi(x)\) / \(x\sigma(x)\) | Transformer 常用 |
| SwiGLU | 門控變體 | 現代 LLM（Llama 等）常用 |

## 訓練：反向傳播與梯度下降

1. **前向傳播**：輸入經過每一層算出預測。
2. **計算損失**：與正確答案比較（交叉熵、均方誤差）。
3. **反向傳播**：用連鎖律從輸出往回算每個參數的梯度。
4. **更新參數**：最佳化器（SGD、AdamW）沿負梯度方向調整。

!!! question "大腦會做反向傳播嗎？"
    標準反向傳播需要對稱的回饋權重與分離的前向／反向階段，生物上不太可能。研究中的替代方案包括：回饋對齊（feedback alignment）、預測編碼網路、平衡傳播（equilibrium propagation）、樹突誤差計算、forward-forward 演算法。詳見 [NeuroAI](../brain-mind/neuroai.md)。

## 主要架構

| 架構 | 歸納偏誤 | 典型應用 | 詳見 |
|---|---|---|---|
| 多層感知器 MLP | 無特殊結構 | 表格資料、Transformer 內部 | — |
| 卷積網路 CNN | 局部性、平移等變 | 影像、音訊 | [電腦視覺](../models/computer-vision.md) |
| 循環網路 RNN / LSTM / GRU | 時間順序、遞迴狀態 | 序列、時間序列 | [NLP](../models/nlp.md) |
| Transformer | 全域注意力、置換等變（加位置編碼） | 幾乎所有模態 | [Transformer](../models/transformer.md) |
| 狀態空間模型 SSM（S4、Mamba） | 線性遞迴、長序列高效 | 長序列、音訊、基因體 | [Transformer](../models/transformer.md) |
| 圖神經網路 GNN | 圖結構、置換不變 | 分子、社群網路 | [GNN](../models/gnn.md) |
| 自編碼器 / VAE | 瓶頸壓縮 | 表徵學習、生成 | [生成模型](../models/generative.md) |
| 擴散模型 | 逐步去噪 | 影像、影片、分子生成 | [生成模型](../models/generative.md) |

## 讓深度網路能訓練的關鍵技巧

- **好的初始化**：Xavier/Glorot、He 初始化
- **正規化層**：BatchNorm、LayerNorm、RMSNorm
- **殘差連接**：ResNet，讓梯度能直通，數百層網路可訓練
- **Dropout**、權重衰減、資料增強
- **最佳化器**：AdamW、學習率 warmup + cosine decay、梯度裁剪
- **混合精度訓練**：BF16/FP16/FP8 加速並節省記憶體
- **分散式訓練**：資料平行、張量平行、管線平行、ZeRO/FSDP

## 表徵學習與自監督

深度學習真正的威力在於**學習表徵**。近年最重要的轉變是**自監督學習**：從未標註資料本身製造學習訊號。

- **遮罩預測**：BERT 遮字、MAE 遮影像塊
- **下一個 token 預測**：GPT 系列
- **對比學習**：SimCLR、MoCo、CLIP——拉近同一物件的不同視角、推開不同物件
- **聯合嵌入預測架構（JEPA）**：在表徵空間而非像素空間預測（LeCun 提倡）

這與大腦的**預測處理**理論相呼應：大腦不斷預測感官輸入並以預測誤差更新內部模型（見 [認知科學](../brain-mind/cognitive-science.md)）。

## 縮放定律（Scaling Laws）

Kaplan et al.（2020）與 Hoffmann et al.（2022，Chinchilla）發現：語言模型的損失隨參數量、資料量、計算量呈**冪律下降**。Chinchilla 指出在固定計算預算下，參數與訓練 token 數應等比例增加（約每參數 20 個 token）。實務上，為了推論效率，許多模型會訓練遠超此比例的 token。

2024 年後出現**測試時運算縮放**：讓模型在回答前「思考」更久（長思維鏈、搜尋、多次取樣），也能穩定提升推理表現。

## 理論未解之謎

- 為何過度參數化的網路能泛化？（隱式正規化、平坦極小值、神經正切核 NTK）
- 頓悟（grokking）：訓練很久之後突然泛化
- 湧現能力（emergent abilities）：是真的相變還是評估指標造成的假象？（Schaeffer et al., 2023）
- 表徵收斂假說：不同模型、不同模態是否收斂到相似的世界表徵？（Huh et al., 2024「柏拉圖表徵假說」）

## 學習資源

- [動手學深度學習 d2l-zh](https://zh.d2l.ai/)（CC BY-SA 4.0，強烈推薦）
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/)（免費 PDF）
- Andrej Karpathy《Neural Networks: Zero to Hero》
- 李宏毅《機器學習》系列
- Stanford CS231n（視覺）、CS224n（NLP）
- fast.ai《Practical Deep Learning for Coders》
