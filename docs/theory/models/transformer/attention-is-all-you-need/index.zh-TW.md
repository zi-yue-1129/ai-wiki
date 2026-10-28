---
translation_reviewed: 2026-10-28
---

# Attention Is All You Need（Vaswani 等人，2017）

本論文提出 Transformer，這是一種只由多頭縮放點積注意力構成的序列模型。它移除了遞迴與卷積，因此每個位置都能並行計算，任意兩個位置之間也只隔固定的步數。

## 問題

LSTM、GRU 等循環式編碼器–解碼器一次讀入一個 token。在單一樣本內，計算無法在位置之間並行，而遠處 token 的資訊必須經過很多步才能傳遞。論文的表 1 把這點具體化：長度為 $n$ 的序列經過循環層需要 $O(n)$ 次依序運算，而自注意力層只需要 $O(1)$ 次，且任意兩個位置之間只需 $O(1)$ 步即可連接。

## 核心想法

模型以查詢 $Q$、鍵 $K$ 與值 $V$ 計算注意力。每個查詢與所有的鍵比較，softmax 權重則形成值的混合。論文並行地執行 $h = 8$ 個注意力函數，各自使用學得的輸入投影，最後把結果串接起來，這就是多頭注意力。

注意力本身不考慮順序，因此嵌入會加上位置編碼。論文採用不同波長的正弦函數。作者也試過學得的位置嵌入，並回報結果幾乎相同。

## 方程式或演算法

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V
$$

縮放因子 $1/\sqrt{d_k}$ 的作用是：當 $d_k$ 很大時，點積的量值會變大，把 softmax 推進梯度極小的區域。論文以此說明縮放的理由，並回報在 $d_k$ 較大時，加性注意力勝過未縮放的點積注意力。

編碼器是 $N = 6$ 層完全相同的堆疊。每層都有多頭自注意力子層與逐位置的前饋網路，每個子層外都有殘差連接與層正規化。解碼器同樣有 $N = 6$ 層，多了一個編碼器–解碼器注意力子層，並在自注意力中遮蔽未來的位置，因此位置 $t$ 的預測只依賴較早的輸出。模型寬度為 $d_{\text{model}} = 512$，前饋網路內層寬度為 $d_{ff} = 2048$，每個頭的 $d_k = d_v = 64$。

## 結果

- WMT 2014 英譯德：大型模型達 28.4 BLEU，比先前回報的最佳結果（包括集成模型）高出 2.0 BLEU 以上。
- WMT 2014 英譯法：單一模型達 41.8 BLEU，在八個 P100 GPU 上訓練 3.5 天（大型模型）。
- 基礎模型訓練了 10 萬步，在八個 P100 GPU 上約 12 小時。

論文也回報，此模型可遷移到英文的成分句法剖析。

## 限制

- 自注意力每層的成本為 $O(n^2 \cdot d)$（表 1），因此計算量與記憶體隨序列長度呈二次方成長。論文把受限注意力（只看每個位置附近的鄰域）留作未來工作。
- 實驗涵蓋翻譯與句法剖析。原始模型是編碼器–解碼器。多數後續語言模型所用的僅解碼器形式，是之後的改寫，例如 GPT-2 技術報告所示。
- 位置資訊透過論文所選的固定編碼注入。後來的模型改變了這項設計。

## 關鍵方法

簡要比較本論文所處的注意力設計：

- [加性注意力（Bahdanau）](../bahdanau-attention/index.md)：在循環式編碼器–解碼器中，以小型前饋網路為每個來源位置計分。Transformer 移除了遞迴，改用點積計分。
- [注意力變體](../attention-variants/index.md)：之後對注意力運算本身的修改，改變了它的成本或結構。

## 關聯

- 母主題：[Transformer 與注意力機制](../index.md)
- 認知科學：「注意力」一詞借自感知與記憶中對某些資訊的選擇。Transformer 的運算是對表徵的學得加權，並非大腦注意力的模型，論文也沒有任何生物學主張。

## 應用

- 機器翻譯（論文本身的任務），之後是語言模型，僅解碼器的 Transformer 成為標準架構。
- 視覺：見[視覺 Transformer](../vision-transformer/index.md)。

## 開放問題

- 如何在保有完整注意力的建模能力之下，降低長輸入的二次方成本。
- 注意力權重揭示了模型計算的什麼，以及這種解讀在何處失效。參考文獻中的 Elhage 等人框架，以殘差流為研究對象。

## 參考文獻

### 開創性論文

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力取代遞迴。
- Bahdanau, D., Cho, K. & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR. https://arxiv.org/abs/1409.0473 — 在序列到序列的翻譯中加入可學習的注意力，此想法後來被 Transformer 推廣。
- Luong, M.-T., Pham, H. & Manning, C. D. (2015). *Effective Approaches to Attention-based Neural Machine Translation*. EMNLP. https://arxiv.org/abs/1508.04025 — 比較神經機器翻譯中的全域與局部注意力，以及多種計分函數。
- Radford, A., et al. (2019). *Language Models are Unsupervised Multitask Learners*. OpenAI 技術報告. https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf — GPT-2 報告，描述後來模型所採用的僅解碼器 Transformer 語言模型。
- Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits*. Anthropic. https://transformer-circuits.pub/2021/framework/index.html — 把殘差流視為注意力頭與 MLP 層共同讀寫的空間，是機械式可解釋性研究的基礎。

### 綜述與教科書

- Tay, Y., et al. (2020). *Efficient Transformers: A Survey*. arXiv. https://arxiv.org/abs/2009.06732 — 綜述許多降低注意力二次方成本的嘗試，並提供方法分類。

### 文章與文件

- Rush, A. M. (2018). *The Annotated Transformer*. Proceedings of Workshop for NLP Open Source Software (NLP-OSS). https://doi.org/10.18653/v1/w18-2509 — 逐篇對照原文的 PyTorch 實作，並附帶註解。

## 延伸學習

- Karpathy, A. (2023). *Let's build GPT: from scratch, in code, spelled out*. YouTube. https://www.youtube.com/watch?v=kCc8FmEb1nY — 從空白檔案現場撰寫一個小型 GPT，寫的同時解說 Transformer 的每個部分。
