"""MkDocs hook: let each page be found from the other language.

Pagefind indexes each language separately, so a Chinese query finds no English
page and the reverse. This hook adds a hidden block to every page with the
terms it should answer to:
- the title of its translation (an English page gets the zh-TW title, and the
  zh-TW page gets the English title);
- any `aliases:` in the front matter, from the English page or the translation.

Titles are used automatically, so no page needs editing. For extra synonyms, add
to the English page's front matter:

    aliases:
      - LLM
      - 大語言模型

The block is hidden with `hidden`, so readers never see it, but Pagefind indexes
the text. Translations inherit the English page's aliases, as with `related:`.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import yaml

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
HEADING = re.compile(r"^#\s+(.+)$", re.M)
TRANSLATION = re.compile(r"\.zh-TW\.md$")
ENGLISH = re.compile(r"\.md$")


def read_page(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def title_of(path: Path) -> str:
    if not path.exists():
        return ""
    meta, body = read_page(path)
    if meta.get("title"):
        return str(meta["title"])
    m = HEADING.search(body)
    return m.group(1).strip() if m else ""


def on_page_markdown(markdown, page, config, files):
    docs = Path(config["docs_dir"])
    src = page.file.src_uri
    if TRANSLATION.search(src):
        english = docs / TRANSLATION.sub(".md", src)
        counterpart = english
        translation = docs / src
    else:
        english = docs / src
        counterpart = docs / ENGLISH.sub(".zh-TW.md", src)
        translation = counterpart

    terms = []
    title = title_of(counterpart)
    if title:
        terms.append(title)
    if english.exists():
        meta, _ = read_page(english)
        terms += [str(alias) for alias in meta.get("aliases") or []]
    if translation.exists() and translation != english:
        meta, _ = read_page(translation)
        terms += [str(alias) for alias in meta.get("aliases") or []]
    if not terms:
        return markdown
    block = " ".join(html.escape(term) for term in dict.fromkeys(terms))
    return f'{markdown}\n\n<div hidden class="search-aliases">{block}</div>\n'
