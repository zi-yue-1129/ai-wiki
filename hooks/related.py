"""MkDocs hook: cross-link pages that belong to more than one category.

A page lists related topics in its front matter, relative to docs/, either as a
topic folder or as a page path:

    related:
      - brain-mind/neuroai                  # = brain-mind/neuroai/index.md
      - models/llm/tokenization.md

Links are made reciprocal automatically: the listed pages also link back, so
each relationship only needs to be declared once, on either page. A "Related
topics" section is appended to the end of every page involved, in each language.
Only English pages (page.md) need the field; translations inherit it.
"""

from __future__ import annotations

import posixpath
import re
from collections import defaultdict
from pathlib import Path

import yaml

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
HEADING = re.compile(r"^#\s+(.+)$", re.M)
TRANSLATION = re.compile(r"\.([a-z]{2}(?:-[A-Za-z]{2})?)\.md$")
TITLES = {"en": "Related topics", "zh-TW": "相關主題"}

_related: dict[str, set[str]] = defaultdict(set)
_docs: Path | None = None


def read_meta(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def english_key(src_uri: str) -> str:
    return TRANSLATION.sub(".md", src_uri)


def resolve(target) -> str:
    """Map a `related` entry to an English page path relative to docs/."""
    target = str(target).strip("/")
    return target if target.endswith(".md") else f"{target}/index.md"


def on_config(config, **kwargs):
    global _docs
    _docs = Path(config["docs_dir"])
    _related.clear()
    for path in _docs.rglob("*.md"):
        if TRANSLATION.search(path.name):
            continue
        meta, _ = read_meta(path)
        key = path.relative_to(_docs).as_posix()
        for target in meta.get("related") or []:
            target = resolve(target)
            if target == key or not (_docs / target).exists():
                continue  # reported by scripts/wiki_status.py --check
            _related[key].add(target)
            _related[target].add(key)
    return config


def title_of(target: str, lang: str) -> str:
    candidates = []
    if lang != "en":
        candidates.append(_docs / target.replace(".md", f".{lang}.md"))
    candidates.append(_docs / target)
    for path in candidates:
        if path.exists():
            meta, body = read_meta(path)
            if meta.get("title"):
                return str(meta["title"])
            m = HEADING.search(body)
            if m:
                return m.group(1).strip()
    return target


def on_page_markdown(markdown, page, config, files, **kwargs):
    key = english_key(page.file.src_uri)
    targets = _related.get(key)
    if not targets:
        return markdown
    lang = config["theme"].get("language", "en")
    lang = "zh-TW" if lang.lower().startswith("zh") else "en"
    here = posixpath.dirname(key)
    items = sorted((title_of(t, lang), posixpath.relpath(t, here or ".")) for t in targets)
    lines = [f"- [{title}]({href})" for title, href in items]
    return markdown.rstrip() + f"\n\n## {TITLES[lang]}\n\n" + "\n".join(lines) + "\n"
