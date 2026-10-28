---
translation_reviewed: 2026-10-28
---

# WaveNet

WaveNet 是一種原始音訊的自回歸模型。它用一疊擴張因果卷積，由波形中所有之前的樣本預測每個樣本。由 van den Oord 等人（2016）提出，它被評為比當時最好的參數式與拼接式語音系統更自然，是 [自回歸生成模型](../index.md)概述中的代表性方法之一。

## 概述

早期的統計式語音合成先預測聲學特徵，再交給獨立的聲碼器（vocoder）重建波形。WaveNet 則直接對波形本身建模，每次生成一個樣本，而語音的取樣率至少是每秒 16,000 個值。因此模型需要數千個樣本的感受野，同時還要能負擔得起執行的成本。

此設計是 [PixelCNN](../pixelcnn/index.md) 的一維版本。擴張卷積在不做池化的情況下擴大感受野，因此輸出保有輸入的時間解析度。

## 核心概念

- **擴張因果卷積**：只看當前與過去樣本的卷積，並以固定步距（即擴張量）跳過部分輸入。每層將擴張量加倍，使感受野隨深度呈指數成長。
- **感受野**：能影響某次預測的過去樣本範圍。在文字轉語音模型中約為 240 毫秒，在多語者模型中約為 300 毫秒。
- **µ-law 壓擴**：一種對數轉換，讓 256 個量化級別比線性級別更有效地涵蓋波形。
- **全域與局部條件**：說話者身分會影響每個時間步，而語言學特徵隨時間變化，並被上採樣到音訊的取樣率。

## 運作方式

波形 \(x = (x_1, \dots, x_T)\) 的聯合分布為

\[
p(x) = \prod_{t=1}^{T} p\big(x_t \mid x_1, \dots, x_{t-1}\big)
\]

每個樣本先經過壓擴並量化為 256 個值，其公式為

\[
f(x_t) = \operatorname{sign}(x_t)\,\frac{\ln(1 + \mu\lvert x_t\rvert)}{\ln(1 + \mu)}, \qquad \mu = 255
\]

網路則輸出這些值上的 softmax。每個殘差區塊套用閘控啟動，\(z = \tanh(W_f * x) \odot \sigma(W_g * x)\)，其中 \(*\) 是擴張因果卷積。殘差與跳接連接把訊號傳過整個堆疊。

擴張排程是關鍵設計。擴張量在每層加倍，依序為 1、2、4，直到 512，然後循環重複。一個這樣的循環覆蓋 1,024 個樣本，在 16 kHz 下約為 64 毫秒。訓練時以量化後樣本的似然為目標，所有時間步都平行計算。生成時則一次抽取一個樣本、把它餵回模型，然後重複到輸出的每個樣本為止。

## 結果

- **文字轉語音。** 在五分制的自然度量表上，以語言學特徵與基頻為條件的 WaveNet，英文與中文的分數都在 4.0 以上，高於以 LSTM 為基礎的參數式與拼接式基準系統。與自然語音的差距，英文縮小了 51%，中文縮小了 69%。
- **多語者。** 以說話者代碼為條件的單一模型，從 VCTK 語料庫約 44 小時的資料中產生了 109 種聲音。加入更多語者後，驗證表現有所提升。

## 限制

- **採樣成本。** 生成一秒 16 kHz 的音訊需要 16,000 個依序的步驟。[Parallel WaveNet](https://arxiv.org/abs/1711.10433) 把模型蒸餾成速度快得多的前饋流模型。
- **上下文有限。** 感受野只涵蓋數百毫秒。在無條件的語音中缺乏長程的連貫性，因為模型只能記住自己最後產生的兩到三個音素。
- **對輸入的依賴。** 只用語言學特徵有時會產生錯誤的重音。加入以較低取樣率輸入的基頻後，論文的測試中這個問題便消失了。

## 未解問題

- **長程結構。** 音樂與長篇語音需要數秒或數分鐘的連貫性。先生成離散語意詞元、再填入聲學細節的模型，例如 [AudioLM](https://arxiv.org/abs/2209.03143)，是對此的一種回應。
- **速度與品質。** Parallel WaveNet 說明了如何從慢模型訓練出快模型。快模型能否在沒有教師模型的情況下匹敵原模型，目前仍不清楚。

## 與其他主題的連結

- **影像的對應方法。** [PixelCNN](../pixelcnn/index.md) 提出了閘控遮罩設計，WaveNet 把它改寫為一維版本。
- **語音。** 後續系統見 [語音與音訊](../../../models/speech/index.md) 的介紹。
- **離散編碼。** 以 [VQ-VAE](../../vae/vq-vae/index.md) 的編碼為對象的 WaveNet 先驗，就是該處所述影像設定的音訊版本。

## 應用

- **語音合成。** Parallel WaveNet 已部署於 Google Assistant，服務數個英文與日文聲音（van den Oord 等人，2017）。
- **音樂。** Jukebox 以多尺度 VQ-VAE 壓縮音訊，並以自回歸方式對編碼建模，能產生數分鐘內保持連貫的歌曲（Dhariwal 等人，2020）。
- **語音編解碼器。** VALL-E 把語音合成視為對編解碼詞元的語言建模，只需三秒的提示即可複製聲音（Wang 等人，2023）。

## 參考文獻

### 開創性論文

- van den Oord, A. et al. (2016). *WaveNet: A Generative Model for Raw Audio*. arXiv. https://arxiv.org/abs/1609.03499 — 論文本身：以擴張因果卷積直接處理原始波形，並包含語音與音樂實驗。
- van den Oord, A. et al. (2017). *Parallel WaveNet: Fast High-Fidelity Speech Synthesis*. arXiv. https://arxiv.org/abs/1711.10433 — 把 WaveNet 蒸餾成前饋流模型，速度比即時快 20 倍以上。
- Yu, F. & Koltun, V. (2016). *Multi-Scale Context Aggregation by Dilated Convolutions*. arXiv. https://arxiv.org/abs/1511.07122 — 以擴張卷積在不損失解析度的情況下聚合廣域上下文。
- Dhariwal, P. et al. (2020). *Jukebox: A Generative Model for Music*. arXiv. https://arxiv.org/abs/2005.00341 — 以多尺度 VQ-VAE 的編碼搭配自回歸 Transformer 來建模音樂。
- Borsos, Z. et al. (2022). *AudioLM: a Language Modeling Approach to Audio Generation*. arXiv. https://arxiv.org/abs/2209.03143 — 把音訊生成視為對離散詞元的語言建模。
- Wang, C. et al. (2023). *Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers*. arXiv. https://arxiv.org/abs/2301.02111 — 把文字轉語音視為對編解碼詞元的語言建模。

### 綜述與教科書

- Bond-Taylor, S., Leach, A., Long, Y. & Willcocks, C. G. (2021). *Deep Generative Modelling: A Comparative Review of VAEs, GANs, Normalizing Flows, Energy-Based and Autoregressive Models*. arXiv. https://arxiv.org/abs/2103.04922 — 把自回歸音訊模型放在其他深度生成模型家族之中。
