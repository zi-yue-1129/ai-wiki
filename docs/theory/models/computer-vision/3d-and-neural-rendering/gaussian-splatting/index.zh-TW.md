---
translation_reviewed: 2026-10-28
---

# 3D 高斯濺射

3D 高斯濺射（3D Gaussian splatting，3DGS）以數百萬個顯式的各向異性三維高斯來表示場景。這些高斯由照片最佳化而來，渲染時將其投影到影像上並加以混合。它於 2023 年提出，在即時渲染速率下達到了最先進的視覺品質。它是[三維視覺與神經渲染](../index.md)頁所列的兩種關鍵方法之一。

## 概述

神經輻射場將場景儲存在網路中，每條射線都必須查詢網路許多次，因此渲染緩慢。[^1] 3DGS 保留了輻射場的體積混合方式，但把場景改為一組顯式的基元。這些基元可以用光柵化器繪製、排序並混合，不需要對每個取樣點進行網路查詢。基元可以被拉伸成橢球形，因此少量基元就能涵蓋細長的結構。

## 關鍵概念

- **高斯基元**：包含位置、決定形狀與方向的共變異數矩陣 $\Sigma$、不透明度 $\alpha$，以及顏色係數。各向異性指高斯可以沿不同軸向拉伸。
- **球諧函數**：定義在球面上的基底，其係數讓每個高斯的顏色隨觀看方向而變。
- **濺射**：將三維高斯投影到影像平面上，形成二維橢圓。
- **自適應密度控制**：在最佳化過程中複製、分裂與修剪高斯。

## 運作方式

方法依下列步驟進行。

1. **初始化**：在相機校正（運動結構，structure from motion）產生的每個稀疏點上放置一個高斯。每個高斯一開始為等向性，其半徑由與最近鄰點的距離決定。
2. **參數化**共變異數為 $\Sigma = RSS^{\top}R^{\top}$，由一個尺度向量與一個表示旋轉的四元數組成。這能確保 $\Sigma$ 在最佳化中始終是有效的共變異數矩陣。
3. **渲染**：對每個像素，依深度排序與之重疊的高斯，然後由前往後混合：

$$C=\sum_i T_i\,\alpha_i\,\mathbf c_i,\qquad T_i=\prod_{j<i}(1-\alpha_j).$$

4. **著色**：以觀看方向對球諧係數求值，得到每個高斯的顏色。較高階的項在訓練中逐步引入。
5. **最佳化**：使用損失 $\mathcal L=(1-\lambda)\mathcal L_1+\lambda\mathcal L_{\text{D-SSIM}}$，其中 $\lambda=0.2$。
6. **控制密度**：每 100 次迭代，視空間位置梯度超過 0.0002 的高斯會被複製或分裂，接近透明的高斯則被移除。不透明度會定期重設為接近零。

標準訓練執行 30,000 次迭代。[^2]

## 結果

論文在 Mip-NeRF 360、Tanks and Temples 與 Deep Blending 三個資料集上評估。下表比較 Mip-NeRF 360 場景上 30,000 次迭代的模型與論文中的基準方法。[^2]

| 方法 | PSNR | LPIPS | 訓練時間 | FPS | 記憶體 |
|---|---|---|---|---|---|
| Plenoxels | 23.08 | 0.463 | 25 分 49 秒 | 6.79 | 2.1 GB |
| Instant-NGP（Big） | 25.59 | 0.331 | 7 分 30 秒 | 9.43 | 48 MB |
| Mip-NeRF 360 | 27.69 | 0.237 | 48 小時 | 0.06 | 8.6 MB |
| 3DGS，7K 次迭代 | 25.60 | 0.279 | 6 分 25 秒 | 160 | 523 MB |
| 3DGS，30K 次迭代 | 27.21 | 0.214 | 41 分 33 秒 | 134 | 734 MB |

在這些場景上，Mip-NeRF 360 的 PSNR 較高，但它需要 48 小時的訓練，且只能以每秒 0.06 幀渲染。30K 的模型則有較好的 SSIM 與 LPIPS，並以高於即時的速率渲染。

## 限制

- **觀測不足的區域。** 輸入照片少見到的區域，會產生拉長或「斑駁」的高斯。[^3]
- **跳動（popping）。** 在視角相關外觀的區域中，大型高斯會造成跳動；簡單的可見性演算法也可能使混合順序突然改變。
- **未做正則化。** 論文的最佳化沒有使用正則化，而正則化本可以改善未觀測區域與跳動的問題。
- **記憶體。** 大型場景在訓練時的 GPU 峰值記憶體，在未最佳化的原型中可能超過 20 GB；渲染所需的模型也有數百 MB。[^4]

## 開放問題

- **抗混疊。** 混合順序的突然改變可以靠抗混疊處理，但論文將其留待未來研究。
- **精簡性。** 數百萬個高斯仍然很大；論文建議以點雲壓縮降低記憶體。
- **編輯與表面。** 顯式基元比網路權重更容易編輯，Chen 與 Wang 的綜述也強調了這一點。[^5] 從高斯中擷取乾淨的表面，則不在原始方法的處理範圍內。

[^1]: Kerbl 等人（2023），摘要：近期較快的方法以速度換取品質；論文回報在 1080p 下的即時顯示。
[^2]: Kerbl 等人（2023），表 1，Mip-NeRF 360 欄位。Mip-NeRF 360 那一列的數值取自其原始論文。
[^3]: Kerbl 等人（2023），第 7.4 節：關於觀測不足區域與拉長偽影的限制。
[^4]: Kerbl 等人（2023），關於記憶體使用的討論。
[^5]: Chen 與 Wang（2024），摘要：3D 高斯濺射提供即時渲染，以及前所未有的可編輯性。

## 參考文獻

### 開創性論文

- Kerbl, B., Kopanas, G., Leimkühler, T. & Drettakis, G. (2023). *3D Gaussian Splatting for Real-Time Radiance Field Rendering*. ACM Transactions on Graphics. https://arxiv.org/abs/2308.04079 — 論文本身：由照片最佳化的顯式高斯，並可即時渲染。
- Zwicker, M., Pfister, H., van Baar, J. & Gross, M. (2001). *EWA volume splatting*. Proceedings Visualization 2001 (VIS '01), IEEE. https://doi.org/10.1109/VISUAL.2001.964490 — 用於體積資料的橢圓高斯濺射，是此方法的早期前身。
- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R. & Ng, R. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV. https://arxiv.org/abs/2003.08934 — 3DGS 以顯式基元取代的輻射場方法。
- Müller, T., Evans, A., Schied, C. & Keller, A. (2022). *Instant Neural Graphics Primitives with a Multiresolution Hash Encoding*. ACM Transactions on Graphics. https://arxiv.org/abs/2201.05989 — 論文比較中的快速輻射場基準。
- Barron, J. T., Mildenhall, B., Verbin, D., Srinivasan, P. P. & Hedman, P. (2021). *Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields*. arXiv. https://arxiv.org/abs/2111.12077 — 在 Mip-NeRF 360 場景上品質高但速度慢的基準。

### 綜述與教科書

- Chen, G. & Wang, W. (2024). *A Survey on 3D Gaussian Splatting*. arXiv. https://arxiv.org/abs/2401.03890 — 系統性概覽三維高斯濺射的原理與應用。
