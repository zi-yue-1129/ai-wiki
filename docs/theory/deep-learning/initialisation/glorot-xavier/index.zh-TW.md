---
translation_reviewed: 2026-10-28
---

# Xavier（Glorot）初始化

Xavier 初始化，或稱 Glorot 初始化，將每個權重矩陣的變異數設為 \(2/(n_{\text{in}}+n_{\text{out}})\)，使前向傳遞的訊號與反向傳遞的梯度，在深層網路中都保持相近的尺度。Glorot 與 Bengio 於 2010 年提出此方法，當時他們正在研究為何從隨機起點訓練的深層網路學習得如此緩慢。它是上層[權重初始化](../index.md)頁面中所比較的方法之一。

## 概述

在 2010 年，深層前饋網路很難從隨機權重開始訓練。Glorot 與 Bengio 追問，為何從隨機初始化出發的標準梯度下降表現得如此糟糕。他們用多種激活函數訓練深層網路，並在訓練過程中監測每一層的激活值與梯度。

他們的主要觀察與 logistic sigmoid 有關。它的平均輸出為正，這會使頂層隱藏層在訓練初期就趨向飽和，而飽和的單元學習得很慢。他們的分析導出一條初始權重尺度的規則，使各層激活值與梯度的變異數大致保持恆定。論文稱之為標準化初始化，現在通常稱為 Xavier 或 Glorot 初始化。

## 關鍵概念

- **扇入與扇出。** 對於稠密層，\(n_{\text{in}}\) 是每個單元的輸入數，\(n_{\text{out}}\) 是該層所餵入的單元數。在論文中，第 \(i\) 層的兩者為 \(n_i\) 與 \(n_{i+1}\)。
- **線性區。** 推導假設在初始化時網路近似為線性，激活函數在零點的導數為一，且輸入與權重彼此獨立。
- **飽和。** sigmoid 或 tanh 單元的輸入很大時，其輸出是平的，梯度接近零。

## 運作方式

在上述線性假設下，一層的預激活值變異數為 \(n\,\mathrm{Var}[W]\,\mathrm{Var}[x]\)。前向條件 \(n_i\mathrm{Var}[W^i] = 1\) 使激活值的變異數在層與層之間保持恆定，反向條件 \(n_{i+1}\mathrm{Var}[W^i] = 1\) 則使梯度的變異數保持恆定。只有在寬度相等時兩個條件才能同時成立，因此作者取兩者的平均：

\[
\mathrm{Var}[W^i] = \frac{2}{n_i + n_{i+1}}.
\]

論文使用具有此變異數的均勻分布，因為在 \([-a, a]\) 上的均勻分布，其變異數為 \(a^2/3\)：

\[
W^i \sim U\left[-\sqrt{\frac{6}{n_i + n_{i+1}}},\; +\sqrt{\frac{6}{n_i + n_{i+1}}}\right]。
\]

程序是從此分布抽取每一層的權重，並將偏置設為零。論文用來比較的標準方案 \(U[-1/\sqrt{n}, 1/\sqrt{n}]\)，在寬的層中其前向增益只有所需數值的三分之一，因此訊號會隨深度縮小。

## 結果

論文的主要證據來自五個隱藏層的全連接網路，訓練資料包括 Shapeset-3×2、MNIST、CIFAR-10 與 ImageNet。對於 tanh 單元，論文表 1 顯示，使用標準化初始化後，測試誤差從 Shapeset-3×2 的 27.15 降至 15.60，從 CIFAR-10 的 55.9 降至 52.92，並從 ImageNet 的 70.58 降至 68.57。論文認為此方案對 tanh 網路相當有幫助。softsign 網路對初始化方式較為穩健，作者認為這是因為其非線性較為平緩。這些數字來自論文本身，此處未重新計算。

## 限制

- **推導是近似的。** 它依賴線性區與獨立性假設，這些假設只在初始化時大致成立，論文並未主張它們在訓練過程中持續成立。
- **它與激活函數綁定。** 整流單元會把一半的輸入歸零，因此不是對稱且零點斜率為一的函數。前向訊號在每一層會損失約一半的二階矩，規則在變異數上因此差了兩倍。[He 初始化](../he-initialisation/index.md)對此作了修正。
- **各層寬度不同。** 只有在寬度相等時兩個條件才能同時成立，因此寬度不同時，折衷方案只是一種經驗法則。
- **未處理殘差路徑與注意力。** 分析針對的是普通的前饋堆疊。殘差網路請見[上層頁面](../index.md)。
- **超參數不能遷移。** 此規則固定的是某一寬度下的起始尺度，並未說明網路變寬時學習率應如何改變。見 [muP](../mup/index.md)。

## 開放問題

- 前向與反向條件之間的折衷，是否適用於形狀差異很大的各層，或應依任務加以調整。
- 此規則如何與 Adam 等自適應最佳化器互動。這些最佳化器會為每個參數重新縮放更新量，可能降低對起始尺度的敏感度。論文的實驗使用的是普通的隨機梯度下降。
- 線性分析對於使用殘差連接與正規化的極深網路，預測能力如何。

## 參考文獻

### 開創性論文

- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — 提出變異數為 \(2/(n_i+n_{i+1})\) 的標準化初始化，依據是讓激活值與梯度的變異數保持恆定。
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — 針對整流單元修正 Xavier 的推導，並顯示 30 層網路在 Xavier 停滯的情況下，可用新方案訓練。

### 文章與文件

- Pennington, J., Schoenholz, S. S. & Ganguli, S. (2017). *Resurrecting the sigmoid in deep learning through dynamical isometry: theory and practice*. arXiv. https://arxiv.org/abs/1711.04735 — 將分析延伸到非線性網路，並顯示哪些激活函數與初始化能使雅可比的所有奇異值都接近一。
- Mishkin, D. & Matas, J. (2015). *All you need is a good init*. arXiv. https://arxiv.org/abs/1511.06422 — 提出一種依資料而定的替代方法：先以正交矩陣初始化每一層，再正規化其輸出的變異數。
- Schoenholz, S. S., Gilmer, J., Ganguli, S. & Sohl-Dickstein, J. (2017). *Deep Information Propagation*. arXiv. https://arxiv.org/abs/1611.01232 — 以平均場理論找出在初始化時限制訊號於隨機網路中傳遞距離的深度尺度。
