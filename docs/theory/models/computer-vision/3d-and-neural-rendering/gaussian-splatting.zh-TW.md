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

三維高斯潑濺把場景表示為一組顯式的三維高斯分布，每一個都有位置、協方差、不透明度與依觀看方向而變的顏色。這些高斯投影到影像平面後加以混合，因而能即時渲染。它是隱式 [NeRF](nerf.zh-TW.md) 表示法的顯式替代方案。

## 概觀

[本章](index.zh-TW.md)涵蓋這個領域。本頁說明此方法。場景依據輸入照片與稀疏點雲進行最佳化。

## 問題

像 NeRF 這樣的輻射場方法能產生高品質的渲染，但對每個像素多次評估網路很慢。論文的目標是保留體積渲染的品質，同時改用光柵化器達到即時速率。

## 核心想法

每個高斯有一個均值、一個協方差、一個不透明度，以及以階數最高為 3 的球諧函數表示的顏色，使顏色依觀看方向而變。協方差由旋轉與縮放建構。最佳化期間，方法每 100 次迭代進行一次稠密化：在位置梯度超過 0.0002 的地方新增高斯，並把過大的高斯依縮放除以 1.6 來分裂。它也會移除幾乎透明的高斯，並每 3000 次迭代重設一次不透明度。論文稱之為密度控制。

## 方程式

每個高斯的協方差為

$$\Sigma = R S S^\top R^\top$$

其中 $R$ 為旋轉，$S$ 為對角縮放。對於一個像素，其顏色是覆蓋它的、依深度排序之高斯 $i$ 的 alpha 混合：

$$C = \sum_{i \in N} c_i \,\alpha_i \prod_{j=1}^{i-1}(1 - \alpha_j)$$

這裡 $c_i$ 是高斯 $i$ 依觀看方向而變的顏色，$\alpha_i$ 是在像素處評估其二維投影後的不透明度。

## 結果

摘要報告，在 1080p 下可以至少每秒 30 幀即時渲染，並具有具競爭力的訓練時間與品質。比較數字見論文的表格。

## 限制

論文的限制章節（第 7.4 節）報告了以下幾點：

- 原型需要的記憶體多於 NeRF，尖峰超過 20 GB。
- 在輸入視角觀察不佳的區域，可能出現瑕疵。
- 大型高斯在與視角相關的區域會造成跳動（popping）。

論文另外報告，在輸入相機附近會出現浮點（floaters，第 5.2 節），並假設輸入場景是靜態的（第 3 節）。

## 關聯

此方法以梯度下降依影像損失訓練，所用的梯度機制見[自動微分](../../../math/automatic-differentiation/index.zh-TW.md)。

## 應用

即時渲染擷取的真實場景，這正是論文評估的情境。

## 開放問題

- 如何在不損失細節的前提下，控制高斯的數量？
- 高斯表示法應如何處理動態場景與光照變化？

## 參考文獻

### 奠基性論文

- Kerbl、Kopanas、Leimkuehler 與 Drettakis，*3D Gaussian Splatting for Real-Time Radiance Field Rendering*，ACM Transactions on Graphics（2023）。https://doi.org/10.1145/3592433 — 介紹此方法、其最佳化與光柵化渲染器。
- Mildenhall、Srinivasan、Tancik、Barron、Ramamoorthi 與 Ng，*NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*，European Conference on Computer Vision（2020）。https://doi.org/10.1007/978-3-030-58452-8_24 — 此方法所替代的隱式輻射場表示法。
- Barron 等人，*Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*，IEEE/CVF International Conference on Computer Vision（2021）。https://doi.org/10.1109/iccv48922.2021.00580 — 以多尺度表示擴展 NeRF，用於抗混疊。

### 綜述與教科書

- Zwicker、Pfister、van Baar 與 Gross，*EWA Splatting*，IEEE Transactions on Visualization and Computer Graphics（2002）。https://doi.org/10.1109/tvcg.2002.1021576 — 橢圓加權平均潑濺，是經典的潑濺方法。
- Kajiya 與 Von Herzen，*Ray tracing volume densities*，SIGGRAPH（1984）。https://doi.org/10.1145/964965.808594 — 透過體積密度進行光線追蹤的早期公式。
