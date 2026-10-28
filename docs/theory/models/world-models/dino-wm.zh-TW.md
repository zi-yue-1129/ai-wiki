---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
tags:
  - world models
  - self-supervised
  - planning
aliases:
  - DINO-WM
  - DINO 世界模型
---

# DINO-WM

DINO-WM 是一種潛在世界模型，預測場景的 patch 特徵在動作作用下如何改變。特徵來自凍結的 DINOv2 編碼器，而以動作為條件的 transformer 在離線軌跡上訓練。規劃時，在這個特徵空間中搜尋動作序列。作者稱之為零樣本規劃（zero-shot planning），因為測試時規劃器不需要任務專用的獎勵或專家示範。

## 概覽

Zhou、Pan、LeCun 與 Pinto (2025) 探討：一種通用、預先訓練的視覺表徵，能否作為規劃用世界模型的狀態空間。他們設定的目標是：模型能以離線資料訓練、能在測試時做最佳化，且不依賴學習得來的獎勵模型或反向模型。評估涵蓋六個模擬環境（PointMaze、Wall、Reach、Push-T、Rope 與 Granular），另加數個泛化變體。最自然的用途是從影像進行規劃：有記錄下來的軌跡可用，且以一張目標影像指定任務。

## 關鍵概念

- **潛在世界模型**：一種預測器，在嵌入空間而非像素空間中，把目前狀態與一個動作映射到下一個狀態。
- **Patch 特徵**：DINOv2 為每個影像 patch 產生一個特徵向量。論文中的觀測被切成 14×14 的格狀網格，每幀共 196 個 patch token，每個 token 為 384 維特徵。
- **凍結的編碼器**：訓練與測試期間，DINOv2 的權重都不更新，只學習預測器。
- **動作條件化**：每個動作經過一個小型 MLP 嵌入，嵌入向量串接到每個 patch token 上。
- **目標匹配成本**：候選計畫的評分，取決於其預測的最終特徵與目標影像特徵的接近程度。

## 運作方式

1. 用凍結的 DINOv2 編碼器把每一幀編碼成 patch token。
2. 用 MLP 嵌入每個動作，並把嵌入串接到該幀的每個 patch token 上。
3. 在一小段歷史幀上執行因果 transformer 預測器，使用幀層級的因果遮罩，預測下一幀的 patch token。歷史長度在某些環境中為 3，在其他環境中為 1。
4. 以離線軌跡與 teacher forcing 訓練。對每個訓練片段，最小化每個預測幀與對應編碼真實幀之間的潛在空間平方距離。
5. 測試時，以交叉熵方法（CEM）進行模型預測控制（MPC）。取樣動作序列，在特徵空間中展開，保留表現最好的一批，重新擬合動作上的高斯分布，然後重複。執行前幾個動作後再重新規劃。

## 關鍵方法

### DINO-WM（Zhou、Pan、LeCun 與 Pinto，2025）

- **問題：** 以像素為單位的世界模型，會把容量花在對控制影響不大的外觀細節上；而且為每台機器人從零開始訓練預測器，成本很高。問題在於，凍結、通用的視覺特徵能否作為規劃的狀態空間。
- **核心想法：** 保持自監督視覺編碼器凍結，只學習其 patch token 上以動作為條件的預測器。規劃時，最佳化動作，使預測的最終特徵與目標影像的特徵吻合。論文另外訓練了一個像素解碼器，但它是獨立訓練的，不用於規劃。
- **方程式或演算法：** 訓練損失是潛在空間中預測幀與編碼後真實下一觀測之間的平方 L2 距離，對片段中每個預測幀都計算。以示意形式寫成：

\[
\mathcal{L}_{\text{pred}} = \sum_{k} \big\lVert \hat z_{k+1} - z_{k+1} \big\rVert_2^2
\]

  規劃則最小化預測的最終潛在向量與目標潛在向量之間的平方距離：

\[
C(a_{1:T}) = \big\lVert \hat z_T - z_g \big\rVert_2^2
\]

  論文比較了 CEM 與透過模型做梯度下降的方法，並指出在其實驗中 CEM 表現較好。預測器以 AdamW 訓練，預測器學習率為 5e-5，訓練 100 個 epoch，批次大小為 32，數值列於論文的超參數表中。

- **結果：** 論文的表 1 在 Maze、Wall、Reach 與 Push-T 上報告成功率（SR，越高越好），在 Rope 與 Granular 上報告 Chamfer 距離（CD，越低越好）。

| 模型 | Maze SR | Wall SR | Reach SR | Push-T SR | Rope CD | Granular CD |
|---|---|---|---|---|---|---|
| IRIS | 0.74 | 0.04 | 0.18 | 0.32 | 1.11 | 0.37 |
| DreamerV3 | 1.00 | 1.00 | 0.64 | 0.30 | 2.49 | 1.05 |
| TD-MPC2 | 0.00 | 0.00 | 0.00 | 0.00 | 2.52 | 1.21 |
| DINO-WM | 0.98 | 0.96 | 0.92 | 0.90 | 0.41 | 0.26 |

  在此表中，DINO-WM 於 Reach、Push-T、Rope 與 Granular 上得分最高。DreamerV3 在 Maze（1.00 對 0.98）與 Wall（1.00 對 0.96）上較高，因此明顯優勢只出現在部分任務上。成功率使用 Maze、Wall、Reach 與 Push-T 各 50 組隨機起點與目標配對，Rope 與 Granular 各 10 組。論文未報告隨機種子或誤差線。

- **限制：** 此方法需要具有良好狀態-動作覆蓋的離線資料，論文指出在複雜環境中這可能不易取得。它需要真實動作標籤，因此難以用於未標註的網路影片。規劃在動作空間中進行，作者建議以階層式延伸來做精細控制。以梯度下降規劃的表現不如 CEM。PushObj 泛化任務仍然困難。Push-T 的訓練資料是已釋出專家軌跡加上雜訊後的重播，因此「不需要專家示範」的說法只適用於測試時，並非整個流程。論文把輸入尺寸同時寫成 196×196 與 224×224，且正文未說明所用的 DINOv2 變體，因此要精確重現需要參考釋出的程式碼。

## 與其他主題的連結

[LAPO](lapo.md) 從影片學習動作，而 DINO-WM 假設動作已知，並研究預測器的狀態空間。[V-JEPA 2](v-jepa-2.md) 走相反的路線：從影片編碼器出發，再以機器人影片做後訓練。兩者都碰到 [動作可控性](action-controllability.md) 所研究的問題：預測器是否真的依賴它所獲得的動作。凍結的視覺特徵來自[自監督](../../paradigms/self-supervised/index.md)這一脈研究。更廣的家族見[總覽頁](index.md)。

## 開放問題

- 凍結的外觀編碼器能否支撐接觸密集的任務，其中細微的視覺細節會決定成敗。
- 規劃成本如何隨時程長度與動作維度成長。論文的計時表比較的是不同批次大小，因此無法得到乾淨的成本曲線。
- 成功率在多次執行之間有多穩定。由於論文未報告種子或誤差線，其離散程度不明。

## 參考文獻

### 奠基性論文

- Zhou, G.、Pan, H.、LeCun, Y. 與 Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025, PMLR 267, pp. 79115–79135. https://proceedings.mlr.press/v267/zhou25t.html — 提出本頁所述的凍結特徵預測器與 CEM 規劃。arXiv 版本見 https://arxiv.org/abs/2411.04983。
- Oquab, M. 等人 (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — 自監督視覺編碼器，其凍結的 patch token 構成 DINO-WM 的狀態空間。
- Assran, M. 等人 (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv:2506.09985. https://arxiv.org/abs/2506.09985 — 以影片預訓練的替代方案，透過機器人影片後訓練加入動作條件。
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv:1803.10122. https://arxiv.org/abs/1803.10122 — 早期的潛在世界模型，學習緊湊的動力學模型並用於控制。

### 綜述與教科書

- Moerland, T. M. 等人 (2020). *Model-based Reinforcement Learning: A Survey*. arXiv:2006.16712. https://arxiv.org/abs/2006.16712 — 學習得來的動力學模型及其在規劃與控制中用法的綜述。
