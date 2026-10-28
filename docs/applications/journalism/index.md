---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm
  - engineering/rag
  - society/safety-alignment
aliases:
  - 新聞與資訊生態
  - Journalism
  - Automated journalism
---

# Journalism and Information Ecosystems

AI touches journalism in two directions. Newsrooms use it to write, verify and distribute stories, and it also changes how information spreads, through platforms that rank and recommend content. This page covers both sides, from automated reporting to the spread of false news.

## Landscape

| Area | Examples |
|---|---|
| Automated reporting | Software that writes routine stories, such as earnings or sports results, from structured data |
| Research and verification | Searching documents and data, and checking claims against sources |
| Transcription and archives | Turning audio and video into searchable text |
| Distribution | Ranking and recommending articles to readers |
| Misinformation | Generating or spreading false content, and detecting it |
| Audience tools | Summaries, translations and personalised newsletters |

## Automated journalism

Automated journalism uses software to turn structured data into news stories. Graefe (2016) reviews research on this practice, including how these systems work and their use in newsrooms, with case studies from the Los Angeles Times and the Associated Press. Carlson (2015) examines the wider effects of automated journalism on labour and on journalistic authority.

## Accountability for algorithms

News organisations also investigate the algorithms that shape public life. Diakopoulos (2014/2015) discusses how journalists can do this, and his book *Automating the News* (2019) covers how algorithms reshape news production and distribution.

## The spread of false news

Vosoughi, Roy & Aral (2018) compare how true and false news spread on Twitter. Detecting and limiting misinformation is a major research area, and it depends partly on how platforms rank content.

## Key methods

Three methods are most relevant. Each links to the page that explains it.

- [Large language models](../../theory/models/llm/index.md): drafting stories and summaries, which need editorial checks because they can state errors fluently.
- [Retrieval-augmented generation](../../engineering/rag/index.md): grounding answers in a document archive, so that every claim can be traced to a source.
- [Safety and alignment](../../society/safety-alignment/index.md): how models are steered away from producing harmful or false content.

## Risks

- **Errors at scale.** Automated stories can repeat a bad data source across many articles at once.
- **Trust.** Readers may not know whether a story was written by a person or a machine, and disclosure practices vary.
- **Economics.** Automated output can replace work that funded local reporting.

## Open questions

- How should newsrooms disclose automated writing so readers can judge it?
- Can verification tools keep pace with the speed of generated misinformation?
- What do local newsrooms need to use these tools without losing editorial control?

## References

### Seminal papers

- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science* 359(6380). https://doi.org/10.1126/science.aap9559 — Compares how true and false news spread on Twitter.
- Carlson, M. (2015). The Robotic Reporter: Automated journalism and the redefinition of labor, compositional forms, and journalistic authority. *Digital Journalism* 3(3). https://doi.org/10.1080/21670811.2014.976412 — Examines automated journalism and its effects on labour and journalistic authority.
- Diakopoulos, N. (2015). Algorithmic Accountability. *Digital Journalism* 3(3). https://doi.org/10.1080/21670811.2014.976411 — Discusses how journalists can investigate the algorithms that shape public information.

### Surveys and textbooks

- Diakopoulos, N. (2019). *Automating the News: How Algorithms Are Rewriting the Media*. Harvard University Press. https://doi.org/10.4159/9780674239302 — A book on how algorithms shape news production and distribution.

### Articles and documentation

- Graefe, A. (2016). *Guide to Automated Journalism*. Tow Center for Digital Journalism, Columbia University. https://data.journalism.columbia.edu/sites/data.journalism.columbia.edu/files/content/guide-to-automated-journalism.pdf — Reviews research on automated journalism, with case studies from the Los Angeles Times and the Associated Press.
