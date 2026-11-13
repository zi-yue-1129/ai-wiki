---
translation_reviewed: 2026-11-13
---

# Informer

Informer 是用於長序列時間序列預測的 Transformer，這項任務是一次預測數百個未來步。它保留 [Transformer](../transformer/index.md) 的編碼器－解碼器結構，但改動三個部分：稱為 ProbSparse 的稀疏注意力機制、在編碼器各層之間縮短序列的蒸餾操作，以及一次產生整個預測期的生成式解碼器。它是 [時間序列預測](index.md) 概觀頁比較的代表性方法之一。

## 問題

預測較長的預測期（例如一週的每小時電力負載），需要一個能把相距很遠的輸出步與輸入步連結起來的模型。Transformer 在這方面表現很好，但它的自注意力會把每個查詢與每個鍵比較，因此成本隨序列長度呈二次成長。它常用的解碼器又一次只產生一步，速度慢，且會累積誤差。論文探討的問題是：Transformer 能否效率夠高，足以處理這樣的長預測期。

## 核心想法

作者觀察到，在訓練好的注意力層中，只有少數查詢的注意力分布非常集中。這些查詢攜帶了大部分資訊，其餘查詢則產生近乎均勻的平均。ProbSparse 注意力只對重要的查詢投入完整計算。蒸餾操作在每個注意力區塊之後把編碼器表示的長度減半；生成式解碼器則以一段已知歷史作為起始上下文，一次填滿整個目標視窗。

## 方程式與演算法

**ProbSparse 注意力。** 對維度為 $d$ 的查詢 $\mathbf{q}_i$ 與鍵 $K$，論文以最大－平均度量衡量某個查詢的注意力分布偏離均勻分布的程度：

$$
M(\mathbf{q}_i, K) = \max_j \frac{\mathbf{q}_i \mathbf{k}_j^\top}{\sqrt{d}} - \frac{1}{L_K}\sum_{j=1}^{L_K}\frac{\mathbf{q}_i \mathbf{k}_j^\top}{\sqrt{d}}
$$

論文不精確計算此值，而是從約 $L_K \ln L_Q$ 個隨機抽樣的鍵內積估計分數，保留前 $u = c \ln L_Q$ 個查詢並給予完整注意力，其中 $c$ 在實務中取 5。其餘查詢則取值的平均。作者將成本表示為時間與記憶體的 $O(L \ln L)$。

**自注意力蒸餾。** 在注意力區塊之間，一個核寬為 3 的一維卷積、ELU 激活函數，以及步幅為 2 的最大池化會把時間維度減半。多個堆疊接收逐步縮短的輸入，其輸出再串接起來，因此編碼器的記憶體用量得以降低。

**生成式解碼器。** 解碼器的輸入由一段起始符號區段（取自目標之前的已知歷史）與目標視窗的零佔位符號串接而成。經過遮罩注意力與全連接層後，所有未來步會一併產生。由於預測結果不會回授為輸入，解碼器避免了逐步推論中的誤差累積。

## 結果

論文在電力變壓器溫度資料集（ETTh1、ETTh2、ETTm1）、用電量資料（ECL）與氣象資料上進行評估。其單變量表格以預測視窗上的平均平方誤差與平均絕對誤差報告結果。在 ETTh1 最長的單變量預測期（720 步）上，Informer 的 MSE 為 0.269，同一格中 DeepAR 為 0.658。論文中標示為 Informer† 的標準注意力變體在該格為 0.257，因此高效機制並非在每一格都獲勝。作者統計單變量與多變量兩組表格，認為 Informer 在多數設定中表現最佳，並報告在數個預測期上，相較於 LSTMa，以及相較於 DeepAR、ARIMA 與 Prophet，其 MSE 都有大幅下降。

## 限制

- 作者指出，多變量設定下的提升小於單變量設定，並將原因留待未來研究。
- 在 ECL 資料集上，較短的預測期中 DeepAR 優於 Informer。作者把 Informer 在較長預測期上的優勢歸因於較好的擴展性。
- 實驗設定為可在單一 GPU 上執行，而記憶體消融實驗也縮小了批次大小、注意力頭數與模型維度。更大規模的結果並未展示。
- 關於 top-$u$ 選取的理論依賴近似。作者以數值例子支持這些近似，並指出其中一個條件可以放寬。
- 後續研究質疑注意力是否必要。Zeng 等人（2023）的批評指出，在常見基準上，簡單的線性模型能與數個 Transformer 預測器（包括 Informer）相當，甚至更好。這個結果取決於所用的資料集與預測期，因此 Transformer 在預測上的價值仍有爭議。

## 關聯

Informer 是帶有更低成本注意力的 [Transformer](../transformer/index.md)，因此若要比較其他高效注意力設計，可參考[注意力變體](../transformer/attention-variants/index.md)頁面。它一次輸出整個預測期，與 [DeepAR](deepar.md) 的自迴歸抽樣，以及 [N-BEATS](n-beats.md) 的全連接基底展開形成對比。它的編碼器－解碼器配置延續[循環網路](../rnn/index.md)頁面所述的序列到序列設定，只是以注意力取代了循環狀態。

## 參考文獻

### 開創性論文

- Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H. & Zhang, W. (2021). Informer: Beyond efficient Transformer for long sequence time-series forecasting. *Proceedings of the AAAI Conference on Artificial Intelligence*, 35(12), 11106–11115. doi:[10.1609/aaai.v35i12.17325](https://doi.org/10.1609/aaai.v35i12.17325) — 提出 ProbSparse 注意力、自注意力蒸餾與生成式解碼器，並包含長預測期實驗。
- Zhou, H. et al. (2020). Informer: Beyond efficient Transformer for long sequence time-series forecasting. arXiv. https://arxiv.org/abs/2012.07436 — 同一篇論文的預印本版本。
- Vaswani, A. et al. (2017). Attention is all you need. arXiv. https://arxiv.org/abs/1706.03762 — Informer 所修改的 Transformer 原始論文。
- Lim, B., Arık, S. Ö., Loeff, N. & Pfister, T. (2021). Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. *International Journal of Forecasting*, 37, 1748–1764. doi:[10.1016/j.ijforecast.2021.03.012](https://doi.org/10.1016/j.ijforecast.2021.03.012) — 另一個以注意力為基礎的多步預測器，並利用注意力解釋其預測。

### 綜述與教科書

- Lim, B. & Zohren, S. (2021). Time-series forecasting with deep learning: a survey. *Philosophical Transactions of the Royal Society A*, 379, 20200209. doi:[10.1098/rsta.2020.0209](https://doi.org/10.1098/rsta.2020.0209) — 綜述深度預測模型的編碼器與解碼器設計，包括以注意力為基礎的模型。
- Zeng, A., Chen, M., Zhang, L. & Xu, Q. (2023). Are Transformers effective for time series forecasting? *Proceedings of the AAAI Conference on Artificial Intelligence*, 37(9), 11121–11128. doi:[10.1609/aaai.v37i9.26317](https://doi.org/10.1609/aaai.v37i9.26317) — 批評文章，指出簡單線性模型在常見基準上能與數個 Transformer 預測器（包括 Informer）相當，甚至更好。
