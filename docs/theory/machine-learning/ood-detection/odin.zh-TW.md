---
translation_reviewed: 2026-10-29
---

# ODIN

ODIN 在預訓練分類器的 softmax 分布外（OOD）偵測器中加入溫度縮放，以及提高分數的輸入擾動，無須重新訓練權重。[^odin] 本頁是[分布外偵測](index.md)的一部分。

## 問題與基準

OOD 偵測器判斷是否將輸入接受為分布內（ID），這和選擇分類標籤不同。Hendrycks 與 Gimpel 以最大 softmax 機率作為基準分數。他們的實驗顯示這種分數具有區分能力，而非證明高分輸入必定熟悉或分類正確。[^baseline]

## 運作方式

令 $f_i(x)$ 為 $K$ 個類別中，第 $i$ 類的 logit，也就是尚未正規化的類別分數。ODIN 使用[^odin]

$$
S_i(x;T)=\frac{\exp(f_i(x)/T)}
{\sum_{j=1}^{K}\exp(f_j(x)/T)},\qquad
\hat y=\arg\max_i f_i(x).
$$

微分時固定 $\hat y$。對 $\varepsilon\geq0$，構造

$$
\tilde x=x+\varepsilon\,\operatorname{sign}
\left(\nabla_x\log S_{\hat y}(x;T)\right),
\qquad
s(x)=\max_i S_i(\tilde x;T).
$$

當 $s(x)>\delta$ 時接受為 ID，否則標記為 OOD。實際流程是先做一次前向傳播，再做一次對輸入求梯度的反向傳播，最後對 $\tilde x$ 再做一次前向傳播。預測類別提供梯度目標，因此不需要真實標籤。分類輸出仍可使用原始影像。[^odin]

### 提高溫度究竟改變了什麼

對固定的 logits 與正溫度 $T$，除以 $T$ 不會改變其排序。當 $T$ 增加，softmax 會更平坦；當 $T\to\infty$，每個類別的機率都趨近 $1/K$。這**不會**將同一輸入中不同類別的機率拉得更開。Guo 等人在校準方法中說明了這種平滑效果，以及預測類別保持不變的性質。[^calibration]

例如，兩個 logits 為 $(2,0)$ 時，最大機率在 $T=1$ 時約為 $0.881$，在 $T=10$ 時約為 $0.550$，並逐漸趨近 $0.5$。這些數值直接由 $1/(1+\exp(-2/T))$ 算出。這個算例說明的是公式，而非實測的 OOD 偵測結果。

OOD 的區分能力涉及**不同輸入之間的分數分布**，而非同一輸入中不同類別機率的距離。偵測與機率校準的目標也不同：Guo 等人以有標籤驗證資料上的負對數概似擬合溫度；為拒絕決策選出的溫度，未必能使信心對應到實際答對的頻率。[^calibration]

## 論文結果及其適用範圍

Liang 等人的表 2 顯示：以 CIFAR-10 訓練的 Dense-BC，對 **TinyImageNet（crop）** 的 FPR，在 TPR 為 95% 時從 **34.7% 降至 4.3%**。此處以 ID 為正類：FPR 指 OOD 輸入被錯誤接受為 ID，而非分類器的類別錯誤率。實驗使用獨立的 iSUN 驗證資料調整參數。[^odin]

這是指定模型與資料集組合的歷史結果，並非部署保證或當前排名。

## 重現與評估偵測器

以下是報告清單，並不主張同一組參數適用於所有分類器：

1. 記錄模型權重版本、輸入正規化、影像縮放與分數方向。
2. 分開調參資料與 OOD 測試集。說明調參時可取得哪些 OOD 樣本。
3. 記錄 $T$、$\varepsilon$ 與 $\delta$，包括施加擾動時使用的座標系統。
4. 在相同資料與操作點下，比較完整偵測器與未修改的 softmax 基準。
5. 報告分數分布、ID 輸入的錯誤拒絕、OOD 輸入的錯誤接受，以及實測執行時間。
6. 檢查多種合理的分布偏移，而非只挑選最容易區分的負類資料集。

門檻表達一項權衡：降低門檻會接受更多輸入，可能同時保留更多 ID 輸入，也接受更多 OOD 輸入。這個分數是決策統計量，並非輸入屬於訓練分布的經認證機率。

## 關聯與替代方法

- **機率校準**調整信心，使其更符合實際答對的頻率；這與偵測陌生輸入不同。[^calibration]
- [馬氏距離偵測器](mahalanobis-distance.md)使用到類別條件特徵分布的距離，而非僅使用輸出機率。[^mahalanobis]
- **能量式偵測**提供另一種以 logits 為基礎的分數。Liu 等人分別研究對預訓練分類器評分，以及使用能量式目標訓練；兩者是不同的實驗設定。[^energy]

這些方法是比較對象，而非 ODIN 全面優於替代方法的證據。

## 限制與可能用途

偵測旗標可以接到棄答或人工審查流程，但接受輸入並不證明分類正確。輸入梯度需要的存取能力，超過僅回傳標籤或機率的服務；擾動流程的成本也高於單次普通前向傳播。實際延遲取決於模型與實作。

驗證資料的選擇、前處理與負類資料的種類，都應列入評估報告。完整的部署決策還須說明拒絕後如何處理，並另外測試該備援流程。

[^odin]: Liang et al.（2018），第 2–4 節與表 2；詳見參考文獻。
[^baseline]: Hendrycks & Gimpel（2017），摘要；詳見參考文獻。
[^calibration]: Guo et al.（2017），第 4.2 節的溫度縮放；詳見參考文獻。
[^mahalanobis]: Lee et al.（2018），摘要；詳見參考文獻。
[^energy]: Liu et al.（2020），摘要；詳見參考文獻。

## 參考文獻

- Liang, S., Li, Y. & Srikant, R. (2018). *Enhancing the Reliability of Out-of-distribution Image Detection in Neural Networks*. ICLR. https://arxiv.org/abs/1706.02690 — 定義溫度縮放、輸入前處理、偵測器及其影像基準評估。
- Hendrycks, D. & Gimpel, K. (2017). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. ICLR. https://arxiv.org/abs/1610.02136 — 建立以最大 softmax 機率為基礎的分類錯誤與 OOD 偵測基準。
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks*. ICML, PMLR 70:1321–1330. https://proceedings.mlr.press/v70/guo17a.html — 說明機率校準，以及以驗證資料的負對數概似擬合溫度縮放。
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. NeurIPS. https://arxiv.org/abs/1807.03888 — 提出使用類別條件高斯模型與馬氏距離的特徵式偵測器。
- Liu, W., Wang, X., Owens, J. D. & Li, Y. (2020). *Energy-based Out-of-distribution Detection*. https://arxiv.org/abs/2010.03759 — 研究預訓練分類器的能量分數，以及用於 OOD 偵測的能量式訓練。
