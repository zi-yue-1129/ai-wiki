---
translation_reviewed: 2026-10-27
---

# 資訊理論

資訊理論由 Claude Shannon 在 1948 年奠定，提供了精確的方式來衡量一個隨機變數帶有多少不確定性，以及一個變數能告訴我們另一個變數多少資訊。它的核心量（熵、交叉熵、KL 散度與互資訊）是大多數機器學習損失函數的基礎，也是許多關於大腦如何編碼世界的假說的基礎。

## 概述

Shannon 問了一個實際的問題：要在有雜訊的通道上可靠地傳送訊息，需要多少位元？他的答案區分了兩個極限。無損壓縮不可能低於來源的熵，而可靠傳輸也不可能超過通道容量，而通道容量本身就是互資訊的最大值。

這些定義的用途遠超電話線路。一個能良好預測資料的模型，實際上就是一個壓縮器；而學習者必須決定該保留哪些資訊、捨棄哪些。資訊理論為這兩個想法提供了共同的語言。這些定義所依賴的機率背景，可參閱[數學基礎](../math/index.md)與[機率圖模型與貝氏方法](../probabilistic/index.md)。

## 核心概念

- **熵** \(H(X) = -\sum_x p(x)\log p(x)\)：\(X\) 各結果的平均「驚訝程度」。若取以 2 為底的對數，單位是位元。
- **交叉熵** \(H(p,q) = -\sum_x p(x)\log q(x)\)：當實際遵循 \(p\) 的結果，改用為 \(q\) 設計的編碼時，平均需要的碼長。
- **KL 散度** \(D_{\mathrm{KL}}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)}\)：用 \(q\) 取代 \(p\) 所多付出的代價。它不為負，只有兩個分布完全相同時才為零，而且不對稱。
- **互資訊** \(I(X;Y) = H(X) - H(X\mid Y)\)：得知 \(Y\) 之後，\(X\) 的不確定性減少了多少。當 \(X\) 與 \(Y\) 獨立時，它恰為零。
- **通道容量**：通道能攜帶的最大互資訊，透過選擇最佳的輸入分布來求得。

兩個恆等式將這些量連結起來。交叉熵可以拆成熵加上 KL 散度：

\[
H(p,q) = H(p) + D_{\mathrm{KL}}(p\,\|\,q)
\]

由於 \(H(p)\) 與模型 \(q\) 無關，最小化資料上的交叉熵，等同於最小化資料與模型之間的 KL 散度。

## 運作方式

**壓縮。** 一枚公平硬幣每次擲出需要一個位元。一枚有 90% 機率出現正面的硬幣，其熵約為 0.47 位元，因此理想編碼可以讓高機率的結果使用短碼，使每次擲硬幣的平均碼長低於半個位元。壓縮之所以有效，是因為它利用了可預測性：模型對資料掌握得越好，能達到的熵就越低。這就是為什麼**困惑度**（交叉熵平均值的指數）是[語言模型](../models/llm/index.md)的標準衡量指標。它可以理解為模型在每一步仍需在多少個等可能的選項之間權衡。

**有雜訊的通道。** 對於以機率 \(p\) 翻轉每個位元的二元對稱通道，其容量為 \(C = 1 - H(p)\)。Shannon 的通道編碼定理指出，任何低於 \(C\) 的傳輸速率都可以在任意小的錯誤率下達成。這個結果是錯誤更正碼的理論基礎。

**把學習看成編碼。** 以交叉熵為損失函數訓練的分類器，對類別輸出而言就是最大概似估計。最小化訓練集上的平均 \(-\log q_\theta(y\mid x)\)，等同於最小化經驗資料分布與模型之間的 KL 散度。這個損失函數在[損失函數頁面](../paradigms/supervised/loss-functions-and-optimization/index.md)有更詳細的說明。

變分自編碼器也用到同樣的想法。它的訓練目標包含一個重建項和一個 KL 項，後者使學到的潛在分布接近一個簡單的先驗分布，因此它出現在[生成模型](../generative/index.md)一節中。

**資訊瓶頸。** Tishby、Pereira 與 Bialek（2000）將表徵學習架構為一種權衡：把輸入 \(X\) 壓縮成一個表徵 \(T\)，同時盡可能保留關於目標 \(Y\) 的資訊。形式上，要最小化 \(I(X;T) - \beta\, I(T;Y)\)，其中 \(\beta\) 決定預測能力相對於壓縮的價值。Alemi 等人（2016）以變分界取代難以計算的項，使這個目標能以神經網路訓練。他們回報，相較於某些標準正則化方法，模型有更好的泛化能力，並且更能抵抗對抗性攻擊。

這個理論尚未定論。Saxe 等人（2019）主張，其中關於深度網路的一些核心論點在一般情況下並不成立。在他們的實驗中，觀察到的壓縮主要取決於所使用的神經非線性函數。

## 與其他主題的連結

**大腦與心智。** 資訊理論很早就進入了神經科學。Barlow（1961）提出，感覺系統應該減少輸入中的冗餘，使有限數量的神經元能攜帶盡可能多的資訊，這就是**效率編碼假說**。Linsker（1988）則提出**最大資訊保存**（infomax）原則：感知處理模型的各層，可以藉由保留關於輸入的資訊而自我組織。這兩個想法都是通往 [NeuroAI](../../brain-mind/neuroai/index.md) 的橋樑。如果大腦是一種有效率的編碼器，那麼資訊瓶頸或以預測為基礎的自監督等目標，或許能解釋其表徵為何呈現現在的樣貌。

這個假說仍有爭議。效率可能受到代謝或其他 Barlow 的理論未涵蓋的限制所塑造，而且從有限的神經紀錄中估計資訊本身就很困難。

**其他基礎。** 互資訊是[非監督學習](../paradigms/unsupervised/index.md)與[自監督學習](../paradigms/self-supervised/index.md)中特徵選擇與表徵想法的基礎。[深度學習](../deep-learning/index.md)頁面則說明如何最佳化由這些量建構的損失函數。

## 應用

- **資料壓縮與通訊。** 位元是資訊的單位，日常裝置中的壓縮與錯誤更正碼都建立在 Shannon 的極限之上。
- **機器學習損失函數。** 交叉熵用於訓練分類器與語言模型。KL 散度出現在變分模型中，也出現在使微調後的模型接近參考模型的懲罰項中。
- **模型評估。** 困惑度（交叉熵的指數）常用來比較語言模型。
- **表徵學習。** 互資訊可用來判斷學到的表徵是否保留了關於目標的資訊，或者是否把容量浪費在無關的細節上。

## 開放問題

- 在高維度中估計互資訊很困難。以樣本為基礎的估計量常有偏差，這使得關於深度網路的主張難以檢驗。
- 資訊瓶頸能否解釋深度網路如何訓練？Saxe 等人（2019）的結果顯示，答案取決於非線性等細節。
- 大腦是否如 Barlow 所說是一種有效率的編碼器？如果是，它最佳化的是哪一個量？

## 參考文獻

以下條目保留原文，便於查閱原始文獻。

### 奠基性論文

- Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27, 379–423 and 623–656. https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf — 奠基之作：以熵衡量資訊，並定義壓縮與可靠通訊的極限。此為網路上的重印版本。
- Linsker, R. (1988). Self-organization in a perceptual network. *Computer*, 21(3), 105–117. https://doi.org/10.1109/2.36 — 提出 infomax 原則：一個分層的感知模型，會藉由保留關於輸入的資訊而自我組織。
- Barlow, H. B. (1961). Possible principles underlying the transformations of sensory messages. In *Sensory Communication*, pp. 217–234. https://mlanthology.org/misc/1961/barlow1961misc-possible — 提出感覺處理會減少冗餘，是效率編碼假說的起源。
- Tishby, N., Pereira, F. C. & Bialek, W. (2000). The information bottleneck method. arXiv:physics/0004057. https://arxiv.org/abs/physics/0004057 — 定義相關資訊，並推導壓縮輸入與預測目標之間的權衡。
- Alemi, A. A., Fischer, I., Dillon, J. V. & Murphy, K. (2016). Deep variational information bottleneck. arXiv:1612.00410. https://arxiv.org/abs/1612.00410 — 使資訊瓶頸能以神經網路訓練，並回報相較某些標準正則化方法有更好的泛化與對抗性強健性。
- Saxe, A. M., Bansal, Y., Dapello, J., Advani, M., Kolchinsky, A., Tracey, B. D. & Cox, D. (2019). On the information bottleneck theory of deep learning. *Journal of Statistical Mechanics*. https://research.ibm.com/publications/on-the-information-bottleneck-theory-of-deep-learning — 主張關於深度網路壓縮的核心論點在一般情況下並不成立，觀察到的壓縮主要取決於非線性函數。

### 教科書與綜述

- MacKay, D. J. C. (2003). *Information Theory, Inference, and Learning Algorithms*. Cambridge University Press. https://www.cambridge.org/0521642981 — 將資訊理論與貝氏推論及學習演算法一併討論的教科書。
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 3 章〈Probability and Information Theory〉以深度學習的角度介紹熵、KL 散度與交叉熵。全文可於線上免費閱讀。

### 講座與影片

- Polyanskiy, Y.（授課教師）。*6.441 Information Theory*. MIT OpenCourseWare, Spring 2016. https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/ — 從基礎出發的研究所課程。課程頁面提供講義與習題，但未列出影片講座。

### 文章與文件

- *Visual Information Theory*. colah's blog (2015). https://colah.github.io/posts/2015-09-Visual-Information/ — 以圖解方式介紹熵、交叉熵、KL 散度與互資訊。
