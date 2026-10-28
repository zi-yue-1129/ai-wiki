---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/models/transformer
tags:
  - 生成模型
  - 正規化流
  - 非監督式學習
aliases:
  - 流模型
  - Flow-based generative models
  - Normalising flows
  - Flow matching
---

# 流模型（Flow-Based Generative Models）

流模型透過一連串可逆映射，把簡單的分布轉換成目標分布。由於每個映射都可逆，且其雅可比行列式容易計算，任何資料點的精確對數似然與精確抽樣都可取得；這是 [VAE](../vae/index.md) 與 [GAN](../gan/index.md) 做不到的。本頁比較兩個主要分支：具離散可逆層的正規化流，以及學習連續速度場的流匹配。方法頁分別是[正規化流](normalising-flows/index.md)與[流匹配](flow-matching/index.md)。家族層級的比較見[生成模型](../generative-models/index.md)頁。

## 概覽

Dinh、Krueger 與 Bengio（2014）以 NICE 提出此想法，它使用加性耦合層，把資料映射到各分量獨立的空間。Dinh、Sohl-Dickstein 與 Bengio（2017）加入仿射耦合層，使映射更有表達力，同時仍保有容易計算的行列式。Rezende 與 Mohamed（2015）則早已為正規化流建立一般框架，用來建構變分推論中有彈性的後驗近似。流匹配（Lipman 等人，2023）從連續時間的角度追求同樣的目標，訓練一個把雜訊移到資料的速度場。

## 關鍵概念

- **變數變換**：若 \(x = f(z)\)，\(z\sim p_z\)，且 \(f\) 可逆，則 \(\log p_x(x) = \log p_z(f^{-1}(x)) + \log\lvert\det \partial f^{-1}/\partial x\rvert\)。
- **耦合層**：把輸入分成兩部分，保留其中一部分，另一部分則以前一部分計算出的尺度與平移來轉換，使雅可比矩陣為三角形。
- **速度場**：在流匹配中，定義 ODE 的時間相依向量場，其 ODE 軌跡把雜訊帶到資料。
- **連續正規化流**：以 ODE 定義的流，透過瞬時變數變換給出精確似然。

## 運作方式

對於 \(x = f(z)\)，\(z\sim p_z\)，變數變換給出

\[
\log p_x(x) = \log p_z\big(f^{-1}(x)\big) + \log\left|\det \frac{\partial f^{-1}(x)}{\partial x}\right|
\]

正規化流堆疊可逆層 \(f = f_K \circ \cdots \circ f_1\)，並以上述變數變換計算似然。抽樣時，從基底分布抽取 \(z\)，再一次計算 \(f(z)\)。訓練以梯度下降最大化資料上平均的精確對數似然，不需要對抗賽局，也不需要近似後驗。

流匹配則定義一條從雜訊 \(x_0\) 到資料 \(x_1\) 的路徑，訓練網路 \(v_\theta(x,t)\) 去回歸該路徑的速度，並以 ODE \(\mathrm{d}x/\mathrm{d}t = v_\theta(x,t)\) 從 \(t=0\) 積分到 \(t=1\) 來抽樣。訓練時不需要模擬 ODE，這是它與早期連續流的主要實務差異。

## 關鍵方法

- [正規化流（Dinh 等人，2017；Kingma 與 Dhariwal，2018）](normalising-flows/index.md)：具精確似然的離散可逆層。Real NVP 使用仿射耦合；Glow 加入可逆 1×1 卷積。
- [流匹配（Lipman 等人，2023）](flow-matching/index.md)：沿機率路徑回歸速度場，並以 ODE 抽樣。它也涵蓋擴散路徑作為特例。

## 關聯

- 擴散模型與流匹配共享連續時間的觀點，見 [DDPM](../diffusion/ddpm.md) 與[擴散模型](../diffusion/index.md)頁。
- 流匹配是近來數個影像與影片生成器的訓練目標，它們使用 Transformer 去噪器，見 [DiT](../../../../models/transformer/dit/index.md)。
- 變數變換的想法也是[分群與混合模型](../../clustering/index.md)中密度估計的基礎。
- 以流做變分推論時，後驗的機制相同，見[機率方法](../../../probabilistic/index.md)。

## 應用

以精確似然做密度估計與異常偵測、影像與音訊合成、分子構形生成，以及貝氏推論中的後驗近似。

## 開放問題

- 在保有精確似然的同時，能否達到擴散與 GAN 模型的樣本品質。
- 可逆性是否真的限制模型能學到的東西，或只是成本。
- 以合理的運算量擴展到非常高的解析度。

## 參考文獻

### 開創性論文

- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — 把正規化流定義為用於有彈性後驗的可逆變換。
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — 提出具單位雅可比行列式的加性耦合層。
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2017). *Density Estimation Using Real NVP*. ICLR. https://arxiv.org/abs/1605.08803 — 提出用於影像的仿射耦合層與多尺度架構。
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS（arXiv）. https://arxiv.org/abs/1807.03039 — 加入可逆 1×1 卷積與 actnorm，並展示影像的潛在空間操控。
- Lipman, Y., et al. (2023). *Flow Matching for Generative Modeling*. ICLR（arXiv）. https://arxiv.org/abs/2210.02747 — 以無需模擬的回歸在機率路徑上訓練連續正規化流。

### 綜述與教科書

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 流架構及其在密度估計與推論中的應用綜述。

## 延伸學習

- Eric Jang, *Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows*。連結：https://blog.evjang.com/2018/01/nf2.html — 以淺顯方式介紹現代流架構與其雅可比行列式。
