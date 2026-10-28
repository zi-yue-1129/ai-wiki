# Daily authoring routine

Instructions for the scheduled Claude routine that drafts one page per day as a pull request. Edit this file to change what the routine does; it reads the latest version from `main` every run.

## Each run

1. Start from the latest `main`. Create a branch `auto/<yyyy-mm-dd>-<topic-slug>`.
2. Pick **one** topic, in this order of preference:
    1. An open issue labelled `topic-request` that nobody has claimed.
    2. A stub listed by `python scripts/wiki_status.py --format issue`, preferring core pages (section foundations, models, brain-mind) and section index pages last.
    3. An unticked ★★★ item, then ★★, from "Missing topics" in `docs/reference/roadmap/index.md`.

    Skip any topic that already has an open pull request (check branch names starting `auto/` and PR titles), and skip pages changed on `main` in the last 2 days, since someone may be writing them.
3. Write the English page following `docs/reference/style-guide/index.md` and `templates/page-template.md`:
    - Original prose, encyclopedic tone, 800 to 2000 words.
    - End the page with a `## References` section that follows the Citations rules in the style guide: at least 5 entries across seminal papers, surveys and textbooks, lectures and videos, and articles and documentation. Every entry needs a DOI, arXiv id or URL, and a short note after " — " saying what the source covers, so readers can decide whether to open it.
    - Open every link and check its title, authors, year and content before adding it. Prefer the original paper and official course or channel pages for videos. Never invent a citation, DOI or URL; if you can't verify an entry, leave it out.
    - In the PR body, list each reference with the check you made (for example "opened, abstract matches").
    - Include the brain and mind connection where one genuinely exists.
    - If the topic also belongs to other categories, add those topic folders to `related` (and fitting `tags`) in the front matter (see "Topics in more than one category" in the style guide) rather than duplicating content. Also check whether existing pages should list the new page.
    - Add `aliases` in the front matter with the other names readers search for, such as the Chinese name and common abbreviations, so cross-language search finds the page. Pages you edit should gain `aliases` too.
    - Remove the "Work in progress" admonition. Set `status: draft` and `last_reviewed:` to today in the front matter.
    - New pages go in the folder tree described under "Where pages live" in the style guide (a new sub-topic of an existing topic goes inside that topic's folder). Add them to `nav` in `mkdocs.yml` with a `nav_translations` entry, link them from the parent folder's `index.md`, and tick the roadmap box.
4. Also write the Traditional Chinese translation (`<page>.zh-TW.md` next to the English file) with `translation_reviewed:` set to today, using glossary terms.
5. Run `mkdocs build --strict` and `python scripts/wiki_status.py --check`; fix anything they report.
6. Open a pull request to `main` titled `Draft: <Page title>`, link the issue it closes if any, list the sources used, and point out any claims the reviewer should double-check. Request review from the repository owner. Do not merge.

## Limits

- One page per run. If nothing suitable is left, open no PR.
- If 5 or more `auto/` pull requests are already open and unreviewed, open no new one and stop; the reviewer is behind.
- Never edit workflows, scripts, the license, or pages other than the one being drafted (plus `mkdocs.yml` nav and the roadmap checkbox).
