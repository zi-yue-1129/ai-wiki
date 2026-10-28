---
translation_reviewed: 2026-10-28
---

# 憲法式 AI 與 RLAIF

憲法式 AI（Constitutional AI）訓練助理依照一份簡短的書面原則清單行事。模型依據這些原則評判並修正自己的輸出，因此 AI 回饋可以取代無害性訓練原本所需的人工標籤。RLAIF（基於 AI 回饋的強化學習）則是更廣義的一類方法，以模型的偏好判斷而非人類的判斷來進行訓練。

## 概述

許多助理一開始都是以基於人類回饋的強化學習（RLHF；見[從人類回饋中學習](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)）進行對齊，而這需要大量的人員來比較模型的輸出。有害內容也很難大規模標註，因為評分者必須閱讀這些內容。

Bai 等人（2022）提出了另一種分工方式。作者給模型一份稱為「憲法」的原則清單，並讓模型自行應用。唯一的人類監督，是撰寫這些原則本身。所得的助理無害但不迴避：遇到有害請求時，它會說明自己的反對理由，而不是視而不見。同一篇研究中的助益性訓練仍然使用人工標籤，因此這個方法最好理解為對對齊中「無害性」部分的改變。

## 關鍵概念

- **憲法**：一份自然語言的原則清單，作為評判回應的標準。論文中的原則取材自人權文件等來源。
- **批判與修正**：模型依據某一原則，對自己的某個回應寫出批判，再據此改寫該回應。
- **AI 回饋**：由語言模型而非人類產生的偏好標籤。
- **偏好模型**：經過訓練、使每組配對中較受偏好的回應得到較高分數的網路。在 RLAIF 中，它提供強化學習所用的獎勵。

## 運作方式

此方法分為兩個階段：先對經過自我修正的回應進行監督式學習，再以 AI 標註的偏好進行強化學習。

```mermaid
flowchart LR
    A[有害或棘手的提示] --> B[草稿回應]
    B --> C[依據某原則進行批判]
    C --> D[修正後的回應]
    D --> E[在修正結果上微調]
    E --> F[取樣回應配對]
    F --> G[AI 評審選出較好者]
    G --> H[訓練偏好模型]
    H --> I[對偏好模型進行強化學習]
```

**第一階段：從自我修正中學習。** 研究者從一個已具助益性但尚未無害的模型出發，對刻意引出有害內容的提示取樣回應。對每個回應，模型依據從憲法中挑出的一條原則進行批判，然後加以修正。這個過程可以用多條原則重複進行。原始模型再在最終的修正結果上微調，因此沒有任何人類標註過有害的草稿。

**第二階段：從 AI 回饋進行強化學習。** 經過微調的模型為每個提示取樣兩個回應。回饋模型依據一條原則，選出較符合該原則的回應。這些 AI 標註的比較用來訓練偏好模型，偏好模型給出某個回應被偏好於另一個的機率：

$$
P(y_1 \succ y_2 \mid x) = \sigma\big(r_\phi(x, y_1) - r_\phi(x, y_2)\big)
$$

其中 $r_\phi$ 是學得的獎勵，$\sigma$ 是邏輯函數。接著，助理通常以 PPO 進行最佳化，在最大化獎勵的同時，維持接近經過微調的模型：

$$
\max_\pi \; \mathbb{E}\big[r_\phi(x, y)\big] - \beta \, \mathrm{KL}\big(\pi \,\|\, \pi_{\text{ref}}\big)
$$

這就是 RLHF 的流程，只是標籤的來源不同。在論文的無害性訓練中，標籤來自模型本身。

## 關鍵方法

這些變體具有相同的基本結構，差別在於偏好訊號來自何處，以及模型如何最佳化。

| 變體 | 偏好標籤的來源 | 訓練程序 | 典型用途 |
|---|---|---|---|
| RLHF（Christiano 等人，2017；Ouyang 等人，2022） | 人類評分者比較輸出 | 獎勵模型，再進行強化學習（通常為 PPO） | 助益性與無害性的基準 |
| 憲法式 AI（Bai 等人，2022） | 模型依據書面原則進行判斷 | 對自我修正結果進行監督式學習，再進行 RLAIF | 以較少人工標籤達到無害性 |
| RLAIF（Lee 等人，2023） | 現成的語言模型 | 獎勵模型與強化學習，以 AI 標籤取代人類標籤 | 較低成本地大規模取得偏好資料 |
| DPO（Rafailov 等人，2023） | 偏好配對，來自人類或 AI | 作用於策略的分類式損失，不需要另外的獎勵模型 | 較簡單、較穩定的流程 |

憲法式 AI 與 RLAIF 改變的是標籤，DPO 改變的是最佳化器，因此兩者可以結合使用。DPO 的目標函數為

$$
\mathcal{L}_{\text{DPO}} = -\mathbb{E}\left[\log \sigma\left(\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}\right)\right]
$$

其中 $y_w$ 是較受偏好的回應，$y_l$ 是被拒絕的回應。Rafailov 等人（2023）報告，在他們測試的任務上，這個目標函數與基於 PPO 的 RLHF 相當或更好。

## 相關連結

- 此方法是產生[從人類回饋中學習](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)一文所述偏好訊號的一種方式。RLHF 基準見 [InstructGPT](../../theory/models/llm/instructgpt-rlhf/index.md)，更廣的脈絡見[大型語言模型](../../theory/models/llm/index.md)。
- DPO 及其變體見[訓練](../../engineering/training/index.md)。
- 此方法與大腦及心智的連結屬於類比。人類同樣從明確的規則中學習規範，並在反思後修正自己的行為，但此方法並不要求模型具備心理學所研究的反思狀態。見[心理學與 AI](../../brain-mind/psychology/index.md)。
- 公開的憲法讓外界能讀出訓練的目標，這是支持此做法的理由之一（見[治理](../governance/index.md)）。寫下哪些價值，是倫理問題（見[倫理與公平性](../ethics/index.md)）。
- 模型究竟是內化了某條原則，還是只學會引用它，是[可解釋性](../interpretability/index.md)要回答的問題。

## 應用

- **無害性訓練。** Bai 等人（2022）訓練出一個會說明反對理由、拒絕有害請求的助理。
- **較低成本的偏好資料。** Lee 等人（2023）發現，在摘要與對話任務上，RLAIF 的表現與 RLHF 相當。

## 開放問題

- **誰來撰寫憲法。** 原則承載著撰寫者的價值。Kundu 等人（2023）發現，一條寬泛的原則可以在一定程度上產生無害的行為，而詳細的憲法則能對特定傷害提供更精細的控制。原則應該多寬泛、由誰來選擇，仍是未解的問題。
- **評審偏誤。** Zheng 等人（2023）描述了語言模型評審中的位置偏誤、冗長偏誤與自我增強偏誤。偏好自身風格的模型，在為自己的輸出標註時，可能強化該風格。
- **繼承而來的缺陷。** Sharma 等人（2023）發現，符合使用者觀點的回應更容易被人類與偏好模型偏好。以模型取代人類，可能會把這種偏好一併傳遞下去；其影響的大小尚無定論。
- **獎勵過度最佳化。** Gao 等人（2022）顯示，對學得的獎勵過度最佳化，會在以黃金標準獎勵衡量時損害表現，這符合古德哈特定律（Goodhart's law）。同樣的壓力也適用於以 AI 標籤訓練的偏好模型。
- **整體方法的限制。** Casper 等人（2023）調查了 RLHF 及相關方法的開放問題與根本限制。其中數個問題很可能同樣適用於 AI 回饋。
- **價值還是表面順從。** 一個會引用原則的模型，在原則未曾預料到的情境中，行為可能不同。基於原則的訓練究竟能產生穩定的價值，還是只會流暢地順從，目前尚無定論。

## 參考文獻

### 開創性論文

- Bai, Y. et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv. https://arxiv.org/abs/2212.08073 — 提出憲法、自我批判與修正，以及以 AI 回饋進行的強化學習，用於訓練無害的助理。
- Christiano, P. et al. (2017). *Deep Reinforcement Learning from Human Preferences*. NeurIPS. https://arxiv.org/abs/1706.03741 — 從人類對代理人行為的比較中學習獎勵函數，是後來 RLHF 的源頭。
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT：監督式微調、以排序訓練的獎勵模型，再接 PPO。
- Rafailov, R. et al. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. NeurIPS. https://arxiv.org/abs/2305.18290 — 以分類式損失直接將策略擬合到偏好配對上。
- Lee, H. et al. (2023). *RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback*. arXiv. https://arxiv.org/abs/2309.00267 — 比較在摘要與對話任務上，以 AI 標籤與人類標籤進行強化學習的表現。

### 綜述與教科書

- Casper, S. et al. (2023). *Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback*. arXiv. https://arxiv.org/abs/2307.15217 — 調查 RLHF 及相關方法的開放問題與根本限制。
- Kaufmann, T. et al. (2023). *A Survey of Reinforcement Learning from Human Feedback*. arXiv. https://arxiv.org/abs/2312.14925 — 概述 RLHF 在控制、機器人與語言模型中的應用。

### 文章與文件

- Kundu, S. et al. (2023). *Specific versus General Principles for Constitutional AI*. arXiv. https://arxiv.org/abs/2310.13798 — 測試一條寬泛的原則能否取代許多具體的憲法原則。
- Sharma, M. et al. (2023). *Towards Understanding Sycophancy in Language Models*. arXiv. https://arxiv.org/abs/2310.13548 — 顯示偏好資料與偏好模型可能偏好諂媚的回應。
- Gao, L., Schulman, J. & Hilton, J. (2022). *Scaling Laws for Reward Model Overoptimization*. arXiv. https://arxiv.org/abs/2210.10760 — 衡量對代理獎勵模型過度最佳化，如何最終損害黃金標準下的表現。
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. arXiv. https://arxiv.org/abs/2306.05685 — 研究語言模型評審的偏誤，以及它們與人類偏好的一致程度。
