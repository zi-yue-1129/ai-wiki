---
translation_reviewed: 2026-10-28
---

# 深度信念網路（Hinton、Osindero 與 Teh，2006）

深度信念網路是由多層潛變數堆疊而成的模型，訓練時一次只訓練一層，每一層都從下一層的輸出中學習。2006 年提出這個程序的論文，通常被視為[深度學習革命](../index.md)這一章所描述的復興的起點。

## 概述

在 2006 年之前，以隨機權重從頭開始、以梯度為基礎訓練具有數個隱藏層的網路，效果常常不佳。下層接收到的學習訊號很弱；在 Glorot 與 Bengio（2010）的實驗中，較深的網路表現還不如較淺的網路。當時並沒有廣泛被接受的可靠解法。反向傳播的早期歷史見於[反向傳播的復興](../../expert-systems-and-winters/backpropagation-revival/index.md)一章。

Hinton、Osindero 與 Teh 提出了另一條路線。每一層先以貪婪的方式，學成其下一層的生成模型。之後才針對任務調整整個網路，並以這個預訓練找到的權重作為起點（Hinton 等人，2006）。同一組作者的後續論文把相同想法用在深度自編碼器上，在其研究的資料上，學到的低維編碼比主成分分析更好（Hinton 與 Salakhutdinov，2006）。

## 關鍵概念

- **受限玻爾茲曼機（restricted Boltzmann machine, RBM）**：一個兩層模型，可見單元對應資料，隱藏單元對應學到的特徵。連結只存在於兩層之間。
- **對比散度（contrastive divergence）**：RBM 的快速近似學習規則，以短的取樣鏈取代無法精確計算的梯度（Hinton，2002）。
- **貪婪逐層預訓練（greedy layer-wise pretraining）**：一次只訓練一層，並固定其下方各層的權重。
- **互補先驗（complementary priors）**：論文為隱藏層選擇的先驗，用來抵消「解釋消除」（explaining away）效應，使某一層的後驗分布可以分解。

## 運作方式

對於可見向量 $\mathbf{v}$ 與隱藏向量 $\mathbf{h}$，一個 RBM 會為每種配置指定一個能量：

$$
E(\mathbf{v}, \mathbf{h}) = -\mathbf{a}^\top \mathbf{v} - \mathbf{b}^\top \mathbf{h} - \mathbf{v}^\top W \mathbf{h},
\qquad
P(\mathbf{v}, \mathbf{h}) = \frac{e^{-E(\mathbf{v}, \mathbf{h})}}{Z}.
$$

由於同一層內沒有連結，給定另一層時，該層的所有單元都可以一次取樣，因此近似學習的成本很低。單步對比散度更新，是把在資料上量得的統計量，與經過一次重建後量得的統計量相比較：

$$
\Delta W \propto \langle \mathbf{v}\mathbf{h}^\top \rangle_{\text{data}} - \langle \mathbf{v}\mathbf{h}^\top \rangle_{\text{reconstruction}}.
$$

對於三個隱藏層，論文的最終模型在下層為有向結構，最上面兩層則為無向結構：

$$
P(\mathbf{v}, \mathbf{h}^1, \mathbf{h}^2, \mathbf{h}^3) = P(\mathbf{h}^2, \mathbf{h}^3)\, P(\mathbf{h}^1 \mid \mathbf{h}^2)\, P(\mathbf{v} \mid \mathbf{h}^1).
$$

訓練依下列步驟進行：

1. 訓練一個 RBM，以資料作為可見層，以第一隱藏層作為隱藏層。
2. 凍結其權重，並為每個訓練範例計算第一隱藏層的激活值。
3. 把這些激活值當作第二個 RBM 的資料，以同樣方式訓練它。
4. 依所需層數重複。最上面兩層保留為無向 RBM。
5. 以對比版本的清醒–睡眠（wake-sleep）演算法，對所有權重進行聯合微調。

## 結果

論文以三個隱藏層的網路，評估手寫數字影像與其標籤。依作者所述，此模型是影像與標籤聯合分布的良好生成模型，而且其數字分類結果優於當時最好的判別式學習演算法。

這些都是小型基準任務上的結果，此處以定性方式描述；具體數字見原始論文。

## 限制

- **成本。** 每個 RBM 都需要取樣，加上對資料需要多次掃描，使預訓練速度很慢。
- **預訓練的角色。** 較好的初始化（Glorot 與 Bengio，2010）、[批次正規化](../../../../theory/deep-learning/normalisation/batch-normalisation/index.md)與[丟棄法](../../../../theory/deep-learning/dropout/index.md)，之後使深度網路得以直接訓練，減少了對貪婪預訓練的需求。
- **規模。** 證據來自小型資料集，而非[ImageNet](../imagenet/index.md)頁面所描述的大型影像任務。

## 開放問題

- 逐層預訓練為什麼有幫助？Bengio 等人（2006）談到中間表徵的作用，但這個問題只得到部分解答。
- 無監督預訓練在[Transformer](../../../../theory/models/transformer/attention-is-all-you-need/index.md)之後的語言模型中以另一種形式回歸。它是同一個原理嗎？

## 關聯

深度信念網路是一個具有特徵層級結構的生成模型，因此很自然地可以與視覺皮質的階層模型相比較（參見 [NeuroAI](../../../../brain-mind/neuroai/index.md)）。伴隨的自編碼器研究見於[自編碼器與表徵](../../../../theory/paradigms/unsupervised/autoencoders-and-representations/index.md)。

## 參考文獻

### 開創性論文

- Hinton, G. E., Osindero, S. & Teh, Y.-W. (2006). A fast learning algorithm for deep belief nets. *Neural Computation*. https://doi.org/10.1162/neco.2006.18.7.1527 — 提出深度信念網路的貪婪逐層訓練，是這場復興的起點。
- Hinton, G. E. & Salakhutdinov, R. R. (2006). Reducing the dimensionality of data with neural networks. *Science*. https://doi.org/10.1126/science.1127647 — 顯示預訓練過的深度自編碼器，學到的低維編碼比主成分分析更好。
- Bengio, Y., Lamblin, P., Popovici, D. & Larochelle, H. (2006). Greedy layer-wise training of deep networks. *Advances in Neural Information Processing Systems 19*. https://proceedings.neurips.cc/paper/2006/hash/5da713a690c067105aeb2fae32403405-Abstract.html — 把貪婪逐層預訓練擴展到 RBM 以外的其他層類型。
- Hinton, G. E. (2002). Training products of experts by minimizing contrastive divergence. *Neural Computation*. https://doi.org/10.1162/089976602760128018 — 提出對比散度，使 RBM 的訓練變得可行。

### 綜述與教科書

- Bengio, Y. (2009). Learning deep architectures for AI. *Foundations and Trends in Machine Learning*. https://doi.org/10.1561/2200000006 — 關於深度架構，以及如何逐層訓練它們的專著。
- LeCun, Y., Bengio, Y. & Hinton, G. (2015). Deep learning. *Nature*. https://doi.org/10.1038/nature14539 — 由該領域三位奠基者撰寫的回顧，探討多層網路如何學習表徵。

### 文章與文件

- Glorot, X. & Bengio, Y. (2010). Understanding the difficulty of training deep feedforward neural networks. *Proceedings of AISTATS 2010*. https://proceedings.mlr.press/v9/glorot10a.html — 分析深度前饋網路為何難以訓練，並提出較好的初始化方法。
