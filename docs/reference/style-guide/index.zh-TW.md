---
references: not-required  # lists and meta pages cite through their entries
translation_reviewed: 2026-10-28
---

# 寫作風格指南

說明本站頁面如何撰寫，讓數百頁、由許多作者寫成的內容，讀起來像同一部作品。

## 語言

- **英文是主要語言。** 每個主題都先有英文頁（`topic.md`）。
- **繁體中文是次要語言。** 翻譯與英文頁並排放置，命名為 `topic.zh-TW.md`。缺少翻譯時會自動退回英文。
- 修改英文頁的意思時，可以在同一個 PR 中更新翻譯，或暫時不改；狀態報告會標示落後的翻譯。確認翻譯與最新英文頁對照無誤後，請在該翻譯的前言中設定 `translation_reviewed: YYYY-MM-DD`。
- 兩種語言都請使用[詞彙表](../glossary/index.zh-TW.md)中的術語，讓翻譯保持一致。新增的術語也請加入詞彙表。

## 頁面位置

頁面以資料夾樹狀組織，深度可依主題需要增加：

```text
docs/
  <section>/                 例如 theory/
    index.md                 區段總覽
    <topic>/                 例如 llm/
      index.md               主題總覽
      <subtopic>.md          一個聚焦的頁面，例如 tokenization.md
      <subtopic>.zh-TW.md    它的翻譯
      <subtopic>/            當它需要自己的子頁面時，改成資料夾
        index.md
```

- 每個主題都有自己的資料夾與 `index.md` 總覽（以及 `index.zh-TW.md`），即使還沒有子頁面也一樣。總覽會連結到它的子頁面。
- 某些區段會把主題再分一層，例如 `theory/paradigms/<paradigm>/index.md`。
- 當頁面長出子頁面時，請把 `<subtopic>.md` 改為 `<subtopic>/index.md`，並把它的翻譯一起移過去。
- 檔案與資料夾名稱使用小寫英文加連字號。
- 移動或重新命名頁面時，請把舊路徑與新路徑加入 `mkdocs.yml` 的 `redirect_maps`，讓既有連結仍然有效。

## 方法頁與上層總覽

- 每個具名方法（讀者會以名稱查詢的模型、演算法或架構）都有自己的頁面，寫明詳細內容：問題、核心想法、方程式或演算法、結果與限制。放在主題資料夾中，檔名為 `<method>.md` 或 `<method>/index.md`。
- 上層頁面（主題或區段總覽）只保留簡要的比較：每種方法一行、說明彼此的差異，並連結到每個方法頁面。不重複其詳細內容。
- 新增子主題、方法或其他子頁面時，請在同一個 PR 中更新每個上層頁面的比較與總覽，不只是直接上層。
- 每個子頁面都必須連結自其上層的 `index.md`。`python scripts/wiki_status.py --check` 在缺少連結時會發出警告。

## 理論還是模型？

Models 是 Theory 的子區段，因此兩類頁面都放在 `docs/theory/` 之下。依頁面的主題決定：

- **Theory**（`theory/<topic>/`）說明某事物一般上*如何*運作：數學、學習訊號、學習理論、推論。理論頁面即使把其中的網路換成另一種，仍應說得通。
- **Models**（`theory/models/<topic>/`）說明一個具體的模型或系統*是什麼*，以及它用在哪裡：例如 transformer、擴散模型等具名的模型家族，或以它們建構的系統，例如 LLM 或 agent。

當某項技術同時屬於兩者時，理論放在 Theory，模型特定的應用放在 Models，並以 `related:` 相互連結。不要在兩個區段重複相同的內容。

## 讀者與語氣

- 為來自各領域的好奇讀者寫作：心理學學生、醫師、工程師。第一次出現的專有名詞要加以解釋，或連結到說明它的頁面。
- 使用中立、百科全書式的語氣。公平描述爭論，並說明各方持有什麼觀點。
- 偏好短段落、具體例子，以及每節只談一個概念。

## 頁面結構

新頁面請從[頁面範本](https://github.com/zi-yue-1129/ai-wiki/blob/main/templates/page-template.md)開始。不適用的段落可以省略，但請維持以下順序：

1. 標題（`# 標題`）與一到兩句的摘要
2. 概述、關鍵概念、運作方式
3. 關鍵方法：重要方法的簡要比較，連結到各方法自己的頁面；該頁面包含問題、核心想法、方程式或演算法、結果與限制（見上文「方法頁與上層總覽」與範本）
4. 與其他頁面的連結（特別是大腦與心智的角度）
5. 應用、開放問題
6. 參考資料，然後是「延伸學習」（非正式的指引，見下文「引用」）

尚未完成的頁面，請在頂端保留以下提示框。狀態報告會據此把它標記為樁頁：

```markdown
!!! info "Work in progress"
    This page is being written.
```

## 前言

所有欄位都是選填的。

| 欄位 | 值 | 意義 |
|---|---|---|
| `status` | `stub`、`draft`、`complete` | 覆寫自動判定的狀態（有上述標記即為樁頁；低於 400 字為草稿；其餘為完成） |
| `last_reviewed` | `YYYY-MM-DD` | 最近一次確認整頁仍然正確的時間。超過 12 個月未更新的頁面會被標記 |
| `related` | 相對於 `docs/` 的主題資料夾（或 `.md` 頁面）清單 | 本頁同時屬於的其他類別主題。會產生雙向的「相關主題」區段（見下文） |
| `tags` | 詞語清單 | 跨領域的主題，會彙整在標籤頁上 |
| `references` | `not-required` | 讓清單或後設頁面免於參考資料檢查 |
| `translation_reviewed` | `YYYY-MM-DD` | 用於翻譯頁：最近一次與英文頁對照的時間 |

## 跨多個類別的主題

許多主題同時屬於多個類別：強化學習既是一種學習典範、也是大腦中多巴胺的模型，還是機器人學的工具。每個主題都有**一個主要資料夾**，依讀者最可能先找的地方決定，並在其英文頁的前言中，連結到其他類別：

```yaml
---
related:
  - brain-mind/memory-learning
  - applications/robotics
tags:
  - reinforcement learning
---
```

- `related` 列出相對於 `docs/` 的主題資料夾（`brain-mind/neuroai` 指 `brain-mind/neuroai/index.md`）；單一子頁面可以用檔案名稱指定，例如 `models/llm/tokenization.md`。每個關係只需宣告一次，放在任一頁面上皆可：建置會在**兩個**頁面、每種語言中都加入「相關主題」區段，標題以該語言顯示。不要手動撰寫「相關主題」區段。
- `tags` 依跨領域的主題將頁面分組；每個標籤都會列在參考區的標籤頁上。
- `related` 只用於共享同一主題的頁面，而不是你在文中提到的每個頁面。凡是需要說明關聯的地方，也請在文中加上內部連結。
- 不要把相同的內容複製到兩個類別；寫一次，然後連結過去。
- 若 `related` 的條目不存在，`python scripts/wiki_status.py --check` 會失敗。

## 連結

- 連結到其他頁面時，使用指向 `.md` 檔案的相對路徑：`[Transformers](../transformer/index.md)`。
- 不要連結到其他頁面的標題（`page.md#heading`）：各語言的標題不同，會導致建置失敗。
- 外部連結優先使用穩定的來源（DOI、arXiv 摘要頁、官方文件），而非部落格的轉載。
- 外部連結都要可以點擊：使用 Markdown 連結 `[文字](https://...)`，或直接貼上完整的 `https://` 網址。單獨的 DOI（`doi:10.…`）或 arXiv 編號（`arXiv:2005.11401`）無法點擊，因此也要附上其 `https://` 網址。

## 來源與授權

- 內容採用 **CC BY-SA 4.0** 授權。請以自己的文字撰寫。
- 每個非顯而易見的主張都需要來源。見下文的引用一節。
- 在註明出處的前提下，你可以改寫 CC BY、CC BY-SA 或 MIT 來源的材料。非商業（NC）或禁止改作（ND）授權的材料只能連結，不能複製。
- 圖片：只能使用自己的或公開授權的圖片，並在圖說中註明授權與來源。

## 引用

好的參考資料讓頁面值得信賴，也能幫助學習。每個主題頁面都以 `## References` 區段結尾（zh-TW 頁面使用「參考資料」）。

**數量：** 至少 5 筆條目，越多越好。盡量涵蓋以下四種類型。建置會檢查條目（`--check`）：每一筆都需要可以點擊的連結（完整的 `https://` 網址；單獨的 DOI 或 arXiv 編號不算）。

**應包含的內容**

- **奠基性論文。** 引入或定義這個概念的論文。優先採用原始發表。
- **綜述與教科書。** 讀者可以用來深入學習的回顧與書籍。若有合法的免費版本，請連結該版本。
- **講義。** 大學或研究實驗室的課程頁面。請寫明講者、課程名稱與年份。影片不是參考資料（見下文規則）。
- **文章與文件。** 官方文件、原作者或實驗室的文章，以及審慎的新聞報導。優先採用一手來源，而非評論。

**格式**

條目夠多時，請依以下標題分組。每筆條目一行：引用資訊、連結，然後是破折號與簡短說明，讓讀者能判斷是否值得開啟：

```markdown
## References

### Seminal papers

- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, replacing recurrence with multi-head self-attention.
- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *J. Physiology*. doi:[10.1113/jphysiol.1962.sp006837](https://doi.org/10.1113/jphysiol.1962.sp006837) — The original receptive-field study of cat visual cortex, the root of later convolutional vision models.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Comprehensive textbook covering the mathematics and practice of deep learning, free online.

### Lectures

- Lecturer, *Course title*, University, Year. https://example.edu/course — Full lecture series on the topic from first principles, with problem sets.

### Articles and documentation

- Organization. *Page title*. https://example.org/page — Practical walkthrough of the method, with diagrams.
```

上面的範例僅示範格式，條目內容為英文。你撰寫的條目請依其來源原文呈現。

**規則**

1. **加入前先開啟每個連結。** 確認標題、作者、年份，以及它確實支持你引用的內容。絕不猜測 DOI、arXiv 編號或 URL，也不要引用你連摘要都沒讀過的論文。每個 DOI 都要對照能顯示它的來源（出版商頁面、Crossref，或會顯示 DOI 的資料庫）。憑記憶寫下的 DOI 不算已驗證。
2. **以註腳（`[^1]`）引用特定主張**，指向對應的條目。通用的閱讀清單則保留在參考資料中。
3. **為每筆條目加上註解。** 在連結後加一個破折號，並用一到兩句話說明該來源涵蓋什麼、適合誰。描述的是內容，而非評價其好壞，讓讀者能判斷是否值得開啟。
4. **影片不是參考資料。** 不要在參考資料中引用 YouTube 影片或演講錄影。若大學或研究實驗室的課程頁面是唯一來源，就引用該頁面；否則引用影片所解說的論文。影片可以列在「延伸學習」之下（見下文）。
5. **不要複製。** 引用來源並不代表可以重製其文字、圖表或示意圖。請改寫並連結。
6. **失效連結**由每週的連結檢查找出。請以封存副本或更新的來源取代，不要直接刪除條目。
7. 純清單或後設頁面（路線圖、詞彙表、參考清單）在前言中設定 `references: not-required`。區段總覽會自動免除。
8. **只用一手來源。** 部落格、電子報、YouTube 與其他影片頻道、書商頁面，以及書目彙整網站（Semantic Scholar 鏡像、scilit、researchr、RePEc 等類似網站）都不是參考資料。請引用論文本身、官方報告、標準或法規。若只能確認到彙整網站的頁面，請在 PR 說明中註明，而不要把該條目加入。

**每個外部資源都要有連結，正式與非正式來源分開。** 每個條目（無論位於哪個區段）都要以可以點擊的 `https://` 連結指向來源。正式來源（論文、官方報告、標準、法規、書籍）放在參考資料中。部落格、影片與彙整網站絕不放在參考資料中，可依下文所述列在「延伸學習」之下。CI 會對變更的頁面執行這兩項規則（`wiki_status.py --check`），`wiki_status.py --unlinked` 則會列出全站其餘的條目。

**延伸學習**

部落格、影片講座與其他非正式的指引，仍能幫助讀者進一步學習。請把它們列在 `## Further learning` 標題之下（放在 `## References` 之後，zh-TW 頁面可使用「延伸學習」），每行一筆，附上連結，並在後面以 " — " 加上說明。這些條目不是參考資料：建置不會計入，也絕不支持頁面上的主張；主張必須有參考資料中的條目作為依據。書商頁面與書目彙整網站即使在此也不列出。延伸閱讀與延伸學習的條目都需要 DOI、arXiv 編號或 URL，與參考資料條目相同。`python scripts/wiki_status.py --unlinked` 會列出全站所有沒有連結的條目。

```markdown
## Further learning

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*. Hugging Face blog. https://huggingface.co/blog/annotated-diffusion — Step-by-step code walk-through of DDPM, useful for checking the equations on this page.
```

## 格式

- 數學：`$行內$` 與 `$$獨立行$$`（MathJax）。
- 圖表：Mermaid 程式碼區塊。
- 提示框：`!!! note`、`!!! tip`、`!!! warning`。
- 在 `includes/abbreviations.md` 中定義的縮寫會在全站各處顯示提示框；新增縮寫請加入該檔案。
