---
translation_reviewed: 2026-10-28
---

# 自適應方法

自適應方法為每個參數提供各自的步長。接收到較大或較頻繁梯度的參數會走較小的步，較少更新的參數則走較大的步。今日用來訓練大型神經網路的最佳化器，大多屬於這個家族。本頁說明其共通概念與最知名的成員。[概述](../index.md)說明這些方法在各最佳化家族中的位置。

## 概述

普通 SGD 對所有參數使用同一個學習率 \(\eta\)。實際網路中各參數的尺度差異很大：每個批次只出現一次的嵌入列、正規化層的增益，以及注意力權重所見的梯度，可能相差好幾個數量級。這時 \(\eta\) 必須小到足以應付最大的梯度，使其他參數的進展變慢。

自適應方法會保存梯度的移動統計量，並以逐參數的尺度去除每次更新。這個尺度通常是近期梯度的均方根，因此每個座標的更新量大致是單位大小。

## 核心概念

- **二階矩估計**：平方梯度的移動平均 \(v_t\)，用來衡量每個參數的梯度曾經有多大。
- **一階矩估計**：梯度的移動平均 \(m_t\)，作為動量使用。
- **偏差校正**：移動平均從零開始，因此早期估計偏小。除以 \(1-\beta^t\) 可以修正。
- **\(\epsilon\)**：防止除以零的小常數。它的值影響梯度極小時的行為。
- **解耦權重衰減**：把衰減直接作用在參數上，置於自適應步驟之外（見下文）。

## 運作方式

Adam 結合了動量項與逐參數尺度：

\[
\begin{aligned}
m_t &= \beta_1 m_{t-1} + (1-\beta_1)\, g_t \\
v_t &= \beta_2 v_{t-1} + (1-\beta_2)\, g_t^2 \\
\theta_t &= \theta_{t-1} - \eta\, \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
\end{aligned}
\]

其中 \(\hat m_t = m_t/(1-\beta_1^t)\)，\(\hat v_t = v_t/(1-\beta_2^t)\)。典型值為 \(\beta_1 \approx 0.9\)、\(\beta_2 \approx 0.999\)。

由於每個座標都被縮放，每個方向的更新量大致以 \(\eta\) 為上限。這使 Adam 對梯度尺度較不敏感，但 \(v_t\) 變動時有效學習率也會隨時間改變，這也是學習率排程重要的原因之一。

## 變體

| 方法 | 想法 | 狀態 |
|---|---|---|
| AdaGrad | 累加所有過去的平方梯度；適合稀疏特徵 | 規劃中 |
| RMSProp | 以平方梯度的指數移動平均取代總和 | 規劃中 |
| Adam | 動量加上自適應尺度，並做偏差校正 | 本頁 |
| AdamW | 具解耦權重衰減的 Adam | 本頁 |
| LARS、LAMB | 依權重範數逐層縮放步長，用於極大批次 | 規劃中 |
| Adafactor | 以因式分解的二階矩估計節省記憶體 | 規劃中 |
| Lion | 以動量的符號作為更新；記憶體比 Adam 少 | 規劃中 |
| Shampoo、SOAP | 由梯度的矩陣統計量建構的預條件子 | 規劃中，見[二階方法](../second-order.md) |
| Muon | 對矩陣參數做正交化的動量更新 | 規劃中 |

## 關鍵方法

### Adam（Kingma & Ba，2014/2015）

- **問題：** 隨機梯度雜訊大且稀疏，一階方法需要仔細、針對問題調整的學習率。
- **核心想法：** 利用每個參數梯度的一階與二階矩的移動估計，為每個參數調整步長，並對初期步驟做偏差校正。
- **公式或演算法：** 即上述更新式，其中 \(\beta_1 \approx 0.9\)、\(\beta_2 \approx 0.999\)，\(\epsilon\) 為小常數。
- **結果：** 摘要描述此方法在實務上表現良好，且優於其他隨機最佳化器。摘要中沒有基準測試數字，實驗結果見論文正文。
- **限制：** 論文的收斂分析是在線上凸最佳化框架下進行，而非針對深度網路。在某些影像任務上，Adam 的泛化能力可能比帶動量的 SGD 差；其逐參數縮放也與 L2 正則化相互干擾（見 AdamW）。

### AdamW（Loshchilov & Hutter，2017/2019）

- **問題：** 對自適應方法而言，在損失中加上 L2 懲罰項並不等同於權重衰減。懲罰項會被自適應分母重新縮放，因此梯度較大的參數其正則化效果會減弱。
- **核心想法：** 把權重衰減直接作用在參數上，置於自適應步驟之外，使衰減係數與梯度縮放脫鉤。
- **公式或演算法：** \(\theta_t = \theta_{t-1} - \eta\big(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda\,\theta_{t-1}\big)\)。
- **結果：** 摘要指出，脫鉤後的衰減能大幅改善 Adam 的泛化能力，使其在影像分類上能與帶動量的 SGD 競爭。摘要中未給出具體數字。
- **限制：** 衰減係數與學習率仍會互相影響，且此效益主要是在影像分類上回報的。AdamW 如今常用於 Transformer 模型，但在其他任務上的優勢仍取決於調校。

## 關聯

- [SGD 與動量](../sgd-and-momentum.md)是這些方法比較的非自適應基準。
- [損失函數與最佳化](../../paradigms/supervised/loss-functions-and-optimization/index.md)說明作為正則化項的權重衰減。
- [數學](../../math/index.md)提供矩估計與凸性的背景。

## 應用

- Adam 與 AdamW 常用於訓練 Transformer 與其他大型網路。
- 當最佳化器狀態太大而無法完整保存時，會使用 Adafactor 等省記憶體的變體。

## 開放問題

- 自適應方法為何有時泛化比帶動量的 SGD 差？調校何時能縮小差距？
- 在極大批次大小下，哪種逐參數縮放規則最好？

## 參考文獻

### 開創性論文

- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR. https://arxiv.org/abs/1412.6980 — 提出 Adam，一種利用梯度偏差校正矩估計的自適應方法。
- Loshchilov, I. & Hutter, F. (2019). Decoupled Weight Decay Regularization. ICLR. https://arxiv.org/abs/1711.05101 — 指出 L2 正則化與權重衰減在 Adam 下不同，並提出 AdamW。
- Duchi, J., Hazan, E. & Singer, Y. (2011). Adaptive Subgradient Methods for Online Learning and Stochastic Optimization. *JMLR*. https://jmlr.org/papers/v12/duchi11a.html — 提出 AdaGrad，依每個座標累積的平方梯度縮放步長。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — 隨機梯度方法綜述，包含自適應變體，以及它們在大型資料集上的取捨。

### 文章與文件

- PyTorch 文件，*torch.optim*。https://pytorch.org/docs/stable/optim.html — Adam、AdamW 等最佳化器的參考實作與其確切更新規則。
