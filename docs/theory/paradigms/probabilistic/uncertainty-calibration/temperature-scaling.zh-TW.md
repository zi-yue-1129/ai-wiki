---
translation_reviewed: 2026-10-30
---

# 溫度縮放

溫度縮放是一種事後校準方法，在 softmax 之前，把神經網路的 logits 除以一個學得的純量，也就是溫度。它不改變預測的標籤，只調整機率的信心程度。本頁是[不確定性量化與校準](index.md)的一部分。

## 概述

以交叉熵損失訓練的現代神經網路，即使準確，在測試資料上往往也過度自信。Guo 等人（2017）發現，校準偏差隨模型大小與深度增加，而以保留資料擬合的單一純量就能修正大部分偏差。溫度縮放是最簡單的此類修正，以其成本而言很難被超越。

## 關鍵概念

- **Logits**：網路在 softmax 之前產生的未正規化分數 \(z\)。
- **溫度**：一個正的純量 \(T\)。大於一的值使分布變得平滑，小於一的值則使其變得尖銳。
- **負對數概似（NLL）**：在保留集上最小化的損失，用來擬合 \(T\)。
- **事後**：在訓練之後套用，因此不改變網路的權重。

## 運作方式

校準後的機率為

\[
\hat p_k = \frac{\exp(z_k/T)}{\sum_j \exp(z_j/T)}.
\]

參數 \(T\) 的選擇使驗證集上標籤的 NLL 最小。由於把所有 logits 除以同一個正數不會改變它們的排序，預測的類別以及準確率都不會改變，只有信心程度改變。Guo 等人（2017）以簡單的一維最佳化來擬合 \(T\)，並報告它在影像基準上大幅降低深度網路的期望校準誤差。


<div style="max-width:100%;overflow-x:auto" role="group" aria-label="Temperature scaling animation">
<div style="width:640px">
<img src="../../../../assets/concept-animations/temperature-softmax-still.svg" data-motion-src="../../../../assets/concept-animations/temperature-softmax-motion.svg" alt="固定示意 logits 為 A=3、B=1、C=0；溫度從 0.5 上升至 2 再下降時，softmax 機率長條連續變化，但預測類別始終為 A。" width="640" height="360">
</div>
</div>

*原創教學動畫（CC BY-SA 4.0）。* 以固定示意 logits（3、1、0）計算溫度由 0.5 增至 2 再返回時的 softmax 機率。動畫計算 41 個精確取樣點，點與點之間採視覺插值，**插值影格不是額外的模型運算結果**；所有正溫度下的 argmax 均為 A。**數值並非實際模型輸出，也不是透過驗證集擬合的校準溫度。** MkDocs 網站可播放／暫停；[GitHub 靜態預覽](../../../../assets/concept-animations/temperature-softmax-still.svg) 顯示 T=1。手機可水平捲動查看原尺寸圖。理論來源見參考文獻中的 Guo 等人（2017）。

## 變體

- **向量縮放**為每個類別使用各自的尺度與偏置，較有彈性，但需要更多資料。
- **矩陣縮放**對 logits 使用完整的線性映射，是此族中表達力最強的，也最容易過擬合。
- **直方圖分箱**擬合一個從信心到準確率的分段常數映射，是非參數的替代方法。

## 結果與限制

- 成本低、只有一個參數，且不改變分類器的預測，因此很容易部署。
- 它是全域的修正，無法修正隨類別或輸入而異的校準偏差。
- 它需要一個與測試分布相似的保留集，在分布偏移下效果較差。
- 當測試資料與校準資料不同時，其效益可能較弱，因為擬合得到的溫度假設兩者相似。

## 應用

- **部署分類器**：不需重新訓練，即可修正已訓練網路的信心程度。
- **基準比較**：影像分類器校準研究中的標準基準。
- **決策門檻**：校準後，對預測機率設定的門檻才有意義。

## 開放問題

- 分布偏移下的校準只得到部分解決，在某一分布上擬合的單一溫度可能無法遷移。
- 校準方法是否同樣有助於語言模型與其他大型生成式模型，仍是待實證的問題。

## 參考文獻

### 奠基性論文

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70. https://proceedings.mlr.press/v70/guo17a.html — 為神經網路提出溫度縮放，並與其他校準方法比較。
- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review* 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 — 提出機率預測的適當評分規則，是校準的對應指標。
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning*, 625–632. https://doi.org/10.1145/1102351.1102430 — 比較分類器的校準方法，包括 Platt 縮放與等張迴歸。

### 綜述與教科書

- DeGroot, M. H. & Fienberg, S. E. (1983). The comparison and evaluation of forecasters. *The Statistician* 32(1/2), 12–22. https://doi.org/10.2307/2987588 — 定義機率預測的校準。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋校準與事後方法。
- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/gal16.html — 為同類網路提供另一種不確定性的途徑。
