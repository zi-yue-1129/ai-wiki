# Daily authoring routine

Instructions for the scheduled Claude routine that drafts one page per day as a pull request. Edit this file to change what the routine does; it reads the latest version from `main` every run.

## Each run

1. Start from the latest `main`. Create a branch `auto/<yyyy-mm-dd>-<topic-slug>`.
2. Pick **one** topic, in this order of preference:
    1. An open issue labelled `chapter` that nobody has claimed, ordered by priority: `priority:core` first, then `priority:important`, `priority:nice`, and unranked drafts and stubs last. Use the issue's `Closes #n` in the PR.
    2. Only if no chapter issue is open: a stub listed by `python scripts/wiki_status.py --format issue`, preferring core pages (sections theory, brain-mind) and section index pages last.

    Skip any topic that already has an open pull request (check branch names starting `auto/` and PR titles), and skip pages changed on `main` in the last 2 days, since someone may be writing them.
3. Write the English page following `docs/reference/style-guide/index.md` and `templates/page-template.md`:
    - Original prose, encyclopedic tone, 800 to 2000 words.
    - End the page with a `## References` section that follows the Citations rules in the style guide: at least 5 entries across seminal papers, surveys and textbooks, lectures and videos, and articles and documentation. Every entry needs a DOI, arXiv id or URL, and a short note after " — " saying what the source covers, so readers can decide whether to open it.
    - Open every link and check its title, authors, year and content before adding it. Prefer the original paper and official course or channel pages for videos. Never invent a citation, DOI or URL; if you can't verify an entry, leave it out.
    - In the PR body, list each reference with the check you made (for example "opened, abstract matches").
    - Include the brain and mind connection where one genuinely exists.
    - Add a `## Key methods` section after "How it works" (pattern in `templates/page-template.md`): a brief comparison of two to four landmark methods, one line each, linking to each method's own page. Write each method as its own detailed page in the topic folder, with problem, core idea, equation or algorithm, results and limitations, in the same PR. Every paper named there must also appear in References, and its results must come from the paper itself, never from memory.
    - When you add a child page or a method, update the comparison and overview of every ancestor page in the same PR (see "Method pages and parent overviews" in the style guide).
    - If the topic also belongs to other categories, add those topic folders to `related` (and fitting `tags`) in the front matter (see "Topics in more than one category" in the style guide) rather than duplicating content. Also check whether existing pages should list the new page.
    - Add `aliases` in the front matter with the other names readers search for, such as the Chinese name and common abbreviations, so cross-language search finds the page. Pages you edit should gain `aliases` too.
    - Remove the "Work in progress" admonition. Set `status: draft` and `last_reviewed:` to today in the front matter.
    - New pages go in the folder tree described under "Where pages live" in the style guide (a new sub-topic of an existing topic goes inside that topic's folder). Add them to `nav` in `mkdocs.yml` with a `nav_translations` entry, and link them from the parent folder's `index.md`.
4. Also write the Traditional Chinese translation (`<page>.zh-TW.md` next to the English file) with `translation_reviewed:` set to today, using glossary terms.
5. Run `mkdocs build --strict` and `python scripts/wiki_status.py --check`; fix anything they report.
6. Open a pull request to `main` titled `Draft: <Page title>`. If the page has a chapter issue, end the description with `Closes #<issue number>` so the issue closes on merge. List the sources used, and point out any claims the reviewer should double-check. Request review from the repository owner. Do not merge.

## Limits

- One topic per run, including its method pages and the parent overviews it changes. If nothing suitable is left, open no PR.
- If 5 or more `auto/` pull requests are already open and unreviewed, open no new one and stop; the reviewer is behind.
- Never edit workflows, scripts, the license, or pages other than the topic being drafted, its method pages, the parent overviews above them (plus `mkdocs.yml` nav).
- Do not add a `Co-Authored-By` line to commit messages, even if other attribution guidance says to. Commit messages are a subject line and a short body; add no other attribution trailers.
