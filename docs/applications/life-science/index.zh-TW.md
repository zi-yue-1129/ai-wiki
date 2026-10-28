# 生命科學與藥物發現

## 蛋白質結構：AlphaFold 時刻

- **方法頁面**：[AlphaFold 2](alphafold-2.md)（Jumper 等人，2021），包含其演算法、信心分數與限制
- **CASP14（2020）**：AlphaFold 2 對多數目標預測的蛋白質結構，精確度已可與實驗結果並駕齊驅，解決了困擾業界 50 年的重大挑戰
- **AlphaFold 蛋白質結構資料庫**：收錄超過 2.14 億筆預測結構，免費開放（[Varadi 等人，2024](https://doi.org/10.1093/nar/gkad1011)）
- **AlphaFold 3（2024）**：可預測蛋白質與 DNA、RNA、配體及離子所形成的複合物
- **2024 年諾貝爾化學獎**：David Baker（計算蛋白質設計），以及 Demis Hassabis 與 John Jumper（蛋白質結構預測）
- 開放的替代方案：RoseTTAFold、OpenFold、[ESMFold](esm/esmfold.md)（源自蛋白質語言模型）、Boltz、Chai

## 蛋白質設計

| 工具 | 方法 |
|---|---|
| [RFdiffusion](rfdiffusion/index.md) | 擴散模型，生成新的蛋白質骨架，用於結合子、酵素與對稱組裝體 |
| ProteinMPNN | 設計能摺疊成指定骨架的胺基酸序列 |
| [ESM 家族](esm/index.md)：[ESM-2](esm/esm-2.md) 與 [ESMFold](esm/esmfold.md)，蛋白質語言模型 | 從數百萬條序列中學習演化限制；ESM3 生成了一種新的螢光蛋白 |
| 反向摺疊、結合子設計流程 | 與高通量的實驗室測試結合使用 |

## 基因組學與分子生物學

- **變異效應預測**：AlphaMissense 對數千萬個錯義變異進行分類；SpliceAI 預測剪接效應
- **DNA 語言模型**：Enformer（由序列預測基因表現）、Evo 與 Evo 2（跨生命的基因組尺度模型）、Nucleotide Transformer
- **單細胞生物學**：在數千萬個細胞上訓練的基礎模型（scGPT、Geneformer），用於細胞類型標註與擾動預測——不過簡單的基準方法有時也很有競爭力
- **空間轉錄組與影像**：分割（Cellpose）、形態特徵分析（Cell Painting）
- **虛擬細胞**計畫的目標，是模擬細胞在各種擾動下的行為

## 藥物發現流程

```mermaid
flowchart LR
  T[標靶辨識] --> H[命中物發現]
  H --> L[先導化合物最佳化]
  L --> P[臨床前試驗]
  P --> C[臨床試驗]
```

| 階段 | AI 方法 |
|---|---|
| 標靶辨識 | 知識圖譜、遺傳學、以 LLM 進行文獻探勘 |
| 命中物發現 | 結合對接與機器學習的虛擬篩選、生成式化學、DNA 編碼文庫分析 |
| 先導化合物最佳化 | 性質預測（ADMET）、多目標生成式設計、結合實驗室迴圈的主動學習 |
| 臨床前試驗 | 毒性預測、數位病理 |
| 臨床試驗 | 病患分層、試驗設計、試驗點選擇、合成對照組 |

- **Insilico Medicine** 的 rentosertib（用於特發性肺纖維化）：標靶與分子都由 AI 找出與設計，2025 年在第二期 a 階段試驗中報告正向結果（*Nature Medicine*）
- **抗生素發現**：深度學習找到了 halicin（Stokes et al., 2020, *Cell*）與 abaucin；生成式模型設計出新的抗生素候選分子
- 現實檢驗：AI 發現的分子在第一期試驗的成功率很高，但截至 2025 年，尚無 AI 設計的藥物完成第三期試驗並獲得核准；主要瓶頸仍在生物學，而非化學

## 實驗室自動化與代理人

- 自動駕駛實驗室結合機器人、貝氏最佳化與[主動學習](../../theory/paradigms/active/index.md)
- LLM 代理人規劃實驗、撰寫實驗室流程並分析資料（見[科學發現](../science/index.md)）

## 生物安全

同樣的工具也可能被用來設計有害的製劑。目前的因應包括：篩檢 DNA 合成訂單、評估模型對生物濫用的助長程度，以及負責任的釋出政策（見[安全與對齊](../../society/safety-alignment/index.md)）。

## 關鍵方法

下列三種方法是上文多數蛋白質與基因組工具的基礎。每一項都連結到解釋該方法的頁面。

- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md)：對序列做自注意力。ESM 等蛋白質語言模型把它應用在胺基酸序列上（Vaswani et al., 2017；Lin et al., 2023）。
- [去噪擴散](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)：模型學習逆轉逐步加噪的過程，取樣即可產生新資料。RFdiffusion 以擴散生成蛋白質骨架（Ho et al., 2020；Watson et al., 2023）。
- [圖神經網路](../../theory/models/gnn/message-passing/gin/index.md)：在原子與化學鍵之間做訊息傳遞。GIN 是論文證明其判別能力與 Weisfeiler–Leman 圖測試相當的變體（Xu et al., 2019）。

## 參考文獻

### 開創性論文

- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
- Jumper, J. et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2，在 CASP14 中於多數目標上可與實驗方法媲美。
- Abramson, J. et al. (2024). Accurate structure prediction of biomolecular interactions with AlphaFold 3. *Nature*. https://doi.org/10.1038/s41586-024-07487-w — 將結構預測擴展到涉及 DNA、RNA、配體與離子的複合體。
- Watson, J. L. et al. (2023). De novo design of protein structure and function with RFdiffusion. *Nature*. https://doi.org/10.1038/s41586-023-06415-8 — RFdiffusion，一種生成新蛋白質骨架的擴散模型。
- Lin, Z. et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — ESM 語言模型與 ESMFold，僅從單一序列預測結構。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 本頁連結的擴散方法頁所依據的 DDPM 論文。
- Xu, K. et al. (2019). How Powerful are Graph Neural Networks? ICLR. https://arxiv.org/abs/1810.00826 — GIN，證明其判別能力與 Weisfeiler–Leman 圖測試相當。
- Stokes, J. M. et al. (2020). A Deep Learning Approach to Antibiotic Discovery. *Cell*. https://doi.org/10.1016/j.cell.2020.01.021 — 以深度學習篩選出抗生素候選物 halicin。

## 延伸學習

- [AlphaFold DB](https://alphafold.ebi.ac.uk/) — AlphaFold 預測蛋白質結構的免費資料庫。
- [RCSB PDB](https://www.rcsb.org/) — 實驗測定之生物大分子結構的典藏庫。
- [DeepChem](https://deepchem.io/) — 化學與藥物發現深度學習的開源工具包。
- [RDKit](https://www.rdkit.org/) — 處理分子的開源化學資訊學工具包。
- [TDC — Therapeutics Data Commons](https://tdcommons.ai/) — 藥物發現 AI 的基準資料集與任務。
