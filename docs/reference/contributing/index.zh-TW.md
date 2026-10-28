---
references: not-required  # lists and meta pages cite through their entries
translation_reviewed: 2026-10-28
---

# 參與貢獻

本站的目標是涵蓋 AI 的所有面向，從數學、神經科學，到各個領域如何運用它。要做到這一點，需要持續的貢獻。歡迎各種協助，從修正一個錯字到撰寫整個章節都可以。

## 參與方式

| 你想要 | 做法 |
|---|---|
| 修正錯字或小錯誤 | 點選任何頁面頂端的 ✏️ 編輯按鈕，在 GitHub 上編輯並開啟拉取請求 |
| 回報事實錯誤 | 開啟[更正議題](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=correction.yml) |
| 建議缺少的主題 | 開啟[主題建議](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=topic-request.yml) |
| 撰寫頁面 | 選一個開放的[章節議題](https://github.com/zi-yue-1129/ai-wiki/issues?q=is%3Aissue+is%3Aopen+label%3Achapter)，並依下方步驟進行 |
| 翻譯 | 選一個尚未有繁體中文翻譯的頁面（每週的健康報告會列出），或開啟[翻譯請求](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=translation.yml) |
| 審閱 | 對照最新知識檢查較舊的頁面，並更新其 `last_reviewed` 日期 |

## 撰寫或擴充頁面

1. 閱讀[寫作風格指南](../style-guide/index.zh-TW.md)，特別是其中的引用一節：每個主題頁面都需要一個參考資料區段，至少包含 5 筆已驗證的條目。
2. 為避免重複工作，請先在相關議題留言（或開一個新議題），說明你正在處理。
3. 新增頁面時，將 `templates/page-template.md` 複製到正確的資料夾（請見風格指南的頁面位置一節），並加入 `mkdocs.yml` 的 `nav`。若是樁頁，請把 "Work in progress" 提示框換成實際內容。
4. 本機預覽：

    ```bash
    pip install -r requirements.txt
    mkdocs serve
    ```

5. 執行 CI 會跑的檢查：

    ```bash
    mkdocs build --strict
    python scripts/wiki_status.py --check
    ```

6. 若主題也屬於其他類別，請在前言中以 `related` 連結（見風格指南）。
7. 開啟拉取請求。若頁面有對應的章節議題，請在說明中加入 `Closes #<議題編號>`，合併後議題會自動關閉。

## 翻譯頁面

1. 在英文頁面 `<page>.md` 旁建立 `<page>.zh-TW.md`（若是資料夾總覽，則在 `index.md` 旁建立 `index.zh-TW.md`）。
2. 翻譯整頁，保持標題、連結與結構不變。術語請使用[詞彙表](../glossary/index.zh-TW.md)。
3. 若頁面是新加入導覽的，請在 `mkdocs.yml` 的 `nav_translations` 中加入翻譯後的導覽標題。
4. 在前言中設定 `translation_reviewed: YYYY-MM-DD`。

## 自動化維護

這些工作在 GitHub Actions 上執行，讓問題不會被忽略：

- **每個拉取請求**：嚴格的網站建置（會抓出失效的內部連結），以及結構檢查（每頁都在導覽中、每個翻譯都有英文頁、前言格式正確）。PR 中變更的頁面必須有完整的參考資料區段，且只能使用正式來源（不得使用部落格、影片或彙整網站）；每筆「延伸閱讀」或「延伸學習」條目都需要連結。既有頁面在編輯時才會被檢查。
- **每週**：*Wiki health report* 議題會列出樁頁、草稿、一年以上未審閱的頁面、過時或缺少的翻譯、失效的外部連結，以及每一筆需要補上連結或移至「延伸學習」的來源條目。

## 授權

你的貢獻依 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 授權釋出。
