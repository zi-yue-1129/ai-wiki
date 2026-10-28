---
translation_reviewed: 2026-10-28
---

# QLoRA

QLoRA 在一個凍結權重以 4 位元儲存的基底模型上訓練 LoRA 適配器，以微調大型模型。Dettmers 等人（2023）報告，這使微調 650 億參數模型所需的記憶體降到 48 GB 以下，因此能放進單張 GPU，同時在其測試的基準上與 16 位元全參數微調相當。它是 [LoRA](index.zh-TW.md) 的一種變體，依賴對基底模型進行[量化](../../quantisation/index.zh-TW.md)。

## 問題

LoRA 減少了可訓練參數的數量，但凍結的基底模型仍須以完整的 16 位元大小放在記憶體中。對一個 650 億參數的模型，光是基底就超過一張 48 GB GPU 的記憶體，因此微調需要多張加速器。把基底量化為 4 位元可以縮小它，但單純的 4 位元模型會損失準確度，而且梯度必須穿過它才能到達適配器。

## 關鍵概念

- **4 位元 NormalFloat（NF4）：** 用於基底權重的 4 位元資料型別。它的階層是標準常態分布的分位數，重新縮放到固定範圍，使每個階層涵蓋的權重數量大致相同。這組數值是非對稱的，使零能被精確表示。
- **雙重量化：** 量化所用的縮放常數也佔用記憶體，因此論文也對這些常數進行量化。論文報告每個參數約節省 0.37 位元。
- **分頁最佳化器：** 最佳化器狀態保存在 NVIDIA 統一記憶體中，當 GPU 記憶體不足時在 GPU 與 CPU 記憶體之間移動。這能吸收長序列造成的記憶體尖峰。

## 運作方式

基底模型的權重以 NF4 儲存並凍結。每個被適配的層，其輸出由 4 位元的基底權重（在矩陣乘法前反量化）加上 LoRA 更新組成，梯度則穿過凍結的 4 位元模型回傳到適配器。只有適配器會被訓練，並以較高精度儲存。雙重量化與分頁最佳化器分別減少常數與最佳化器狀態的記憶體。

論文在 8 個指令資料集上微調了 1,000 多個模型，包括 LLaMA 與 T5 模型，其中包含 330 億與 650 億參數的規模。

## 結果

摘要指出，這個方法能在單張 48 GB GPU 上微調 650 億參數模型，同時保留完整 16 位元微調的表現。最佳的模型系列 Guanaco，依論文在 Vicuna 基準上達到 ChatGPT 效能水準的 99.3%，且只需在一張 GPU 上約 24 小時的微調。

正文報告，在 GLUE 與 Super-NaturalInstructions 上，使用最多 30 億參數的 RoBERTa 與 T5 模型，4 位元適配器微調與 16 位元全參數微調相當。在 LLaMA 模型（7 至 650 億參數）的 MMLU 上，搭配雙重量化的 NF4 與 16 位元 LoRA 相當。4 位元浮點變體則落後約一個百分點。

## 限制

- **較大規模未完全驗證。** 作者因資源成本，沒有證明在 330 億與 650 億參數規模上，QLoRA 能完全與 16 位元微調相當。
- **評估範圍窄。** 評估僅限於 MMLU、Vicuna 基準與 OA 基準，因此對其他任務的泛化未經測試，負責任 AI 的分析也有限。
- **只測試一種位元寬度與一種適配器方法。** 主要實驗只測試 4 位元儲存與 LoRA。
- **聚焦於聊天機器人。** 研究以指令微調與聊天機器人效能為中心。作者認為，現有的聊天機器人基準無法可靠地衡量聊天品質，這限制了所報告比較的適用範圍。

## 開放問題

- **最大規模的差距。** 4 位元適配器微調在 330 億與 650 億參數上，以及在指令微調以外的任務上，能否與 16 位元微調相當，論文未能確定。
- **分頁何時會拖慢訓練。** 論文留待未來研究，何時分頁最佳化器會拖慢訓練；它只報告，在批次大小 16 的 650 億參數模型上，其速度與一般最佳化器相當。

## 相關連結

QLoRA 是把 LoRA 應用於量化後的基底，因此 [LoRA](index.zh-TW.md) 頁面的適配器數學完全適用。它的記憶體節省來自[量化](../../quantisation/index.zh-TW.md)中的數值格式，它服務的微調實務則見[訓練](../../../../engineering/training/index.zh-TW.md)。它所節省的記憶體，正是[記憶體階層與頻寬](../../../../engineering/hardware/memory-hierarchy/index.zh-TW.md)所討論的頻寬與容量成本。

## 參考文獻

### 開創性論文

- Dettmers, T., Pagnoni, A., Holtzman, A., Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — 在凍結的 4 位元基底上微調 LoRA 適配器，使 650 億參數模型能在單張 48 GB GPU 上訓練。
- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 在凍結權重上學習低秩更新，這是 QLoRA 所延伸的方法。

### 綜述與教科書

- Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M. W., Keutzer, K. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 綜述 QLoRA 基底儲存所依據的量化方法。

### 文章與文件

- Krishnamoorthi, R. (2018). *Quantizing deep convolutional networks for efficient inference: A whitepaper*. arXiv:1806.08342. https://arxiv.org/abs/1806.08342 — 顯示逐通道的 8 位元量化能讓許多 CNN 維持接近浮點數的準確度，是把基底以低位元儲存的訓練後對應做法。
- Gholami, A., 等人 (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — 主張對 AI 服務而言，主要瓶頸是記憶體頻寬而非運算，而把基底儲存為 4 位元正能緩解這項壓力。
