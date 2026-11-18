---
translation_reviewed: 2026-11-18
---

# FaceNet

FaceNet 使用深度卷積網路，把人臉影像映射成 128 維向量，讓歐氏距離成為身分相似度的判斷依據。學到的空間可用於新的身分，不必為每位新人物重新訓練嵌入網路。父頁[嵌入與表徵學習](index.md)將它歸於度量學習。

## 問題

較早系統常先訓練固定身分類別的分類器，再取中間層作為人臉表示。分類器的輸出類別由訓練身分決定，但中間特徵仍可轉用於新身分，不能說它們完全不具泛化能力。Schroff、Kalenichenko 與 Philbin（2015）改為直接最佳化距離表示，讓同一嵌入適用於驗證、辨識與分群。

## 核心概念

網路 \(f\) 將影像映射為單位長度向量，\(\lVert f(x)\rVert_2=1\)。每個三元組包含錨點 \(x^a\)、同一人的正例 \(x^p\)，以及不同人的負例 \(x^n\)。訓練要求錨點到正例的平方距離，比到負例至少小一個間隔 \(\alpha\)。

因為直接訓練距離關係，推論可比較向量，不需為每次驗證另外建立身分類別的分類器。

## 方程與演算法

對 \(N\) 個三元組，損失為

\[
L=\sum_{i=1}^N\left[\lVert f(x_i^a)-f(x_i^p)\rVert_2^2-\lVert f(x_i^a)-f(x_i^n)\rVert_2^2+\alpha\right]_+.
\]

\([z]_+=\max(z,0)\)；滿足間隔時該項為零。論文使用 \(\alpha=0.2\)。

三元組選擇很重要。作者在含數千張人臉、每身分約 40 張影像的批次內進行線上挖掘，使用錨點與正例配對，再選擇**半困難負例**：距離比正例遠，但仍落在間隔內。始終選最困難的負例，可能在訓練早期導致不良局部解；論文以所有輸出趨同的崩塌情況說明風險。

## 結果

[原論文第 5.6–5.7 節](https://arxiv.org/abs/1503.03832)報告：

| 資料集 | 評估流程 | 準確率 |
|---|---|---|
| Labeled Faces in the Wild（LFW） | 標準不受限流程，加上額外人臉對齊 | 99.63% ± 0.09 個百分點（標準誤） |
| YouTube Faces DB | 每影片最先偵測到人臉的 100 個影格，計算跨影片所有影格配對相似度的平均 | 95.12% ± 0.39 |

主要評估採 128 維向量。第 5.4 節指出，在作者的測試中，每維量化為一個位元組未降低準確率；這不是對任意資料的保證。上述數值均為原論文量測。人臉分群僅展示使用者照片集中的定性範例，沒有量化分群分數。

## 限制

- **訓練成本**：CPU 叢集上花費 1,000–2,000 小時，指經過的訓練時間，不是把所有核心加總的 CPU 核心小時。作者指出約 500 小時後損失下降速度明顯變慢。
- **標籤雜訊**：極低誤接受率下的 ROC 曲線急降，被作者歸因於測試標籤雜訊。
- **影像品質**：縮圖過小會降低表現；主要模型訓練影像為 220×220 像素。
- **挖掘證據有限**：離線三元組實驗尚無定論，論文也未直接比較「只選困難錨點／正例」與「使用全部錨點／正例」策略。
- **尚待研究**：錯誤案例分析與更小模型仍是後續方向。

## 參考資料

### 奠基論文

- Schroff, F., Kalenichenko, D. & Philbin, J. (2015). *FaceNet: A Unified Embedding for Face Recognition and Clustering*. arXiv. https://arxiv.org/abs/1503.03832 — 定義三元組損失、半困難挖掘與本頁人臉驗證結果。
- Hermans, A., Beyer, L. & Leibe, B. (2017). *In Defense of the Triplet Loss for Person Re-Identification*. arXiv. https://arxiv.org/abs/1703.07737 — 研究三元組損失在行人再辨識中的效果。

### 綜述與教科書

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 學習表示與跨任務應用的背景。

### 文章與文件

- Khosla, P. et al. (2020). *Supervised Contrastive Learning*. arXiv. https://arxiv.org/abs/2004.11362 — 以類別標籤建立批次對比學習目標。
- Wang, T. & Isola, P. (2020). *Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere*. arXiv. https://arxiv.org/abs/2005.10242 — 分析單位球面表示的對齊與均勻性。
