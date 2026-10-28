---
translation_reviewed: 2026-10-28
---

# LocalGLMnet（Richman & Wüthrich 2021）

LocalGLMnet 是一種神經網路，保留廣義線性模型的加法、係數形式，但讓每個係數取決於所定價的保單。它為表格型保險資料而設計，同時要求準確度與可解釋性。它也是父頁面[保險與精算科學](../index.md)所介紹的方法之一。

## 概述

在表格資料上，深度網路的預測通常優於廣義線性模型，但其學到的結構難以閱讀，而變數選擇發生在模型內部，無法直接檢視。Richman 與 Wüthrich（2021）探討能否保留 GLM 的結構，同時仍享有表徵學習的能力。他們的答案是一種形式上接近 GLM 的架構。其係數是輸入的函數，因此模型可以讀作一個會隨保單改變的 GLM。

論文在一個具有已知非線性均值的合成迴歸問題上測試此架構，並在一個具有理賠件數的法國汽車第三者責任險（MTPL）資料集上測試。

## 關鍵概念

- **回歸注意力**：特徵 $j$ 的係數 $\hat\beta_j(x)$，取決於整個輸入向量 $x$。論文稱之為回歸注意力。
- **局部 GLM**：在任一保單的小鄰域內，模型的行為就像係數固定為該保單取值的 GLM。
- **跳躍連接**：原始特徵直接饋入輸出層，與網路的深層部分並行。
- **加法分解**：線性預測子分解為每個特徵一項，即 $\hat\beta_j(x)\,x_j$。論文將這些項與夏普利值及積分梯度相連。
- **卜瓦松偏差**：用於擬合理賠件數的損失函數，對卜瓦松模型的均值是嚴格一致的。

## 運作方式

此網路有兩個部分。前饋網路將輸入 $x$ 映射為與 $x$ 維度相同的向量 $\beta(x)$。輸出是均值的連結值，其計算方式為 $\beta(x)$ 與原始輸入的內積：

$$
g\big(\mu(x)\big) = \beta_0 + \langle \beta(x),\, x \rangle,
$$

其中 $g$ 為連結函數，$\beta_0$ 為截距，$\beta(x)$ 為學得的回歸注意力。若將 $\beta(x)$ 固定，這就是一個 GLM；因為 $\beta(x)$ 會變動，它是一個局部 GLM。

擬合程序遵循神經網路的標準做法。

1. 將每張保單的特徵輸入前饋網路，得到 $\beta(x)$。
2. 計算 $\beta(x)$ 與原始特徵 $x$ 的內積，並對件數套用對數連結。
3. 以隨機梯度下降法，在訓練資料上最小化卜瓦松偏差。
4. 使用驗證集進行提早停止，以避免過度擬合。
5. 讀出個別保單的各 $\hat\beta_j(x)$，並對特徵值作圖，檢查學得的效果是否合理。

## 結果

在合成範例中，論文將樣本外的均方誤差與已知的迴歸函數相比，由於反應變數的變異數為 1，該函數的 MSE 約為 1。[^1] GLM 的樣本外 MSE 為 1.527，僅含截距的模型為 1.792，而 LocalGLMnet 為 1.005。GLM 受限於其預測子的線性形式，而 LocalGLMnet 則趨近於真實函數。

在 MTPL 資料上，論文報告的樣本外卜瓦松偏差損失（單位為 $10^{-2}$）為：僅含截距的空模型 25.445、一般前饋網路 23.873、LocalGLMnet 23.945。簡化版的 LocalGLMnet 為 23.912。作者指出，LocalGLMnet 為了可解釋的結構而犧牲了一點預測能力。相較於空模型的差距，它與一般網路的差距很小。

[^1]: Richman 與 Wüthrich（2021）的表 1，arXiv:2107.11059。上段引用的 MTPL 損失值出自表 2。

## 限制

- **解釋是局部且近似的。** 只有在學得的注意力平滑變化的地方，才能把每個 $\hat\beta_j(x)$ 讀作係數。雜訊較大的注意力可能產生誤導。
- **犧牲了部分準確度。** 在 MTPL 資料上，可解釋模型的準確度低於一般網路，論文亦承認此點。
- **分解不等於因果。** 加法項解釋的是已擬合的模型，並不表示某特徵導致理賠。
- **評估有限。** 論文使用一個合成設定與一個保險資料集。在其他表格領域的結果，以及與現代提升樹的比較，需要另外測試。
- **訓練成本。** 神經網路需要仔細調校與提早停止，這對習慣 GLM 的實務人員來說可能並不具備。

## 未解問題

- 監理機關是否會接受學得的回歸注意力作為費率的解釋？需要哪些文件？
- 當特徵包含文字、影像或車聯網時間序列時，相對於 GLM 的優勢是否仍然成立？
- 能否把 Lindholm 等人（2022）那樣的公平性限制直接建入架構，而非事後套用？

## 參考文獻

### 開創性論文

- Richman, R. & Wüthrich, M. V. (2021). LocalGLMnet: interpretable deep learning for tabular data. arXiv. https://arxiv.org/abs/2107.11059 — 本頁介紹的架構，附合成與法國 MTPL 實驗。
- Lindholm, M. et al. (2022). A multi-task network approach for calculating discrimination-free insurance prices. arXiv. https://arxiv.org/abs/2207.02799 — 為保險價格設計、可避免代理歧視的神經網路，並可在受保護屬性資料部分缺漏時訓練。

### 綜述與教科書

- Wüthrich, M. V. & Merz, M. (2023). *Statistical Foundations of Actuarial Learning and its Applications*. Springer. https://doi.org/10.1007/978-3-031-12409-9 — 關於精算資料之 GLM 與前饋網路的教科書，論文以其設定作為基準。
- Ohlsson, E. & Johansson, B. (2010). *Non-Life Insurance Pricing with Generalized Linear Models*. Springer. https://doi.org/10.1007/978-3-642-10791-7 — LocalGLMnet 所要延伸的 GLM 實務。

### 文章與文件

- Rudin, C. (2018). Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead. arXiv. https://arxiv.org/abs/1811.10154 — 主張高風險決策應使用本身即可解釋的模型。
