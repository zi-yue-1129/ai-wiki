---
translation_reviewed: 2026-10-28
---

# 自回歸生成模型

自回歸生成模型把整個物件的機率寫成一連串預測的乘積，每個預測都以前面的部分為條件，即 \(p(x)=\prod_t p(x_t\mid x_{<t})\)。它們一次採樣一個部分來生成資料。同一套做法驅動了語言模型、像 PixelCNN 這樣的像素級影像模型、像 WaveNet 這樣的音訊模型，以及如今用來建模影像與音訊詞元的 Transformer 解碼器。

## 概述

依機率的鏈式法則，任何聯合分布都可以拆成條件分布。只有當每個條件分布都能被學習時，這種拆分才有用，而自回歸模型用一個網路、依固定順序讀取前面的元素來學習它們。訓練就是一般的最大似然，因此模型能為每個樣本給出精確的似然值。這正是自回歸模型與 [VAE](../vae/index.md) 和 [GAN](../gan/index.md) 不同之處，也是此家族出現在[生成模型](../index.md)概述中的原因。

代價是生成速度。訓練時，每個條件分布都能同時計算，因為前面的真實值已知。採樣時，每個新元素必須先被抽出，下一個才能預測，因此生成長度為 \(T\) 的序列需要經過網路 \(T\) 次。[擴散模型](../diffusion/index.md)則做出相反的取捨，在固定的步數內精煉整個物件。

下一個詞元預測就是把同一模型套用到文字上。[大型語言模型](../../models/llm/index.md)是以詞元為對象的自回歸模型，其訓練目標正是上面定義的對數似然。因此，此家族已被應用於文字、語音、影像、影片與音樂，各方法的主要差異在於「元素」是什麼，以及條件分布如何計算。

## 核心概念

- **因式分解**：有序序列上的聯合分布，\(p(x_1,\dots,x_T)=\prod_t p(x_t\mid x_{<t})\)。順序是建模的選擇，對影像與音訊而言通常固定，例如光柵順序或時間順序。
- **因果遮罩**：一種限制，阻止位置 \(t\) 的預測看到位置 \(t\) 及之後的內容。它可以由遮罩卷積、因果卷積或三角形的注意力遮罩來實現。
- **平行訓練與依序採樣**：遮罩式架構在訓練時能於一次計算中算出所有條件分布，但在生成時每次只能取樣一個元素。
- **離散輸出**：每個條件分布都是有限集合上的 softmax，例如 256 個亮度級別或一個詞彙表的詞元。
- **分詞器**：許多模型處理的是離散單位而非原始資料。文字會被切成[詞元](../../models/llm/tokenisation/index.md)，而影像與音訊則可以由學得的量化器（如 [VQ-VAE](../vae/vq-vae/index.md)）對應為詞元。
- **每維位元數**：以 2 為底的負對數似然，除以樣本中的數值個數。它是像素級與波形級模型常用的分數。

## 運作方式

模型把序列 \(x = (x_1,\dots,x_T)\) 的機率定義為

\[
p(x) = \prod_{t=1}^{T} p_\theta\big(x_t \mid x_{<t}\big)
\]

並透過最小化資料集上的負對數似然 \(-\sum_t \log p_\theta(x_t\mid x_{<t})\) 來訓練。計算每個條件分布的網路可以是遮罩卷積、擴張因果卷積，或帶有因果注意力的 Transformer。無論採用哪種架構，生成的過程都遵循同一個迴圈：

```mermaid
flowchart LR
    A["目前已生成的元素"] --> B["網路給出 p(x_t 給定 x_<t)"]
    B --> C["從分布中抽出 x_t"]
    C --> D["把 x_t 加入上下文"]
    D --> A
```

有兩個設計選擇決定了大部分行為。第一是分詞器或輸入表示，它決定序列長度。同樣的內容，用像素、顏色調色盤、波形樣本或學得的編碼表示，得到的序列長度可以相差很大。第二是網路可用的上下文，對卷積而言是感受野，對 Transformer 而言是注意力範圍。較大的上下文能捕捉較長程的結構，但每一步的成本也較高。

## 主要方法

三個代表性方法展示了上述選擇在像素與音訊樣本上的表現。每個方法都有自己的頁面，包含問題、方程式、結果與限制。

| 方法 | 年份 | 資料 | 架構 | 主要想法 |
|---|---|---|---|---|
| [PixelCNN](pixelcnn/index.md) | 2016 | 影像像素 | 遮罩卷積 | 依光柵順序由較早的像素預測每個像素，並可平行訓練 |
| [WaveNet](wavenet/index.md) | 2016 | 原始音訊樣本 | 擴張因果卷積 | 預測每個波形樣本，感受野涵蓋數百毫秒 |
| [Image GPT](image-gpt/index.md) | 2020 | 低解析度像素或顏色詞元 | Transformer 解碼器 | 不使用卷積結構來預測像素，並學得可用於分類的特徵 |

PixelCNN 與 WaveNet 保留了各自輸入的卷積歸納偏置，而 Image GPT 則移除了它們。以詞元為基礎的系統，例如 VQ-VAE 先驗與音訊語言模型，則把同樣的目標套用到學得的編碼上，從而讓序列保持較短。

## 與其他主題的連結

- **語言。** 語言的情況見[大型語言模型](../../models/llm/index.md)頁面，其使用的詞元則見[分詞](../../models/llm/tokenisation/index.md)。本頁不重複那些內容。
- **語音與音訊。** WaveNet 這類波形模型、編解碼詞元模型與語音語言模型，見[語音與音訊](../../models/speech/index.md)的介紹。
- **離散編碼。** [VQ-VAE](../vae/vq-vae/index.md) 學得 PixelCNN 與 WaveNet 式先驗所建模的編碼，而 Image GPT 則把 VQ-VAE 用於較高解析度的輸入。
- **流模型。** [遮罩自回歸流](../normalising-flows/masked-autoregressive-flow/index.md)使用同樣的遮罩，能以一次計算評估密度，而採樣仍是依序進行的。逆自回歸流則反轉了這個取捨，而 Parallel WaveNet 就是用它來匹配 WaveNet。
- **遮罩預測。** BERT 式模型從兩側預測被遮住的位置，而不只是從過去預測。另一種方法見[遮罩預測](../../paradigms/self-supervised/masked-prediction/index.md)。
- **大腦與心智。** 預測式處理提供了最接近的大腦連結。Schrimpf 等人（2021）發現，較能預測下一個詞的語言模型，也較能預測人類在語言處理時的大腦測量值；Goldstein 等人（2022）則發現，大腦在每個詞出現之前就會持續做出下一個詞的預測。[^1] 另見[語言與大腦](../../../brain-mind/language-in-brain/index.md)與[預測編碼](../../../brain-mind/predictive-coding/index.md)。

## 應用

- **語言與程式碼。** 自回歸語言模型生成文字、程式碼與對話，見[大型語言模型](../../models/llm/index.md)的介紹。
- **語音。** WaveNet 被評為比當時最好的參數式與拼接式系統更自然（van den Oord 等人，2016）。其較快的蒸餾版本 Parallel WaveNet 已部署於 Google Assistant（van den Oord 等人，2017）。VALL-E 等編解碼詞元模型（Wang 等人，2023）只需一段簡短的提示即可合成語音。
- **影像。** 以文字與影像詞元為對象的 Transformer，能依提示生成影像（Ramesh 等人，2021）。Image GPT 以像素訓練的特徵，在 CIFAR-10 上的線性探測準確度達 96.3%（Chen 等人，2020）。
- **音樂。** Jukebox 以自回歸 Transformer 建模 VQ-VAE 的編碼，能產生數分鐘內保持連貫的歌曲（Dhariwal 等人，2020）。
- **壓縮。** 能為資料分配機率的模型，也能為資料給出一個編碼，算術編碼的長度接近理想值。這就是每維位元數可作為壓縮分數的原因。[^2]

## 未解問題

- **速度與似然的取捨。** 依序採樣是主要成本。蒸餾、平行解碼或非自回歸模型能否保持依序模型的品質，是目前活躍的問題。
- **順序與詞元的選擇。** 固定的光柵或時間順序只是一種方便。順序與分詞器在多大程度上限制了模型能表示的內容，尚無定論。
- **長程結構。** 音樂與長篇語音需要數分鐘的連貫性。下一個詞元模型能否在規模化後學到它，或需要階層式的編碼，仍有爭議。
- **大腦證據。** 大腦模型的結果是相關性的。大腦是否以與這些模型相同的方式使用預測，仍未確定。

[^1]: 這些研究把模型的活化與自然語言期間的大腦記錄加以比較。它們顯示兩者共享預測式的結構，但並不表示大腦執行的是與 Transformer 相同的演算法，也不表示大腦是以自回歸的方式產生語音。
[^2]: 這種對應只是近似的。算術編碼會在理想編碼長度之上增加少量的額外開銷，PixelRNN 論文也提到了這一點。

## 參考文獻

### 開創性論文

- van den Oord, A., Kalchbrenner, N. & Kavukcuoglu, K. (2016). *Pixel Recurrent Neural Networks*. ICML (PMLR 48). https://arxiv.org/abs/1601.06759 — 提出 PixelRNN 與 PixelCNN，即以逐像素方式自回歸建模自然影像的模型。
- van den Oord, A. et al. (2016). *WaveNet: A Generative Model for Raw Audio*. arXiv. https://arxiv.org/abs/1609.03499 — 以擴張因果卷積構成的原始語音與音樂波形自回歸模型。
- Graves, A. (2013). *Generating Sequences With Recurrent Neural Networks*. arXiv. https://arxiv.org/abs/1308.0850 — 顯示每次預測一個值的遞迴網路，能生成長篇的文字與手寫序列。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 把自回歸 Transformer 語言模型擴大到 1,750 億參數，並測試少樣本提示。
- Chen, M. et al. (2020). *Generative Pretraining From Pixels*. ICML (PMLR 119). https://proceedings.mlr.press/v119/chen20s.html — 訓練 GPT-2 風格的 Transformer 來預測像素，並報告可用於分類的特徵。
- van den Oord, A., Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. arXiv. https://arxiv.org/abs/1711.00937 — 學得自回歸先驗可用來建模、以生成影像與語音的離散編碼。
- Ramesh, A. et al. (2021). *Zero-Shot Text-to-Image Generation*. arXiv. https://arxiv.org/abs/2102.12092 — 把文字與影像詞元建模為單一自回歸序列的 Transformer。
- Borsos, Z. et al. (2022). *AudioLM: a Language Modeling Approach to Audio Generation*. arXiv. https://arxiv.org/abs/2209.03143 — 把音訊生成視為對離散語意與聲學詞元的語言建模。

### 綜述與教科書

- Bond-Taylor, S., Leach, A., Long, Y. & Willcocks, C. G. (2021). *Deep Generative Modelling: A Comparative Review of VAEs, GANs, Normalizing Flows, Energy-Based and Autoregressive Models*. arXiv. https://arxiv.org/abs/2103.04922 — 比較自回歸模型與其他深度生成模型家族及其取捨。

### 文章與文件

- Schrimpf, M. et al. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — 把語言模型中的下一詞預測與人類在語言處理時的大腦反應連結起來。
- Goldstein, A. et al. (2022). Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*. https://doi.org/10.1038/s41593-022-01026-4 — 在人類大腦記錄中報告持續的下一詞預測與驚訝訊號。
