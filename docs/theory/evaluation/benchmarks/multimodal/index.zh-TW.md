---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
---

# 多模態基準

多模態基準測試模型能否把所見與所知結合起來。這裡的兩個基準著重點不同：VQA v2 檢驗模型是否真的使用影像，MMMU 檢驗在影像上的專家推理。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [VQA v2](vqa-v2.md) | 關於影像的簡短開放式答案 | 與十個人類答案比對的共識準確率 |
| [MMMU](mmmu.md) | 含影像的大學程度題目 | 準確率，整體與各領域分別報告 |

## 常見問題

- **語言先驗。** 模型可以只靠問題文字作答，這會使分數膨脹。平衡資料能抵消此問題（Goyal et al., 2016）。
- **訊號混合。** 專家題目的分數結合了感知與知識，因此錯誤難以歸因（Yue et al., 2023）。
- **飽和。** 近期系統在舊資料集上分數已很高，促使新基準轉向更困難的題目。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [視覺](../vision/index.md) 涵蓋只看影像的基準。
- [語言](../language/index.md) 涵蓋對應的純文字基準。

## 參考文獻

### 開創性論文

- Antol, S. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — 定義開放式視覺問答任務。
- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — 顯示語言先驗使分數膨脹，並介紹平衡資料。

### 文章與文件

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — 介紹大學程度的多模態基準。
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 描述廣泛的基準設計，包括多模態任務。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集如何揭露對原始資料的適配。
