---
status: complete
last_reviewed: 2026-11-05
translation_reviewed: 2026-11-05
related:
  - theory/deep-learning/normalisation
  - theory/models/transformer
tags:
  - RMSNorm
  - normalisation
  - language models
aliases:
  - 均方根正規化
  - RMSNorm
  - Root mean square layer normalization
---

# RMSNorm

RMSNorm 使用特徵向量的均方根重新縮放，而不減去平均值。它保留尺度正規化機制，同時放棄 LayerNorm 的平移不變性。Zhang 與 Sennrich 將其提出為較簡單的正規化方法，並在數種模型家族中評估。[^rms]

## 問題與範圍

[正規化章節](index.md)比較整個家族。LayerNorm 在指定特徵上計算平均值與中心化二階動差。RMSNorm 則探討：是否只正規化未中心化二階動差，就能以較少運算取得有用的訓練行為。

這是正規化統計量的選擇，與層在模型中的位置是不同決策。RMSNorm 可用於循環與前饋模型，也可用於 Transformer 殘差區塊。[^rms]

## 方程式與軸

對一組待正規化的 $x\in\mathbb{R}^d$，定義均方值 $q$ 與穩定化分母 $r_\epsilon$：

$$
q=\frac{1}{d}\sum_{i=1}^{d}x_i^2,\qquad
r_\epsilon=\sqrt{q+\epsilon},\qquad
y_i=g_i\frac{x_i}{r_\epsilon}.
$$

其中 $g_i$ 是可學習增益，$\epsilon>0$ 用來穩定零附近的除法。數學上的均方根是 $\sqrt q$；$r_\epsilon$ 則納入實作的穩定項。上式沒有加法偏置。[^implementation]

移除平均值相減，並不禁止後續加入偏置。原論文在正規化且乘上增益的數值之後，寫出形如 $f(\bar a_i+b_i)$ 的激活運算。PyTorch 的 RMSNorm 模組提供增益，卻沒有偏置參數。因此，偏置處理應以具體模型或實作為準。[^rms][^implementation]

對形狀為 $[B,T,D]$ 的激活值，語言模型常見選擇是每個詞元的 $D$ 個特徵各成一組。若改在 $[T,D]$ 上正規化，就會耦合不同詞元。PyTorch 2.15 的模組依指定正規化形狀，沿最後幾個維度彙總；使用形狀 $D$ 與 $(T,D)$ 是不同運算，不需要其他批次樣本的統計量。[^implementation]

## 均方根不等於標準差

令 $\mu=d^{-1}\sum_i x_i$，且 $\sigma^2=d^{-1}\sum_i(x_i-\mu)^2$，則 $q=\sigma^2+\mu^2$：未中心化二階動差同時包含分散程度與平均值偏移。

相較之下，LayerNorm 使用：

$$
y_i^{\mathrm{LN}}=g_i\frac{x_i-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta_i.
$$

即使兩種層使用相同增益與 epsilon，中心化仍會改變正規化後的表示。[^layernorm]

在套用增益或偏置之前，令 $z_i=x_i/r_\epsilon$，其特徵平均值與均方值為：

$$
\frac{1}{d}\sum_i z_i=\frac{\mu}{\sqrt{q+\epsilon}},\qquad
\frac{1}{d}\sum_i z_i^2=\frac{q}{q+\epsilon}.
$$

因此，RMSNorm 一般不會產生零平均值或單位變異數。即使是均方值，也只在 $\epsilon=0$ 且 $q>0$ 的理想情況下恰好等於一。可學習的逐特徵增益還會進一步改變這些統計量。

### 比較算例

以下為自行計算的例子，不是效能測量。對下列非常數向量，使用單位增益、無偏置且 $\epsilon=0$：

| 輸入 | 平均值 | 均方根 | 均方根正規化輸出 | 層正規化輸出 |
|---|---|---|---|---|
| $(1,3)$ | 2 | $\sqrt5$ | $(0.4472,1.3416)$ | $(-1,1)$ |
| $(2,6)$ | 4 | $\sqrt{20}$ | $(0.4472,1.3416)$ | $(-1,1)$ |
| $(3,5)$ | 4 | $\sqrt{17}$ | $(0.7276,1.2127)$ | $(-1,1)$ |

將 $(1,3)$ 加倍，不會改變理想均方根正規化輸出。每個特徵加 2 則會改變該輸出，但中心化的 LayerNorm 輸出不變。這兩種變換測試的是不同不變性。

對非零常數向量與正的 epsilon，LayerNorm 在仿射參數之前的中心化輸出為零；RMSNorm 則保留非零訊號。對零向量，正的 epsilon 使兩者都有有限分母與零輸出。

## 尺度不變性與 epsilon

對非零 $x$ 與正純量 $c$，未加穩定項的均方根滿足 $\mathrm{RMS}(cx)=c\,\mathrm{RMS}(x)$，因此理想均方根正規化對正向縮放不變。若純量為負，正規化向量的符號會反轉。

固定的正 epsilon 會使尺度不變性成為近似：

$$
z_\epsilon(cx)=\frac{cx}{\sqrt{c^2q+\epsilon}}
=\frac{x}{\sqrt{q+\epsilon/c^2}}\qquad(c>0).
$$

當 $q$ 遠大於 $\epsilon$ 與 $\epsilon/c^2$ 時，差異變小；零附近則可能有明顯影響。這是對論文理想縮放分析的條件補充，並非與其矛盾。[^rms]

例如，取 $x=(0.001,0.001)$、$c=2$ 與 $\epsilon=10^{-6}$，每個輸出座標會從約 0.7071 變為 0.8944。因此，若實作測試要求在有限 epsilon 下仍具精確尺度不變性，測試本身就不正確。

## 實作檢查

- **軸與參數。** 記錄正規化形狀、可學習增益、任何獨立偏置與殘差位置。僅有形狀相同，無法證明運算等價。
- **Epsilon 慣例。** 在平方根內加 epsilon，與在平方根後加 epsilon 不同。兩種公式即使複製相同權重，輸出也不會因此一致。
- **精度與預設值。** 比較實作時明確記錄 epsilon。PyTorch 2.15 文件以運算型別說明省略 epsilon 時的預設值：fp16/bf16/fp32 輸入使用 float32 機器 epsilon；fp64 輸入則使用 float64 機器 epsilon。[^implementation]
- **訓練與評估。** 上述均方根統計量來自當前群組，不使用 BatchNorm 式的批次移動統計量。這描述的是正規化方法，並非模型其他位置的丟棄法或其他層的行為。[^batchnorm]

## 結果與限制

原論文報告，在測試設定中取得與 LayerNorm 相當的任務表現，並將運行時間減少 7% 至 64%。這些結果取決於模型與實作，並不保證現代語言模型解碼時間也會降低同樣比例。[^results]

具體例子是表 2 的 TensorFlow/Nematus RNNSearch 翻譯實驗：LayerNorm 每 1,000 個訓練步驟耗時 $665\pm32.5$ 秒，RMSNorm 則為 $501\pm11.8$ 秒。以報告的中心值計算，時間減少 $(665-501)/665\approx24.7\%$，或約為 $665/501\approx1.33$ 倍的步驟吞吐量。時間減少與吞吐量增加使用不同分母。[^results]

論文也研究**部分均方根正規化**，以特徵子集估計統計量。這會改變估計器，與使用全部特徵的一般 RMSNorm 不同；算術運算較少，本身並不保證實際經過時間較短。[^partial]

效能比較應說明硬體、精度、張量形狀、核心與工作負載，再檢查任務品質與端到端時間。移除中心化會改變函數：在已訓練的檢查點中替換 LayerNorm，一般不是保持輸出的改寫。

## 關聯與應用

LLaMA 是具體的語言模型例子：其架構章節指定以 RMSNorm 對 Transformer 子層進行前置正規化。[^llama] [Transformer 頁面](../../models/transformer/index.md)說明更廣泛的區塊結構。

Xiong 等人分析 Transformer 中的 LayerNorm 位置，這項工作有助於將放置位置與統計量選擇視為不同設計決策，卻沒有證明所有 RMSNorm 模型都能使用相同最佳化器設定或省略暖身。[^placement]

[LayerNorm](../../models/mlp/layer-normalisation/index.md)保留中心化，BatchNorm 則使用跨訓練樣本的統計量。[^layernorm][^batchnorm] 選擇方法時，除了測得的成本，也需要考慮應正規化哪些特徵群組與變換。

## 開放問題

對特定任務，保留特徵平均值何時有利或有害？對小激活值，epsilon、精度與融合實作會如何影響行為？原始效率結果並未替所有架構解答這些問題。

[^rms]: Zhang 與 Sennrich（2019），第 3–4 節與第 4.1 節：正規化數值、後續偏置與激活，以及理想不變性分析。
[^layernorm]: Ba、Kiros 與 Hinton（2016），《Layer Normalization》：逐樣本的平均值與變異數統計量，以及可學習增益與偏置。
[^implementation]: PyTorch 2.15，〈RMSNorm〉API 文件：最後幾個正規化軸、僅含增益的模組、epsilon 位置與運算型別預設值。
[^batchnorm]: Ioffe 與 Szegedy（2015），《Batch Normalization》，與本頁的逐群組均方根公式比較。
[^results]: Zhang 與 Sennrich（2019），摘要及第 6 節，尤其表 2：運行時間範圍、翻譯設定與每 1,000 個訓練步驟耗時。
[^partial]: Zhang 與 Sennrich（2019），第 5 節與第 6.1 節：部分均方根估計與取決於實作的時間測量。
[^llama]: Touvron 等人（2023），第 2.2 節：LLaMA 中的 RMSNorm 與前置正規化。
[^placement]: Xiong 等人（2020），《On Layer Normalization in the Transformer Architecture》：LayerNorm Transformer 中隨位置改變的梯度行為。

## 參考文獻

### 奠基性論文

- Zhang, B. & Sennrich, R. (2019). *Root Mean Square Layer Normalization*. NeurIPS 2019. https://arxiv.org/abs/1910.07467 — 提出完整與部分 RMSNorm，提供不變性分析及任務時間測量。
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). *Layer Normalization*. https://arxiv.org/abs/1607.06450 — 定義逐樣本特徵中心化、變異數正規化與可學習仿射參數。
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. https://arxiv.org/abs/1502.03167 — 提出依賴批次的正規化，可與逐樣本特徵統計量比較。
- Xiong, R. et al. (2020). *On Layer Normalization in the Transformer Architecture*. https://arxiv.org/abs/2002.04745 — 分析 LayerNorm 位置如何影響初始梯度與暖身需求。
- Touvron, H. et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. https://arxiv.org/abs/2302.13971 — 記載 LLaMA 架構採用的 RMSNorm 前置正規化。

### 文章與文件

- PyTorch contributors. *RMSNorm*, PyTorch 2.15 documentation. https://docs.pytorch.org/docs/2.15/generated/torch.nn.RMSNorm.html — 指定正規化軸、仿射增益、epsilon 慣例與數值預設值。
