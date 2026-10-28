---
translation_reviewed: 2026-10-28
---

# 主成分分析

主成分分析（principal component analysis，PCA）找出一組資料變異最大的正交方向，並以各資料點沿著前幾個主要方向的座標來描述它。它是[降維](../../../paradigms/unsupervised/dimensionality-reduction/index.md)家族中的線性成員，也是[AI 的線性代數](../index.md)三個關鍵方法之一。

## 概述

許多資料集的測量特徵遠多於潛在因素。人臉、基因表現譜與數百個神經元的記錄便是例子。PCA 尋找少數新的座標軸，盡可能捕捉變異，使資料可用較少的數字描述。

Pearson（1901）提出了「與一團點最吻合的直線或平面」這一幾何概念。Hotelling（1933）以主成分之名發展出今日仍在使用的形式，並指出主成分就是協方差矩陣的特徵向量。其特徵向量彼此正交，因此各主成分互不相關。

## 核心概念

- **中心化資料**：從各欄減去平均值後的資料 $X \in \mathbb{R}^{n\times d}$。PCA 是針對中心化資料定義的。
- **協方差矩陣**：$C = \frac{1}{n}X^\top X$，是對稱的半正定矩陣，其元素為各特徵之間的協方差。
- **主成分**：使變異 $v^\top C v$ 最大、且與已找到的成分正交的單位向量 $v$。
- **解釋變異比**：對於第 $i$ 個成分，其特徵值為 $\lambda_i$，則其佔總變異的比例為 $\lambda_i / \sum_j \lambda_j$。
- **分數**：每個資料點沿前 $k$ 個成分的座標 $Z = XV_k$。

## 運作方式

第一個主成分求解

$$
v_1 = \arg\max_{\lVert v\rVert = 1} v^\top C v ,
$$

其解是 $C$ 中最大特徵值對應的特徵向量。其餘的成分依序是接下來的特徵向量。寫成 $C = V\Lambda V^\top$ 時，$V$ 的前 $k$ 行給出維度為 $k$ 的最佳線性子空間。投影到該子空間後的重建，在所有秩相同的線性映射中，平方誤差最小。這正是[截斷 SVD](../truncated-svd/index.md)的最佳性結果，套用於中心化資料。

演算法分四步：

1. 減去每個特徵的平均值。若特徵的單位不同，還需再除以標準差。
2. 計算 SVD $X = U\Sigma V^\top$。$V$ 的各行即為主方向，其變異為 $\sigma_i^2 / n$。先建立 $C$ 再做特徵分解，對病態資料較不穩定。
3. 以累積解釋變異的門檻，或下游模型的需求，選擇 $k$。
4. 計算分數 $Z = XV_k$。若要重建，則使用 $\hat X = ZV_k^\top$。

## 結果

PCA 是一個有封閉解的程序，因此其主要結果是理論性的：主方向就是特徵向量，而重建在秩相同的線性映射中是最佳的。實證證據則涉及它與其他方法的比較，以及它的實際應用。

- **人臉。** Sirovich 與 Kirby（1987）用一小組主成分表示人臉影像。Turk 與 Pentland（1991）以同樣的想法建構辨識系統：把人臉投影到由這些成分張成的特徵空間，他們稱之為特徵臉。依摘要，該系統能以接近即時的速度辨識已知的人。
- **自編碼器與 PCA。** Hinton 與 Salakhutdinov（2006）訓練了深度自編碼器，依其摘要，其編碼遠優於 PCA。非線性編碼器因此在實務上可超越線性的最優解。
- **神經群體。** Churchland 等人（2012）與 Gallego 等人（2017）以低維投影描述運動皮質的群體活動，這些投影常以類似 PCA 的方法計算。

## 限制

- **線性。** PCA 只能找出平坦的子空間。彎曲的資料流形若只用少數線性軸來表示，效果很差。
- **變異不等於相關性。** 變異最大的方向可能是雜訊，而感興趣的訊號可能位於變異較小的方向上。
- **對尺度敏感。** 單位較大的特徵會主導成分，除非先將資料標準化；而標準化會改變結果。
- **對離群值敏感。** 平方誤差使極端的點對成分有很大的影響。
- **解釋困難。** 每個成分都是所有特徵的加權混合，往往難以命名。

## 未解問題

- 哪些非線性推廣（例如核 PCA 或自編碼器）能給出既精簡又在不同資料集間穩定的表徵？
- 神經群體活動的主成分是否對應於某種計算，抑或只是記錄與前處理的副產品？
- 若目標是預測而非描述，應如何選擇成分的數目？

## 參考文獻

### 開創性論文

- Hotelling, H.（1933）. Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*. https://doi.org/10.1037/h0071325 — 把主成分定義為變異最大、彼此不相關的變數連續組合。
- Pearson, K.（1901）. LIII. On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*. https://doi.org/10.1080/14786440109462720 — 找出與一團點最吻合的直線與平面，是此方法的幾何起源。
- Sirovich, L. & Kirby, M.（1987）. Low-dimensional procedure for the characterization of human faces. *Journal of the Optical Society of America A*. https://doi.org/10.1364/JOSAA.4.000519 — 以一小組主成分表示人臉影像，是 PCA 用於人臉的早期應用。
- Turk, M. & Pentland, A.（1991）. Eigenfaces for Recognition. *Journal of Cognitive Neuroscience*. https://doi.org/10.1162/jocn.1991.3.1.71 — 描述一套人臉辨識系統，把影像投影到人臉影像的主成分（特徵臉）上。
- Hinton, G. E. & Salakhutdinov, R. R.（2006）. Reducing the Dimensionality of Data with Neural Networks. *Science*. https://doi.org/10.1126/science.1127647 — 比較深度自編碼器編碼與 PCA 的降維效果，報告自編碼器的編碼效果較佳。
- Churchland, M. M. 等人（2012）. Neural population dynamics during reaching. *Nature*. https://doi.org/10.1038/nature11129 — 以低維投影分析伸手動作期間的運動皮質群體活動，是 PCA 在神經科學中的常見用法。
