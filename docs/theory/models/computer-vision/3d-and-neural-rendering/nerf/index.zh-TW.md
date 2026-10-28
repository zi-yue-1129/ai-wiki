---
translation_reviewed: 2026-10-28
---

# 神經輻射場（NeRF）

神經輻射場（Neural Radiance Fields，NeRF）以多層感知器表示靜態場景：輸入三維位置與觀看方向，輸出顏色與體積密度，再沿著相機射線積分來渲染像素。它於 2020 年提出，成為由照片進行新視角合成的參考方法。它是[三維視覺與神經渲染](../index.md)頁所列的兩種關鍵方法之一。

## 概述

在 NeRF 之前，學習式的新視角合成依賴離散的結構。體素格受限於解析度；或者採用每條射線只有一個深度的網路，會使細節被平滑掉。[^1]

NeRF 以單一的連續函數取代這些結構，並透過可微分渲染，僅以每個場景的已知姿態照片來擬合這個函數。

## 關鍵概念

- **輸入與輸出**：輸入一個點 $(x, y, z)$ 與一個觀看方向，輸出密度 $\sigma$ 與顏色 $\mathbf{c}$，因此顏色可隨觀看角度而變。
- **位置編碼**：將輸入映射為不同頻率的正弦與餘弦函數；沒有它，網路難以重現精細的細節。
- **階層式取樣**：粗網路找出密度所在的位置，細網路則在那裡密集取樣。

## 運作方式

以 $\mathbf r(t)=\mathbf o+t\mathbf d$ 表示由相機出發的射線，論文中的連續渲染積分為

$$C(\mathbf r)=\int_{t_n}^{t_f} T(t)\,\sigma(\mathbf r(t))\,\mathbf c(\mathbf r(t),\mathbf d)\,dt,\qquad T(t)=\exp\!\Big(-\int_{t_n}^{t}\sigma(\mathbf r(s))\,ds\Big).$$

沿每條射線以分層取樣近似此積分，即得到 alpha 合成：

$$\hat C(\mathbf r)=\sum_{i=1}^{N} T_i\,(1-e^{-\sigma_i\delta_i})\,\mathbf c_i,\qquad T_i=\exp\Big(-\sum_{j<i}\sigma_j\delta_j\Big),$$

其中 $\delta_i$ 為相鄰取樣點之間的距離。每個輸入座標先被編碼為八度頻率的正弦與餘弦，位置使用 $L=10$，方向使用 $L=4$。

一個訓練步驟如下。

1. 取一批 4096 條射線，每個被取樣的像素對應一條。
2. 在 $N_c=64$ 個分層取樣點上評估粗網路，並合成顏色 $\hat C_c$。
3. 利用粗網路的權重，再放置 $N_f=128$ 個取樣點，評估細網路，並合成 $\hat C_f$。
4. 以 Adam 最小化 $\hat C_c$ 與 $\hat C_f$ 相對於照片顏色的平方誤差。

訓練需要 10 萬至 30 萬次迭代，每個場景在一張 NVIDIA V100 上約需一到兩天。[^2]

## 結果

在所比較的方法中，NeRF 在每個基準上的 PSNR 都最高；在真實的前向拍攝場景上，LLFF 的 LPIPS 略優。[^3]

| 方法 | 合成 360° 漫反射場景 | 合成 360° 寫實場景 | 真實前向拍攝場景 |
|---|---|---|---|
| SRN | 33.20 | 22.26 | 22.84 |
| NV | 29.62 | 26.05 | 未報告 |
| LLFF | 34.38 | 24.88 | 24.13 |
| NeRF | 40.15 | 31.01 | 26.50 |

基準方法每個場景至少需要 12 小時的訓練，而 NeRF 的權重約為 5 MB。[^4]

## 限制

- **逐場景最佳化。** 每個場景都需要自己的網路，並從頭訓練。
- **渲染緩慢。** 渲染一張影像需要 1.5 億至 2 億次網路查詢；論文回報在 V100 上約需 30 秒渲染一幀。[^2]
- **靜態場景。** 移動的內容與變化的光線不在此方法的範圍內。
- **混疊與無界場景。** 每個像素只用一條射線，會使不同尺度的精細細節變得模糊；內容位於任意距離的場景仍然困難。[^5][^6]

## 開放問題

- **速度。** 哈希格點編碼能將訓練縮短至數秒，並在 1080p 下把渲染縮短至數十毫秒。[^7] 顯式的基元後來達到了即時速率；見[3D 高斯濺射](../gaussian-splatting/index.md)。
- **跨場景泛化。** 一個網路能否在不做逐場景最佳化的前提下，為未見過的場景產生輻射場，仍是活躍的研究問題。
- **編輯與幾何。** 存在權重中的場景難以編輯，而從密度中擷取的表面往往含有雜訊。

[^1]: Mildenhall 等人（2020），第 6.3 節：SRN 每條射線只保留一個深度與顏色；NV 的顯式 128³ 體素格無法在高解析度下擴展到精細細節。
[^2]: Mildenhall 等人（2020），第 5.3 節與附錄 A：約 10 萬至 30 萬次迭代；以論文的射線數計，每幀約 30 秒。
[^3]: Mildenhall 等人（2020），表 1，PSNR 數值；論文亦回報 SSIM 與 LPIPS。NV 未在真實前向拍攝資料上報告，因為它只重建有界範圍內的物件。
[^4]: Mildenhall 等人（2020），第 6.3 節：LLFF 在一個寫實合成場景上需要超過 15 GB，而 NeRF 約為 5 MB。
[^5]: Barron 等人（2021，*Mip-NeRF*），摘要：以錐形截頭體取代射線，可減少混疊。
[^6]: Barron 等人（2021，*Mip-NeRF 360*），摘要：NeRF 類模型在無界場景中表現不佳。
[^7]: Müller 等人（2022），摘要：多解析度哈希編碼使訓練在數秒內完成，並在 1920×1080 下以數十毫秒渲染。

## 參考文獻

### 開創性論文

- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R. & Ng, R. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV. https://arxiv.org/abs/2003.08934 — 論文本身：以體積渲染擬合的連續五維場景函數。
- Barron, J. T., Mildenhall, B., Tancik, M., Hedman, P., Martin-Brualla, R. & Srinivasan, P. P. (2021). *Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*. ICCV. https://arxiv.org/abs/2103.13415 — 以錐形截頭體取代射線，減少 NeRF 渲染中的混疊。
- Barron, J. T., Mildenhall, B., Verbin, D., Srinivasan, P. P. & Hedman, P. (2021). *Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields*. arXiv. https://arxiv.org/abs/2111.12077 — 以非線性參數化將 NeRF 擴展到無界的 360 度場景。
- Müller, T., Evans, A., Schied, C. & Keller, A. (2022). *Instant Neural Graphics Primitives with a Multiresolution Hash Encoding*. ACM Transactions on Graphics. https://arxiv.org/abs/2201.05989 — 以哈希格點編碼與融合的 GPU 核心，加速訓練與渲染。

### 綜述與教科書

- Tewari, A., Thies, J., Mildenhall, B., Srinivasan, P., Tretschk, E., Wang, Y., et al. (2021). *Advances in Neural Rendering*. arXiv. https://arxiv.org/abs/2111.05849 — 神經渲染及其所用場景表示的綜述。
