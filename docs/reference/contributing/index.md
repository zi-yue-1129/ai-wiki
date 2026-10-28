---
references: not-required  # lists and meta pages cite through their entries
---

# Contributing

This wiki aims to cover everything about AI, from the mathematics to the neuroscience to how each field uses it. It only gets there with steady contributions. All help is welcome, from fixing a typo to writing a whole section.

## Ways to help

| You want to | Do this |
|---|---|
| Fix a typo or small error | Click the ✏️ edit button at the top of any page, edit on GitHub, and open a pull request |
| Report a factual error | Open a [correction issue](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=correction.yml) |
| Suggest a missing topic | Open a [topic request](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=topic-request.yml) |
| Write a page | Pick an open [chapter issue](https://github.com/zi-yue-1129/ai-wiki/issues?q=is%3Aissue+is%3Aopen+label%3Achapter) and follow the steps below |
| Translate | Pick a page without a 繁體中文 translation (the weekly health report lists them), or open a [translation request](https://github.com/zi-yue-1129/ai-wiki/issues/new?template=translation.yml) |
| Review | Check an older page against current knowledge and set its `last_reviewed` date |

## Writing or expanding a page

1. Read the [Style Guide](../style-guide/index.md), especially its Citations section: every topic page needs a References section with at least 5 verified entries.
2. To avoid duplicate work, comment on the related issue (or open one) saying you are working on it.
3. For a new page, copy `templates/page-template.md` into the right folder (see [Where pages live](../style-guide/index.md)) and add it to `nav` in `mkdocs.yml`. For a stub, replace the "Work in progress" admonition with real content.
4. Preview locally:

    ```bash
    pip install -r requirements.txt
    mkdocs serve
    ```

5. Run the checks the CI runs:

    ```bash
    mkdocs build --strict
    python scripts/wiki_status.py --check
    ```

6. If the topic also belongs to other categories, link them with `related` in the front matter (see the [Style Guide](../style-guide/index.md)).
7. Open a pull request. If the page has a chapter issue, add `Closes #<issue number>` to the description so the issue closes when the PR is merged.

## Translating a page

1. Create `<page>.zh-TW.md` next to the English page `<page>.md` (for a folder overview, `index.zh-TW.md` next to `index.md`).
2. Translate the whole page, keeping headings, links and structure the same. Use the [Glossary](../glossary/index.md) for terms.
3. Add the translated nav title under `nav_translations` in `mkdocs.yml` if the page is new to the nav.
4. Set `translation_reviewed: YYYY-MM-DD` in the front matter.

## Automated maintenance

These run on GitHub Actions so problems don't pile up unnoticed:

- **Every pull request**: strict site build (catches broken internal links) and a structure check (every page in the nav, every translation has an English page, valid front matter). Pages changed in the PR must have a complete References section, with formal sources only (no blogs, videos or aggregators), and every Further reading or Further learning entry needs a link. Existing pages are checked once they are edited.
- **Every week**: a *Wiki health report* issue lists stubs, drafts, pages not reviewed for a year, outdated or missing translations, broken external links, and every source entry that needs a link or a move to Further learning.

## License

By contributing you agree that your contribution is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
