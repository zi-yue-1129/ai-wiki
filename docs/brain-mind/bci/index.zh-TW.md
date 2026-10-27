# 腦機介面與神經解碼

**腦機介面（BCI）**記錄大腦活動、解碼，並用來控制裝置或溝通——或把訊號送回神經系統。近期大部分進展來自 AI 解碼器。

## 記錄方式

| 方式 | 侵入性 | 訊號品質 | 典型用途 |
|---|---|---|---|
| EEG | 非侵入 | 空間解析度低、雜訊多 | P300 拼字、SSVEP、運動想像、神經回饋、消費級頭戴裝置 |
| fNIRS | 非侵入 | 血流動力學較慢 | 研究、簡單溝通 |
| MEG／OPM-MEG | 非侵入 | 時間解析度佳；昂貴（OPM 感測器可穿戴） | 研究解碼 |
| fMRI | 非侵入 | 空間好、速度慢 | 研究中解碼影像與語言 |
| ECoG／立體 EEG | 需手術，置於腦表或腦內 | 高品質 | 語音解碼、癲癇監測 |
| 血管內（Stentrode） | 經由血管 | 中等 | 發訊息與電腦控制 |
| 植入式微電極陣列（Utah 陣列、Neuralink、Paradromics 等） | 穿透式 | 單神經元解析度 | 游標、機械手臂、手寫、語音 |

## 里程碑

| 年份 | 成就 |
|---|---|
| 1970 年代 | Vidal 提出「腦機介面」一詞 |
| 1988 | P300 拼字器（Farwell & Donchin） |
| 2006 | BrainGate：四肢癱瘓者以皮質內陣列控制游標（Hochberg et al.） |
| 2012 | 人能控制機械手臂伸手與抓取 |
| 2016–2021 | 以皮質內微刺激恢復觸覺 |
| 2021 | 手寫 BCI：想像中的手寫以每分鐘約 90 字解碼（Willett et al., *Nature*） |
| 2023 | 語音神經義肢以大詞彙量達每分鐘 62–78 字，包括數位化身的聲音（Willett et al.；Metzger et al., *Nature*） |
| 2023 | 腦與脊髓之間的「數位橋」恢復行走（Lorach et al., *Nature*） |
| 2024 | 以個人化合成聲音達約 97% 準確率的語音 BCI（Card et al., *NEJM*）；Neuralink 首批人體植入 |
| 2025 | 低延遲、近即時的串流腦到語音合成（Littlejohn et al.；Wairagkar et al.） |

## AI 的貢獻

- **序列模型**（RNN、Transformer）把神經活動映射到音素、字元或運動指令
- **語言模型**修正解碼錯誤——和語音辨識用的是同一招
- **跨時段與跨人的自監督預訓練**（如 POYO、NDT 系列的神經基礎模型）減少重新校準
- **生成模型**從大腦活動重建影像與聲音
- **閉環適應**處理非平穩的記錄

## 非侵入式的感知與思維解碼

- **fMRI 解碼影像**：以大腦活動為條件的 Stable Diffusion 可重建觀看的影像（Takagi & Nishimoto, 2023）；MindEye 及後續研究利用 Natural Scenes Dataset 提升了保真度
- **fMRI 解碼語言**：語意解碼器重建人聽到或想像的故事大意（Tang, LeBel, Jain & Huth, 2023, *Nature Neuroscience*）——它需要受試者配合，且需要大量個人化的訓練資料
- **MEG 即時解碼**影像與語音（Meta AI, 2023）

!!! warning "不是讀心術"
    目前的非侵入式解碼器都是針對個人的，需要數小時校準，重建的是語意大意而不是精確的念頭，而且受試者若抗拒就會失效。儘管如此，快速的進展仍促使人們重視**神經隱私**的保護。

## 臨床與消費應用

- 為漸凍症、閉鎖症候群、腦幹中風患者提供溝通
- 運動恢復：機械手臂、功能性電刺激、脊髓橋接
- 感覺恢復：人工耳蝸（最成功的神經介面）、視網膜與皮質視覺義肢
- **深部腦刺激**治療帕金森氏症，部分地區已核准適應性（閉環）DBS
- 神經回饋（證據品質不一）；消費級 EEG 的睡眠與專注監測

## 倫理：神經權利

- **心智隱私**：神經資料可能揭露健康狀況與心理狀態
- **認知自由與身分**：刺激可能改變情緒或人格
- **能動性**：由解碼器中介的行動，誰負責？
- **公平與遺棄**：公司停止支持植入裝置時怎麼辦？
- **法規**：智利於 2021 年修憲保護神經資料；科羅拉多與加州於 2024 年把神經資料納入隱私法；UNESCO 於 2025 年通過神經科技倫理建議書

## 學習資源

- Wolpaw & Wolpaw,《Brain-Computer Interfaces: Principles and Practice》
- [BCI Society](https://bcisociety.org/)
- [MNE-Python](https://mne.tools/)、[MOABB](https://moabb.neurotechx.com/)（基準）、[BrainFlow](https://brainflow.org/)
- [NeuroTechX](https://neurotechx.com/) 社群
- Yuste et al. (2017), "Four ethical priorities for neurotechnologies and AI", *Nature*
