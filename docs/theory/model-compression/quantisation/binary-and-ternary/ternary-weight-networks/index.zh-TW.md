---
translation_reviewed: 2026-10-28
---

# 三值權重網路

三值權重網路（TWN）把每個權重限制為 \(\{-\alpha, 0, +\alpha\}\) 三個值之一。零值讓網路在量化時可以把小權重歸零，以適中的儲存成本保留比二值編碼更多的資訊。它位於 [BinaryConnect](../binaryconnect/index.zh-TW.md) 與[剪枝](../../../pruning/index.zh-TW.md)之間，屬於[二值與三值](../index.zh-TW.md)家族。

## 問題

二值權重丟棄太多資訊，因為每個權重都必須是 \(\pm 1\)，即使它的真實值接近零。三值編碼能精確表示接近零的權重，代價是多一點儲存空間與一些額外運算。

## 核心想法

當權重量值低於門檻時量化為零，其餘則量化為 \(\pm \alpha\)。門檻與尺度依每個濾波器選定，使三值權重與全精度權重之間的期望平方誤差最小。訓練與其他低位元方法一樣，使用直通估計器。

## 公式或演算法

三值近似為 \(W_t = \alpha \cdot t\)，其中 \(t_i \in \{-1, 0, +1\}\)。門檻 \(\Delta\) 由濾波器的平均絕對值設定，近似誤差最小的選擇；\(\alpha\) 則是高於門檻的權重的平均量值。零項對乘積沒有貢獻，因此運算化簡為加法與減法。

## 結果

摘要報告最高可達 16 倍的模型壓縮。與全精度之間的準確度差距，見論文的表格，不宜拿不同論文使用的不同網路直接比較。

## 限制

三值運算要獲得加速，需要跳過零項的硬體或核心程式。壓縮比假設三值編碼儲存得很有效率，而訓練排程也會影響最終準確度。

## 開放問題與相關變體

- **學習得到的門檻**：以平均量值設定門檻是一種啟發式方法；逐層學習門檻是自然的延伸，後續研究正在探索。
- **相關**：[XNOR-Net](../xnor-net/index.zh-TW.md) 使用帶尺度的二值權重，而[結構化剪枝](../../../pruning/structured-pruning/index.zh-TW.md)則移除整個通道，產生結構不同、零值較多的編碼。

## 相關連結

零值較多的三值編碼是一種稀疏表示，因此其運算與[剪枝](../../../pruning/index.zh-TW.md)相關。用來取代乘法的加法與減法，適合 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)中討論的位元層級單元。

## 參考文獻

### 開創性論文

- Li, F., Liu, B., Wang, X., Zhang, B., Yan, J. (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — 三值權重，帶有量值門檻與尺度，最高可達 16 倍壓縮。
- Rastegari, M., 等人 (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — 帶尺度的二值替代方案，TWN 在其基礎上加入零值。
- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — 三值網路所放寬的兩值方法。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 在低位元方法中回顧三值與二值權重。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Esser, S. K., 等人 (2019). *Learned Step Size Quantization*. arXiv:1902.08153. https://arxiv.org/abs/1902.08153 — 學習量化尺度，是此處門檻啟發式方法的訓練期替代方案。
