---
translation_reviewed: 2026-10-29
---

# 隱馬可夫模型

隱馬可夫模型（HMM）是一種有向圖模型：隱藏狀態序列依循馬可夫鏈變動，每個狀態再發出一個觀測值。我們只看得到觀測值，必須從中推斷狀態。本頁是[機率圖模型](index.md)的一部分。

## 概述

許多序列背後都有一個沒有直接測量的狀態，例如正在說的音素、DNA 序列中的基因區段，或一連串感測器讀數背後的天氣。HMM 以兩層結構來描述這件事：隱藏鏈 \(z_1,\dots,z_T\) 承載狀態，觀測值 \(x_1,\dots,x_T\) 則由狀態發出。模型簡單，推論是精確的，並且曾長期是語音辨識的標準工具（Rabiner，1989）。

## 關鍵概念

- **轉移矩陣** \(A\)：\(A_{ij}=p(z_t=j\mid z_{t-1}=i)\)。
- **發射模型** \(B\)：分布 \(p(x_t\mid z_t)\)，可為離散或連續的。
- **初始分布** \(\pi\)：\(p(z_1)\)。
- **馬可夫性質**：時刻 \(t\) 的隱藏狀態只依賴時刻 \(t-1\) 的狀態。

## 運作方式

聯合分布沿著鏈分解：

\[
p(x_{1:T},z_{1:T}) = \pi(z_1)\prod_{t=2}^{T}A_{z_{t-1}z_t}\prod_{t=1}^{T}B_{z_t}(x_t).
\]

Rabiner（1989）把標準問題整理為三項：

1. **評估**：計算 \(p(x_{1:T})\)。前向遞迴 \(\alpha_t(j)=B_j(x_t)\sum_i \alpha_{t-1}(i)A_{ij}\) 可在 \(K\) 個狀態下以 \(O(TK^2)\) 的時間求得，且 \(p(x_{1:T})=\sum_j\alpha_T(j)\)。
2. **解碼**：找出最可能的狀態序列。Viterbi 演算法把前向遞迴中的求和換成求最大值，並保留回溯指標。Viterbi（1967）提出此演算法，用於解碼迴旋碼。
3. **學習**：估計 \(A\)、\(B\) 與 \(\pi\)。Baum–Welch 程序是期望最大化的一個實例，它利用前向與後向遞迴計算各狀態的後驗機率。Baum 等人（1970）給出此方法最早的統計分析。

**前向–後向**演算法把前向掃描與後向掃描 \(\beta_t\) 合併，得到每個時間點的後驗 \(p(z_t\mid x_{1:T})\)。它就是鏈上的[信念傳播](belief-propagation.md)。

### 教學動畫：Viterbi 解碼與回溯

![四階段 Viterbi 狀態格，呈現最大乘積分數與 A–B–A 回溯路徑](../../../../assets/concept-animations/viterbi-trellis-motion.svg)

*原創教學動畫，CC BY-SA 4.0。* [GitHub 靜態預覽](../../../../assets/concept-animations/viterbi-trellis-still.svg)。在 MkDocs 網站可使用**播放／暫停**按鈕，也可用 Tab 與 Enter 操作；啟用減少動態效果時，顯示最終路徑的靜態圖。

範例包含 A、B 兩個隱藏狀態與三個觀測值。**教學示意**的初始分布為 \(\pi=(0.6,0.4)\)，轉移矩陣的 A、B 列分別為 \((0.7,0.3)\)、\((0.4,0.6)\)，三個時間點的 A/B 發射概似依序為 \((0.8,0.3)\)、\((0.2,0.9)\)、\((0.7,0.4)\)。Viterbi 遞迴 \(\delta_t(j)=p(x_t\mid z_t=j)\max_i[\delta_{t-1}(i)A_{ij}]\) 對每個狀態保留最佳前驅，而不是像前向演算法那樣對所有路徑求和。節點上的分數經過四捨五入；最後一步 \(\delta_3(A)=0.036288\)、\(\delta_3(B)=0.031104\)，回溯得到 **A → B → A**。這是最可能的**聯合狀態序列**，不是逐時間點獨立最大化邊際機率的結果。所有數值均為手算示意，**不是模型實測輸出**（Viterbi，1967；Rabiner，1989）。

## 變體

- **離散 HMM** 從有限字母表發出觀測值，**高斯 HMM** 則發出連續向量，通常每個狀態使用一個高斯混合。
- **輸入–輸出 HMM** 與**隱半馬可夫模型**，分別以依輸入而變的轉移及明確的狀態持續時間，擴充基本形式。
- 具連續狀態的線性高斯狀態空間模型，其推論導向卡爾曼濾波器（Kalman，1960）。

## 結果與限制

- 三種演算法對鏈狀結構都是精確且有效率的。成本隨狀態數的平方成長。
- 馬可夫假設很強。時刻 \(t\) 的狀態不記得更早的歷史，因此長程依賴必須靠擴大狀態空間來編碼。
- 在許多任務中，判別式與神經序列模型已取代 HMM，但 HMM 仍是推論與可解釋機率結構的清楚基準。
- 以 Baum–Welch 學習得到的是概似的局部最大值，結果取決於初始化。

## 應用

- **語音辨識**：狀態對應音素或次音素單位，觀測值為聲學特徵向量（Rabiner，1989）。
- **解碼**：Viterbi 解碼迴旋碼，演算法之名即由此而來（Viterbi，1967）。
- **生物資訊學**：從序列偵測基因與蛋白質功能域，隱藏狀態標記功能區段。

## 開放問題

- 隱藏狀態的數量大多仰賴經驗決定，而用於模型選擇的準則並不完善。
- 序列中的長程結構需要更多狀態或更豐富的模型，也使推論成本上升。
- 在資料充足的任務上，HMM 與神經序列模型之間的差距已有大量記錄，但其原因只得到部分理解。

## 參考文獻

### 奠基性論文

- Baum, L. E., Petrie, T., Soules, G. & Weiss, N. (1970). A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains. *The Annals of Mathematical Statistics* 41(1), 164–171. https://doi.org/10.1214/aoms/1177697196 — 提出估計隱馬可夫模型參數的期望最大化式程序。
- Viterbi, A. J. (1967). Error bounds for convolutional codes and an asymptotically optimum decoding algorithm. *IEEE Transactions on Information Theory* 13(2), 260–269. https://doi.org/10.1109/TIT.1967.1054010 — 提出 Viterbi 演算法，用以解碼最可能的狀態序列。
- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE* 77(2), 257–286. https://doi.org/10.1109/5.18626 — 針對評估、解碼與學習三大問題的 HMM 教學綜述，並含語音應用。
- Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering* 82(1), 35–45. https://doi.org/10.1115/1.3662552 — 線性高斯模型（HMM 的連續狀態對應）的遞迴估計器。

### 綜述與教科書

- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；有 HMM 推論與學習的章節。
- Kschischang, F. R., Frey, B. J. & Loeliger, H.-A. (2001). Factor graphs and the sum-product algorithm. *IEEE Transactions on Information Theory* 47(2), 498–519. https://doi.org/10.1109/18.910572 — 說明前向–後向演算法即因子圖上的和積訊息傳遞。
