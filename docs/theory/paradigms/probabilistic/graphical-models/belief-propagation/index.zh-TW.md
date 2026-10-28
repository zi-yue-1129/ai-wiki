---
translation_reviewed: 2026-10-28
---

# 信念傳播

信念傳播（belief propagation, BP），又稱和積演算法（sum-product algorithm），透過在相鄰節點之間傳遞訊息，計算圖模型中的邊際機率。在樹上，它給出精確的邊際分布；在有迴路的圖上，它給出的近似往往效果良好。它是[機率圖模型](../index.md)的核心方法之一。

## 概述

若要計算單一邊際分布，直接的做法是對其他變數的每個配置求和，成本隨變數數目呈指數成長。信念傳播則利用圖的結構：每個節點把自己從其他鄰居學到的摘要，送給每個鄰居。在樹上，只需兩次遍歷（從葉到根，再返回），每個邊際分布都是精確的。

把同樣的更新套用到有迴路的圖上，就得到循環信念傳播（loopy belief propagation），它沒有收斂或正確性的一般保證。Kschischang 等人（2001）在因子圖上給出統一的描述，Kschischang 與 Frey（1998）則把複合碼的迭代解碼與圖上的機率傳播連結起來。Wainwright 與 Jordan（2008）把這個演算法置於變分框架之中，因此它與[變分推論](../../variational-inference/index.md)相連。

## 核心概念

- **訊息** \(m_{i \to j}\)：節點 \(i\) 告訴鄰居 \(j\) 關於其變數的資訊，摘要了它從其他鄰居學到的內容。
- **信念**：變數的（近似）邊際分布，與其各因子傳入的所有訊息之乘積成正比。
- **和積與最大積**：和積計算邊際分布。把求和換成求最大值，就得到最大積，它計算最可能的整體配置（MAP）。

## 運作方式

在因子圖上，設變數為 \(x\)、因子為 \(f\)，訊息為

\[
m_{x \to f}(x) = \prod_{g \in N(x)\setminus f} m_{g \to x}(x), \qquad
m_{f \to x}(x) = \sum_{x_f \setminus x} f(x_f)\prod_{y \in N(f)\setminus x} m_{y \to f}(y),
\]

其中 \(N(\cdot)\) 表示鄰居，\(x_f\) 是因子 \(f\) 的變數。變數的信念為

\[
b_x(x) \propto \prod_{f \in N(x)} m_{f \to x}(x).
\]

演算法如下：

1. 將所有訊息初始化為均勻值。
2. 依選定的排程，使用上面兩式更新訊息。
3. 當訊息的變化小於容差，或達到固定迭代次數時停止。
4. 讀取信念作為邊際分布。在樹上，經過兩次遍歷後信念即為精確值。

把每個求和換成求最大值，就得到最大積，它在樹上對 MAP 是精確的。

## 實驗結果

Murphy、Weiss 與 Jordan（2013）在四個貝氏網路上，比較循環信念與精確邊際分布，其中兩個是真實世界網路，分別是 ALARM 與 QMR。循環信念常常收斂，而且收斂時能很好地近似正確的邊際分布。在 QMR 上，它們會振盪，與正確的後驗分布沒有明顯關係，而用來防止振盪的簡單方法會得到錯誤結果。

Weiss（2000）分析了只有單一迴路的圖。他把局部傳播計算出的信念與正確的邊際分布聯繫起來，並顯示對於其中一類圖，MAP 指派是可證明最優的，但邊際分布並不正確。

## 限制

- **沒有一般的收斂保證。**在有迴路的圖上，訊息可能振盪而無法穩定（Murphy 等人，2013）。
- **重複計數。**證據可能在迴路中循環，因而被計入不止一次，使計算出的邊際分布可能有誤（Weiss，2000）。
- **因子大小。**每個訊息都要對其因子的變數求和，因此大型因子的代價很高。

## 開放問題

- 循環信念傳播在什麼條件下收斂，並給出準確的邊際分布？單迴路分析與振盪結果顯示，答案取決於圖的結構與交互作用的強度，但一般理論尚不存在。
- 大腦是否執行類似訊息傳遞的計算？Lee 與 Mumford（2003）以及 Ma 等人（2006）為皮質提出了這類計算，與[預測編碼](../../../../../brain-mind/predictive-coding/index.md)的解釋一致。目前證據尚不能決定這與其他機制孰對。
- 像[圖神經網路](../../../../models/gnn/index.md)那樣學習得到的訊息傳遞，能否在保持速度的同時修正循環信念傳播的錯誤？

## 參考文獻

### 開創性論文

- Kschischang, F. R., Frey, B. J. & Loeliger, H.-A. (2001). Factor graphs and the sum-product algorithm. *IEEE Transactions on Information Theory*. https://doi.org/10.1109/18.910572 — 提供本頁各處使用的因子圖和積訊息傳遞描述。
- Kschischang, F. R. & Frey, B. J. (1998). Iterative decoding of compound codes by probability propagation in graphical models. *IEEE Journal on Selected Areas in Communications*. https://doi.org/10.1109/49.661110 — 把圖上的機率傳播應用於複合碼的迭代解碼。
- Weiss, Y. (2000). Correctness of Local Probability Propagation in Graphical Models with Loops. *Neural Computation*. https://doi.org/10.1162/089976600300015880 — 分析在只有單一迴路的圖上，局部傳播計算的內容，以及其 MAP 指派何時最優。
- Murphy, K. P., Weiss, Y. & Jordan, M. I. (2013). *Loopy Belief Propagation for Approximate Inference: An Empirical Study*. arXiv. https://arxiv.org/abs/1301.6725 — 在四個貝氏網路上比較循環信念傳播與精確邊際分布，某些情況下收斂並給出良好近似，另一情況則出現振盪。

### 綜述與教科書

- Wainwright, M. J. & Jordan, M. I. (2008). *Graphical Models, Exponential Families, and Variational Inference*. Foundations and Trends in Machine Learning. https://doi.org/10.1561/2200000001 — 綜述，將訊息傳遞演算法置於變分推論之中。

### 文章與文件

- Lee, T. S. & Mumford, D. (2003). Hierarchical Bayesian inference in the visual cortex. *Journal of the Optical Society of America A*. https://doi.org/10.1364/JOSAA.20.001434 — 主張視覺皮質執行階層式貝氏推論，各層之間的訊號扮演訊息的角色。
- Ma, W. J., Beck, J. M., Latham, P. E. & Pouget, A. (2006). Bayesian inference with probabilistic population codes. *Nature Neuroscience*. https://doi.org/10.1038/nn1790 — 主張神經元群體能表示機率分布，因此貝氏計算可由神經群體執行。
