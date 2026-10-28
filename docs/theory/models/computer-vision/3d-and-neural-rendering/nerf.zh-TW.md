---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/3d-and-neural-rendering
tags:
  - NeRF
  - neural rendering
  - view synthesis
aliases:
  - 神經輻射場
  - NeRF
  - Neural radiance field
---

# NeRF：神經輻射場

NeRF 把場景表示為一個神經網路，它把三維位置與觀看方向映射到顏色與密度。新視角沿相機射線對這個函數積分來渲染。它是學習式視圖合成的里程碑方法，大多數後續的神經渲染工作都以它為起點。

## 概觀

[本章](index.zh-TW.md)描述了這個領域。本頁詳細說明一個方法：對一個固定場景的多張照片擬合一個多層感知器，使其能從新的相機位置渲染視角。

## 問題

給定一個場景的幾十張影像與已知的相機位姿，產生來自不在該集合中的視點的逼真影像。早期的視圖合成方法使用離散的體素格或網格，它們不是記憶體耗費大，就是遺失細節。

## 核心想法

場景是一個連續函數 $F_\Theta(\mathbf{x}, \mathbf{d}) = (\mathbf{c}, \sigma)$。它接收位置 $\mathbf{x}$ 與觀看方向 $\mathbf{d}$，回傳發射的顏色 $\mathbf{c}$ 與體積密度 $\sigma$。網路的訓練目標是讓渲染出的像素與照片相符。有兩個細節很關鍵。輸入會先經過位置編碼，使網路能表示高頻細節。渲染在密度高的地方沿射線更密集地取樣，論文稱之為階層式取樣策略。

## 方程式

像素的顏色是沿相機射線 $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$ 的積分：

$$C(\mathbf{r}) = \int_{t_n}^{t_f} T(t)\,\sigma(\mathbf{r}(t))\,\mathbf{c}(\mathbf{r}(t), \mathbf{d})\,dt, \qquad T(t) = \exp\!\left(-\int_{t_n}^{t}\sigma(\mathbf{r}(s))\,ds\right)$$

這裡 $T(t)$ 是累積透射率。積分透過沿射線取樣點來近似，損失函數則是渲染像素與觀察像素顏色之間的平方誤差。

## 結果

摘要報告，此方法對複雜場景的新視角合成達到最佳水準。與先前方法的比較見論文的結果表，本頁不重述。

## 限制

- 訓練很慢，因為每個場景都需要各自最佳化，渲染時每個像素又需要許多次網路評估。
- 此表示法是隱式的，因此編輯、重新打光與抽取幾何，比網格困難。
- 原始方法假設場景是靜態的，且相機位姿已知。

後續工作以更快的格點與顯式表示處理了這些限制，包括[三維高斯潑濺](gaussian-splatting.zh-TW.md)。

## 關聯

NeRF 建立在[章節概觀](index.zh-TW.md)中也出現的體積渲染概念上。它的最佳化依賴[自動微分](../../../math/automatic-differentiation/index.zh-TW.md)中的梯度機制。

## 開放問題

- 輻射場能否在不損失品質的前提下，以互動速度訓練與渲染？
- 表示法應如何處理移動的物體與變化的光照？

## 參考文獻

### 奠基性論文

- Mildenhall、Srinivasan、Tancik、Barron、Ramamoorthi 與 Ng，*NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*，European Conference on Computer Vision（2020）。https://doi.org/10.1007/978-3-030-58452-8_24 — NeRF 原始論文，包含體積渲染的公式與位置編碼。
- Barron 等人，*Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields*，IEEE/CVF International Conference on Computer Vision（2021）。https://doi.org/10.1109/iccv48922.2021.00580 — 以多尺度表示擴展 NeRF，以減少混疊。
- Kerbl、Kopanas、Leimkuehler 與 Drettakis，*3D Gaussian Splatting for Real-Time Radiance Field Rendering*，ACM Transactions on Graphics（2023）。https://doi.org/10.1145/3592433 — 與隱式 NeRF 表示法相對的顯式替代方案。

### 綜述與教科書

- Kajiya 與 Von Herzen，*Ray tracing volume densities*，SIGGRAPH（1984）。https://doi.org/10.1145/964965.808594 — 透過參與介質進行渲染的早期公式，NeRF 的積分即建立於其上。
- Max，*Optical models for direct volume rendering*，IEEE Transactions on Visualization and Computer Graphics（1995）。https://doi.org/10.1109/2945.468400 — 體積渲染背後光學模型的綜述。
