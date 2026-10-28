---
translation_reviewed: 2026-10-28
---

# 三值權重網路

三值權重網路（TWN）把每個權重限制為 \(\{-\alpha, 0, +\alpha\}\) 三個值之一。零值讓網路在量化時能捨棄很小的權重，因此與二值編碼相比，它保留了更多資訊，而儲存成本只略為增加。它位於[二值與三值](../index.zh-TW.md)系列中，介於 [BinaryConnect](../binaryconnect/index.zh-TW.md) 與[剪枝](../../../pruning/index.zh-TW.md)之間。

## 問題

二值權重會丟失太多資訊，因為即使真實值接近零，每個權重仍必須是 \(\pm 1\)。三值編碼可以精確表示接近零的權重，代價是多一點儲存與少量額外運算。

## 核心想法

當權重的絕對值低於門檻時，把它量化為零；否則量化為 \(\pm \alpha\)。門檻與縮放係數按濾波器選定，使三值權重能夠緊密逼近全精度權重。門檻是平均幅度的固定比例，縮放係數則是通過門檻的權重之平均幅度。

## 公式或演算法

三值近似為 \(W_t = \alpha \cdot t\)，其中 \(t_i \in \{-1, 0, +1\}\)；當 \(|W_i|\) 低於門檻 \(\Delta\) 時 \(t_i\) 為零。論文給出的經驗法則是

\[
\Delta^\ast \approx 0.7 \cdot \mathbb{E}(|W|) \approx \frac{0.7}{n} \sum_{i=1}^{n} |W_i|
\]

其中 \(n\) 是濾波器中的權重數。縮放係數是高於門檻之權重的平均幅度，即 \(\alpha^\ast = \frac{1}{|I_\Delta|} \sum_{i \in I_\Delta} |W_i|\)，其中 \(I_\Delta = \{i : |W_i| > \Delta\}\)。論文的 0.7 係數是由假設的權重分布推導出來的，因此是近似值，並非精確最優。零項對乘積沒有貢獻，因此運算簡化為加法與減法。

論文在前向與反向傳播時使用三值權重，但參數更新時不使用，從而保留實數權重，這與 [BinaryConnect](../binaryconnect/index.zh-TW.md) 相同。

## 結果

摘要報告最高可達 16 倍的模型壓縮。與全精度之間的準確率差距，見論文的表格；不應拿使用不同網路的論文來互相比較。

## 限制

三值運算需要能跳過零項的硬體或核心，才能獲得加速。壓縮比假設三值編碼有被有效儲存，而門檻規則的選擇會影響最終準確率。

## 未解問題與相關變體

- **可學習的門檻。** 以平均幅度設定門檻是一種啟發式方法；逐層學習量化器是自然的延伸，後續工作有所探討，例如[學習式步長量化](../../quantisation-aware-training/lsq/index.zh-TW.md)。
- **相關。** [XNOR-Net](../xnor-net/index.zh-TW.md) 使用帶縮放的二值權重；[結構化剪枝](../../../pruning/structured-pruning/index.zh-TW.md)移除整個通道，產生另一種零值較多、結構不同的編碼。

## 與其他主題的連結

許多零值的三值編碼是一種稀疏表示，因此其運算與[剪枝](../../../pruning/index.zh-TW.md)相關。以加減法取代乘法的運算，適合 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)所討論的位元層級單元。

## 參考文獻

### 奠基性論文

- Li, F., Liu, B., Wang, X., Zhang, B., Yan, J. (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — 三值權重，門檻約為平均幅度的 0.7 倍，縮放係數取自保留下來的權重；最高可達 16 倍壓縮。
- Rastegari, M., Ordonez, V., Redmon, J., Farhadi, A. (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — 帶縮放的二值方法，TWN 以零值對其加以延伸。
- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — 三值網路所放寬的二值方法。

### 綜述與教科書

- Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M. W., Keutzer, K. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 在低位元方法中綜述三值與二值權重。

### 講座與影片

（本頁未檢核任何項目）

### 文章與文件

- Esser, S. K., McKinstry, J. L., Bablani, D., Appuswamy, R., Modha, D. S. (2019). *Learned Step Size Quantization*. arXiv:1902.08153. https://arxiv.org/abs/1902.08153 — 在訓練期間學習量化步長，是本頁門檻啟發式方法的可學習替代方案。
