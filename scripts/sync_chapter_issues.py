#!/usr/bin/env python3
"""Keep chapter issues in step with the pages they track.

Usage:
    python scripts/sync_chapter_issues.py [--dry-run] [--issues FILE]

A chapter issue names its page on a line such as "Planned page: `docs/...`",
"Existing draft: `docs/...`" or "Existing stub: `docs/...`". The page's status,
as wiki_status.py reads it, decides what happens:

- A complete page with an open chapter issue: the issue is closed.
- A stub or draft page with no chapter issue at all: an issue is opened for it.
  Section overviews, and pages marked `references: not-required`, are skipped.

Issues are never reopened, and a planned page that does not exist yet stays open.
Writes go through the `gh` CLI, which reads GH_TOKEN (GitHub Actions provides it).
--issues FILE reads the issue list from a JSON file instead of GitHub, for testing.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import wiki_status as ws

PAGE_LINE = re.compile(r"^(?:- )?(?:Planned page|Existing draft|Existing stub):\s*`(docs/[^`]+)`", re.M)
CHAPTER_LABEL = "chapter"
OPEN_TITLE = {"draft": "Expand draft: {title}", "stub": "Write stub: {title}"}
OPEN_BODY = {
    "draft": "Existing draft: `{key}`\n\nOpened automatically: this page is a draft with no chapter issue. "
    "Expand it to a complete page, then merge a PR whose description says `Closes #<this issue>`.",
    "stub": "Existing stub: `{key}`\n\nOpened automatically: this page is a stub with no chapter issue. "
    "Write it, then merge a PR whose description says `Closes #<this issue>`.",
}


def list_issues(path: str | None) -> list[dict]:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    out = subprocess.run(
        ["gh", "issue", "list", "--label", CHAPTER_LABEL, "--state", "all", "--limit", "1000",
         "--json", "number,state,title,body"],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def page_key(path: Path) -> str:
    return f"docs/{path.relative_to(ws.DOCS).as_posix()}"


def is_overview(path: Path) -> bool:
    """Section overviews and topic folders that list other pages are not chapters."""
    rel = path.relative_to(ws.DOCS)
    if rel.name != "index.md":
        return False
    if len(rel.parts) <= 2:
        return True
    return any(child.is_dir() and (child / "index.md").exists() for child in path.parent.iterdir())


def plan(issues: list[dict]) -> tuple[list[tuple[int, str]], list[dict]]:
    linked: dict[str, list[dict]] = {}
    for issue in issues:
        match = PAGE_LINE.search(issue.get("body") or "")
        if match:
            linked.setdefault(match.group(1), []).append(issue)

    to_close: list[tuple[int, str]] = []
    to_open: list[dict] = []
    for path in ws.english_pages():
        key = page_key(path)
        page = ws.load_page(path)
        issues_for_page = linked.get(key, [])

        if page.status == "complete":
            for issue in issues_for_page:
                if issue["state"] == "OPEN":
                    to_close.append((issue["number"], f"Closed automatically: `{key}` is complete."))
        elif page.status in OPEN_BODY and not issues_for_page and not is_overview(path):
            meta, _ = ws.read(path)
            if meta.get("references") == "not-required":
                continue
            to_open.append({
                "key": key,
                "title": OPEN_TITLE[page.status].format(title=page.title),
                "body": OPEN_BODY[page.status].format(key=key),
                "labels": [CHAPTER_LABEL, f"section:{page.section}"],
            })
    return to_close, to_open


def apply(to_close: list[tuple[int, str]], to_open: list[dict]) -> None:
    labels = sorted({label for item in to_open for label in item["labels"] if label.startswith("section:")})
    for label in labels:
        subprocess.run(["gh", "label", "create", label, "--force", "--color", "ededed"], check=True)
    for item in to_open:
        subprocess.run(
            ["gh", "issue", "create", "--title", item["title"], "--body-file", "-",
             *sum((["--label", label] for label in item["labels"]), [])],
            input=item["body"], text=True, check=True,
        )
    for number, comment in to_close:
        subprocess.run(["gh", "issue", "close", str(number), "--comment", comment], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="print what would change and exit")
    parser.add_argument("--issues", metavar="FILE", help="read issues from a JSON file instead of GitHub")
    args = parser.parse_args()

    to_close, to_open = plan(list_issues(args.issues))
    for number, _ in to_close:
        print(f"close #{number}")
    for item in to_open:
        print(f"open  {item['key']}: {item['title']}")
    print(f"{len(to_close)} to close, {len(to_open)} to open.")
    if not args.dry_run:
        apply(to_close, to_open)
    return 0


if __name__ == "__main__":
    sys.exit(main())
