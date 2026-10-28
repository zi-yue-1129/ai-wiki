---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/computer-vision
  - brain-mind/neuroai
tags:
  - 3D vision
  - neural rendering
  - view synthesis
aliases:
  - 三維視覺
  - 神經渲染
  - 神經輻射場
  - Neural rendering
---

# 三維視覺與神經渲染

三維視覺讓機器從影像中還原場景的幾何形狀，神經渲染則讓機器從新的視角產生該場景的新影像。兩個問題在視圖合成（view synthesis）中相遇：模型從幾張照片學習場景，並從未見過的位置渲染它。

## 概觀

二維影像記錄的是光線到達單一視點時的情況。深度、形狀與遮擋在投影過程中會遺失，因此要還原它們，需要多個視角或習得的先驗知識。古典方法使用多視角幾何與三角測量。學習式方法則擬合一種表示法，例如神經網路或一組基元，使其能預測深度，或從新的相機位置渲染顏色。

## 關鍵概念

- **深度估計（depth estimation）**：從單張或多張影像預測相機到每個像素的距離。
- **點雲（point cloud）**：一組三維點，通常來自深度感測器，用作場景表示。
- **輻射場（radiance field）**：在每個三維位置與觀看方向上給出顏色與密度的函數。
- **體積渲染（volume rendering）**：沿相機射線對顏色與密度積分，以計算像素顏色。
- **新視角合成（novel view synthesis）**：從不在訓練集中的相機位置渲染場景。

## 運作方式

深度估計從影像預測深度圖。Eigen、Puhrsch 與 Fergus 為此使用多尺度深度網路，結合粗略的全域視野與較細的局部細節 [(Eigen et al., 2014)](https://arxiv.org/abs/1406.2283)。點雲網路直接處理三維資料。PointNet 以共用的逐點網路與對稱的池化步驟處理無序的點集合，因此輸出不依賴點的順序 [(Charles et al., 2017)](https://doi.org/10.1109/CVPR.2017.16)。

神經渲染方法接著使用場景表示產生影像。兩大方法家族各自有獨立的頁面。

## 關鍵方法

有兩個里程碑式的方法定義了目前的領域。

- [NeRF](nerf.zh-TW.md)：神經輻射場，一個將三維位置與觀看方向映射到顏色與密度的 MLP，並以體積積分渲染。它能做出高品質的視圖合成，但需要對每個場景做長時間的最佳化。
- [三維高斯潑濺](gaussian-splatting.zh-TW.md)：以三維高斯分布組成的顯式場景，透過光柵化渲染。它的設計目標是快速渲染與快速訓練。

## 關聯

這裡的幾何與[電腦視覺](../index.zh-TW.md)中的三維與感知主題有重疊。渲染與最佳化步驟依賴[自動微分](../../../math/automatic-differentiation/index.zh-TW.md)中所述的微分。生物視覺如何透過立體與運動線索建立三維感知，相關研究連結自[腦與心智](../../../../brain-mind/index.zh-TW.md)。

## 應用

新視角合成用於電影與遊戲的資產擷取、虛擬導覽，以及機器人的地圖建構。深度估計支援自駕車、擴增實境與機器人抓取。生成式三維（創造場景而非還原場景）是活躍的研究領域，建立在相同的表示法上。

## 開放問題

- 如何讓神經場景表示同時做到訓練快、渲染快？
- 當輸入視角稀少或含糊時，生成式與還原式的三維模型應如何結合？
- 學習得到的深度與三維模型，在訓練場景以外的範圍泛化得有多好？

## 參考文獻

### 奠基性論文

- Mildenhall、Srinivasan、Tancik、Barron、Ramamoorthi 與 Ng，*NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*，European Conference on Computer Vision（2020）。https://doi.org/10.1007/978-3-030-58452-8_24 — 提出用於視圖合成的神經輻射場，並採用體積渲染。
- Kerbl、Kopanas、Leimkuehler 與 Drettakis，*3D Gaussian Splatting for Real-Time Radiance Field Rendering*，ACM Transactions on Graphics（2023）。https://doi.org/10.1145/3592433 — 以顯式的高斯場景表示，用於快速且高品質的渲染。
- Eigen、Puhrsch 與 Fergus，*Depth Map Prediction from a Single Image using a Multi-Scale Deep Network*（2014）。https://arxiv.org/abs/1406.2283 — 用於單眼深度預測的早期深度網路。
- Charles、Su、Mo 與 Guibas，*PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation*，IEEE Conference on Computer Vision and Pattern Recognition（2017）。https://doi.org/10.1109/CVPR.2017.16 — 直接處理無序點雲的網路。

### 綜述與教科書

- Hartley 與 Zisserman，*Multiple View Geometry in Computer Vision*，Cambridge University Press（2004，第二版）。https://doi.org/10.1017/CBO9780511811685 — 學習式三維方法所建立的多視角幾何標準教科書。
