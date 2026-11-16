---
translation_reviewed: 2026-11-15
---

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
| LoRA（Hu et al., 2021） | 在選定的矩陣上加入低秩更新 \(W + BA\) | 低 | 參數高效的適配；可行時與全參數微調比較 |
| [QLoRA](../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.zh-TW.md)（Dettmers et al., 2023） | 在 4-bit 量化的基底模型上做 LoRA | 極低 | 記憶體受限的適配；需確認實際 GPU 需求 |
| [DoRA](../../theory/model-compression/low-rank-and-efficient-architectures/lora/dora.zh-TW.md) 等其他 LoRA 變體 | 將大小與方向分解等 | 低 | 有時品質更好 |
| [適配器](../../theory/paradigms/transfer/fine-tuning-and-adaptation/adapters.zh-TW.md)、[前綴](../../theory/paradigms/transfer/fine-tuning-and-adaptation/prefix-tuning.zh-TW.md)與[提示微調](../../theory/paradigms/transfer/fine-tuning-and-adaptation/prompt-tuning.zh-TW.md) | 插入的小模組或學習得到的提示 | 極低 | 同一基底模型服務多項任務 |
| 持續預訓練 | 在領域文本上更新所有權重 | 高 | 新的領域或語言 |

記憶體欄是定性比較，不是 GPU 容量保證。LoRA 減少可訓練參數、梯度與最佳化器狀態，但基底權重與中間活化值仍占用記憶體。QLoRA 進一步量化凍結的基底權重，並非把整個訓練運算都量化。[^lora][^qlora][^memory]

## LLM 的後訓練

1. 在指令—回應配對上做**監督式微調（SFT）**（品質重於數量）
2. **偏好最佳化**：
    - 使用獎勵模型與 PPO 的 RLHF
    - **DPO**（Rafailov et al., 2023）及其變體（IPO、KTO、ORPO、SimPO）
    - RLAIF／憲法式 AI（Constitutional AI）
3. 針對推理、數學與程式碼的**可驗證獎勵強化學習**（GRPO 及相關方法）
4. **安全訓練**與拒絕回答的校準
5. 從更強的教師模型進行**蒸餾**

給定較偏好的回應 \(y_w\) 與較不偏好的回應 \(y_l\)，DPO 目標為：[^dpo]

\[
L = -\log \sigma\!\left(\beta \log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)} - \beta \log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\right)
\]

## LoRA 微調的實務流程

把以下步驟視為實驗檢查表，而非通用的超參數配方。資料量、LoRA 秩、學習率與訓練長度都應依模型與任務選擇。

1. **先定義比較方式。** 明確列出目標行為與失敗案例，建立提示工程或檢索增強生成（RAG）基準線。區分訓練資料、用來選擇設定的驗證集，以及留給最終比較的測試集；反覆用測試集調參會造成資訊洩漏。[^splits] 指標與資料切分設計可參考[評估](../evaluation/index.zh-TW.md)。
2. **檢查訓練範例。** 確認資料來源、涵蓋範圍與重複項目。用預定的 tokenizer 與對話範本處理範例，再檢查 token 長度與訓練標籤。決定損失涵蓋整段序列、完成部分，或助理回合。TRL 的僅助理回合損失，需要能提供助理 token 遮罩的相容範本。[^sft]
3. **明確選擇適配器目標。** 確認實際層名稱與可訓練參數量。PEFT 的 `target_modules="all-linear"` 是達成 QLoRA 式覆蓋範圍的選項，不是每項 LoRA 任務的必要設定。依驗證結果調整秩、縮放、學習率與訓練長度，不要直接套用固定的秩或 epoch 數。[^peft][^splits]
4. **先做短程記憶體與正確性檢查。** 使用具代表性的序列長度，包含較長範例。開始長時間訓練前，先跑過前向傳播、反向傳播、最佳化器更新與評估。記錄實際設定的尖峰記憶體與吞吐量；只放得下權重並不足夠。[^memory]
5. **同時評估行為與損失。** 在相同解碼設定下比較生成結果與基準線。追蹤目標任務品質、重要語言或任務子群，以及通用能力與安全行為是否退步。SFT 損失衡量 token 預測，不能取代這些行為檢查。[^sft][^instructgpt] 用驗證資料選擇檢查點，再報告保留測試集的結果。[^splits]
6. **封裝可重現的結果。** 記錄基底模型版本、tokenizer／範本、資料切分、函式庫版本、隨機種子、精度與適配器設定。保留適配器檢查點；若合併權重或改變推論精度，應對實際部署的產物重新評估。PEFT 支援分別載入適配器，也支援將其合併至基底模型。[^peft]

### 記憶體控制與取捨

| 控制方式 | 檢查重點 |
|---|---|
| LoRA／QLoRA | 可訓練參數較少，不代表不需儲存基底權重或活化值；僅知道基底權重是 4-bit，無法決定訓練尖峰記憶體。[^lora][^qlora][^memory] |
| 序列長度 | 設定上限前先檢查 token 長度分布。截斷可能丟棄答案或其他重要監督訊號。[^trl-memory] |
| 較小的微批次 + 梯度累積 | 在數個較小的前向／反向批次上累積梯度後才更新權重。如此可支援較大的有效批次，而不必同時保存全部活化值；相較於原本就放得下的大批次，這並不是提升吞吐量的方法。[^accumulation] |
| 活化值檢查點 | 反向傳播時重新計算部分中間活化值，避免全部儲存；以額外運算交換記憶體。[^checkpointing] |

請查閱實際使用版本的函式庫文件。不同模型與版本支援的範本、序列打包策略、量化後端與權重合併方式可能不同。

## 其他技術

- **知識蒸餾**（教師 → 學生）
- **模型合併**（任務算術、TIES、SLERP）
- **量化感知訓練**
- **課程式學習與資料混合**排程
- **超參數搜尋**：隨機搜尋、貝氏最佳化、基於族群的訓練

[^lora]: Hu et al. (2021)，見參考文獻。
[^qlora]: Dettmers et al. (2023)，見參考文獻。
[^dpo]: Rafailov et al. (2023)，見參考文獻。
[^instructgpt]: Ouyang et al. (2022)，見參考文獻。
[^splits]: scikit-learn，*Cross-validation: evaluating estimator performance*，見參考文獻。
[^peft]: Hugging Face PEFT，*LoRA*，見參考文獻。
[^sft]: Hugging Face TRL，*SFT Trainer*，見參考文獻。
[^memory]: Hugging Face Transformers，*GPU memory usage*，見參考文獻。
[^trl-memory]: Hugging Face TRL，*Reducing Memory Usage*，見參考文獻。
[^accumulation]: Hugging Face Transformers，*Gradient accumulation*，見參考文獻。
[^checkpointing]: Hugging Face Transformers，*Gradient checkpointing*，見參考文獻。

## 參考文獻

### 開創性論文

- Micikevicius, P., 等人 (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — 顯示 16 位元訓練在多種架構上可把記憶體用量減少近 2 倍，並需搭配主權重與損失縮放。
- Shoeybi, M., 等人 (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. arXiv:1909.08053. https://arxiv.org/abs/1909.08053 — 以層內模型平行訓練 83 億參數的 Transformer，在 512 張 GPU 上達到 76% 的擴展效率。
- Rajbhandari, S., 等人 (2019). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. arXiv:1910.02054. https://arxiv.org/abs/1910.02054 — 在資料與模型平行訓練中消除記憶體冗餘，同時維持較低的通訊量。
- Houlsby, N., 等人 (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — 提出適配器模組，在 GLUE 上達到的平均分數，比全參數微調低 0.4 分，同時每個任務只增加 3.6% 參數。
- Dettmers, T., 等人 (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — 在凍結的 4 位元基底上微調 LoRA 適配器，使 650 億參數模型能在單張 48 GB GPU 上訓練。
- Hu, E. J., 等人 (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — 凍結預訓練權重並訓練低秩更新矩陣，是本頁 LoRA 流程的基礎。
- Ouyang, L., 等人 (2022). *Training language models to follow instructions with human feedback*. NeurIPS 2022. https://arxiv.org/abs/2203.02155 — InstructGPT：先用示範資料做監督式微調，再依獎勵模型進行強化學習，形成後訓練的典型流程。
- Hoffmann, J., 等人 (2022). *Training Compute-Optimal Large Language Models*. arXiv:2203.15556. https://arxiv.org/abs/2203.15556 — Chinchilla：說明固定運算預算下，模型規模與訓練 token 數應一起成長。
- Kaplan, J., 等人 (2020). *Scaling Laws for Neural Language Models*. arXiv:2001.08361. https://arxiv.org/abs/2001.08361 — 描述損失、參數、資料與運算量之間的冪次關係，提供大規模預訓練的依據。
- Rafailov, R., 等人 (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. NeurIPS 2023. https://arxiv.org/abs/2305.18290 — 直接用偏好配對訓練策略，不需另外建立獎勵模型或執行強化學習迴圈。

### 書籍與課程

- Lambert, N. *Reinforcement Learning from Human Feedback*. https://rlhfbook.com/ — 免費線上書籍，涵蓋指令微調、獎勵建模、直接對齊與評估。
- Hugging Face. *The Ultra-Scale Playbook: Training LLMs on GPU Clusters*. https://huggingface.co/spaces/nanotron/ultrascale-playbook — 開放書籍，介紹分散式訓練、平行化與記憶體／通訊取捨，附程式碼與基準測試。
- Hashimoto, T. & Liang, P. *CS336: Language Modeling from Scratch*. Stanford，2025 年春季。https://cs336.stanford.edu/spring2025/ — 封存課程，附 tokenization、訓練系統、尺度律、資料與對齊作業。

### 官方文件

- Hugging Face PEFT. *LoRA*. https://huggingface.co/docs/peft/developer_guides/lora — 說明目標模組、秩與縮放設定，以及適配器載入與合併。
- Hugging Face TRL. *SFT Trainer*. https://huggingface.co/docs/trl/sft_trainer — 說明資料格式、對話範本、損失遮罩與適配器訓練。
- Hugging Face TRL. *Reducing Memory Usage*. https://huggingface.co/docs/trl/reducing_memory_usage — 說明支援的訓練器如何選擇序列長度，以及截斷與打包的取捨。
- Hugging Face Transformers. *GPU memory usage*. https://huggingface.co/docs/transformers/model_memory_anatomy — 區分訓練記憶體中的權重、最佳化器狀態、梯度、活化值與暫存張量。
- Hugging Face Transformers. *Gradient accumulation*. https://huggingface.co/docs/transformers/grad_accumulation — 說明有效批次、累積步數與依 token 數進行的損失正規化。
- Hugging Face Transformers. *Gradient checkpointing*. https://huggingface.co/docs/transformers/grad_checkpointing — 說明活化值重算，以及記憶體與運算量之間的取捨。
- scikit-learn. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — 區分訓練、驗證與測試，並說明用測試資料調參的風險。

## 學習資源

- Hugging Face [TRL](https://huggingface.co/docs/trl)、[PEFT](https://huggingface.co/docs/peft) — 後訓練與參數高效適配的函式庫入口。
- [Unsloth 文件](https://unsloth.ai/docs) — 實務環境設定與特定模型的訓練指南；使用時需確認所選模型的需求。
- [Axolotl 文件](https://docs.axolotl.ai/) — 透過設定檔進行微調，並提供資料格式與支援模型指南。
