---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/3d-and-neural-rendering
tags:
  - Gaussian splatting
  - neural rendering
  - real-time rendering
aliases:
  - 3D 高斯潑濺
  - 高斯潑濺
  - 3D Gaussian splatting
---

# 三維高斯潑濺

三維高斯潑濺把場景表示為大量顯式的三維高斯分布，每一個都有位置、形狀、不透明度與顏色。這些高斯投影到影像平面上後加以混合，使渲染速度很快。它是作為 [NeRF](nerf.zh-TW.md) 的替代方案出現在視圖合成中，以一組顯式基元取代隱式網路。

## 概觀

[本章](index.zh-TW.md)涵蓋這個領域。本頁說明此方法。每個場景都依據照片與稀疏點雲進行最佳化。結果可以用光柵化渲染，這是圖形硬體上的標準操作，而不必對每個像素多次評估網路。

## 問題

像 NeRF 這樣的輻射場方法品質很高，但渲染與訓練都很慢。問題在於保留體積渲染的品質，同時讓兩者都快到足以互動使用。

## 核心想法

場景是一組各向異性的三維高斯分布。每個高斯有一個均值、一個決定其形狀與方向的協方差、一個不透明度，以及以球諧函數表示、與觀看方向相關的顏色。高斯被投影到相機上成為二維橢圓，並依深度排序合成。參數依據輸入影像以梯度下降最佳化。訓練期間，方法會在重建效果差的地方新增高斯，並移除幾乎透明的高斯，作者稱之為自適應密度控制。

## 方程式

對於一個像素，其顏色是覆蓋它的、依深度排序之高斯 $i$ 的 alpha 混合：

$$C = \sum_{i \in N} c_i \,\alpha_i \prod_{j=1}^{i-1}(1 - \alpha_j)$$

這裡 $c_i$ 是高斯 $i$ 與視角相關的顏色，$\alpha_i$ 是該高斯在像素處評估其二維投影後的不透明度。高斯的三維協方差被分解為旋轉與縮放，這使它在最佳化過程中保持半正定。

## 結果

論文報告，在它評估的場景上能得到高品質的新視角，並能以即時速度在高解析度下渲染，訓練時間也遠比逐場景的 NeRF 最佳化短。確切數字見論文的結果表，此處不重述。

## 限制

- 高斯的數量可能增長得很大，會消耗記憶體。
- 在輸入視角觀察不佳的區域，品質可能下降。
- 此表示法是顯式的，因此方法若需要推理表面或拓撲，就必須謹慎處理。

## 關聯

投影步驟是電腦圖學中潑濺方法的一個實例，Zwicker 等人分析了用於渲染的橢圓加權潑濺 [(Zwicker et al., 2002)](https://doi.org/10.1109/tvcg.2002.1021576)。最佳化所需的梯度，依照[自動微分](../../../math/automatic-differentiation/index.zh-TW.md)中的方式計算。

## 應用

為電影、遊戲與虛擬實境即時擷取與顯示真實世界的場景。與 NeRF 相比，其顯式形式也更容易編輯，並能與網格管線結合。

## 開放問題

- 如何在不損失細節的前提下，控制基元的數量？
- 高斯表示法應如何處理動態場景與光照變化？

## 參考文獻

### 奠基性論文

- Kerbl、Kopanas、Leimkuehler 與 Drettakis，*3D Gaussian Splatting for Real-Time Radiance Field Rendering*，ACM Transactions on Graphics（2023）。https://doi.org/10.1145/3592433 — 介紹此方法、其最佳化與光柵化渲染器的論文。
- Mildenhall、Srinivasan、Tancik、Barron、Ramamoorthi 與 Ng，*NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*，European Conference on Computer Vision（2020）。https://doi.org/10.1007/978-3-030-58452-8_24 — 此方法所比較的隱式輻射場方法。
- Barron 等人，*Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*，IEEE/CVF International Conference on Computer Vision（2021）。https://doi.org/10.1109/iccv48922.2021.00580 — 抗混疊的輻射場變體，作為品質比較的對照。

### 綜述與教科書

- Zwicker、Pfister、van Baar 與 Gross，*EWA Splatting*，IEEE Transactions on Visualization and Computer Graphics（2002）。https://doi.org/10.1109/tvcg.2002.1021576 — 橢圓加權平均潑濺，是把高斯投影到影像上的經典方法。
- Kajiya 與 Von Herzen，*Ray tracing volume densities*，SIGGRAPH（1984）。https://doi.org/10.1145/964965.808594 — 電腦圖學中體積渲染的早期公式。
