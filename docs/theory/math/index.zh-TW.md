# 數學基礎

AI 用到的數學主要有五塊。這頁說明每塊「用在哪裡」與「最少要懂什麼」。

## 1. 線性代數

> 詳細頁面：[AI 所需的線性代數](linear-algebra/index.md)，包含[奇異值分解](linear-algebra/svd.md)與[特徵值分解](linear-algebra/eigendecomposition.md)。


**用在哪裡**：資料就是向量與矩陣；神經網路每一層是矩陣乘法加非線性；嵌入（embedding）是向量空間中的點；注意力是向量內積。

**最少要懂**：

- 向量、矩陣、張量；矩陣乘法的形狀規則
- 內積與餘弦相似度：\( \cos\theta = \frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\|\mathbf{b}\|} \)（語意搜尋的基礎）
- 線性轉換、秩、基底
- 特徵值分解與奇異值分解（SVD）：PCA、LoRA 的低秩概念
- 範數（L1、L2）：正規化

## 2. 微積分

> 詳細頁面：[微積分與最佳化基礎](calculus/index.md)，包含[牛頓法](calculus/newtons-method.md)與[拉格朗日乘數法](calculus/lagrange-multipliers.md)。


**用在哪裡**：訓練＝最小化損失函數，需要梯度。

**最少要懂**：

- 偏微分與梯度 \( \nabla_\theta L \)
- 連鎖律（反向傳播就是系統性地套用連鎖律）
- 雅可比矩陣與海森矩陣的概念
- 泰勒展開（理解最佳化器與曲率）

\[
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y}\cdot\frac{\partial y}{\partial z}\cdot\frac{\partial z}{\partial w}
\]

## 3. 機率與統計

> 詳細頁面：[AI 所需的機率與統計](probability-statistics/index.md)，包含[最大概似估計](probability-statistics/maximum-likelihood.md)與[最大後驗估計](probability-statistics/maximum-a-posteriori.md)。


**用在哪裡**：模型輸出機率分布；語言模型就是 \( p(x_t \mid x_{<t}) \)；不確定性估計；評估時的信賴區間與顯著性檢定。

**最少要懂**：

- 條件機率、貝氏定理 \( p(\theta\mid D) = \frac{p(D\mid\theta)p(\theta)}{p(D)} \)
- 常見分布：伯努利、類別、高斯、泊松
- 期望值、變異數、共變異數
- 最大概似估計（MLE）與最大後驗估計（MAP）
- 抽樣、蒙地卡羅方法
- 假設檢定、bootstrap（評估模型差異是否顯著）

## 4. 資訊理論

**用在哪裡**：交叉熵損失、KL 散度（VAE、RLHF 的 KL 懲罰、知識蒸餾）、困惑度（perplexity）、互資訊（表徵學習、神經編碼）。

| 量 | 定義 | 直覺 |
|---|---|---|
| 熵 | \( H(p) = -\sum p(x)\log p(x) \) | 平均驚訝程度 |
| 交叉熵 | \( H(p,q) = -\sum p(x)\log q(x) \) | 用 q 編碼 p 的成本，分類損失 |
| KL 散度 | \( D_{KL}(p\|q) = \sum p\log\frac{p}{q} \) | 兩個分布的差距（不對稱） |
| 互資訊 | \( I(X;Y) = H(X) - H(X\mid Y) \) | 知道 Y 後對 X 的不確定性減少多少 |
| 困惑度 | \( \exp(H) \) | 語言模型平均在幾個選項間猶豫 |

資訊理論也是神經科學的重要工具：**有效編碼假說**（Barlow, 1961）認為感覺神經元的反應會最大化資訊傳遞並減少冗餘，這與稀疏編碼、自監督學習的目標高度相關。

## 5. 最佳化

**用在哪裡**：所有訓練都是最佳化問題。

- 梯度下降：\( \theta \leftarrow \theta - \eta\nabla_\theta L \)
- 隨機梯度下降（SGD）與小批次
- 動量、Adam、AdamW（現今最常用）
- 學習率排程：warmup、cosine decay
- 凸與非凸：深度網路的損失面非凸，但實務上 SGD 能找到泛化良好的解
- 約束最佳化與拉格朗日乘數（SVM、RLHF 的 KL 約束）

## 6. 其他常見工具

- **圖論**：知識圖譜、GNN、神經連結體（connectome）
- **動力系統**：RNN、神經元模型、擴散模型的 SDE/ODE 觀點
- **賽局論**：GAN、多代理人、機制設計
- **數值方法**：浮點精度（FP32/BF16/FP8）、數值穩定（log-sum-exp）

## 學習資源

- [Mathematics for Machine Learning](https://mml-book.github.io/)（免費 PDF）
- 3Blue1Brown《線性代數的本質》《微積分的本質》《神經網路》系列影片
- [d2l-zh 附錄：深度學習的數學](https://zh.d2l.ai/chapter_appendix-mathematics-for-deep-learning/index.html)
- MIT 18.06（Gilbert Strang 線性代數）
