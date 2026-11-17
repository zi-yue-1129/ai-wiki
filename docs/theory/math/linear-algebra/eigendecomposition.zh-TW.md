---
translation_reviewed: 2026-11-17
---

# 特徵值分解

特徵值分解把方陣寫成其特徵向量與特徵值的形式。對稱矩陣的特徵向量彼此正交，特徵值為實數，因此此分解常用於共變異數矩陣與損失函數的海森矩陣。本頁是[線性代數](index.md)的一部分。

## 概述

方陣 \(A\) 的特徵向量是非零向量 \(\mathbf{v}\)，\(A\) 作用後方向不變：\(A\mathbf{v} = \lambda \mathbf{v}\)。純量 \(\lambda\) 為特徵值，即 \(A\) 沿該方向拉伸的倍數。沿特徵向量方向，矩陣只做簡單的縮放，因此重複作用很容易分析：\(A^k\mathbf{v} = \lambda^k\mathbf{v}\)。

## 關鍵概念

- **特徵對**：特徵值與其對應的特徵向量。
- **譜定理**：實對稱矩陣的特徵值皆為實數，且有一組標準正交的特徵向量。
- **半正定矩陣**：所有特徵值皆非負的對稱矩陣。共變異數矩陣即屬此類。
- **譜半徑**：特徵值絕對值的最大值。矩陣重複相乘時，增長或衰減取決於譜半徑大於或小於一。

## 運作方式

對實對稱 \(n\times n\) 矩陣，譜定理給出

\[
A = Q\Lambda Q^\top, \qquad \Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n),
\]

其中正交矩陣 \(Q\) 的各欄為特徵向量。二次型因此沿特徵方向分解：

\[
\mathbf{x}^\top A \mathbf{x} = \sum_{i} \lambda_i \, (\mathbf{q}_i^\top \mathbf{x})^2 .
\]

因此每個特徵值就是該二次函數在其自身方向上的曲率。這是海森矩陣的特徵值對最佳化很重要的原因：大的特徵值標示陡峭方向，小的則標示平坦方向（見[微積分與最佳化](../calculus/index.md)）。

求主特徵向量的一個標準方法是冪迭代，即反覆套用 \(A\) 並正規化結果。當主特徵值與其他特徵值有明顯間隔時，它會收斂到絕對值最大特徵值所對應的特徵向量（見 [Golub 與 Van Loan](index.md)）。

### 動態範例：冪迭代逐步靠近主特徵向量

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/power-iteration-convergence-still.svg" data-motion-src="../../../assets/concept-animations/power-iteration-convergence-motion.svg" data-still-src="../../../assets/concept-animations/power-iteration-convergence-still.svg" alt="對稱矩陣反覆作用於向量，經正規化後逐步靠近最大特徵值所對應的特徵向量，右側角度誤差逐輪縮小。" style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub 可讀的冪迭代靜態預覽](../../../assets/concept-animations/power-iteration-convergence-still.svg)


設定**人工合成的正定矩陣** $A=Q\operatorname{diag}(3,1)Q^\top$，其中 $Q=R(25^\circ)$。初始單位向量 $x_0$ 位於 97°，與主特徵向量 $q_1$ 相差 **72°**。每次先計算 $Ax_k$（橘色箭頭會暫時伸長），再依 $x_{k+1}=Ax_k/\|Ax_k\|_2$ 正規化。角度誤差遵循 $\tan\delta_k=\tan(72^\circ)/3^k$；前五次更新後，誤差依序約為 **45.7°、18.9°、6.5°、2.2°、0.7°**。右側長條的長度與這些角度誤差成正比，並非訓練損失。只有箭頭停留在正規化迭代點時，對應列才會反白；標示「套用矩陣／正規化」的過渡期間不顯示列框。到達 $x_5$ 後，循環重設為 $x_0$。

此收斂需要起始向量在唯一、絕對值最大的特徵值所對應方向具有非零分量；條件不成立時，結果可能不同。動畫中連接精確迭代點的過渡影格只是幾何示意，**不代表額外計算步驟或實測執行時間**。MkDocs 提供**播放／暫停**控制；GitHub 可直接查看靜態版本。窄螢幕可以水平捲動。原創圖像，**CC BY-SA 4.0**。


### 動態範例：對稱映射保留特徵方向

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/eigen-linear-map-still.svg" data-motion-src="../../../assets/concept-animations/eigen-linear-map-motion.svg" data-still-src="../../../assets/concept-animations/eigen-linear-map-still.svg" alt="橘色單位向量沿圓周轉動，青綠色轉換結果沿橢圓移動；兩條特徵方向在映射後保持固定。" style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub 可讀的特徵方向靜態預覽](../../../assets/concept-animations/eigen-linear-map-still.svg)

考慮**人工合成的對稱矩陣** \(A=Q\operatorname{diag}(3,1)Q^\top\)，其中 \(Q=R(35^\circ)\)。對正交特徵向量 \(\mathbf q_1,\mathbf q_2\)，

\[
\mathbf x(\theta)=\cos\theta\,\mathbf q_1+\sin\theta\,\mathbf q_2,\qquad
A\mathbf x(\theta)=3\cos\theta\,\mathbf q_1+\sin\theta\,\mathbf q_2.
\]

輸入端點沿圓周移動，輸出端點則描繪橢圓。\(\theta=0\) 時，\(\mathbf q_1\) 分量放大三倍；\(\theta=90^\circ\) 時，\(\mathbf q_2\) 分量保持不變。一般方向的輸入與輸出不一定共線。**左右圖面採不同繪圖尺度**，應比較各圖內的形狀與方向，而非跨圖箭頭的絕對長度。角度掃描只是幾何示範，**不是迭代求解或模型訓練**。原創圖，**CC BY-SA 4.0**。

### 動態反例：實數旋轉矩陣未必有實特徵向量

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/eigen-rotation-no-real-still.svg" data-motion-src="../../../assets/concept-animations/eigen-rotation-no-real-motion.svg" data-still-src="../../../assets/concept-animations/eigen-rotation-no-real-still.svg" alt="相鄰兩次迭代的實向量相差九十度，右側軌跡的標記依序走過四個方向並回到起點。" style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub 可讀的旋轉軌跡靜態預覽](../../../assets/concept-animations/eigen-rotation-no-real-still.svg)

旋轉矩陣 \(R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}\) 將每個非零**實向量**映射到與原向量正交的方向。橘色箭頭代表 \(\mathbf x_{k-1}\)，青綠色箭頭代表 \(\mathbf x_k=R\mathbf x_{k-1}\)；右側標記顯示模 4 的離散迭代狀態。四次矩陣乘法後，\(R^4\mathbf x_0=\mathbf x_0\)。因為對任意實向量皆有 \(\mathbf x^\top R\mathbf x=0\)，而 \(R\) 可逆，因此不存在非零**實**特徵向量。其特徵值 \(\pm i\) 位於**複數域**，與要求矩陣**對稱**的譜定理不矛盾。兩個離散轉向之間的平滑畫面僅為*視覺插值*，**不代表額外的矩陣乘法**。原創圖，**CC BY-SA 4.0**。

兩組範例皆可在 MkDocs 使用**播放／暫停**控制；GitHub 直接顯示靜態 SVG。偏好減少動態時播放器預設暫停。手機可將焦點移到圖面區域，利用方向鍵水平捲動。

## 主要方法

特徵值分解是線性代數中兩個代表性的矩陣分解之一，另一個是奇異值分解。

- [奇異值分解](svd.md)：適用於任意矩陣。對半正定對稱矩陣，其奇異值等於特徵值，兩種分解在此一致。

方陣且對稱時（如共變異數矩陣或海森矩陣）使用特徵值分解；資料或權重矩陣為非方陣時使用奇異值分解。

## 與其他頁面的連結

- [主成分分析](../../paradigms/unsupervised/dimensionality-reduction/pca.md)以共變異數矩陣的特徵向量作為主方向，各方向上的變異數即對應的特徵值。
- [機率與統計](../probability-statistics/index.md)中多元高斯分布的共變異數矩陣，即以此方式對角化。
- [微積分與最佳化](../calculus/index.md)以海森矩陣及其特徵值描述損失函數的局部形狀。

## 應用

- **主成分分析**：資料集的主成分即其共變異數矩陣的特徵向量（Bishop, 2006 涵蓋 PCA）。
- **曲率與條件數**：海森矩陣最大與最小特徵值之比，說明一個二次目標用梯度下降解有多困難（Boyd & Vandenberghe, 2004）。
- **穩定性分析**：線性動力系統會衰減或增長，取決於其矩陣的特徵值。

## 開放問題

- 對非常大的矩陣（例如大型網路的海森矩陣）計算特徵值分解成本高昂，實用方法依賴近似，而其精確度難以保證。
- 非對稱矩陣的特徵值可能為複數或病態，因此其特徵值分解比對稱矩陣可靠度低。

## 參考文獻

### 奠基性論文

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 以共變異數矩陣的特徵向量定義 PCA 的教科書說明。

### 綜述與教科書

- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — 涵蓋對稱特徵值問題與冪迭代。
- Trefethen, L. N. & Bau, D. (1997). *Numerical Linear Algebra*. SIAM. https://people.maths.ox.ac.uk/trefethen/text.html — 研究所教材，涵蓋特徵值問題及其數值行為。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋 PCA 及其所對角化的共變異數矩陣。

### 講義

- Strang, G., *18.06 Linear Algebra*, MIT. https://web.mit.edu/18.06/www/ — 課程講次包含特徵值與特徵向量，之後是對角化。

### 文章與文件

- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — 免費線上教材；涵蓋海森矩陣特徵值所參與的二階條件，以及二次問題的條件數。
