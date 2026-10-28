---
translation_reviewed: 2026-10-28
---

# OpenPose（Cao 等人，2017）

OpenPose 是一套系統，能在一次前向計算中找出影像裡每個人的關節，並借助學得的肢段方向場把關節連成骨架。它讓即時的多人姿態估計變得實用，也是運動影片中最常被使用的姿態工具。它是父頁面[運動分析與表現](../index.md)所介紹的方法之一。

## 概述

在一張照片中估計一個人的姿態，是可以應付的問題。估計整支球隊的姿態則困難得多，因為身體彼此重疊時，系統必須判斷哪一個手肘屬於哪一位球員。早期的做法先用方框偵測每個人，再在每個方框內估計姿態。這種由上而下的策略準確，但成本隨人數增加。OpenPose 則採取相反的路線：它先在影像中偵測所有身體部位，再把它們分組為各個人。因此它的執行時間主要取決於影像本身，而不是影像中出現多少人。球員近距離接觸的運動影片，正是這項特性最重要的情境。

## 關鍵概念

- **身體部位（關節）信心圖**：對每一種關節，一張影像，其每個像素的值估計該關節位於該處的可能性。
- **部位親和場（part affinity field, PAF）**：對每一根肢段，一個雙通道的向量場，其在肢段上的值指向從一個關節到下一個關節的方向。它同時編碼肢段的位置與朝向。
- **由下而上的解析（bottom-up parsing）**：先偵測所有關節，再把它們組裝成人，而不是先偵測人。
- **階段（stages）**：網路以數個依序進行的階段逐步修正預測，每一階段都接收影像特徵與前一階段的輸出。
- **關鍵點（keypoint）**：一個帶有名稱的關節位置，例如腳踝或手腕。一般的輸出是每人一組關鍵點。

## 運作方式

令 $x_{j_1}$ 與 $x_{j_2}$ 為肢段 $c$ 兩端的兩個關節，並令 $v$ 為從 $x_{j_1}$ 指向 $x_{j_2}$ 的單位向量。真實的 PAF 為

$$
L_c^{*}(p) = \begin{cases} v & \text{若 } p \text{ 位於肢段 } c \text{ 上}, \\ 0 & \text{其他情況。} \end{cases}
$$

對影像中偵測到的兩個候選關節 $d_{j_1}$ 與 $d_{j_2}$，論文沿著兩者之間的線段對預測的場做積分，以判斷它們是否屬於同一根肢段：

$$
E = \int_{u=0}^{1} L_c\big(p(u)\big)\cdot \frac{d_{j_2}-d_{j_1}}{\lVert d_{j_2}-d_{j_1}\rVert}\,du, \qquad p(u) = (1-u)\,d_{j_1} + u\,d_{j_2}.
$$

分數高表示場沿著線段的方向指向，因此這兩個關節很可能相連。訓練時，在每個階段 $t$ 上對 PAF 與信心圖都最小化 L2 損失，並以遮罩 $W$ 忽略未標註的區域。

1. **特徵。** 一個共用的卷積骨幹網路，以影像分類網路為初始權重，把影像轉換為特徵圖。
2. **修正。** 每一階段根據特徵與前一階段的結果，預測 PAF 與信心圖。論文報告指出，只修正 PAF 比同時修正兩種輸出更快，也更準確。
3. **找出關節。** 最終信心圖的局部極大值即為候選關節位置。
4. **關聯。** 對每一種肢段，演算法以 $E$ 為所有候選配對評分，並以貪婪式的配對選出一組互不衝突的連接，使每個關節最多只連到一個夥伴。
5. **組裝。** 把相連的肢段合併為每人一副骨架。

## 結果

CVPR 論文的 arXiv 摘要報告了兩項主要結果。該方法在首屆 COCO 2016 關鍵點挑戰賽中獲得第一名，並且在 MPII 多人基準上，於準確度與效率兩方面都明顯超越先前的最佳成績。無論影像中有多少人，它都能即時執行。擴充後的期刊版本（預印本為 arXiv:1812.08008）加入了一個結合身體與腳部的關鍵點偵測器，它使用一套附有標註的足部資料集訓練；論文報告，這個合併模型比依序執行兩個偵測器更快，同時保有各部分的準確度。這些基準都是一般用途的影像集，而非運動影片，因此證據所涉及的是一般影像。

## 限制

- **二維。** 系統只估計影像平面上的關節位置。生物力學分析或三維定位需要多部已校正的攝影機，或另外的提升模型。
- **遮擋與擁擠。** 爭球時的人牆或防守陣型中，球員會遮住彼此的關節，此時分組步驟可能把肢段連到錯誤的人身上。
- **動態模糊與拍攝角度。** 快速衝刺、踢球以及轉播中的變焦，會產生模糊或不尋常的視角，這些在基準資料中很少出現。
- **沒有時間模型。** 單一影格的系統無法在各影格之間保持身分一致。要在整場比賽中追蹤球員，還需要額外的步驟；參見[影片模型](../../../theory/models/computer-vision/video/index.md)以了解更廣的背景。
- **領域偏移。** 球衣、場地標線與隊服顏色，與模型訓練所用的一般影像集不同，因此應該實際測量運動影片上的準確度，而不應想當然。

## 開放問題

- 二維姿態系統在職業比賽影片上表現如何，又需要多少運動專用的訓練資料？
- 能否把多部攝影機的姿態估計融合，在比賽中得到可靠的三維關節位置？
- 關節位置的小誤差，是否會改變據此得出的傷病風險或技術判斷？這與[主題概述](../index.md)中的傷病討論有關。
- 同樣的關節與肢段表徵，也支撐著動作知覺的研究。Johansson（1973）顯示，觀察者能從幾個發光點看出人體的動作，因此機器的表徵與人類所用的表徵有多接近，仍是一個開放的問題。[運動控制](../../../brain-mind/motor-control/index.md)頁面則說明人如何協調動作。

## 參考文獻

### 開創性論文

- Cao, Z. 等人（2017）。Realtime multi-person 2D pose estimation using part affinity fields。*CVPR*。https://doi.org/10.1109/CVPR.2017.143 — 提出部位親和場，以及後來成為 OpenPose 的由下而上流程。
- Cao, Z. 等人（2021）。OpenPose: realtime multi-person 2D pose estimation using part affinity fields。*IEEE Transactions on Pattern Analysis and Machine Intelligence*。https://doi.org/10.1109/TPAMI.2019.2929257 — 期刊擴充版，加入結合身體與腳部的關鍵點偵測器，並分析只修正 PAF 的做法。
- Cao, Z. 等人（2016）。Realtime multi-person 2D pose estimation using part affinity fields。arXiv。https://arxiv.org/abs/1611.08050 — 會議論文的預印本，其摘要報告在 COCO 2016 關鍵點挑戰賽中獲得第一名。
- Cao, Z. 等人（2018）。OpenPose: realtime multi-person 2D pose estimation using part affinity fields。arXiv。https://arxiv.org/abs/1812.08008 — 期刊擴充版的預印本，描述結合身體與腳部的偵測器，以及它相對於依序執行兩個偵測器的速度。
- Wei, S.-E. 等人（2016）。Convolutional pose machines。arXiv。https://arxiv.org/abs/1602.00134 — 以卷積預測器逐階段修正部位位置，是本文所用分階段設計的前身。
- Newell, A.、Yang, K. 與 Deng, J.（2016）。Stacked hourglass networks for human pose estimation。arXiv。https://arxiv.org/abs/1603.06937 — 人體姿態估計網路，在重複的沙漏模組中跨尺度處理特徵。

- Johansson, G.（1973）。Visual perception of biological motion and a model for its analysis。*Perception & Psychophysics*。https://doi.org/10.3758/BF03212378 — 顯示觀察者能從關節上幾個發光點辨識人體的動作。

### 綜述與教科書

- Chen, Y.、Tian, Y. 與 He, M.（2020）。Monocular human pose estimation: a survey of deep learning-based methods。arXiv。https://arxiv.org/abs/2006.01423 — 綜述以深度學習從單張影像與影片估計人體姿態的方法。
- Sun, K. 等人（2019）。Deep high-resolution representation learning for human pose estimation。arXiv。https://arxiv.org/abs/1902.09212 — 在整個網路中保留高解析度特徵，是此任務中廣泛使用的後續架構。
