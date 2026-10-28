---
translation_reviewed: 2026-10-28
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- theory/models/speech
tags:
- neuroscience
- perception
- speech
aliases:
  - 聽覺系統
  - 聽覺皮層
  - 耳蝸
  - 音調拓撲
  - Auditory System
  - Auditory Cortex
  - Cochlea
  - Tonotopy
---

# 聽覺系統

聽覺把空氣中的壓力波轉換為人們日常使用的語音、音樂與警示聲。本頁說明耳蝸與聽覺皮層如何完成這件事，以及在聲音上訓練的深度網路如何被用來模擬皮層。它是[視覺知覺與視覺系統](../visual-perception/index.md)的聽覺對應頁。

## 概述

聲音到達耳朵時，只是一個起伏的壓力訊號，但聽者仍能在嘈雜的房間裡從一個人的聲音中分辨出字詞、辨認旋律，並定位聲音的來源。聽覺系統必須把這個混合訊號拆成各個聲源，並還原每個聲源的內容。它的早期階段把聲音分解為頻率帶，後期階段則抽取音高、音素與說話者身分等特徵。[神經科學基礎](../neuroscience/index.md)說明了研究這些階段所用的記錄方法。

## 關鍵概念

- **耳蝸**：內耳中呈螺旋狀的器官。其基底膜與毛細胞把聲音振動轉為神經放電，每個位置調諧於不同的頻率。
- **音調拓撲**：頻率在某個結構上的有序排列。相鄰位置對相鄰頻率作出反應。
- **頻譜圖（耳蝸圖）**：聲音的時間－頻率圖像。許多聽覺模型以它為起點。
- **聽覺階層**：從初級聽覺皮層到周邊非初級區域的一系列階段，對愈來愈複雜的聲音特徵作出反應。
- **雞尾酒會問題**：在多人說話中跟隨其中一人的任務，是語音在噪音中辨識的經典測試。

## 核心想法

1. **耳蝸依頻率分類聲音。** 基底膜攜帶一道行進波，其波峰位置由頻率決定。高頻波峰在靠近基部處，低頻波峰在靠近頂端處。外毛細胞提供主動放大，使安靜聲音的調諧更為銳利（Robles & Ruggero, 2001）。
2. **頻率圖延續到皮層。** 人類初級聽覺皮層含有兩張互為鏡像的音調拓撲圖（Formisano 等人, 2003）。
3. **核心之外，各區域逐漸專精。** 非初級區域包括對音高、音樂與語音具有選擇性的區域（Kell 等人, 2018）。Rauschecker 與 Scott（2009）綜述聽覺皮層中的圖與路徑，並參照靈長類研究。Hickok 與 Poeppel（2007）則綜述皮層中語音處理的組織方式。
4. **皮層追隨被注意的聲音。** Cherry（1953）研究聽者在兩段語音同時呈現時的語音辨識。來自非初級人類聽覺皮層的記錄顯示，在兩人混合語音中，皮層編碼被注意說話者的特徵（Mesgarani & Chang, 2012）。這暗示注意力影響皮層編碼的內容，而不只是耳朵接收到的內容。
5. **受訓練的網路呈現類似皮層的階層。** 僅訓練於辨識字詞與音樂類型的深度網路，重現了類似人類的行為，並且比頻譜時間濾波器模型更能預測功能性磁振造影（fMRI）反應。它的中間層最能預測初級皮層，較深的層則最能預測非初級區域（Kell 等人, 2018）。

## 運作方式

聲音進入耳蝸後，被濾波成彼此重疊的頻率通道。毛細胞把每個通道的運動轉為聽神經的脈衝。訊號接著經過腦幹到達視丘，再進入初級聽覺皮層。每個階段保留部分頻率圖，並加入依賴時間的特徵，例如響度變化的速率。

語音在噪音中的情況最為困難。多人的聲音在頻率與時間上彼此重疊，系統必須利用音高、時間、方位等線索，並借助注意力，才能將它們分開。與此相關的機制在視覺中由[偏向競爭](../attention-brain-machine/biased-competition/index.md)理論描述。

## 主要方法

每種方法都有自己的頁面。此列表只是比較。

- [任務最佳化神經網路（Kell 等人，2018）](kell-2018/index.md)：在語音與音樂任務上訓練深度網路，再測試它與行為及大腦反應的吻合程度，訓練過程中不使用大腦資料。
- [多解析度頻譜時間模型（Chi 等人，2005）](chi-2005/index.md)：以人工設計的方式描述皮層分析，依頻譜與時間結構表示聲音。受訓練的網路正是拿來與這類模型比較的對象。

## 連結

- **視覺系統**：同樣的問題，即為某任務訓練的網路能否預測皮層，最先是在視覺上檢驗的。見[效能最佳化網路（Yamins 等人，2014）](../visual-perception/yamins-2014/index.md)。
- **NeuroAI**：聽覺的情況是[NeuroAI](../neuroai/index.md)頁面中任務最佳化範式表格的一列。
- **語言**：語音路徑連結到[Hickok 與 Poeppel 的雙路徑模型](../language-in-brain/hickok-poeppel-2007/index.md)，以及[大腦中的語言](../language-in-brain/index.md)。
- **注意力**：雞尾酒會問題是注意力問題，見[注意力與腦機](../attention-brain-machine/index.md)。
- **神經影像**：本頁的部分人類研究來自 fMRI，其限制見[BOLD fMRI](../neuroimaging-methods/bold-fmri/index.md)。
- **感受野**：聽覺神經元在時間與頻率上都有感受野。視覺的情況見[視覺皮層的感受野](../neuroscience/receptive-fields-hubel-wiesel/index.md)。

## 應用

- **助聽器與人工耳蝸**：它們取代或增強耳蝸的頻率分析，其設計依賴上述的耳蝸力學。
- **語音技術**：語音辨識系統及其前端使用以頻譜圖為基礎的特徵，這正是聽覺模型的起點。見[語音與音訊](../../theory/models/speech/index.md)。
- **語音神經義肢**：解碼與語音相關的腦訊號以恢復溝通，見[語音神經義肢](../bci/speech-neuroprosthesis/index.md)。

## 開放問題

- **相似性能走多遠？** 網路與皮層階層的吻合是部分的。網路仍有一些可靠的反應無法解釋，而且其最後幾層對皮層的預測很差。
- **哪些任務塑造了階層？** Kell 等人（2018）只用了兩項任務。若改用其他任務，例如聲源定位或說話者辨識，是否會改變與皮層相符的層，目前不得而知。
- **聽者如何分開人聲？** 選擇單一說話者的皮層機制，以及注意力如何改變這些機制，仍在研究中。
- **人類如何從如此少的資料學習？** 網路以數百萬筆有標籤的資料訓練，遠多於人們在聽覺學習中通常接受的明確監督。

## 參考文獻

### 開創性論文

- Cherry, E. C.（1953）。Some experiments on the recognition of speech, with one and with two ears. *Journal of the Acoustical Society of America*。https://doi.org/10.1121/1.1907229 — 研究兩段語音同時呈現時的語音辨識，以及不同語音分別送入兩耳時的聽者行為。
- Formisano, E., Kim, D.-S., Di Salle, F., van de Moortele, P.-F., Ugurbil, K. & Goebel, R.（2003）。Mirror-symmetric tonotopic maps in human primary auditory cortex. *Neuron*。https://doi.org/10.1016/S0896-6273(03)00669-X — 報告人類初級聽覺皮層中兩張互為鏡像的音調拓撲圖。
- Mesgarani, N. & Chang, E. F.（2012）。Selective cortical representation of attended speaker in multi-talker speech perception. *Nature*。https://doi.org/10.1038/nature11020 — 顯示來自非初級人類聽覺皮層的記錄，在兩人混合語音中編碼被注意說話者的特徵。
- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H.（2018）。A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*。https://doi.org/10.1016/j.neuron.2018.03.044 — 在語音與音樂任務上訓練網路，並與人類行為及聽覺皮層 fMRI 比較。

### 綜述與教科書

- Robles, L. & Ruggero, M. A.（2001）。Mechanics of the mammalian cochlea. *Physiological Reviews*。https://doi.org/10.1152/physrev.2001.81.3.1305 — 綜述耳蝸力學：行進波、音調的位置編碼與外毛細胞放大。
- Rauschecker, J. P. & Scott, S. K.（2009）。Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*。https://doi.org/10.1038/nn.2331 — 綜述聽覺皮層中的圖與路徑，參照靈長類研究，並討論其對人類語音處理的意義。
- Hickok, G. & Poeppel, D.（2007）。The cortical organization of speech processing. *Nature Reviews Neuroscience*。https://doi.org/10.1038/nrn2113 — 綜述語音處理在皮層中的組織方式。
