---
translation_reviewed: 2026-10-28
---

# 最佳化

訓練模型就是選擇參數，使損失函數變小。最佳化是執行這項搜尋的演算法集合。本 wiki 中幾乎每種方法，從線性迴歸到大型語言模型，最後都要靠最佳化器完成。

## 概述

把模型寫成 \(f_\theta\)，參數為 \(\theta\)，訓練損失是資料上的平均：\(L(\theta)=\frac{1}{N}\sum_i \ell(f_\theta(x_i), y_i)\)。學習就是尋找 \(\theta^\* = \arg\min_\theta L(\theta)\)。因為搜尋的對象是數百萬到數十億個數字，我們依賴指向「上坡」方向的梯度 \(\nabla_\theta L\)，並朝反方向移動。這套方法的效果取決於損失曲面的形狀：是否為凸函數、曲率多大，以及我們對梯度的估計有多雜訊。

這些搜尋所用的數學在[數學](../math/index.md)中，使用它的訓練流程在[深度學習](../deep-learning/index.md)中。損失與正則化的監督式學習觀點在[損失函數與最佳化](../paradigms/supervised/loss-functions-and-optimization/index.md)中。本頁討論演算法本身。

## 核心概念

- **梯度下降**：反覆更新 \(\theta \leftarrow \theta - \eta \nabla L(\theta)\)，其中 \(\eta\) 是學習率。
- **隨機梯度下降（SGD）**：用隨機抽出的小批次估計梯度，而不是用整個資料集。每一步便宜但有雜訊。
- **學習率**：步長 \(\eta\)。太大會發散，太小則進展緩慢。學習率排程會在訓練過程中調整它。
- **動量**：平均過去的梯度，使更新沿著一致的方向前進，並抑制震盪。
- **凸性**：凸函數沒有虛假的局部極小值，因此任何局部極小值都是全域極小值。神經網路的損失通常是非凸的。
- **平滑性（梯度的Lipschitz 常數）**：梯度變化速度的上界 \(L\)。它決定最大的安全步長 \(\eta \le 1/L\)。
- **條件數**：當各方向的曲率差異很大時，普通梯度下降會來回震盪。依參數逐一縮放有助於改善。
- **損失地形**：\(L(\theta)\) 在高維空間中的曲面，包含鞍點、平坦區域，以及寬窄不一的極小值。

## 運作方式

### 梯度下降與其雜訊

對於凸且 \(L\)-平滑的損失，取 \(\eta = 1/L\) 的梯度下降在 \(T\) 步後以 \(O(1/T)\) 的速率降低損失。若損失是強凸的，收斂速率為線性（幾何級數）。隨機梯度是梯度 \(\nabla L\) 的無偏估計 \(g_t\)，因此期望更新與完整梯度一致，但會增加變異。若步長遞減，雜訊會逐漸平均掉，經典的 Robbins–Monro 條件 \(\sum \eta_t = \infty\) 與 \(\sum \eta_t^2 < \infty\) 保證收斂。

雜訊不只是干擾。它能幫助最佳化器逃離尖銳的鞍點，並傾向於找到較平坦的極小值。許多研究將此與較好的泛化能力連結，不過這個連結仍有爭議。

### 動量

重球動量（Polyak，1964）保留速度 \(v_t = \beta v_{t-1} + g_t\)，並以 \(\theta \leftarrow \theta - \eta v_t\) 更新。Nesterov 的變體改在前瞻點計算梯度，而不是目前的點。訓練卷積網路時，使用 SGD 搭配動量相當普遍。

### 自適應方法

自適應方法為每個參數保留一個尺度。梯度較大的參數走較小的步，較少更新的參數則走較大的步。Adam 同時保存梯度及其平方的移動平均：

\[
\begin{aligned}
m_t &= \beta_1 m_{t-1} + (1-\beta_1)\, g_t \\
v_t &= \beta_2 v_{t-1} + (1-\beta_2)\, g_t^2 \\
\theta_t &= \theta_{t-1} - \eta\, \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
\end{aligned}
\]

其中 \(\hat m_t\) 與 \(\hat v_t\) 是經過偏差校正的 \(m_t\) 與 \(v_t\)。Adam 及其相近方法常用於訓練 Transformer，通常比 SGD 需要較少的學習率調校。下方的關鍵方法說明了它的權重衰減實作為何重要。

### 二階與擬牛頓方法

牛頓法使用 Hessian 矩陣 \(H\)，以步長 \(-H^{-1}\nabla L\) 修正曲率。對 \(d\) 個參數而言，精確的 Hessian 有 \(d^2\) 個元素，因此實務上會近似它。Shampoo 與 K-FAC 是大規模訓練中使用的例子。它們不如 Adam 常見，但會出現在超大型模型的研究中。

## 關鍵方法

### Adam（Kingma & Ba，2014/2015）

- **問題：** 隨機梯度雜訊大且稀疏，一階方法需要仔細、針對問題調整的學習率。
- **核心想法：** 利用每個參數梯度的一階與二階矩的移動估計，為每個參數調整步長，並對初期步驟做偏差校正。
- **公式或演算法：** 即上述更新式，其中 \(\beta_1 \approx 0.9\)、\(\beta_2 \approx 0.999\)，\(\epsilon\) 為小常數。論文的預設值列於演算法方框中。
- **結果：** 摘要描述此方法在實務上表現良好，且優於其他隨機最佳化器。摘要中沒有基準測試數字，實驗結果見論文正文。
- **限制：** 論文的收斂分析是在線上凸最佳化框架下進行，而非針對深度網路。在某些影像任務上，Adam 的泛化能力可能比帶動量的 SGD 差；其逐參數縮放也與 L2 正則化相互干擾（見 AdamW）。

### AdamW（Loshchilov & Hutter，2017/2019）

- **問題：** 對自適應方法而言，在損失中加上 L2 懲罰項並不等同於權重衰減。懲罰項會被自適應分母重新縮放，因此梯度較大的參數其正則化效果會減弱。
- **核心想法：** 把權重衰減直接作用在參數上，置於自適應步驟之外，使衰減係數與梯度縮放脫鉤。
- **公式或演算法：** \(\theta_t = \theta_{t-1} - \eta\big(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda\,\theta_{t-1}\big)\)。
- **結果：** 摘要指出，脫鉤後的衰減能大幅改善 Adam 的泛化能力，使其在影像分類上能與帶動量的 SGD 競爭。摘要中未給出具體數字。
- **限制：** 衰減係數與學習率仍會互相影響，且此效益主要是在影像分類上回報的。AdamW 如今是許多 Transformer 模型的預設選擇，但在其他任務上的優勢仍取決於調校。

## 關聯

- **數學：** 凸性、泰勒展開與 Hessian 是解釋方法為何有效的工具。見[數學](../math/index.md)。
- **深度學習：** 反向傳播計算 \(\nabla L\)，而最佳化器決定如何使用它。見[深度學習](../deep-learning/index.md)。
- **正則化：** 權重衰減、提早停止與雜訊注入都作用在同一個目標上，可視為對最佳化的隱含改變。見[損失函數與最佳化](../paradigms/supervised/loss-functions-and-optimization/index.md)。
- **大腦與心智：** 生物學習無法精確跟隨梯度，因此尋找局部、合理的學習規則是 [NeuroAI](../../brain-mind/neuroai/index.md) 的主要主題。精確的反向傳播需要對稱的回饋權重，而生物電路並不明顯具有這種結構。

## 應用

- 用 SGD 加動量訓練影像分類器，用 AdamW 訓練 Transformer。
- 大規模語言模型訓練中的超參數搜尋與學習率排程。
- SVM、邏輯迴歸與控制中的凸最佳化，上述收斂速率可提供理論保證。

## 開放問題

- 隨機與自適應方法為何能找到泛化良好的解，即使損失曲面有許多極小值？
- 學習率的暖身與排程，在極大批次下會如何互動？
- 二階資訊能否在數十億參數的模型規模上，以可接受的成本使用？
- 生物學習中對應的最佳化機制為何，哪些規則能以局部方式實作？

## 參考文獻

### 開創性論文

- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*. doi:10.1214/aoms/1177729586 — 提出使用遞減步長的隨機逼近，是隨機梯度下降的基礎。
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:10.1016/0041-5553(64)90137-5 — 提出重球動量，並分析其在二次問題上的加速效果。
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR. https://arxiv.org/abs/1412.6980 — 提出 Adam，一種利用梯度偏差校正矩估計的自適應方法。
- Loshchilov, I. & Hutter, F. (2019). Decoupled Weight Decay Regularization. ICLR. https://arxiv.org/abs/1711.05101 — 指出 L2 正則化與權重衰減在 Adam 下不同，並提出 AdamW。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — 針對大型資料集的隨機梯度方法綜述，並包含收斂分析。
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — 凸分析與演算法的標準教科書，作者提供免費 PDF。

### 講座與影片

- Li, H., Xu, Z., Taylor, G., Studer, C. & Goldstein, T. (2018). Visualizing the Loss Landscape of Neural Nets. NeurIPS. https://arxiv.org/abs/1712.09913 — 損失曲面的視覺化方法，說明網路設計如何改變地形幾何。

### 文章與文件

- Stanford CS231n, *Optimization* 講義。https://cs231n.github.io/optimization-1/ — 針對初學者、內容清楚且附圖的梯度下降、學習率與動量筆記。
