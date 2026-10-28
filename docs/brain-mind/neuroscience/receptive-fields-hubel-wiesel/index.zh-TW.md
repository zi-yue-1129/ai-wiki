---
translation_reviewed: 2026-10-28
related:
- theory/models/cnn
tags:
- neuroscience
- vision
aliases:
  - 視覺皮質的感受野
  - Receptive Fields in Visual Cortex
  - Hubel and Wiesel
---

# 單一神經元記錄與視覺皮質（Hubel & Wiesel, 1962）

貓視覺皮質的單一神經元記錄顯示，有些細胞對定向邊緣有反應，另一些細胞則對較大區域內的這類邊緣有反應。這種兩層式的型態，是卷積網路所用階層式特徵偵測器的生物學起點。

本頁屬於[神經科學基礎](../index.md)。它詳細說明一項里程碑式的研究。

## 概述

落在視網膜上的光是一格格的亮度值，沒有標示出邊緣或形狀。Hubel 與 Wiesel 問的是：視覺皮質如何把這些輸入轉換成我們所見的特徵？他們的答案是：個別神經元各自對一種小而特定的圖樣有反應，而更高層的神經元再把這些圖樣組合成更大的圖樣。

## 核心概念

- **感受野（receptive field）**：視野中的一個區域，在這個區域內的刺激會改變神經元的放電。
- **簡單細胞（simple cell）**：具有分開的開區（on）與關區（off），對特定方向、特定位置的邊緣有反應。
- **複雜細胞（complex cell）**：對較大區域內、特定方向的邊緣都有反應，不需要固定位置。
- **方向選擇性（orientation selectivity）**：神經元的放電強烈依賴邊緣的角度，而這正是細胞偵測的特徵。

## 問題

視覺皮質如何從落在視網膜上的光，建立邊緣與形狀的表徵？在這項研究之前，皮質細胞的感受野大多不為人知，因此不清楚皮質計算的是哪些特徵。

## 核心想法

在麻醉貓的初級視覺皮質中記錄單一神經元，同時在不同位置與方向呈現光點與光條。接著依反應型態將細胞分類：具固定開區與關區的簡單細胞，以及在較大區域內整合的複雜細胞。作者提出，複雜細胞接收來自數個具相同方向偏好的簡單細胞的輸入，因此由較小、位置特定的特徵，建立出較大、對位置寬容的特徵。

## 方法

1. 在給定的位置與方向呈現刺激，例如一條光條。
2. 記錄神經元的放電。
3. 依反應標定感受野，劃出開區與關區。
4. 依反應型態把細胞歸為簡單或複雜細胞。

## 結果

研究在貓的初級視覺皮質中發現了具方向選擇性的細胞，並依上述的簡單與複雜兩類加以排列。所報告的階層結構，即複雜細胞整合簡單細胞的輸出，正是後來啟發電腦視覺中階層式特徵偵測器的想法。本文是對記錄細胞的定性描述，並非附有數值基準的擬合模型。

## 限制

- **麻醉的貓。**記錄是在麻醉下進行的，這可能使皮質細胞的反應與清醒動物不同。
- **過度簡化的階層。**後續研究發現，皮質細胞比兩種類別所暗示的更多樣，而且複雜細胞的反應並不純粹是簡單細胞輸出的總和。
- **只涵蓋視覺皮質。**本研究沒有說明這些特徵如何用於辨識，這是後續關於物件表徵的研究問題。

## 與其他主題的關聯

- **卷積網路**：在每個位置偵測相同局部特徵的卷積層，是簡單到複雜這個想法的計算版本。見[卷積神經網路](../../../theory/models/cnn/index.md)。
- **大腦中的視覺知覺**：同樣的物件辨識問題，也在[視覺知覺](../../visual-perception/index.md)中研究，其中包括能預測高階視覺區神經反應的深度網路。
- **母主題**：[神經科學基礎](../index.md)。

## 應用

- **視覺模型**：把局部特徵偵測器逐層匯集成較大特徵，是影像分類與偵測所用卷積網路的設計原則。
- **臨床視覺研究**：感受野定位用於研究視覺障礙，以判斷缺陷發生在視覺路徑的哪個位置。這是研究用途，此處並未描述臨床程序。

## 開放問題

- **簡單與複雜的二分法有多普遍？**皮質細胞的變異比兩類更多，兩類之間的界線仍有爭議。
- **這些特徵如何支持辨識？**感受野解釋了局部特徵偵測器，但沒有說明它們如何組合成物件的身份。
- **深度網路與它們相比如何？**比較模型單元與記錄神經元，是活躍的研究領域，見[視覺知覺](../../visual-perception/index.md)。

## 參考文獻

### 開創性論文

- Hubel, D. H. & Wiesel, T. N.（1959）。Receptive fields of single neurones in the cat's striate cortex. *The Journal of Physiology*。https://doi.org/10.1113/jphysiol.1959.sp006308 — 首次記錄貓紋狀皮質中的感受野，引入了開區與關區的概念。
- Hubel, D. H. & Wiesel, T. N.（1962）。Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*。https://doi.org/10.1113/jphysiol.1962.sp006837 — 發現具方向選擇性的簡單細胞與複雜細胞，是階層式視覺模型的生物學靈感來源。

- Hubel, D. H. & Wiesel, T. N.（1968）。Receptive fields and functional architecture of monkey striate cortex. *The Journal of Physiology*。https://doi.org/10.1113/jphysiol.1968.sp008455 — 把感受野的結果擴展到猴子，並描述方向偏好的柱狀組織。
- Fukushima, K.（1980）。Neocognitron: A self-organizing neural network model for a mechanism of pattern recognition unaffected by shift in position. *Biological Cybernetics*。https://doi.org/10.1007/BF00344251 — 以 Hubel 與 Wiesel 的細胞類型為基礎的簡單層與複雜層階層網路，是卷積網路的早期前身。

### 綜述與教科書

- Neuroscience Online: An Electronic Textbook for the Neurosciences. Department of Neurobiology and Anatomy, UTHealth McGovern Medical School。https://nba.uth.tmc.edu/neuroscience/ — 免費、開放取用的神經科學電子教科書。
- Felleman, D. J. & Van Essen, D. C.（1991）。Distributed hierarchical processing in the primate cerebral cortex. *Cerebral Cortex*。https://doi.org/10.1093/cercor/1.1.1 — 描繪靈長類皮質中視覺區的階層，把簡單到複雜的想法延伸到 V1 之外。
