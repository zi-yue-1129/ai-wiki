---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/world-models
  - theory/models/transformer
tags:
  - video
  - action recognition
  - video generation
aliases:
  - 影片理解
  - 影片生成
  - 動作辨識
  - Video understanding
---

# 影片理解與生成

影片在影像上加入了時間。理解影片的模型必須辨識跨越影格的動作與事件；生成影片的模型則必須讓物件在相鄰影格之間保持一致。本章涵蓋動作辨識、影片 Transformer，以及影片擴散模型，後者與影像擴散模型一樣，從雜訊中生成影片片段。

## 概觀

影片是一連串的影格，因此大部分困難在於模型如何處理時間軸。早期方法把影像網路沿時間方向延伸；後來的方法在空間與時間上使用注意力，或在遮蔽的影片上訓練。生成還多一項要求：輸出必須在許多影格中都合理，而不只是每一格都清晰。

## 關鍵概念

- **動作辨識（action recognition）**：對影片片段中的動作分類，例如跑步或烹飪。
- **雙流網路（two-stream network）**：一條流處理單格的外觀，另一條流處理光流所表示的運動。
- **時空卷積（spatiotemporal convolution）**：除了空間核以外，還有時間核的卷積。
- **影片 Transformer（video Transformer）**：應用於時空區塊（tubelet）詞元的 Transformer。
- **影片擴散（video diffusion）**：對一串影格去噪的擴散模型，常以文字為條件。

## 運作方式

Simonyan 與 Zisserman 使用兩條流，一條處理靜態影格，另一條處理堆疊的光流，並顯示兩者結合能很好地分類動作 [(Simonyan and Zisserman, 2014)](https://arxiv.org/abs/1406.2199)。Tran 等人使用三維卷積，直接從片段中學習時空特徵 [(Tran et al., 2015)](https://arxiv.org/abs/1412.0767)。Carreira 與 Zisserman 把二維濾波器膨脹為三維，以重用預訓練的影像權重，這就是 [I3D](i3d.zh-TW.md)。

Transformer 改變了設計。Arnab 等人建立了 [ViViT](vivit.zh-TW.md)，這是一個用於影片分類的純 Transformer [(Arnab et al., 2021)](https://arxiv.org/abs/2103.15691)。像 VideoMAE 那樣的遮蔽影片預訓練，可減少所需的標註資料量 [(Tong et al., 2022)](https://arxiv.org/abs/2203.12602)。

在生成方面，Ho 等人把擴散模型擴展到影片，顯示同一套去噪目標可以產生連貫的短片段 [(Ho et al., 2022)](https://arxiv.org/abs/2204.03458)。[影片擴散](video-diffusion.zh-TW.md)是這個家族的方法頁。

## 關鍵方法

- [I3D](i3d.zh-TW.md)：膨脹的卷積網路，用於動作辨識，並在大型標註資料集上訓練。
- [ViViT](vivit.zh-TW.md)：作用於時空詞元的 Transformer，並具有多種注意力分解方式。
- [影片擴散](video-diffusion.zh-TW.md)：串接式或潛在空間的擴散模型，以文字為條件生成影格。

## 關聯

具有一致動態的影片生成，與預測環境如何變化的[世界模型](../../world-models/index.zh-TW.md)密切相關。Transformer 的概念見[Transformer](../../transformer/index.zh-TW.md)。視覺任務的整體地圖見[電腦視覺](../index.zh-TW.md)。

## 應用

動作辨識支援運動分析、監控影片回顧與影片搜尋。影片理解支援內容審核與無障礙字幕。影片生成支援電影的前期視覺化、廣告與合成訓練資料，並引發[錯誤資訊與深偽](../../../../society/misinformation/index.zh-TW.md)中討論的合成媒體問題。

## 開放問題

- 生成的影片在物件開始漂移或物理規律失效之前，能維持多久的一致性？
- 影片預訓練學到的是世界的動態，還是主要是影格的統計特性？
- 當許多基準片段僅憑單一影格就能解出時，動作辨識應如何評估？

## 參考文獻

### 奠基性論文

- Simonyan 與 Zisserman，*Two-Stream Convolutional Networks for Action Recognition in Videos*（2014）。https://arxiv.org/abs/1406.2199 — 分別處理外觀與光流的雙流網路。
- Tran、Bourdev、Fergus、Torresani 與 Paluri，*Learning Spatiotemporal Features with 3D Convolutional Networks*（2015）。https://arxiv.org/abs/1412.0767 — 用於影片特徵的三維卷積。
- Carreira 與 Zisserman，*Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset*（2017）。https://arxiv.org/abs/1705.07750 — I3D 模型與 Kinetics 資料集。
- Arnab、Dehghani、Heigold、Sun、Lučić 與 Schmid，*ViViT: A Video Vision Transformer*（2021）。https://arxiv.org/abs/2103.15691 — 用於影片分類的純 Transformer。
- Ho、Salimans、Gritsenko、Chan、Norouzi 與 Fleet，*Video Diffusion Models*（2022）。https://arxiv.org/abs/2204.03458 — 用於影片生成的擴散模型。

### 文章與文件

- Tong、Song、Wang 與 Wang，*VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training*（2022）。https://arxiv.org/abs/2203.12602 — 影片 Transformer 的遮蔽預訓練。
