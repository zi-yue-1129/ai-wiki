# 生成模型

生成模型學習資料分布 \(p(x)\)，並能**產生新的樣本**；判別模型則學習 \(p(y\mid x)\)。

生成式建模是一種**方法**，而不是一種架構。[模型](../models/index.md)中的任何家族，例如卷積、循環、Transformer 或狀態空間網路，都可以訓練成生成模型。下面各節的家族是生成式演算法，差別在於它們如何表示分布，以及如何從中取樣。

## 模型家族

| 家族 | 核心想法 | 優點 | 缺點 | 例子 |
|---|---|---|---|---|
| 自回歸 | \(p(x)=\prod_t p(x_t\mid x_{<t})\) | 可精確計算似然，擴展性好 | 採樣必須依序進行 | GPT、PixelCNN、WaveNet |
| VAE | 編碼到潛在空間再解碼；最大化 ELBO | 潛在空間有結構 | 樣本較模糊 | VAE、VQ-VAE |
| GAN | 生成器對判別器 | 樣本清晰，採樣快 | 不穩定，模式崩潰 | StyleGAN、BigGAN |
| 正規化流 | 可逆的變換 | 可精確計算似然 | 架構受限 | RealNVP、Glow |
| 擴散模型 | 學習逐步去除雜訊 | 品質高、穩定、多樣 | 採樣步數多（已大幅改善） | DDPM、Stable Diffusion、Imagen |
| 流匹配（Flow matching） | 學習從雜訊到資料的速度場 | 訓練簡單，採樣快 | — | Stable Diffusion 3、Flux |
| 能量基模型 | 學習能量函數 \(E(x)\) | 彈性高 | 採樣困難 | Hopfield 網路、EBM |

## 生成對抗網路

完整說明，並為各代表性方法（原始 GAN、DCGAN、Wasserstein GAN）各設一頁：[生成對抗網路](gan/index.md)。GAN 以訓練不穩定換取一次前向傳播的快速取樣；擴散模型則以較多的取樣步數換取穩定的訓練。

## 擴散模型

完整說明包含比較表，以及每個方法各自的頁面（DDPM、DDIM、潛在擴散、DiT、無分類器引導），見[擴散模型](diffusion/index.md)。

![擴散模型動態概念圖：從雜訊開始，經過多個去噪步驟逐漸產生具有結構的樣本。](../../assets/concept-animations/diffusion-denoising.gif)

*動態概念圖 · 原創示意，CC BY-SA 4.0。*

**動畫解讀：** 生成時從雜訊開始，反覆透過學到的反向過程逐步去噪，最後形成具有結構的樣本。像素圖只是**概念示意，並非真正模型生成的影像**。模型訓練所用的正向過程則是逐步為乾淨資料加入雜訊。

**前向過程**：逐步加入高斯雜訊，直到資料變成純雜訊。
**反向過程**：訓練一個網路在每一步預測雜訊；生成時從純雜訊開始逐步去噪。

簡化的目標函數：

\[
L = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

關鍵技術：

- **潛在擴散**：在 VAE 的潛在空間中進行擴散，大幅降低成本（Stable Diffusion）
- **無分類器引導（classifier-free guidance）**：在提示遵循度與多樣性之間取捨
- **擴散 Transformer（DiT）**：以 Transformer 取代 U-Net 作為去噪器；廣泛用於影片生成
- **快速採樣**：DDIM、DPM-Solver、一致性模型、蒸餾——從約 1000 步降到幾步甚至一步
- **控制**：ControlNet、LoRA、IP-Adapter

## 應用領域

- 影像、影片、3D、音樂、語音（見[多模態模型](../models/multimodal/index.md)、[藝術與創作](../../applications/creative/index.md)）
- 蛋白質設計（RFdiffusion）、分子與材料生成（見[生命科學](../../applications/life-science/index.md)）
- 天氣（GenCast 以擴散模型產生機率預報）
- 機器人策略（Diffusion Policy）
- 資料擴增與合成資料

## 與大腦的連結

- **以生成模型進行感知推論**：Helmholtz 的「無意識推論」與預測編碼認為，大腦使用內部的生成模型來預測並解釋感官輸入
- **Helmholtz 機器與醒睡演算法**（Hinton et al., 1995）：受睡眠啟發的生成模型訓練方式
- **夢與想像**：一種假說把夢視為大腦生成模型的離線樣本，有助於泛化（Hoel, 2021，「過度擬合的大腦假說」）
- **以擴散模型從 fMRI 重建影像**（Takagi & Nishimoto, 2023）——見[腦機介面](../../brain-mind/bci/index.md)

## 學習資源

- Lilian Weng，"What are Diffusion Models?"
- Hugging Face Diffusion Models Course
- Stanford CS236，*Deep Generative Models*
- Yang Song，"Generative Modeling by Estimating Gradients of the Data Distribution"
- *Understanding Deep Learning*，第 14–18 章

## 參考文獻

### 開創性論文

- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1406.2661 — 提出 GAN：生成器與判別器彼此對抗地訓練。
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — 變分自編碼器，一種以重參數化的變分下界訓練的潛在變數模型。
- Ho, J., et al. (2020). *Denoising Diffusion Probabilistic Models*. arXiv. https://arxiv.org/abs/2006.11239 — 顯示學習逆轉逐步加噪的過程，能產生高品質的影像。
- Rombach, R., et al. (2022). *High-Resolution Image Synthesis with Latent Diffusion Models*. CVPR. https://arxiv.org/abs/2112.10752 — 在壓縮後的潛在空間中進行擴散，即 Stable Diffusion 採用的方法。

### 綜述與教科書

- Yang, L., et al. (2022). *Diffusion Models: A Comprehensive Survey of Methods and Applications*. arXiv. https://arxiv.org/abs/2209.00796 — 綜述擴散方法及其在視覺、音訊與其他領域的應用。

### 文章與文件

- Weng, L. (2021). *What are Diffusion Models?* Lil'Log. https://lilianweng.github.io/posts/2021-07-11-diffusion-models/ — 清楚推導擴散模型的訓練目標及其變體，並附有圖解。
