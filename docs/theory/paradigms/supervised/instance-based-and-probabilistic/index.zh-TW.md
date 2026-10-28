---
tags:
  - supervised learning
  - probabilistic models
  - bayesian
---

# 基於實例與機率的分類器

這兩個家族，一類透過與儲存的範例相似度來推理新輸入（k 近鄰），另一類則透過明確的機率模型來推理（單純貝氏、判別分析、高斯過程）。

## k 近鄰（kNN）

儲存訓練集；要分類 $x$ 時，在某種距離（歐氏距離、餘弦距離、學習得到的度量）下找出最近的 $k$ 個範例，然後投票（迴歸則取平均）。它沒有訓練階段。kNN 會受到維度災難的影響——在高維空間中距離不再有資訊量；查詢速度慢的問題，則可以用近似最近鄰索引（HNSW、乘積量化）緩解。Cover & Hart（1967）證明，當 $n\to\infty$ 時，1-NN 的誤差至多為貝氏誤差的兩倍。現代的檢索增強系統，例如 kNN-LM 與向量資料庫查詢，本質上就是在學習得到的嵌入上做 kNN。

## 生成式分類器

這類方法對 $p(x\mid y)$ 與 $p(y)$ 建模，再套用貝氏定理：$p(y\mid x)\propto p(x\mid y)p(y)$。

- **單純貝氏**假設在給定類別下，特徵彼此條件獨立。這個假設並不正確，但在文字與垃圾郵件過濾上，即使資料很少也常有良好表現。
- **線性／二次判別分析**假設各類別的密度為高斯分布，並分別假設共享（LDA）或各自（QDA）的共變異數。
- **隱馬可夫模型與條件隨機場**把這個想法延伸到序列；CRF 是其判別式的對應版本。

Ng & Jordan（2001）指出，生成式分類器較快達到其（較高的）漸近誤差，而像邏輯迴歸這類判別式分類器則在資料較多時勝出。

## 高斯過程（GP）

GP 對函數加上先驗 $f\sim\mathcal{GP}(m,k)$，並在每個點回傳完整的預測分布：

$$
\mu_* = K_*^\top (K+\sigma^2 I)^{-1} y,\qquad \sigma_*^2 = k_{**} - K_*^\top (K+\sigma^2 I)^{-1}K_*.
$$

GP 在資料點很少時仍能給出校準良好的不確定性，也驅動貝氏最佳化與[主動學習](../../active/index.md)。精確推論的成本是 $O(n^3)$，因此大資料集會使用稀疏與變分近似。

## 與其他概念的連結

貝氏觀點與[機率與貝氏方法](../../probabilistic/index.md)相連。在心理學中，範例理論（exemplar theory）的類別化與 kNN 相似，原型理論則對應類別中心分類器。

## 參考文獻

### 開創性論文

- Cover, T. M. & Hart, P. E. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), 21–27. https://doi.org/10.1109/TIT.1967.1053964 — 證明最近鄰規則的漸近誤差上界。
- Ng & Jordan (2001), "On discriminative vs. generative classifiers: a comparison of logistic regression and naive Bayes", NeurIPS. https://papers.nips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html — 比較各分類器需要多少資料，以及各自何時勝出。
- Bartlett, Jordan & McAuliffe (2006), "Convexity, classification, and risk bounds", *JASA* 101(473), arXiv:math/0612821. https://arxiv.org/abs/math/0612821 — 說明哪些凸替代損失仍能得到良好的分類器。
- Niculescu-Mizil & Caruana (2005), "Predicting good probabilities with supervised learning", ICML. https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting — 對常見分類器的機率校準做實證比較。
- Guo et al. (2017), "On calibration of modern neural networks", ICML, arXiv:1706.04599 — 顯示預測的機率可能校準不良，並提出以溫度縮放作為修正。

### 綜述與教科書

- Rasmussen & Williams，*Gaussian Processes for Machine Learning*，MIT Press（2006）。免費線上章節：https://gaussianprocess.org/gpml/chapters — 高斯過程模型及其推論的標準參考書。

### 講座與影片

- Hand, D. J. & Yu, K. (2001). Idiot’s Bayes: not so stupid after all? *International Statistical Review*, 69(3), 385–398. https://doi.org/10.1111/j.1751-5823.2001.tb00465.x — 說明即使獨立性假設不成立，樸素貝氏分類器為何仍表現良好。

### 文章與文件

（除上列項目外，無其他參考。）

## 延伸學習

- StatQuest with Josh Starmer，關於單純貝氏的單元，YouTube。https://www.youtube.com/@statquest — 以視覺化、逐步的方式說明單純貝氏如何計算類別機率。

## 延伸閱讀

- Murphy，*Probabilistic Machine Learning: An Introduction*，MIT Press（2022）。免費線上版：https://probml.github.io/pml-book/ — 涵蓋樸素貝氏等機率分類器。
