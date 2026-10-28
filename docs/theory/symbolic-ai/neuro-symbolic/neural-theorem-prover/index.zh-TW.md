---
translation_reviewed: 2026-10-28
---

# 神經定理證明器（Neural Theorem Prover）

神經定理證明器以反向鏈結回答知識庫的查詢，但符號比對是以學得向量之間的可微分相似度完成，而不是精確的合一。Rocktäschel 與 Riedel 於 2017 年以預印本形式提出端到端可微分的版本。它是[神經符號 AI 概述](../index.md)中神經證明方向的代表方法。

## 概述

古典證明與知識庫推理依賴離散的比對：兩個符號要麼合一，要麼不合一。這使得無法以梯度下降從資料學習符號的表示。Prolog 的反向鏈結是古典程序的範例：要證明一個目標，系統找出結論與之相符的規則，並遞迴地證明該規則的前提。

Rocktäschel 與 Riedel 以軟性比對取代精確比對。他們的網路以符號的稠密向量表示進行證明，結構以 Prolog 反向鏈結的方式遞迴建立。由於每一步都可微分，梯度下降便能學會兩個符號相似，並在證明中運用這種相似性。[^1]

## 關鍵概念

- **反向鏈結（backward chaining）**：從目標出發，尋找結論與之相符的規則，並遞迴地證明其前提。
- **合一（unification）**：找出使兩個項相等的代換。古典證明器精確地使用它。
- **軟合一（soft unification）**：兩個符號之間的相符程度，以其嵌入搭配徑向基底函數核計算。
- **證明分數（proof score）**：一個證明的分數，值在 $[0,1]$ 之間，由沿途的軟性比對組成，使查詢得到一個分數，而非是或否的答案。

## 運作方式

單一查詢的程序如下。

1. **嵌入符號。** 每個述詞與常項都有可學習的向量表示。
2. **尋找候選步驟。** 對於目標，考慮每個事實，以及每條頭部可能與之相符的規則。
3. **軟性比對。** 以徑向基底函數核為兩個嵌入計分，例如高斯核 $k(\mathbf{a}, \mathbf{b}) = \exp(-\lVert \mathbf{a} - \mathbf{b} \rVert^2 / \mu)$，其中 $\mu$ 為頻寬。
4. **遞迴。** 以相同方式證明規則的本體，並沿鏈條把各比對分數相乘。
5. **合併替代證明。** 將不同證明的分數合併（此處取最大值），得到該查詢的分數。
6. **訓練。** 以梯度下降調整嵌入與規則參數，使知識庫所支持的事實獲得高分。

同一套機制也能歸納規則。摘要指出，網路會學習把相似的符號放在彼此接近的位置、在證明中利用這些相似性、歸納邏輯規則，並把給定規則與歸納規則結合起來進行多跳推理。[^1]

## 結果

摘要報告，此架構在四個基準知識庫中的三個上，表現優於最先進的神經連結預測模型 ComplEx，同時歸納出可解釋、無函數符號的一階邏輯規則。[^1] 基準名稱與詳細數字見論文，本頁未加引述。

## 限制

- **遞迴的成本。** 反向鏈結會探索候選規則與比對，其成本隨證明深度與規則數目增長。實務上，對替代證明的搜尋必須加以限制。
- **相似不等於相同。** 嵌入相近的兩個符號可能被視為相等，因此證明可能看似合理，卻依賴一個錯誤的比對。
- **無函數的規則。** 歸納出的規則不含函數符號，因此排除了會建構新項的結構，例如串列。
- **適用範圍狹窄。** 結果涉及知識庫補全與查詢回答，此方法並不處理開放式語言或感知。

## 開放問題

- 軟合一能否與精確檢查結合，使學得的相似性不致產生無效證明？
- 此方法能擴展到多大的知識庫，以及無界的證明搜尋？
- 它歸納出的規則，能否由形式化的證明助手檢查？

## 關聯

神經定理證明器與 [∂ILP](../differentiable-ilp/index.md) 都會學習規則，但方向不同。∂ILP 從範例學習規則，神經定理證明器則證明查詢，並在證明的過程中附帶歸納出規則。後來的神經證明器轉而處理形式化數學，而非知識庫。GPT-f 以 Transformer 語言模型產生 Metamath 證明；[^2] LeanDojo 為 Lean 的證明器加入檢索；[^3] AlphaProof 則以強化學習搜尋 Lean 證明。[^4] 在以 Lean 為基礎的系統中，證明以文字撰寫，且只有在 Lean 4 檢查通過後才被接受。[^5] 見[數學與形式證明](../../../../applications/mathematics/index.md)與 [AlphaProof](../../../../applications/mathematics/alphaproof/index.md)。

## 應用

- **知識庫補全。** 推論不完整知識庫中缺少的事實，如摘要中的實驗所示。[^1]
- **多跳查詢。** 回答需要串接多個事實與規則的問題。

[^1]: Rocktäschel 與 Riedel（2017），見上文。結果與能力取自摘要。
[^2]: Polu 與 Sutskever（2020），見上文。
[^3]: Yang 等人（2023），見上文。
[^4]: Hubert 等人（2025），見上文。
[^5]: de Moura 與 Ullrich（2021），見上文。

## 參考文獻

### 開創性論文

- Rocktäschel, T. & Riedel, S. (2017). *End-to-End Differentiable Proving*. arXiv. https://arxiv.org/abs/1705.11040 — 建立以反向鏈結證明知識庫查詢的神經網路，其中的軟性符號比對由資料學得。
- Polu, S. & Sutskever, I. (2020). *Generative Language Modeling for Automated Theorem Proving*. arXiv. https://arxiv.org/abs/2009.03393 — 介紹 GPT-f，一個以 Transformer 為基礎、針對 Metamath 的證明器，其證明被採納入主要函式庫。

### 文章與文件

- Yang, K. et al. (2023). *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models*. arXiv. https://arxiv.org/abs/2306.15626 — 開源的 Lean 工具組，包含資料、模型與基準，並含一個以檢索增強的證明器。
- Hubert, T. et al. (2025). *Olympiad-level formal mathematical reasoning with reinforcement learning*. Nature. https://doi.org/10.1038/s41586-025-09833-y — 描述 AlphaProof，它透過強化學習學會找出形式化的 Lean 證明，並帶有測試時適應。
- de Moura, L. & Ullrich, S. (2021). *The Lean 4 Theorem Prover and Programming Language*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-030-79876-5_37 — 描述 Lean 4，即 AlphaProof 所用的證明助手與程式語言。
