---
translation_reviewed: 2026-10-28
---

# 三維視覺與神經渲染

三維視覺從一組影像中還原場景的深度、形狀與相機位置；神經渲染則根據學習得到的場景模型，產生同一場景的新影像。現代系統將兩者結合：由網路估計幾何，同時以學習得到的場景表示，例如[神經輻射場](nerf/index.md)與[3D 高斯濺射](gaussian-splatting/index.md)，渲染出從未拍攝過的相機位置所見的逼真影像。

## 概述

照片會丟失深度。位於不同距離的點可能呈現相同的顏色，因此一張照片可以對應許多種三維場景。人類通常在不自覺的情況下，靠著立體視差、運動視差、陰影與透視來解決這個歧義。電腦視覺試圖從像素中還原同樣的資訊：每個點有多遠、表面是什麼樣子、相機位於何處。神經渲染則是反向的過程：給定一個場景的模型，它預測從新視角拍下的影像，這項任務稱為*新視角合成*。

傳統系統使用顯式的幾何，例如網格與體素格。從約 2020 年起，場景改以神經網路的權重來儲存，並以照片擬合。2023 年，顯式的高斯基元讓即時顯示的速率重新達成。[^1]

本頁涵蓋深度估計、點雲、輻射場與生成式三維。二維影像生成則見[生成模型](../../../generative/index.md)。

## 關鍵概念

- **深度圖**：每個像素的值為該像素所見表面到相機的距離。從單張影像估計深度是不適定問題，而整體尺度是最大的不確定來源。[^2]
- **點雲**：由三維點組成的無序集合，來自深度感測器（例如 LiDAR）或重建。由於點的順序不具意義，處理點雲的網路必須具備排列不變性。[^3]
- **輻射場**：對每個三維點、每個觀看方向，給出顏色與密度的函數。密度描述一點吸收或發出光線的強弱。
- **體積渲染**：沿相機射線將各點的顏色加總以形成像素，權重由密度與透射率決定。
- **可微分渲染**：輸出會隨場景參數平滑變化的渲染器，因此渲染出的像素與拍攝的像素可以透過梯度下降來對齊。
- **分數蒸餾**：以預訓練的二維擴散模型作為三維模型渲染結果的評判者。[^4]

## 運作方式

多數現代三維系統共用同一個迴圈。一個帶有可學習參數的場景表示，依已知或估計的相機姿態進行渲染；渲染出的像素與照片比較；誤差再反向傳播回參數。當損失夠小時，參數本身就是三維模型。

```mermaid
flowchart LR
  P[照片與相機姿態] --> R[場景表示：網路、格點或高斯]
  R --> D[可微分渲染器]
  D --> C[渲染出的像素]
  C -- 與照片比較的損失 --> U[梯度更新]
  U -. 更新參數 .-> R
```

各個方向的差異，在於它們預測什麼，以及最佳化什麼。

**由影像估計深度。** Eigen 等人（2014）以兩個堆疊的網路從單張照片預測深度：一個產生粗略的全域深度圖，另一個做局部精修，並以尺度不變的誤差訓練。[^5] MiDaS 混合了標註不相容的多個資料集，並使用對深度範圍與尺度變化不變的損失。[^6] Depth Anything 將訓練資料擴充到數千萬張無標籤影像，由自動流程加上標註，並報告了強勁的零樣本結果。[^7] DUSt3R 採取不同的路線：從兩張或更多張影像、無需已知的校正參數，回歸出一張*點圖*，即共用座標系中每個像素對應的三維位置，並使用標準的 Transformer 編碼器與解碼器。[^8]

**點雲。** PointNet 直接處理原始的點集合。每個點通過一個共用的多層感知器，再以對稱的池化運算合併結果，因此輸出不依賴點的順序。它可用於分類、部件分割與場景解析。[^9] PointNet++ 以階層方式套用同樣的想法，在巢狀的鄰域上擷取局部結構，同時也保留整體形狀。[^10]

**輻射場。** NeRF 以多層感知器，將三維位置與觀看方向映射為顏色與密度，並沿著射線積分來渲染像素。3D 高斯濺射保留了可微分渲染的迴圈，但改用顯式的各向異性高斯，在 GPU 上投影並混合。兩者各有專頁：[NeRF](nerf/index.md) 與[3D 高斯濺射](gaussian-splatting/index.md)。

**生成式三維。** 生成式三維借用二維擴散模型的先驗知識，因為三維訓練資料稀少。DreamFusion 最佳化一個 NeRF，使其從隨機視角渲染的影像，在凍結的文字生成影像擴散模型眼中看起來合理，且不需要任何三維訓練資料。[^11] Zero-1-to-3 微調擴散模型，使其能改變單一物件的視角，並以合成資料學習相機的控制方式。[^12]

## 關鍵方法

以下比較兩種代表性方法。每一項都連結到自己的頁面，其中有方程式、結果與限制。

| 方法 | 年份 | 表示方式 | 差異所在 | 頁面 |
|---|---|---|---|---|
| NeRF | 2020 | 隱式：沿相機射線查詢的 MLP | 以體積積分渲染的連續場景函數；每個場景訓練與渲染都慢 | [NeRF](nerf/index.md) |
| 3D 高斯濺射 | 2023 | 顯式：數百萬個各向異性三維高斯 | 以光柵化取代逐射線行進；配合快速的最佳化即可即時渲染 | [3D 高斯濺射](gaussian-splatting/index.md) |

## 連結

- **大腦與心智。** 雙眼視差，也就是兩眼影像之間的微小差異，是深度的強線索。Marr 與 Poggio（1979）提出視覺系統如何配對兩張影像以還原深度的理論。[^13] Hubel 與 Wiesel（1962）描述了貓視覺皮質中，會回應來自雙眼輸入的神經元。[^14] 另見[知覺與視覺系統](../../../../brain-mind/visual-perception/index.md)與[視覺皮質的感受野](../../../../brain-mind/neuroscience/receptive-fields-hubel-wiesel/index.md)。大腦是否以與輻射場相似的形式儲存場景，目前尚不清楚。
- **Transformer。** DUSt3R 使用 Transformer 編碼器與解碼器。見[視覺 Transformer](../../transformer/vision-transformer/index.md)。
- **擴散模型。** 分數蒸餾與以視角為條件的生成，都依賴[擴散模型](../../../generative/diffusion/index.md)。
- **自監督。** Depth Anything 從大量無標籤影像中學習，這與[自監督學習](../../../paradigms/self-supervised/index.md)所探討的設定相同。

## 應用

- **自動駕駛。** 深度估計與 LiDAR 點雲，能在三維中定位車輛、行人與車道。見[自動駕駛](../../../../applications/autonomous-driving/index.md)。
- **電影、遊戲與虛擬製作。** 擷取的場景可以沿新的相機路徑渲染，生成的資產也能放入場景中。Tewari 等人（2021）以綜述的方式介紹神經渲染在逼真合成上的應用。[^1] 見[藝術、媒體與創意](../../../../applications/creative/index.md)。
- **機器人與地圖建構。** 深度與三維地圖支援導航與物件操作。

## 開放問題

- **尺度與公制深度。** 相對深度比以公尺計的深度更容易學習。Depth Anything 在以公制標籤微調後回報了強勁的結果。[^7]
- **稀疏與無界場景。** 當照片稀少或場景無界時，輻射場會產生模糊或偽影。Mip-NeRF 360 部分處理了這個問題。[^15]
- **幾何或外觀。** 輻射場方法以渲染出的影像來評判，但許多應用需要精確的表面，而從中擷取的表面往往不如影像精確。
- **前饋式或逐場景最佳化。** DUSt3R 以單次前向計算預測幾何，而 NeRF 與高斯濺射則逐場景最佳化。前饋式模型能否達到最佳化的品質，尚未確定。
- **一致性。** 二維先驗是逐一評判每個視角，因此生成的物件在不同視角間可能不一致。

[^1]: Tewari 等人（2021）與 Xie 等人（2021）回顧了這個領域。Kerbl 等人（2023）回報在 1080p 下的即時渲染。
[^2]: Eigen 等人（2014），摘要：不確定性的主要來源是整體尺度。
[^3]: Qi 等人（2016），摘要：點雲沒有固定的結構，因此網路必須尊重點的排列不變性。
[^4]: Poole 等人（2022），摘要：二維擴散模型作為最佳化參數化影像生成器的先驗。
[^5]: Eigen 等人（2014），摘要：先做粗略的全域預測，再做局部精修，並使用尺度不變的誤差。
[^6]: Ranftl 等人（2019），摘要：目標函數對深度範圍與尺度的變化不敏感，且可以混合多個資料集。
[^7]: Yang 等人（2024），摘要：約 6,200 萬張無標籤影像經自動標註；以 NYUv2 與 KITTI 的公制深度微調後，建立了新的最佳結果。
[^8]: Wang 等人（2023），摘要：不需要事先的校正或姿態資訊。
[^9]: Qi 等人（2016），摘要：同一架構涵蓋物件分類、部件分割與場景語意解析。
[^10]: Qi 等人（2017），標題：在度量空間中的點集合上進行階層式特徵學習。
[^11]: Poole 等人（2022），摘要：隨機初始化的 NeRF 經最佳化後，其渲染結果在擴散先驗下達到低損失。
[^12]: Liu 等人（2023），摘要：模型以合成資料訓練，並能零樣本泛化到真實世界的影像。
[^13]: Marr 與 Poggio（1979），標題：人類立體視覺如何配對影像以還原深度的計算理論。
[^14]: Hubel 與 Wiesel（1962），標題：貓視覺皮質中的雙眼交互作用。
[^15]: Barron 等人（2021，*Mip-NeRF 360*），摘要：NeRF 類模型在無界場景上會產生模糊的渲染結果。

## 參考文獻

### 開創性論文

- Marr, D. & Poggio, T. (1979). *A computational theory of human stereo vision*. Proceedings of the Royal Society of London, Series B. https://doi.org/10.1098/rspb.1979.0029 — 提出視覺系統如何配對兩眼影像以還原深度。
- Hubel, D. H. & Wiesel, T. N. (1962). *Receptive fields, binocular interaction and functional architecture in the cat's visual cortex*. The Journal of Physiology. https://doi.org/10.1113/jphysiol.1962.sp006837 — 描述貓視覺皮質中的感受野與雙眼交互作用。
- Eigen, D., Puhrsch, C. & Fergus, R. (2014). *Depth Map Prediction from a Single Image using a Multi-Scale Deep Network*. NeurIPS. https://arxiv.org/abs/1406.2283 — 由粗到細的雙網路，用於單張影像深度估計，並以尺度不變誤差訓練。
- Ranftl, R., Lasinger, K., Hafner, D., Schindler, K. & Koltun, V. (2019). *Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer*. arXiv. https://arxiv.org/abs/1907.01341 — 以混合資料集訓練單一深度模型，並採用對深度範圍與尺度不變的損失。
- Yang, L., Kang, B., Huang, Z., Xu, X., Feng, J. & Zhao, H. (2024). *Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data*. CVPR. https://arxiv.org/abs/2401.10891 — 以約 6,200 萬張無標籤影像訓練的單目深度基礎模型。
- Wang, S., Leroy, V., Cabon, Y., Chidlovskii, B. & Revaud, J. (2023). *DUSt3R: Geometric 3D Vision Made Easy*. arXiv. https://arxiv.org/abs/2312.14132 — 以單一模型從未標定姿態的影像回歸點圖。
- Qi, C. R., Su, H., Mo, K. & Guibas, L. J. (2016). *PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation*. arXiv. https://arxiv.org/abs/1612.00593 — 以排列不變池化直接處理原始點雲的網路。
- Qi, C. R., Yi, L., Su, H. & Guibas, L. J. (2017). *PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space*. NeurIPS. https://arxiv.org/abs/1706.02413 — PointNet 的階層式擴展，在巢狀的點鄰域上學習特徵。
- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R. & Ng, R. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV. https://arxiv.org/abs/2003.08934 — 以神經輻射場表示靜態場景，並由已知姿態的照片最佳化。
- Kerbl, B., Kopanas, G., Leimkühler, T. & Drettakis, G. (2023). *3D Gaussian Splatting for Real-Time Radiance Field Rendering*. ACM Transactions on Graphics. https://arxiv.org/abs/2308.04079 — 由照片最佳化的顯式各向異性高斯，並可即時渲染。
- Poole, B., Jain, A., Barron, J. T. & Mildenhall, B. (2022). *DreamFusion: Text-to-3D using 2D Diffusion*. arXiv. https://arxiv.org/abs/2209.14988 — 將凍結的二維擴散模型蒸餾到 NeRF 中，以生成文字到三維的內容。
- Liu, R., Wu, R., Van Hoorick, B., Tokmakov, P., Zakharov, S. & Vondrick, C. (2023). *Zero-1-to-3: Zero-shot One Image to 3D Object*. ICCV. https://arxiv.org/abs/2303.11328 — 以視角為條件的擴散模型，為單一物件生成新視角影像。

- Barron, J. T., Mildenhall, B., Verbin, D., Srinivasan, P. P. & Hedman, P. (2021). *Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields*. arXiv. https://arxiv.org/abs/2111.12077 — 將 NeRF 擴展到無界的 360 度場景。

### 綜述與教科書

- Tewari, A., Thies, J., Mildenhall, B., Srinivasan, P., Tretschk, E., Wang, Y., et al. (2021). *Advances in Neural Rendering*. arXiv. https://arxiv.org/abs/2111.05849 — 神經渲染及其場景表示的綜述。
- Xie, Y., Takikawa, T., Saito, S., Litany, O., Yan, S., Khan, N., et al. (2021). *Neural Fields in Visual Computing and Beyond*. arXiv. https://arxiv.org/abs/2111.11426 — 回顧視覺運算中以座標為輸入的神經場，涵蓋形狀、場景與外觀。
- Chen, G. & Wang, W. (2024). *A Survey on 3D Gaussian Splatting*. arXiv. https://arxiv.org/abs/2401.03890 — 系統性概覽三維高斯濺射的原理與應用。
