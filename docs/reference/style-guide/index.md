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
  <section>/                 e.g. models/
    index.md                 section overview
    <topic>/                 e.g. llm/
      index.md               topic overview
      <subtopic>.md          a focused page, e.g. tokenization.md
      <subtopic>.zh-TW.md    its translation
      <subtopic>/            becomes a folder once it needs its own sub-pages
        index.md
```

- Every topic gets its own folder with an `index.md` overview (and `index.zh-TW.md`), even before it has sub-pages. The overview links to its children.
- Some sections group topics one level deeper, e.g. `foundations/paradigms/<paradigm>/index.md`.
- When a page grows sub-pages, turn `<subtopic>.md` into `<subtopic>/index.md` and move its translation along with it.
- File and folder names are lowercase English with hyphens.

## Audience and tone

- Write for a curious reader from any field: a psychology student, a doctor, an engineer. Explain jargon on first use or link to the page that does.
- Neutral, encyclopedic tone. Describe debates fairly and say who holds which view.
- Prefer short paragraphs, concrete examples and one idea per section.

## Page structure

Start new pages from the [page template](https://github.com/zi-yue-1129/ai-wiki/blob/main/templates/page-template.md). Sections can be dropped when they don't apply, but keep this order:

1. Title (`# Heading`) and a one- or two-sentence summary
2. Overview, key concepts, how it works
3. Connections to other pages (especially the brain and mind angle)
4. Applications, open questions
5. Further reading and references

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
| `related` | list of paths relative to `docs/` | Pages in other categories this topic also belongs to. Builds a reciprocal *Related pages* section (see below) |
| `translation_reviewed` | `YYYY-MM-DD` | On a translation: last time it was checked against the English page |

## Topics in more than one category

Many topics belong to several categories at once: reinforcement learning is a learning paradigm, a model of dopamine in the brain, and a tool in robotics. Each topic has **one home folder**, chosen by where a reader would look first, and is connected to its other categories with `related` in the front matter:

```yaml
---
related:
  - brain-mind/memory-learning/index.md
  - applications/robotics/index.md
---
```

- Declare each relationship once, on either page. The build adds a *Related pages* section to **both** pages, in every language, using each page's translated title where one exists.
- Use English page paths relative to `docs/`; translations inherit the field.
- Use `related` for pages that share a subject, not for every page you mention. Link inline in the text as well wherever the connection is explained.
- Don't copy the same content into two categories; write it once and link to it.
- `python scripts/wiki_status.py --check` fails if a `related` path doesn't exist.

## Links

- Link to other pages with relative paths to the `.md` file: `[Transformers](../transformer/index.md)`.
- Don't link to a heading on another page (`page.md#heading`): headings differ between languages and break the build.
- Prefer stable external links (DOI, arXiv abs pages, official docs) over blog mirrors.

## Sources and licensing

- Content is licensed **CC BY-SA 4.0**. Write in your own words.
- Every non-obvious claim needs a source, as a footnote (`[^1]`) or in the references list.
- You may adapt material from CC BY, CC BY-SA or MIT sources with attribution. Material under non-commercial (NC) or no-derivatives (ND) licenses may only be linked, not copied.
- Images: only your own or openly licensed ones, with the license and source in the caption.

## Formatting

- Math: `$inline$` and `$$display$$` (MathJax).
- Diagrams: Mermaid code blocks.
- Callouts: `!!! note`, `!!! tip`, `!!! warning`.
- Abbreviations defined in `includes/abbreviations.md` get tooltips everywhere; add new ones there.
