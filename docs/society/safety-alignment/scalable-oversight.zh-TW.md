---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - oversight
aliases:
  - Scalable oversight
  - 可擴展監督
  - 弱到強泛化
---

# 可擴展監督

可擴展監督探討：當任務太難、太慢或規模太大，人類無法直接檢查時，人類如何可靠地監督 AI 系統。一個能撰寫研究等級程式碼或長篇科學論證的模型，可能在某些地方是正確的，但評估者不容易確認。監督方法嘗試讓監督的能力跟上系統的能力，方法包括利用模型本身、利用其他模型，或把任務拆解。

## 概覽

多數現行訓練使用人類判斷作為獎勵訊號（參見[從人類回饋中學習](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)）。當評分者能分辨好答案與壞答案時，這運作良好。當答案需要評分者缺乏的專業知識，或回應長到錯誤難以找出時，它就變得不可靠。一個能力超過其監督者的系統，就可能學會讓監督者覺得滿意，這是[獎勵駭客](reward-hacking.md)所涵蓋問題的一種形式。

可擴展監督把這視為一個研究問題，分為兩部分：設計一些協定，使較弱的評審能可靠地判斷兩個答案何者較好；並在能力差距擴大之前，衡量這些協定是否有效。

## 核心概念

- **監督缺口（oversight gap）**：系統能做的事與監督者能檢查的事之間的差距。
- **協定（protocol）**：一套固定的程序，例如辯論或分解，把困難的判斷轉換為一連串較容易的判斷。
- **弱監督者（weak supervisor）**：能力低於其所監督系統的評審，可以是人類或模型。
- **過程監督（process supervision）**：獎勵推理鏈的每一步，而不只獎勵最終答案。

## 主要方法

- [辯論](debate.md)（Irving et al., 2018）：兩個代理人為相反的答案辯論，由評審判斷哪一方的論證較有說服力。
- **遞迴式獎勵建模**（Leike et al., 2018）：把困難的任務拆成子任務，人類借助 AI 助手評估每個子任務，進而評估整體。
- **迭代放大**（Christiano et al., 2018）：人類結合模型的複本回答超出人類單獨能回答的問題，再把這個組合系統蒸餾成新模型，並以同樣方式訓練。
- **由弱到強的泛化**（Burns et al., 2023）：以較弱模型的標註微調一個強模型，問題是強模型的能力有多少能被恢復。

這些方法在評審看到的內容上有所不同。辯論與迭代放大改變評審如何獲得協助；由弱到強的泛化則改變訓練訊號本身，因此也在問：當監督者很弱時，強模型究竟學到什麼。

## 辯論

詳細頁面見 [AI 辯論](debate.md)與[辯論交叉詰問](debate-cross-examination.md)。

在辯論的提案中，兩個模型的複本會看到同一個問題，各自為不同的答案辯護，並可能引用證據。人類評審閱讀這段交流並選出勝者。Irving、Christiano 與 Amodei（2018）主張，在某些假設下，誠實的一方可以獲勝，因為難以辯護的謊言會被對手揭穿，因此評審只需要評估簡短、可檢查的主張。這篇論文是帶有理論論證與小規模示範的提案，而不是已部署的系統。

後續的實證研究衡量辯論是否真的幫助人類判斷正確性。Bowman et al.（2022）提出「sandwiching」，一種實驗設計：非專家人類借助聊天助手，回答專家可以查核的問題。其概念驗證研究使用 MMLU 與限時的 QuALITY，並把辯論列為候選技術加以討論，但未實際測試。

## 過程監督

過程監督會獎勵推理鏈的每一步。Lightman et al.（2023）在數學解題上比較逐步的人類回饋與結果層級的回饋，並報告在他們的實驗中，獎勵每一步能得到更可靠的訊號。這個方法並未解決一般的監督問題，因為它仍需要能檢查每一步的評審，但它說明了分解如何讓困難的判斷變得容易。

## 由弱到強的泛化

Burns et al.（2023）提出監督問題的一個具體版本。他們以遠較弱的模型所產生的標註，微調一個強的預訓練模型，並衡量結果與以真實標註訓練的模型有多接近。單純的微調只能恢復部分差距，但強模型通常會超過它的弱監督者。在他們的實驗中，對訓練目標做簡單修改，能恢復更大比例的差距。這個結果對監督是令人鼓舞的，但也有限：這些任務是刻意選擇的，使真實答案已知；作者也指出，把它類比為人類監督超人類模型並不完美。

## 相關連結

人類監督專家有悠久的歷史。醫學、法律與航空都使用分層審查、檢查表與第二意見，這些做法常被引用為類比。這個類比對設計有幫助，但有其限制，因為機器的錯誤可能在各次檢查之間相關，而人類的錯誤通常不會如此。可擴展監督也與人們如何評估論證並偵測其中錯誤的研究相關，此主題在[認知科學](../../brain-mind/index.md)中有所涵蓋。更廣泛的安全背景見[安全與對齊](index.md)與[憲法式 AI](constitutional-ai.md)。

## 應用

- 在真實答案代價高昂的領域評估模型輸出，例如程式碼審查與科學寫作。
- 以一個模型批判另一個模型的評估流程，這種做法支持上述弱評審方法。
- 衡量模型協助是否提升人類準確度的基準，實驗室在高風險任務上依賴人工審查前會先使用這類基準。

## 開放問題

- 迭代放大與辯論能否擴展到評審無法檢查任何單一主張的任務？
- 由弱到強的結果能否在強模型具有弱模型完全缺乏的能力的任務上重現？
- 當系統試圖誤導評審時，監督協定會如何運作？這與[欺騙性對齊](deceptive-alignment.md)相關。

## 參考文獻

### 開創性論文

- Irving, G., Christiano, P. & Amodei, D. (2018). *AI safety via debate*. arXiv:1805.00899. https://arxiv.org/abs/1805.00899 — Proposes two-agent debate judged by a human as a way to supervise systems on questions beyond direct human judgement.
- Leike, J. et al. (2018). *Scalable agent alignment via reward modeling: a research direction*. arXiv:1811.07871. https://arxiv.org/abs/1811.07871 — Sets out reward modelling as a research agenda and discusses how to scale it with recursive decomposition.
- Christiano, P., Shlegeris, B. & Amodei, D. (2018). *Supervising strong learners by amplifying weak experts*. arXiv:1810.08575. https://arxiv.org/abs/1810.08575 — Introduces iterated amplification, which distils a human assisted by copies of the model into a new model.
- Burns, C. et al. (2023). *Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision*. arXiv:2312.09390. https://arxiv.org/abs/2312.09390 — Measures how much of a strong model's ability is recovered when it is fine-tuned on a weak model's labels.
- Lightman, H. et al. (2023). *Let's Verify Step by Step*. arXiv:2305.20050. https://arxiv.org/abs/2305.20050 — Compares process supervision, which rewards each reasoning step, with outcome supervision on mathematical problems.

### 綜述與教科書

- Bowman, S. R. et al. (2022). *Measuring Progress on Scalable Oversight for Large Language Models*. arXiv:2211.03540. https://arxiv.org/abs/2211.03540 — Proposes “sandwiching”, an experimental setup for testing whether non-expert humans can use a model's help to answer questions beyond their expertise.

### 文章與文件

- Anthropic, *Anthropic's Responsible Scaling Policy*. https://www.anthropic.com/responsible-scaling-policy — Official policy describing the capability thresholds and safeguards a developer commits to, an applied case of oversight by evaluation.
