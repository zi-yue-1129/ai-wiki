# 藝術、媒體與創作

## 依媒介的工具

| 媒介 | 能力 | 例子 |
|---|---|---|
| 圖像 | 文字生圖、編輯、局部重繪、風格轉換、放大 | Midjourney、DALL·E／GPT 影像生成、Stable Diffusion、Flux、Adobe Firefly、Imagen |
| 影片 | 文字或圖片生成影片、編輯、口型同步、虛擬人像 | Sora、Veo、Kling、Runway、Pika |
| 音樂與聲音 | 歌曲生成、音軌分離、母帶處理、語音 | Suno、Udio、MusicGen、ElevenLabs |
| 寫作 | 草擬、編修、腦力激盪、互動式小說 | LLM 助理 |
| 3D 與遊戲 | 素材生成、貼圖、動畫 | 3D 生成模型、從影片擷取動作 |
| 設計 | 版面、標誌、UI 草圖 | 內建生成功能的設計工具 |
| 電影與視覺特效 | 去背（rotoscoping）、年齡調整、預演、配音 | 製作公司的流程 |

## 創造力研究

- **AI 有創造力嗎？** Boden 區分了組合式、探索式與轉換式的創造力（Boden, 2009）；多數生成式 AI 擅長前兩種
- **人機共創**：研究發現，AI 的點子可能提高個人的創意評分，卻降低各人產出的**多樣性**（Doshi & Hauser, 2024, *Science Advances*）
- **計算創造力**是一個歷史悠久的研究領域（AARON、EMI／David Cope）

## 著作權與所有權

訓練資料與 AI 輸出的所有權，在多個國家的法院與立法機關仍有爭議，規則尚未定論。引用任何特定立場前，請查閱目前的判決與官方指引。

## 來源與不實資訊

- 政治上的深偽（deepfake）與未經同意的私密影像
- **內容憑證**（C2PA）、隱形浮水印（SynthID）與平台標示
- 偵測是一場軍備競賽，單靠偵測並不可靠

## 對創意工作的經濟影響

在生成式 AI 推出後，部分自由撰稿與插畫工作的需求下降（Hui et al., 2024），同時也有創作者利用 AI 擴大產出。見[經濟與就業](../../society/economics/index.md)。

## 關鍵方法

下列三種方法構成多數影像與影片生成器的基礎。每一項都連結到解釋該方法的頁面。

- [去噪擴散](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)：模型學習逆轉逐步加噪的過程（Ho et al., 2020）。
- [潛在擴散](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/latent-diffusion.md)：在壓縮的潛在空間中做擴散，使高解析度影像生成變得可行（Rombach et al., 2022）。
- [無分類器引導](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/classifier-free-guidance.md)：不需獨立分類器，即可把樣本導向文字提示（Ho & Salimans, 2022）。

## 參考文獻

### 開創性論文

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 本頁連結的擴散方法頁所依據的 DDPM 論文。
- Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. arXiv. https://arxiv.org/abs/2112.10752 — 潛在擴散，在壓縮的潛在空間中進行擴散。
- Ho & Salimans (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — 不需獨立分類器，即可把擴散樣本導向提示詞。
- Doshi & Hauser (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*. https://doi.org/10.1126/sciadv.adn5290 — 發現 AI 點子提高個人創意，卻降低各作者作品的多樣性。
- Boden (2009). Computer Models of Creativity. *AI Magazine*. https://doi.org/10.1609/aimag.v30i3.2254 — 計算創造力的回顧，包含三種創造力類型。
- Epstein et al. (2023). Art and the science of generative AI. *Science*. https://doi.org/10.1126/science.adh4451 — 概述生成式 AI 在藝術中的用途，以及它對創作者的影響。

### 文章與文件

- Hui et al. (2024). The Short-Term Effects of Generative Artificial Intelligence on Employment: Evidence from an Online Labor Market. *Organization Science*. https://doi.org/10.1287/orsc.2023.18441 — 線上勞動市場研究，探討生成式 AI 對自由接案需求的影響。
