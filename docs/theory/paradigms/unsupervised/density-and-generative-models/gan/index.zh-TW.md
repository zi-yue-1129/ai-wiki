---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/paradigms/imitation
tags:
  - 生成模型
  - 對抗式訓練
  - 非監督式學習
aliases:
  - 生成對抗網路
  - GAN
  - Generative adversarial network
---

# 生成對抗網路（GAN）

生成對抗網路讓兩個網路彼此對抗地訓練。生成器把隨機雜訊轉換為樣本，判別器則試著分辨這些樣本與真實資料。生成器透過騙過判別器而進步，因此模型不需要寫出似然函數，也能學會生成資料。數年間，GAN 是清晰影像合成的主流方法。家族層級的比較見[生成模型](../generative-models/index.md)頁，其他替代方法是 [VAE](../vae/index.md) 與[流模型](../flow/index.md)。

## 概覽

Goodfellow 等人（2014）將此框架提出為生成器 \(G\) 與判別器 \(D\) 之間的極小極大賽局。論文指出，在理想化的假設下，此賽局有唯一解：生成器恢復資料分布，判別器處處輸出二分之一。以多層感知器與反向傳播訓練從一開始就可行，而且此方法不需要馬可夫連。

## 關鍵概念

- **生成器** \(G(z)\)：將雜訊 \(z\sim p_z\) 映射為樣本。
- **判別器** \(D(x)\)：輸出 \(x\) 來自資料而非生成器的機率。
- **極小極大賽局**：\(D\) 最大化分類正確率，\(G\) 則使其最小化。
- **模式崩潰**：生成器只產生少數幾種樣本。
- **評論家（critic）**：輸出為無界分數而非機率的判別器，見於 Wasserstein 形式中。

## 運作方式

價值函數為

\[
\min_G \max_D \; V(D, G) = \mathbb E_{x\sim p_{\text{data}}}[\log D(x)] + \mathbb E_{z\sim p_z}[\log(1 - D(G(z)))]
\]

在固定生成器時，最佳判別器為 \(D^*(x) = p_{\text{data}}(x)/(p_{\text{data}}(x)+p_g(x))\)。代入價值函數後得到 \(-\log 4 + 2\,\mathrm{JSD}(p_{\text{data}}\,\|\,p_g)\)，因此生成器最小化的是資料與模型之間的 Jensen–Shannon 散度。實務上生成器使用非飽和損失 \(-\log D(G(z))\)，因為原始損失在判別器很有把握時梯度會消失。

訓練交替進行：對真實與生成樣本的小批次做幾次判別器更新，再做一次生成器更新。生成時抽取 \(z\sim p_z\) 並套用一次 \(G\)，相較於自迴歸或擴散的抽樣非常快。

## 關鍵方法

各種命名變體針對訓練穩定性或架構。以下簡短比較連到每個方法各自的頁面。

- **生成對抗網路（Goodfellow 等人，2014）**：原始的極小極大框架，詳見下方。
- **[DCGAN（Radford 等人，2015）](dcgan.md)**：使用卷積式的生成器與判別器，並加上架構規則，使影像上的訓練更穩定。
- **[WGAN（Arjovsky 等人，2017）](wgan.md)**：以 Wasserstein 距離取代 Jensen–Shannon 目標，並以權重裁剪強制 Lipschitz 限制。
- **[WGAN-GP（Gulrajani 等人，2017）](wgan-gp.md)**：以在內插樣本上的梯度懲罰取代權重裁剪。

### 生成對抗網路（Goodfellow 等人，2014）

- **問題：** 在不需要早期方法中難以計算的似然函數，也不需要馬可夫連的情況下，學習生成模型。
- **核心想法：** 在極小極大賽局中同時訓練生成器與判別器，讓生成器透過判別器的訊號被推向資料分布。
- **公式或演算法：** 上述的價值函數。每一輪：抽取雜訊與真實資料的小批次，以梯度上升更新 \(D\) 以最大化 \(V\)，再抽取新的雜訊，並更新 \(G\) 以最小化 \(-\log D(G(z))\)。
- **結果：** 摘要提到對生成樣本做了定性與定量評估，並表示此方法展現了潛力，但未給出具體數字。論文的實驗以 MNIST、多倫多人臉資料庫與 CIFAR-10 評估樣本品質。
- **限制：** 訓練不穩定，且對架構與學習率敏感。模式崩潰可能使資料分布的部分被遺漏。缺乏似然函數，因此模型難以比較，評估也依賴代理指標。

## 關聯

- 對抗的概念也出現在對抗式模代學習中：判別器對示範與策略的表現打分，見[對抗式模代](../../../imitation/adversarial-imitation/index.md)。
- GAN 的生成器通常是卷積式的，因此其架構與[卷積網路](../../../../models/cnn/index.md)重疑。
- 從 Jensen–Shannon 散度的角度，本方法與[資訊理論](../../../../information-theory/index.md)相連。
- 影像 GAN 是許多影像到影像系統的基礎，見[多模態模型](../../../../models/multimodal/index.md)。

## 應用

影像合成與編輯、超解析度、資料擴增、影像風格之間的領域轉換，以及逼真的語音與人臉生成。近年許多用途已轉向擴散模型。

## 開放問題

- 在不需仔細調校的情況下穩定訓練，以及梯度懲罰與譜正規化等修正能否推廣到不同任務。
- 不依賴單一代理指標，評估樣本品質與多樣性。
- 在非常大的規模下，對抗目標能否仍與基於似然与擴散的模型保持競爭力。

## 參考文獻

### 開創性論文

- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS（arXiv）. https://arxiv.org/abs/1406.2661 — 提出對抗框架、價值函數與非飽和訓練方法。
- Radford, A., Metz, L. & Chintala, S. (2016). *Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks*. ICLR（arXiv）. https://arxiv.org/abs/1511.06434 — 提出 DCGAN，並給出在影像上穩定訓練卷積 GAN 的架構指引。
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. arXiv. https://arxiv.org/abs/1701.07875 — 提出 Wasserstein 目標，以改善 GAN 訓練的穩定性。
- Gulrajani, I., et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS（arXiv）. https://arxiv.org/abs/1704.00028 — 以梯度懲罰取代權重裁剪。

### 綠論與教科書

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — 框架與其訓練問題的教程式綜述。

## 延伸學習

- Lilian Weng, *From GAN to WGAN*。https://lilianweng.github.io/posts/2017-08-20-gan/ — 以推導與圖示說明 GAN 與 Wasserstein 目標。
