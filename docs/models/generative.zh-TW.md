# 生成模型

生成模型學習資料分布 \(p(x)\)，能**產生新樣本**。判別模型則學 \(p(y\mid x)\)。

## 主要家族

| 家族 | 核心想法 | 優點 | 缺點 | 代表 |
|---|---|---|---|---|
| 自迴歸模型 | \(p(x)=\prod_t p(x_t\mid x_{<t})\) | 精確概似、可擴展 | 逐步生成較慢 | GPT、PixelCNN、WaveNet |
| VAE | 編碼到潛在空間再解碼，最大化 ELBO | 有結構的潛在空間 | 樣本較模糊 | VAE、VQ-VAE |
| GAN | 生成器與判別器對抗 | 樣本銳利、生成快 | 訓練不穩、模式崩塌 | StyleGAN、BigGAN |
| 正規化流 | 可逆變換、精確概似 | 精確概似 | 架構受限 | RealNVP、Glow |
| 擴散模型 | 學習逐步去噪 | 品質高、穩定、多樣 | 取樣步數多（已大幅改善） | DDPM、Stable Diffusion、Imagen |
| 流匹配 | 學習從雜訊到資料的速度場 | 訓練簡單、取樣快 | — | Stable Diffusion 3、Flux 等 |
| 能量模型 | 學能量函數 \(E(x)\) | 彈性大 | 取樣困難 | Hopfield、EBM |

## 擴散模型

**前向過程**：逐步對資料加高斯雜訊，直到變成純雜訊。
**反向過程**：訓練神經網路預測每一步加入的雜訊，從純雜訊一步步還原出資料。

訓練目標（簡化）：

\[
L = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

關鍵技術：

- **潛在擴散（Latent Diffusion）**：在 VAE 的潛在空間擴散，大幅降低成本（Stable Diffusion）
- **無分類器引導（CFG）**：平衡條件遵循與多樣性
- **DiT（Diffusion Transformer）**：以 Transformer 取代 U-Net 作為去噪網路，影片生成（Sora 等）多採此類架構
- **快速取樣**：DDIM、DPM-Solver、一致性模型、蒸餾，從上千步降到數步甚至一步
- **控制**：ControlNet、LoRA、IP-Adapter

## 應用範圍

- 影像、影片、3D、音樂、語音生成（見 [多模態](multimodal.md)、[藝術創作](../applications/creative.md)）
- 蛋白質設計（RFdiffusion）、分子生成、材料設計（見 [生命科學](../applications/life-science.md)）
- 天氣預報（GenCast 以擴散模型做機率性預報）
- 機器人策略（Diffusion Policy）
- 資料增強與合成資料

## 與大腦的關聯

- **生成模型作為知覺理論**：Helmholtz 的「無意識推論」、預測編碼都主張大腦有一個生成模型，用來預測與解釋感官輸入
- **Helmholtz 機器與 wake-sleep 演算法**（Hinton et al., 1995）：受睡眠啟發的生成模型訓練法
- **夢與想像**：有假說認為作夢是大腦生成模型的離線取樣，有助於泛化（Hoel 2021〈過擬合大腦假說〉）
- **從 fMRI 重建影像**：用擴散模型把腦活動解碼成看到的影像（Takagi & Nishimoto, 2023），見 [腦機介面](../brain-mind/bci.md)

## 學習資源

- Lilian Weng〈What are Diffusion Models?〉
- Hugging Face Diffusion Models Course
- Stanford CS236《Deep Generative Models》
- Yang Song〈Generative Modeling by Estimating Gradients of the Data Distribution〉
- 《Understanding Deep Learning》第 14–18 章
