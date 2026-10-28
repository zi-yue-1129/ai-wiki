---
translation_reviewed: 2026-10-28
---

# 相位-振幅耦合與調變指數

相位-振幅耦合是快速振盪的振幅依賴於較慢振盪相位的現象。Tort 等人（2010）提出了一個量測方法，即調變指數，將耦合的強度化為單一數值。本頁是[神經振盪與同步](../index.md)所列方法之一。

## 概述

大腦的節律不只是並行運作。在海馬迴與新皮質中，快速 γ 振盪的振幅常隨較慢 θ 節律的相位起伏。Canolty 等人（2006）在人類皮質中報告了這一現象。這種現象稱為跨頻耦合。最受研究的案例是 θ–γ 耦合，它與記憶有關（見[主題頁](../index.md)的「與其他主題的關聯」一節）。

描述耦合比量測它容易。量測必須與機率下的結果比較，這點在設計時需要考慮。Tort 等人所提出的指數正是為此而設計，至今仍是常見的選擇。

## 關鍵概念

- **跨頻耦合（CFC）**：慢振盪的相位調變快振盪振幅的交互作用。
- **相位**：慢振盪在其週期中的位置，從帶通濾波後的訊號取得，通常使用 Hilbert 轉換。
- **振幅包絡**：快振盪平滑變化的強度，同樣以 Hilbert 轉換取得。
- **相位區間（bin）**：慢週期的一個切片，例如寬 20 度。在每個區間內計算快振盪的平均振幅。
- **替代資料**：打亂或時間平移後的記錄版本，用來估計機率下的耦合。

## 運作方式

分析依循固定的步驟。

1. 將記錄分別以慢頻帶（相位頻帶）與快頻帶（振幅頻帶）帶通濾波。
2. 以 Hilbert 轉換取得慢訊號的瞬時相位 $\phi(t)$，以及快訊號的振幅包絡 $A(t)$。
3. 將相位範圍分成 $N$ 個區間。
4. 在每個區間 $j$ 中平均快振幅得到 $A_j$，並標準化為分布 $p_j = A_j / \sum_k A_k$。
5. 計算此分布的熵 $H = -\sum_{j=1}^{N} p_j \log p_j$，並得到調變指數

$$\mathrm{MI} = \frac{\log N - H}{\log N}.$$

若每個區間的振幅相同，則 $p_j = 1/N$，$H = \log N$，MI 為 0。若所有振幅都落在單一區間，則 $H = 0$，MI 為 1。Tort 等人將此指標描述為 Kullback–Leibler 距離的一種調整，它衡量經驗相位-振幅分布偏離均勻分布的程度。上式的標準化形式，就是此距離除以其最大值。

6. 將數值與替代分布比較，例如由時間平移的振幅序列所構成的分布，以判斷耦合是否超過機率水準。

## 結果

- **人類皮質（Canolty 等人，2006）。** 皮質電圖記錄顯示，4 到 8 Hz 的 θ 相位調變了 80 到 150 Hz 的高 γ 功率，且在 θ 振幅較高時調變較強。
- **比較與大鼠海馬迴（Tort 等人，2010）。** 作者將其指數與其他七種耦合量測比較，發現它特別適合此任務。他們接著將其應用於自由活動大鼠的記錄，並報告 CA3 與 CA1 區呈現不同的耦合特徵。
- **記憶（Tort 等人，2009）。** 大鼠學習將項目與空間情境相連時，CA3 的 θ–γ 耦合增強。低 γ 頻段（30 到 60 Hz）更強地受 θ 相位調變，而耦合強度與正確率的提升相關。作者認為耦合可能在記憶提取中扮演角色。

## 限制

- **強度，而非機制。** 此指數量測振幅依賴相位的強度。它無法說明因果，也無法說明影響的方向。
- **對分析選擇敏感。** 結果取決於濾波器、相位區間數與資料長度。Tort 等人討論了這些依賴性，並建議使用替代資料控制。
- **人為假象。** 耦合可能因慢波形的形狀，或因相鄰頻帶重疊而出現在濾波後的訊號中。需要謹慎選擇濾波器並進行替代檢驗，才能區分真實耦合與假象。

## 開放問題

- **耦合對記憶是否必要？** 與學習的相關性並不能說明節律是否必要，還是只是伴隨著有用的腦狀態。
- **耦合承載什麼？** Lisman 與 Jensen（2013）提出，θ–γ 耦合組織一串項目，每個 γ 子週期對應一個項目。檢驗這個提議需要能解析個別項目的記錄。
- **哪些頻率組合重要？** 許多頻率組合都曾報告過耦合。目前不清楚哪些反映一般機制，哪些只針對特定任務。

## 參考文獻

### 開創性論文

- Tort, A. B. L., Komorowski, R., Eichenbaum, H. & Kopell, N. (2010). Measuring phase-amplitude coupling between neuronal oscillations of different frequencies. *Journal of Neurophysiology*. https://doi.org/10.1152/jn.00106.2010 — 提出調變指數，並與其他耦合量測比較。
- Canolty, R. T. et al. (2006). High gamma power is phase-locked to theta oscillations in human neocortex. *Science*. https://doi.org/10.1126/science.1128115 — 人類皮質電圖記錄，顯示 θ 相位調變高 γ 功率。
- Tort, A. B. L., Komorowski, R. W., Manns, J. R., Kopell, N. J. & Eichenbaum, H. (2009). Theta–gamma coupling increases during the learning of item–context associations. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.0911331106 — 大鼠海馬迴記錄，顯示 CA3 的 θ–γ 耦合在聯想學習期間增強。
- Lisman, J. E. & Jensen, O. (2013). The theta-gamma neural code. *Neuron*. https://doi.org/10.1016/j.neuron.2013.03.007 — 提出每個 θ 週期內的 γ 子週期代表連續項目，作為神經編碼。

### 綜述與教科書

- Canolty, R. T. & Knight, R. T. (2010). The functional role of cross-frequency coupling. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2010.09.001 — 綜述跨頻耦合在腦活動中被提出的功能角色。
- Colgin, L. L. (2016). Rhythms of the hippocampal network. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn.2016.21 — 綜述海馬迴迴路的 θ 與 γ 節律，以及它們與記憶和導航的關係。
