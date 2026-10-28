# 訓練與微調

## 大規模預訓練

| 要素 | 說明 |
|---|---|
| 運算量 | 以 FLOPs 計量；前沿訓練任務超過 10²⁵–10²⁶ FLOPs |
| 平行化 | 資料、張量、管線、序列／脈絡與專家平行；ZeRO／FSDP 分片 |
| 精度 | BF16 為標準；FP8 訓練日益普遍 |
| 穩定性 | 學習率預熱、梯度裁剪、謹慎的初始化、QK 正規化、損失突增監控 |
| 資料配比 | 網路、程式碼、數學、多語言、合成資料；課程式安排與在高品質資料上的退火 |
| 檢查點 | 頻繁、分片儲存，並為數千個加速器提供容錯能力 |

對稠密 Transformer 的粗略運算估計：**訓練 FLOPs ≈ 6 × 參數量 × token 數**。

## 微調方法

| 方法 | 改變的部分 | 記憶體 | 適用時機 |
|---|---|---|---|
| 全參數微調 | 所有權重 | 最高 | 資料與運算資源充足；需要大幅改變行為時 |
| LoRA（Hu et al., 2021） | 在選定的矩陣上加入低秩更新 \(W + BA\) | 低 | 大多數適配任務的預設選擇 |
| [QLoRA](../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.zh-TW.md)（Dettmers et al., 2023） | 在 4-bit 量化的基底模型上做 LoRA | 極低 | 在單一 GPU 上微調大模型 |
| DoRA 等其他 LoRA 變體 | 將大小與方向分解等 | 低 | 有時品質更好 |
| 適配器、前綴／提示微調 | 插入的小模組或學習得到的提示 | 極低 | 同一基底模型服務多項任務 |
| 持續預訓練 | 在領域文本上更新所有權重 | 高 | 新的領域或語言 |

## LLM 的後訓練

1. 在指令—回應配對上做**監督式微調（SFT）**（品質重於數量）
2. **偏好最佳化**：
    - 使用獎勵模型與 PPO 的 RLHF
    - **DPO**（Rafailov et al., 2023）及其變體（IPO、KTO、ORPO、SimPO）
    - RLAIF／憲法式 AI（Constitutional AI）
3. 針對推理、數學與程式碼的**可驗證獎勵強化學習**（GRPO 及相關方法）
4. **安全訓練**與拒絕回答的校準
5. 從更強的教師模型進行**蒸餾**

給定較偏好的回應 \(y_w\) 與較不偏好的回應 \(y_l\)，DPO 目標為：

\[
L = -\log \sigma\!\left(\beta \log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)} - \beta \log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\right)
\]

## LoRA 微調的實務流程

1. 定義目標行為，並**先建立評估集**
2. 先試提示工程與 RAG；只有當它們不足時才微調
3. 以基底模型的對話格式，蒐集數百到數千筆高品質範例
4. 從 LoRA 秩 8–64 開始，套用在注意力與 MLP 投影層上，學習率約 1e-4 到 2e-4，訓練 1–3 個 epoch
5. 觀察驗證損失與任務評估；檢查是否發生通用能力與安全行為的**災難性遺忘**
6. 合併或服務適配器；在模型卡中記錄資料與設定

## 其他技術

- **知識蒸餾**（教師 → 學生）
- **模型合併**（任務算術、TIES、SLERP）
- **量化感知訓練**
- **課程式學習與資料混合**排程
- **超參數搜尋**：隨機搜尋、貝氏最佳化、基於族群的訓練

## 參考文獻

### 開創性論文

- Micikevicius, P., 等人 (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — 顯示 16 位元訓練在多種架構上可把記憶體用量減少近 2 倍，並需搭配主權重與損失縮放。
- Shoeybi, M., 等人 (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. arXiv:1909.08053. https://arxiv.org/abs/1909.08053 — 以層內模型平行訓練 83 億參數的 Transformer，在 512 張 GPU 上達到 76% 的擴展效率。
- Rajbhandari, S., 等人 (2019). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. arXiv:1910.02054. https://arxiv.org/abs/1910.02054 — 在資料與模型平行訓練中消除記憶體冗餘，同時維持較低的通訊量。
- Houlsby, N., 等人 (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — 提出適配器模組，在 GLUE 上與全參數微調的差距在 0.4% 以內，每個任務只增加 3.6% 參數。
- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 在凍結權重上學習低秩更新，對 GPT-3 175B 最多可減少 10,000 倍的可訓練參數。
- Dettmers, T., 等人 (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — 在凍結的 4 位元基底上微調 LoRA 適配器，使 650 億參數模型能在單張 48 GB GPU 上訓練。

## 學習資源

- Hugging Face [TRL](https://huggingface.co/docs/trl)、[PEFT](https://huggingface.co/docs/peft)
- Stanford CS336
- *The Ultra-Scale Playbook*（Hugging Face，2025），關於分散式訓練
- Lambert，*RLHF Book*（可免費線上閱讀）
- Unsloth 與 Axolotl 文件，實務微調
