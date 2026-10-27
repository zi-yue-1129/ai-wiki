#!/usr/bin/env python3
"""Report the state of every wiki page: completeness, staleness, translations.

Usage:
    python scripts/wiki_status.py --format page   > includes/status.md
    python scripts/wiki_status.py --format issue  > health-report.md
    python scripts/wiki_status.py --check          # exit 1 on structural problems

How a page's status is decided (English page = docs/**/<name>.md):
  1. `status:` in the page's front matter wins (stub / draft / complete).
  2. Otherwise a page containing the "Work in progress" admonition is a stub.
  3. Otherwise a page under DRAFT_WORDS words is a draft, else complete.

A page is stale when its last review (`last_reviewed:` front matter, falling back
to its last git commit) is older than STALE_DAYS.

A translation (<name>.zh-TW.md) is outdated when the English page has a newer
git commit than the translation, unless the translation's front matter sets
`translation_reviewed:` to a date on or after the English page's last commit.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
TRANSLATIONS = ["zh-TW"]
STUB_MARKER = "Work in progress"
DRAFT_WORDS = 400
STALE_DAYS = 365
STATUSES = ("stub", "draft", "complete")
STATUS_ICON = {"stub": "⬜", "draft": "🟨", "complete": "✅"}

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
CJK = re.compile(r"[㐀-鿿]")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\-]*")


@dataclass
class Page:
    path: Path  # relative to docs/
    section: str
    title: str
    status: str
    words: int
    last_commit: dt.date | None
    last_reviewed: dt.date | None
    translations: dict[str, str]  # lang -> "missing" | "up to date" | "outdated"

    @property
    def stale(self) -> bool:
        return self.last_reviewed is not None and (TODAY - self.last_reviewed).days > STALE_DAYS


TODAY = dt.date.today()


def git_date(path: Path) -> dt.date | None:
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", str(path)],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.strip()
    return dt.date.fromisoformat(out) if out else None


def read(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, text[m.end():]


def as_date(value) -> dt.date | None:
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return None
    return None


def word_count(body: str) -> int:
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    return len(WORD.findall(body)) + len(CJK.findall(body))


def is_translation(path: Path) -> bool:
    return any(path.name.endswith(f".{lang}.md") for lang in TRANSLATIONS)


def english_pages() -> list[Path]:
    return sorted(p for p in DOCS.rglob("*.md") if not is_translation(p))


def load_page(path: Path) -> Page:
    meta, body = read(path)
    rel = path.relative_to(DOCS)
    heading = re.search(r"^#\s+(.+)$", body, re.M)
    title = meta.get("title") or (heading.group(1).strip() if heading else rel.stem)

    words = word_count(body)
    status = meta.get("status")
    if status not in STATUSES:
        if STUB_MARKER in body:
            status = "stub"
        elif words < DRAFT_WORDS:
            status = "draft"
        else:
            status = "complete"

    last_commit = git_date(path)
    last_reviewed = as_date(meta.get("last_reviewed")) or last_commit

    translations = {}
    for lang in TRANSLATIONS:
        tpath = path.with_name(f"{path.stem}.{lang}.md")
        if not tpath.exists():
            translations[lang] = "missing"
            continue
        tmeta, _ = read(tpath)
        t_date = as_date(tmeta.get("translation_reviewed")) or git_date(tpath)
        if last_commit and t_date and t_date < last_commit:
            translations[lang] = "outdated"
        else:
            translations[lang] = "up to date"

    section = rel.parts[0] if len(rel.parts) > 1 else "home"
    return Page(rel, section, title, status, words, last_commit, last_reviewed, translations)


def nav_paths() -> set[str]:
    class Loader(yaml.SafeLoader):
        pass

    # mkdocs.yml uses !!python/... tags; treat them as opaque.
    Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda *a: None)
    cfg = yaml.load(MKDOCS_YML.read_text(encoding="utf-8"), Loader=Loader)
    found: set[str] = set()

    def walk(node):
        if isinstance(node, str):
            found.add(node)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)

    walk(cfg.get("nav", []))
    return found


def link(page: Page, base: str) -> str:
    return f"[{page.title}]({base}{page.path.as_posix()})"


def render(pages: list[Page], base: str, heading: str) -> str:
    out: list[str] = []
    by_section: dict[str, list[Page]] = defaultdict(list)
    for p in pages:
        by_section[p.section].append(p)

    counts = {s: sum(p.status == s for p in pages) for s in STATUSES}
    total = len(pages)
    done = counts["complete"]
    out.append(f"{heading} Overview\n")
    out.append(
        f"**{total}** English pages: {STATUS_ICON['complete']} {counts['complete']} complete · "
        f"{STATUS_ICON['draft']} {counts['draft']} draft · {STATUS_ICON['stub']} {counts['stub']} stub "
        f"(**{done * 100 // max(total, 1)}%** complete). Generated {TODAY.isoformat()}.\n"
    )

    out.append("| Section | Pages | Complete | Draft | Stub | " + " | ".join(f"{l} translated" for l in TRANSLATIONS) + " |")
    out.append("|---|---:|---:|---:|---:|" + "---:|" * len(TRANSLATIONS))
    for section in sorted(by_section):
        sp = by_section[section]
        row = [section, str(len(sp))] + [str(sum(p.status == s for p in sp)) for s in ("complete", "draft", "stub")]
        for lang in TRANSLATIONS:
            ok = sum(p.translations[lang] == "up to date" for p in sp)
            row.append(f"{ok}/{len(sp)}")
        out.append("| " + " | ".join(row) + " |")
    out.append("")

    def listing(title: str, items: list[Page], extra=lambda p: "") -> None:
        out.append(f"{heading} {title} ({len(items)})\n")
        if not items:
            out.append("None. 🎉\n")
            return
        for p in items:
            out.append(f"- {link(p, base)}{extra(p)}")
        out.append("")

    listing("Stubs waiting to be written", [p for p in pages if p.status == "stub"])
    listing("Drafts to expand", [p for p in pages if p.status == "draft"], lambda p: f" ({p.words} words)")
    listing(
        f"Not reviewed in over {STALE_DAYS} days",
        [p for p in pages if p.stale],
        lambda p: f" (last reviewed {p.last_reviewed})",
    )
    for lang in TRANSLATIONS:
        listing(
            f"{lang} translations behind the English page",
            [p for p in pages if p.translations[lang] == "outdated"],
        )
        listing(
            f"Written pages without a {lang} translation",
            [p for p in pages if p.translations[lang] == "missing" and p.status != "stub"],
        )
    return "\n".join(out)


def check(pages: list[Page]) -> int:
    problems: list[str] = []
    nav = nav_paths()
    for p in pages:
        # An empty nav means navigation is generated from the folder tree.
        if nav and p.path.as_posix() not in nav:
            problems.append(f"docs/{p.path.as_posix()}: not listed in mkdocs.yml nav")
    for t in sorted(DOCS.rglob("*.md")):
        if not is_translation(t):
            continue
        lang = next(l for l in TRANSLATIONS if t.name.endswith(f".{l}.md"))
        source = t.with_name(t.name[: -len(f".{lang}.md")] + ".md")
        if not source.exists():
            problems.append(f"{t.relative_to(ROOT)}: translation has no English page {source.name}")
    for p in pages:
        meta, _ = read(DOCS / p.path)
        if "status" in meta and meta["status"] not in STATUSES:
            problems.append(f"docs/{p.path.as_posix()}: status must be one of {', '.join(STATUSES)}")
        if "last_reviewed" in meta and as_date(meta["last_reviewed"]) is None:
            problems.append(f"docs/{p.path.as_posix()}: last_reviewed must be YYYY-MM-DD")
        related = meta.get("related", [])
        if not isinstance(related, list):
            problems.append(f"docs/{p.path.as_posix()}: related must be a list of paths")
            related = []
        own_topic = p.path.parent.as_posix() if p.path.name == "index.md" else None
        for target in related:
            target = str(target).strip("/")
            if target == own_topic:
                problems.append(f"docs/{p.path.as_posix()}: related lists the page itself")
            elif not (DOCS / target / "index.md").is_file():
                problems.append(
                    f"docs/{p.path.as_posix()}: related topic '{target}' not found "
                    "(use a topic folder relative to docs/, e.g. brain-mind/neuroai)"
                )
    for line in problems:
        print(f"::error::{line}" if "GITHUB_ACTIONS" in os.environ else line)
    print(f"{len(pages)} pages checked, {len(problems)} problem(s).")
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", choices=["page", "issue"], default="issue")
    parser.add_argument("--check", action="store_true", help="validate structure and exit")
    args = parser.parse_args()

    pages = [load_page(p) for p in english_pages()]
    if args.check:
        return check(pages)
    if args.format == "page":
        # Included into docs/reference/roadmap/index.md, so links are relative to that folder.
        print(render(pages, "../../", "###"))
    else:
        base = "https://github.com/zi-yue-1129/ai-wiki/blob/main/docs/"
        print("This report is regenerated weekly by the `maintenance` workflow.\n")
        print(render(pages, base, "##"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
