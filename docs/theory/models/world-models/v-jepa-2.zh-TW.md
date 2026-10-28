---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
tags:
  - world models
  - self-supervised
  - robotics
aliases:
  - V-JEPA 2
  - V-JEPA 2-AC
---

# V-JEPA 2

V-JEPA 2 是一種自監督影片模型，它在表徵空間而非像素空間中預測被遮住的內容。論文把它延伸為世界模型 V-JEPA 2-AC：在少量未標註的機器人影片上，對一個以動作為條件的預測器做後訓練。作者接著用該預測器規劃機器人動作，朝向影像目標前進。

## 概覽

Assran 等人 (2025) 把在大量網路影片上訓練的影片編碼器，加上一個能理解機器人動作的預測器。機器人訓練期間編碼器保持凍結。只需訓練約 3 億參數的預測器，資料是 DROID 資料集中約 62 小時的機器人影片。接著，作者在兩個實驗室的 Franka 機械臂上零樣本部署，使用影像目標，不做任務專用的訓練，也不使用獎勵。論文同時報告了影片理解與問答的結果，但不在本頁的範圍內。

## 關鍵概念

- **聯合嵌入預測架構（JEPA）**：預測輸入中被遮住部分之表徵的模型，而非預測其原始像素。
- **表徵空間中的遮罩去噪**：編碼器看到可見的 patch，預測器則補上被遮住 patch 的表徵。
- **EMA 目標編碼器**：預測目標來自編碼器權重的指數移動平均，並搭配 stop-gradient。論文指出，這樣能避免表徵崩塌。
- **以動作為條件的預測器**：以機器人末端執行器的變化作為輸入，預測下一個表徵的預測器。
- **以 CEM 與 MPC 規劃**：取樣候選動作序列，依其與目標表徵的距離評分，並以表現最好的一批來更新取樣分布。重新規劃前只執行第一個動作。

## 運作方式

1. 在大量影片與影像的混合資料上預訓練影片編碼器。論文的資料組合 VideoMix22M 約有 2,200 萬個樣本，摘要則指出預訓練涵蓋超過一百萬小時的影片。編碼器為參數最多約十億的 ViT-g。
2. 凍結編碼器，並在機器人片段上後訓練以動作為條件的預測器。每個動作是相鄰幀之間末端執行器狀態的 7 維變化，每個狀態是相對於機器人底座的 7 維向量。
3. 控制時，取樣候選動作序列，在表徵空間中預測其結果，並以預測的終態與目標影像表徵的距離評分。保留表現最好的一批，更新取樣分布，只執行第一個動作，然後重新規劃。

## 關鍵方法

### V-JEPA 2（Assran 等人，2025）

- **問題：** 影片模型能很好地學習外觀與動態，但只預測影片的模型，無法告訴機器人它自己的動作會造成什麼結果。論文探討：沒有標籤學到的表徵，能否在少量機器人資料下轉換成以動作為條件的預測器，並驅動真實機械臂的規劃。
- **核心想法：** 以表徵空間中的遮罩預測來預訓練影片編碼器。之後保持編碼器凍結，只在少量機器人影片上後訓練動作預測器，以執行的動作作為輸入。把該預測器放進模型預測控制迴圈，搜尋能到達影像目標的動作。
- **方程式或演算法：** 在預訓練階段，預測器與編碼器被訓練來最小化對被遮住 patch 的預測，與來自 EMA 編碼器之目標表徵之間的 L1 距離。以示意形式寫成：

\[
\min \big\lVert P_\phi\big(\Delta_y, E_\theta(x)\big) - \mathrm{sg}\big(\bar E(y)\big) \big\rVert_1
\]

  對 V-JEPA 2-AC 而言，編碼器凍結，預測器以兩個損失訓練。教師強制（teacher forcing）損失，是在 T = 15 步的視窗上，平均單步預測的 L1 誤差。兩步展開（rollout）損失，則比較兩步自我生成預測後的表徵與真實表徵。總損失為兩者之和。規劃使用 CEM 與模型預測控制，成本為預測的最終表徵與目標表徵之間的 L1 距離。取樣的動作被限制在半徑 0.075 的 L1 球內。抓取與放置任務中，控制器會先朝一個中間子目標優化 4 步，再朝第二個子目標優化 10 步，最後朝最終目標優化 4 步。

- **結果：** 在機器人實驗中，論文以每個任務 10 次試驗的成功次數報告，並對兩個實驗室取平均：

| 方法 | Reach | Grasp Cup | Grasp Box | Reach w/ Obj Cup | Reach w/ Obj Box | Pick-and-Place Cup | Pick-and-Place Box |
|---|---|---|---|---|---|---|---|
| Octo（平均） | 100% | 15% | 0% | 15% | 70% | 15% | 10% |
| V-JEPA 2-AC（平均） | 100% | 65% | 25% | 75% | 75% | 80% | 65% |

  V-JEPA 2-AC 在 Reach 上與 Octo 持平，在表中其餘任務上都較高。Cosmos 的比較只在 Lab 2 進行，Reach 為 80%，Grasp Cup 與 Pick-and-Place Cup 皆為 0%。論文指出，V-JEPA 2-AC 在單一 GPU 上以 800 個樣本與 10 次迭代，每個動作約需 16 秒的規劃時間；Cosmos 以 80 個樣本則約需 4 分鐘。摘要也報告影片理解結果，例如 Something-Something v2 上 77.3 的 top-1 準確率，以及 Epic-Kitchens-100 動作預期上 39.7 的 recall-at-5。這些都不是機器人結果。

- **限制：** 模型沒有明確的相機校正，機器人底座常常不在畫面中，因此動作軸必須隱含地推斷。長程展開時自回歸誤差會累積，搜尋空間也隨時程迅速擴大。目標必須是影像，語言目標留待未來工作。論文中的預測最遠約到 16 秒之後。規模研究只做到十億參數的編碼器。在動作預期上，EK100 基準並未被完全解決，時程拉長時準確率下降。

## 與其他主題的連結

[DINO-WM](dino-wm.md) 是最接近的比較對象。它以凍結的影像編碼器，在目標環境自己的軌跡上訓練預測器；V-JEPA 2 則從一般影片編碼器出發，只在後訓練階段加入機器人影片。[Genie](genie.md) 在像素空間中生成可互動的影片，而 V-JEPA 2 在表徵空間中預測，並將預測器用於規劃。V-JEPA 2 也引出 [動作可控性](action-controllability.md) 所研究的問題：預測器是否真的依賴它所獲得的動作。聯合嵌入預測的想法來自[自監督](../../paradigms/self-supervised/index.md)這一脈研究。更廣的家族見[總覽頁](index.md)。

## 開放問題

- 新的機器人本體需要多少機器人資料，以及 62 小時是否可作為實際的下限。
- 在表徵空間中規劃，是否保留了精確抓取所需的細緻空間資訊。Grasp Box 是 V-JEPA 2-AC 表現最弱的任務，平均只有 25%。
- 結果是否能推廣到論文兩個實驗室以外的相機位置與任務。

## 參考文獻

### 奠基性論文

- Assran, M.、Bardes, A.、Fan, D. 等人 (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv:2506.09985. https://arxiv.org/abs/2506.09985 — 提出 V-JEPA 2 及其以動作為條件的變體 V-JEPA 2-AC，後者在機器人影片上做後訓練，用於零樣本規劃。
- Assran, M. 等人 (2023). *Self-Supervised Learning From Images With a Joint-Embedding Predictive Architecture*. CVPR 2023. https://openaccess.thecvf.com/content/CVPR2023/html/Assran_Self-Supervised_Learning_From_Images_With_a_Joint-Embedding_Predictive_Architecture_CVPR_2023_paper.html — 影像版本的聯合嵌入預測方法，V-JEPA 2 將其延伸到影片。
- Zhou, G.、Pan, H.、LeCun, Y. 與 Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025, PMLR 267. https://proceedings.mlr.press/v267/zhou25t.html — 在凍結影像特徵上的預測器，是從預訓練特徵做規劃的主要比較對象。
- Bruce, J. 等人 (2024). *Genie: Generative Interactive Environments*. ICML 2024, PMLR 235, pp. 4603–4623. https://proceedings.mlr.press/v235/bruce24a.html — 生成式的對應方法：在未標註影片上訓練的潛在動作模型。
- Schmidt, D. & Jiang, M. (2023). *Learning to Act without Actions*. arXiv:2312.10812. https://arxiv.org/abs/2312.10812 — 從無動作影片學習潛在動作，與用機器人影片訓練預測器相對應。論文以 ICLR 2024 spotlight 形式發表。

### 綜述與教科書

- Moerland, T. M. 等人 (2020). *Model-based Reinforcement Learning: A Survey*. arXiv:2006.16712. https://arxiv.org/abs/2006.16712 — 學習得來的動力學模型及其在規劃與控制中用法的綜述。
