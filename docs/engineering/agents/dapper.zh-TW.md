---
status: draft
last_reviewed: 2026-11-27
translation_reviewed: 2026-11-27
tags:
  - distributed tracing
  - observability
aliases:
  - Dapper
  - Dapper tracing
  - Dapper 分散式追蹤系統
---

# Dapper

Dapper 是 Google 於 2010 年描述的分散式追蹤基礎設施。它記錄一個請求如何穿過許多服務，並被設計為在極大規模的系統上持續運作。它提出的 trace、span 與註記模型，正是[代理可觀測性](agent-observability.zh-TW.md)用來追蹤模型與工具呼叫鏈的模型。Dapper 本身不是代理工具。

## 問題

論文從兩項基本要求出發：廣泛部署與持續監控。其三項具體目標為：追蹤必須有低開銷，對正在運作的服務幾乎沒有效能影響；必須具備應用層透明性，程式設計師無須知道追蹤系統的存在；並且能擴展到 Google 的服務與叢集規模。

## 核心想法

Dapper 的追蹤是一棵由巢狀遠端呼叫組成的樹。每個節點是一個 span，即一個基本工作單位，具有 span id 與 parent id。沒有 parent id 的 span 稱為根 span，同一請求的所有 span 共用一個 trace id。每個 span 也是一筆帶時間戳記的紀錄，包含開始與結束時間、遠端呼叫的計時資料，以及零或多個應用程式自訂的註記。論文限制每個 span 的註記總量。識別碼為機率上唯一的 64 位元整數，因此可以由紀錄下來的 span 重建整棵樹。

## 機制

抽樣使常態追蹤負擔得起。第一個正式版本約每 1024 個候選請求記錄一條追蹤，論文也提到高流量服務的抽樣率低至 0.01%。論文指出抽樣是避免延遲惡化所必需的。每台主機上有一個常駐程式收集 span 紀錄，論文報告該程式從未用到超過一個核心的 0.3%。

## 結果

開銷結果來自一個網路搜尋叢集，作者在數種抽樣率下量測延遲與吞吐量。

- 追蹤每個請求（抽樣 1/1）使平均延遲上升 16.3%，吞吐量下降 1.48%。
- 在 1/16 抽樣時，延遲上升 2.12%，吞吐量變化為 −0.08%。
- 在 1/1024 抽樣時，延遲變化為 −0.20%，吞吐量變化為 −0.06%。

論文給出延遲的實驗誤差為 2.5%、吞吐量為 0.15%，並指出低於 1/16 的抽樣頻率落在該誤差之內。論文的其他數據：在 2.2 GHz 的 x86 伺服器上，建立與銷毀一個根 span 平均需 204 奈秒，一個非根 span 需 176 奈秒；未抽樣的註記約 9 奈秒，抽樣的註記約 40 奈秒。每筆 span 紀錄平均 426 位元組，收集的資料量不到網路流量的 0.01%。

## 限制

- 開銷量測來自 Google 內部一個網路搜尋叢集，因此不能直接推論其他工作負載的成本。
- 抽樣以完整性換取成本。在 1/1024 抽樣下，罕見的失敗可能完全沒有留下追蹤。這是依抽樣率所作的推論，並非論文報告的結果。
- 此模型記錄呼叫及其時間，卻不記錄元件為何做出某個決定；代理追蹤同樣需要這類資訊。

其他方法以不同方式處理同一問題。The Mystery Machine 從既有的元件日誌推斷一個請求如何執行；Pivot Tracing 在執行期間加入插樁並串接所收集的事件；Canopy 則是 Facebook 後來的端到端追蹤系統。各方法見參考文獻。

## 關聯

- [代理可觀測性與追蹤](agent-observability.zh-TW.md)把此模型套用到代理執行。
- [AgentOps](agentops.zh-TW.md)在此之上提出應追蹤哪些代理產物。

## 參考文獻

### 開創性論文

- Sigelman, B. H. 等人（2010）。*Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*。Google 技術報告 dapper-2010-1。https://research.google.com/archive/papers/dapper-2010-1.pdf — 提出 trace、span 與註記模型的論文，並報告正式運作系統的開銷。
- Chow, M.、Meisner, D.、Flinn, J.、Peek, D. 與 Wenisch, T. F.（2014）。*The Mystery Machine: End-to-end Performance Analysis of Large-scale Internet Services*。OSDI '14。https://www.usenix.org/conference/osdi14/technical-sessions/presentation/chow — 從既有的元件日誌建立請求執行模型，作為插樁的替代方案。
- Mace, J.、Roelke, R. 與 Fonseca, R.（2015）。*Pivot Tracing: Dynamic Causal Monitoring for Distributed Systems*。SOSP '15。https://cs.brown.edu/~jcmace/papers/mace15pivot.pdf — 結合執行期動態插樁與 happened-before 串接，在執行期關聯各元件的事件。
- Kaldor, J.、Mace, J.、Bejda, M. 等人（2017）。*Canopy: An End-to-End Performance Tracing And Analysis System*。SOSP '17。https://cs.brown.edu/~jcmace/papers/kaldor2017canopy.pdf — 描述 Facebook 的端到端效能追蹤基礎設施。

### 文章與文件

- OpenTelemetry。*Semantic Conventions for GenAI agent and framework spans*。https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md — 把 trace 模型套用到代理操作的 span 慣例。頁面標示為開發中。
