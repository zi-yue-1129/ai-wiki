---
references: not-required  # lists and meta pages cite through their entries
---

# Style Guide

How pages in this wiki are written, so that hundreds of pages by many authors read as one work.

## Language

- **English is the primary language.** Every topic gets an English page first (`topic.md`).
- **Traditional Chinese (繁體中文) is the secondary language.** Translations live next to the English page as `topic.zh-TW.md`. A missing translation falls back to English automatically.
- When you change the meaning of an English page, either update the translation in the same PR or leave it; the status report flags translations that fall behind. After you check a translation against the latest English page, set `translation_reviewed: YYYY-MM-DD` in its front matter.
- Use the terms in the [Glossary](../glossary/index.md) for both languages so translations stay consistent. Add new terms there.

## Where pages live

Pages are organised as a tree of folders that can grow as deep as a topic needs:

```text
docs/
  <section>/                 e.g. theory/
    index.md                 section overview
    <topic>/                 e.g. llm/
      index.md               topic overview
      <subtopic>.md          a focused page, e.g. tokenization.md
      <subtopic>.zh-TW.md    its translation
      <subtopic>/            becomes a folder once it needs its own sub-pages
        index.md
```

- Every topic gets its own folder with an `index.md` overview (and `index.zh-TW.md`), even before it has sub-pages. The overview links to its children.
- Some sections group topics one level deeper, e.g. `theory/paradigms/<paradigm>/index.md`.
- When a page grows sub-pages, turn `<subtopic>.md` into `<subtopic>/index.md` and move its translation along with it.
- File and folder names are lowercase English with hyphens.
- When you move or rename a page, add its old and new paths to `redirect_maps` in `mkdocs.yml`, so existing links keep working.

## Method pages and parent overviews

- Every named method (a model, algorithm or architecture that readers look up by name) gets its own page with the detail: problem, core idea, equation or algorithm, results and limitations. Put it in the topic folder, as `<method>.md` or `<method>/index.md`.
- A parent page, whether a topic or section overview, keeps only a brief comparison: one line per method, what separates them, and a link to each method page. It does not repeat the detail.
- When you add a sub-topic, a method or any other child page, update the comparison and overview of every ancestor page in the same pull request, not only the direct parent.
- Each child page must be linked from its parent's `index.md`. `python scripts/wiki_status.py --check` warns when it is not.

## Theory or models?

Models is a subsection of Theory, so both kinds of page live under `docs/theory/`. Decide by what the page is about:

- **Theory** (`theory/<topic>/`) explains *how* something works in general: mathematics, learning signals, learning theory, inference. A theory page should still make sense if its network were swapped for another one.
- **Models** (`theory/models/<topic>/`) explains *what* a concrete model or system is and where it is used: a named family such as transformers or diffusion models, or a system built from them such as an LLM or an agent.

When a technique belongs to both, put the theory in Theory and the model-specific application in Models, and link the two with `related:`. Don't repeat the same material in both sections.

## Audience and tone

- Write for a curious reader from any field: a psychology student, a doctor, an engineer. Explain jargon on first use or link to the page that does.
- Neutral, encyclopedic tone. Describe debates fairly and say who holds which view.
- Prefer short paragraphs, concrete examples and one idea per section.

## Page structure

Start new pages from the [page template](https://github.com/zi-yue-1129/ai-wiki/blob/main/templates/page-template.md). Sections can be dropped when they don't apply, but keep this order:

1. Title (`# Heading`) and a one- or two-sentence summary
2. Overview, key concepts, how it works
3. Key methods: a brief comparison of the landmark methods, linking to each method's own page, which holds the problem, core idea, equation or algorithm, results and limitations (see "Method pages and parent overviews" and the template)
4. Connections to other pages (especially the brain and mind angle)
5. Applications, open questions
6. References, then Further learning for informal pointers (see Citations)

Unfinished pages keep this admonition at the top, which marks them as stubs in the status report:

```markdown
!!! info "Work in progress"
    This page is being written.
```

## Front matter

All fields are optional.

| Field | Values | Meaning |
|---|---|---|
| `status` | `stub`, `draft`, `complete` | Overrides the automatic status (stub if it has the marker above, draft under 400 words, otherwise complete) |
| `last_reviewed` | `YYYY-MM-DD` | Last time someone checked the whole page is still accurate. Pages older than 12 months are flagged |
| `related` | list of topic folders (or `.md` pages) relative to `docs/` | Topics in other categories this one also belongs to. Builds a reciprocal *Related topics* section (see below) |
| `tags` | list of words | Cross-cutting themes, collected on the Tags page |
| `references` | `not-required` | Exempts a list or meta page from the References check |
| `translation_reviewed` | `YYYY-MM-DD` | On a translation: last time it was checked against the English page |

## Topics in more than one category

Many topics belong to several categories at once: reinforcement learning is a learning paradigm, a model of dopamine in the brain, and a tool in robotics. Each topic has **one home folder**, chosen by where a reader would look first, and is connected to its other categories in the front matter of its English page:

```yaml
---
related:
  - brain-mind/memory-learning
  - applications/robotics
tags:
  - reinforcement learning
---
```

- `related` lists topic folders relative to `docs/` (`brain-mind/neuroai` means `brain-mind/neuroai/index.md`); a single sub-page can be named with its file, e.g. `models/llm/tokenization.md`. Declare each relationship once, on either page: the build adds a *Related topics* section to **both** pages, in every language, with titles in that language. Don't hand-write a "Related topics" section.
- `tags` groups pages by cross-cutting themes; every tag is listed on the Tags page in Reference.
- Use `related` for topics that share a subject, not for every page you mention. Link inline in the text as well wherever the connection is explained.
- Don't copy the same content into two categories; write it once and link to it.
- `python scripts/wiki_status.py --check` fails if a `related` entry doesn't exist.

## Links

- Link to other pages with relative paths to the `.md` file: `[Transformers](../transformer/index.md)`.
- Don't link to a heading on another page (`page.md#heading`): headings differ between languages and break the build.
- Prefer stable external links (DOI, arXiv abs pages, official docs) over blog mirrors.
- Write every external link so it is clickable: a Markdown link `[text](https://...)`, or a full `https://` URL pasted into the text. A bare DOI (`doi:10.…`) or arXiv id (`arXiv:2005.11401`) is not clickable on its own, so give its `https://` address too.

## Sources and licensing

- Content is licensed **CC BY-SA 4.0**. Write in your own words.
- Every non-obvious claim needs a source. See the Citations section below.
- You may adapt material from CC BY, CC BY-SA or MIT sources with attribution. Material under non-commercial (NC) or no-derivatives (ND) licenses may only be linked, not copied.
- Images: only your own or openly licensed ones, with the license and source in the caption.

## Citations

Good references are what make a page trustworthy and useful for learning. Every topic page ends with a `## References` section.

**How many:** at least 5 entries, and more is better. Aim for a spread across the four kinds below. Entries are checked by the build (`--check`): each needs a clickable link (a full `https://` URL; a bare DOI or arXiv id does not count).

**What to include**

- **Seminal papers.** The papers that introduced or defined the idea. Prefer the original publication.
- **Surveys and textbooks.** Reviews and books a reader can use to go deeper. Link a free version when one is legally available.
- **Lectures.** Course pages from universities and research labs. Name the speaker, course and year. Videos are not references (see Citations).
- **Articles and documentation.** Official documentation, posts from the original authors or labs, and careful journalism. Prefer primary sources over commentary.

**Format**

Group entries under these headings when the page has enough of them. Use one line per entry: the citation, the link, then a dash and a short note on what the source covers, so readers can decide whether to open it:

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

**Rules**

1. **Open every link before you add it.** Confirm the title, authors, year and that it says what you cite it for. Never guess a DOI, arXiv id or URL, and never cite a paper you have not at least read the abstract of. Check every DOI against a source that shows it (the publisher page, Crossref, or a database that displays the DOI). A DOI written from memory is not verified.
2. **Cite a specific claim with a footnote** (`[^1]`) that points to the entry. Keep a general reading list in References.
3. **Annotate every entry.** Add a dash and one or two sentences after the link saying what the source covers and who it is for. Describe the content, not how good it is, so readers can decide whether to open it.
4. **Videos are not references.** Do not cite YouTube videos or talk recordings in References. If a course page from a university or research lab is the only source, cite that page; otherwise cite the paper the video explains. A video may be listed under Further learning (see below).
5. **Don't copy.** Citing a source is not a license to reproduce its text, figures or diagrams. Paraphrase, and link.
6. **Dead links** are found by the weekly link check. Replace them with an archived copy or a newer source, don't just delete the entry.
7. Pages that are pure lists or meta pages (the roadmap, the glossary, the reference lists) set `references: not-required` in their front matter. Section overviews are exempt automatically.
8. **Primary sources only.** Blogs, newsletters, YouTube and other video channels, bookseller pages, and bibliographic aggregators (Semantic Scholar mirrors, scilit, researchr, RePEc and similar) are not references. Cite the paper, official report, standard or statute itself. If only an aggregator page can be confirmed, say so in the PR body rather than adding it.

**Every external resource has a link, and formal and informal sources are kept apart.** Each entry, in any section, links to its source with a clickable `https://` link. Formal sources (papers, official reports, standards, statutes, books) go in References. Blogs, videos and aggregators never go in References. They may be listed under Further learning, as described below. CI enforces both rules on changed pages (`wiki_status.py --check`), and `wiki_status.py --unlinked` lists the rest of the wiki.

**Further learning**

Blogs, video lectures and other informal pointers can still help a reader go further. List them under a `## Further learning` heading placed after `## References`, one line each with a link and a note after " — ". These entries are not references: the build does not count them, and they never support a claim on the page, which must be backed by an entry in References. Bookseller pages and bibliographic aggregators are not listed even here. Further reading and Further learning entries need a DOI, arXiv id or URL, just as References entries do; `python scripts/wiki_status.py --unlinked` lists every entry in the wiki that has none.

```markdown
## Further learning

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*. Hugging Face blog. https://huggingface.co/blog/annotated-diffusion — Step-by-step code walk-through of DDPM, useful for checking the equations on this page.
```

## Formatting

- Math: `$inline$` and `$$display$$` (MathJax).
- Diagrams: Mermaid code blocks.
- Callouts: `!!! note`, `!!! tip`, `!!! warning`.
- Abbreviations defined in `includes/abbreviations.md` get tooltips everywhere; add new ones there.
