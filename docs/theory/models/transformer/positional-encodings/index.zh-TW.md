---
related:
- theory/models/llm
aliases:
  - Positional Encodings
  - Positional Embeddings
  - Length Extrapolation
  - 位置編碼
  - 長度外推
tags:
  - positional encoding
  - length generalisation
  - long context
translation_reviewed: 2026-10-28
---

# 位置編碼

注意力把輸入當成一個集合：打亂 token 的順序，輸出也會以相同方式被打亂。因此必須加入位置資訊，可以加在 token 嵌入上、注意力分數上，或查詢與鍵上。選擇很重要，原因有二：編碼決定模型能表示哪些關係，也決定在一種長度上訓練的模型，能否在更長的序列上仍然有效。本頁介紹各類編碼，以及把它們延伸到更長上下文的方法。Transformer 的總覽（包括原始的正弦編碼）見 [Transformers & Attention](../index.md)。

## 概觀

編碼可分為三類：

- **絕對位置編碼**把每個位置索引的向量加到 token 嵌入上。它簡單，但訓練時沒見過的位置，超出訓練範圍後就沒有有意義的向量。
- **相對位置編碼**讓注意力分數取決於兩個 token 之間的距離，而這通常才是語言中真正重要的量。
- **旋轉式與偏置式編碼**把相對依賴內建在查詢–鍵的乘積中，或加上距離懲罰，不需要學習的位置向量。

## 做法

| 方法 | 位置在哪裡進入 | 關鍵論文 |
|---|---|---|
| 正弦編碼 | 加到 token 嵌入上，是索引的固定函數 | Vaswani et al. (2017), arXiv:1706.03762 |
| 相對位置表示 | 對截斷後的距離學習向量，加到鍵與值上 | Shaw et al. (2018), arXiv:1803.02155 |
| 旋轉式（RoPE） | 查詢與鍵依與位置成正比的角度旋轉 | Su et al. (2021), arXiv:2104.09864 |
| ALiBi | 對分數加上與距離成正比的線性懲罰 | Press et al. (2021), arXiv:2108.12409 |
| 位置內插 | 把位置索引縮放到訓練範圍內，再短暫微調 | Chen et al. (2023), arXiv:2306.15595 |
| YaRN | 依頻率的內插，加上注意力的溫度調整 | Peng et al. (2023), arXiv:2309.00071 |

### 相對與旋轉式編碼

Shaw et al. 對截斷後的每個相對距離加入學到的向量，加到鍵與值上。RoPE 採用不同的做法：查詢或鍵中的每對維度，都會依 token 的位置旋轉一個角度。兩個旋轉後向量的內積，就只取決於它們位置的差。RoPE 不需要額外參數，可以搭配一般的鍵值快取，是許多現今開源模型的預設。

![RoPE 動畫：查詢與鍵向量依 token 位置旋轉，同時平移兩個位置索引時，相對角度與內積維持不變。](../../../../assets/concept-animations/rope-relative-rotation.gif)

*原創二維 RoPE 概念動畫，CC BY-SA 4.0。* 對於**相同的原始查詢與鍵向量**及固定旋轉頻率，將位置從 **(1, 3)** 一起平移至 **(4, 6)**，兩個向量會增加相同的旋轉角度。相對位移仍為兩個位置，因此內積不變：$(R_m q)^\top(R_n k)=q^\top R_{n-m}k$。動畫中的箭頭方向只是示意，**不是實測注意力分數**；完整 RoPE 在不同維度對使用不同的旋轉頻率。參見 [Su 等人（2021）](https://arxiv.org/abs/2104.09864)。

### 偏置式編碼

ALiBi 在每個注意力分數上加入與查詢和鍵之間距離成正比的懲罰，每個頭的斜率不同。模型不學習任何位置向量。Press et al. 指出，在短序列上訓練的模型，可以在更長的序列上評估，而不會像正弦編碼那樣崩潰。

### 延伸上下文

在 4,096 個位置上訓練的 RoPE 模型，若給它 16,384 個位置，表現會下降，因為旋轉角度會超出訓練時見過的範圍。位置內插把位置索引除以一個係數，讓較長的序列映射回訓練範圍，再短暫微調。YaRN 更進一步：它保持高頻維度不變，只內插低頻維度，並調整注意力，使較長長度下的熵維持在可比較的水準。另一個想法 NTK-aware scaling，起源於 2023 年的非正式社群文章而非論文，YaRN 則分析了它的行為。

## 取捨

- **外推與準確。** 能外推的編碼（例如 ALiBi）可能在訓練長度上犧牲一些準確度。內插式 RoPE 在訓練範圍內保持準確，但要延伸就需要微調。
- **延伸的成本。** 內插方法需要較長上下文的訓練資料與運算，偏置式方法則不需要。
- **與快取的互動。** 有些快取淘汰方法會丟棄 token，這會改變模型看到的相對距離。位置處理必須與快取保持一致。
- **多模態輸入。** 影像與影片是二維或三維的，因此一維旋轉需要推廣到位置的網格上。

## 相關連結

位置編碼對[注意力變體](../attention-variants/index.md)很重要，因為稀疏與局部模式本身的結構就已編碼了部分位置。它們也與 [KV 快取管理](../kv-cache/index.md)互動：從序列中間移除 token，會改變剩餘 token 所呈現給模型的位置。與大腦的連結是間接的：訓練過的 Transformer 中的循環式位置編碼，可以產生類似位置細胞與網格細胞的表示，見 [Transformers & Attention](../index.md) 頁面。

## 未解問題與更多變體

- **不經微調的長度泛化。** 能外推的方法仍有限，模型往往在名義上限之前就已明顯退化。確切原因尚未定論。
- **沒有明確位置的僅解碼器模型。** 單靠因果遮罩，解碼器就能推斷順序。Kazemnejad et al.（2023）研究了這何時成立，發現它在某些任務上泛化良好，在另一些任務上則很差。
- **縮放的選擇。** YaRN 類方法中的內插係數、頻率帶與注意力溫度，都是靠搜尋選出的。針對目標長度的原則性規則仍缺乏。
- **二維與多模態位置。** 把 RoPE 推廣到影像、影片與文字–影像混合序列，是活躍的研究領域，已有數種相互競爭的設計。
- **位置與記憶。** 只保留短窗口並摘要其餘部分的方法，會引出該保留哪些位置、如何表示其中間隔的問題。

## 參考文獻

### 開創性論文

- Vaswani, A., et al. (2017). *Attention Is All You Need*. arXiv:1706.03762 — 引入加在嵌入上的正弦位置編碼。
- Shaw, P., Uszkoreit, J. & Vaswani, A. (2018). "Self-Attention with Relative Position Representations". NAACL 2018. arXiv:1803.02155 — 在自注意力中，對截斷後的距離使用相對位置向量。
- Su, J., et al. (2021). "RoFormer: Enhanced Transformer with Rotary Position Embedding". arXiv:2104.09864 — 旋轉式位置嵌入，使內積只取決於相對位置。
- Press, O., Smith, N. A. & Lewis, M. (2021). "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation". arXiv:2108.12409 — ALiBi，對注意力分數加上距離懲罰，可外推到更長的輸入。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Chen, S., et al. (2023). "Extending Context Window of Large Language Models via Positional Interpolation". arXiv:2306.15595 — 把位置索引縮放到訓練範圍內，並短暫微調，以容納更長的上下文。
- Peng, B., et al. (2023). "YaRN: Efficient Context Window Extension of Large Language Models". arXiv:2309.00071 — 依頻率的內插與注意力縮放，用於延伸上下文。
- Kazemnejad, A., et al. (2023). "The Impact of Positional Encoding on Length Generalization in Transformers". NeurIPS 2023. arXiv:2305.19466 — 比較各種位置編碼的長度泛化能力，包括不使用明確編碼的情況。
