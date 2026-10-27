"""MkDocs hook: draw the knowledge map from the wiki's own pages.

The map is generated at build time, so it always matches the current content:
- a node is a topic page, grouped under its section (section overviews are not nodes);
- a line joins two topics that link to each other, either through `related:` front
  matter (see hooks/related.py) or through a link in the text;
- a node's colour is its status, as decided by scripts/wiki_status.py.

A page marks where a map belongs with one of these lines, on its own:

    <!-- knowledge-map:overview -->   one node per section, lines weighted by link count
    <!-- knowledge-map:full -->       every topic, then one map per section

Layout is a small deterministic force-directed pass, so the same content always
produces the same picture.
"""

from __future__ import annotations

import html
import math
import posixpath
import random
import re
import sys
import textwrap
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import wiki_status  # noqa: E402  (the status rules live with the coverage report)

MARKER = re.compile(r"^<!-- knowledge-map:(overview|full) -->\s*$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#\s+(.+)$", re.M)
EXCLUDED_SECTIONS = {"start", "reference", "knowledge-map"}  # onboarding, meta and this map are not topics
ITERATIONS = 320
SEED = 7

STATUS_FILL = {"complete": "#43a047", "draft": "#f9a825", "stub": "#9e9e9e"}
STATUS_NAME = {
    "en": {"complete": "complete", "draft": "draft", "stub": "stub"},
    "zh-TW": {"complete": "完成", "draft": "草稿", "stub": "待撰寫"},
}
TEXT = {
    "en": {
        "legend": "Lines join pages that link to each other, through a related topic or a link in the text.",
        "colour": "Colour shows page status.",
        "sections": "By section",
        "links": "links",
        "topics": "topics",
        "section_map": "{title} ({count} topics)",
        "aria": "Knowledge map",
    },
    "zh-TW": {
        "legend": "連線表示兩個頁面彼此連結，來自相關主題或內文中的連結。",
        "colour": "顏色表示頁面狀態。",
        "sections": "依領域分開檢視",
        "links": "條連結",
        "topics": "個主題",
        "section_map": "{title}（{count} 個主題）",
        "aria": "知識地圖",
    },
}
SECTION_FILL = "#5c6bc0"
SVG_STYLE = (
    ".km-line{stroke:var(--md-default-fg-color--lighter);fill:none}"
    ".km-node{stroke:var(--md-default-bg-color);stroke-width:2}"
    ".km-label{fill:var(--md-default-fg-color);font:12px/1.3 var(--md-text-font-family,sans-serif);text-anchor:middle}"
    ".km-section{fill:var(--md-default-fg-color--light);font:600 20px/1.2 var(--md-text-font-family,sans-serif);text-anchor:middle}"
)


@dataclass
class Graph:
    topics: dict[str, dict] = field(default_factory=dict)  # docs-relative path -> info
    sections: dict[str, str] = field(default_factory=dict)  # section -> docs-relative index path
    pairs: set[tuple[str, str]] = field(default_factory=set)


_graph: Graph | None = None


def resolve_related(target: str) -> str:
    target = target.strip("/")
    return target if target.endswith(".md") else f"{target}/index.md"


def linked_pages(rel: str, meta: dict, body: str) -> set[str]:
    """Pages this page points to, from `related:` entries and in-text links."""
    here = posixpath.dirname(rel)
    found = {resolve_related(str(ref)) for ref in meta.get("related") or []}
    for href in LINK.findall(body):
        if "://" in href or href.startswith(("#", "mailto:")):
            continue
        target = href.split("#")[0]
        if not target.endswith(".md"):
            target = target.rstrip("/") + "/index.md"
        found.add(posixpath.normpath(posixpath.join(here, target)))
    found.discard(rel)
    return found


def build_graph(docs: Path) -> Graph:
    graph = Graph()
    for path in sorted(docs.rglob("*.md")):
        if wiki_status.is_translation(path):
            continue
        rel = path.relative_to(docs).as_posix()
        parts = rel.split("/")
        if parts[0] in EXCLUDED_SECTIONS:
            continue
        if len(parts) == 2 and parts[1] == "index.md":
            graph.sections[parts[0]] = rel
        elif len(parts) > 2:
            graph.topics[rel] = {"section": parts[0], "status": wiki_status.load_page(path).status}

    for rel in graph.topics:
        meta, body = wiki_status.read(docs / rel)
        for target in linked_pages(rel, meta, body):
            if target in graph.topics:
                graph.pairs.add(tuple(sorted((rel, target))))
    return graph


def title_in(docs: Path, rel: str, lang: str) -> str:
    path = docs / rel
    if lang != "en":
        localized = path.with_name(f"{path.stem}.{lang}.md")
        if localized.exists():
            path = localized
    meta, body = wiki_status.read(path)
    if meta.get("title"):
        return str(meta["title"])
    heading = HEADING.search(body)
    return heading.group(1).strip() if heading else path.stem


def layout(keys, weights, anchors, width, height, gravity, spread=0.9):
    """Fruchterman-Reingold: nodes repel, linked nodes attract, and each drifts to its anchor."""
    rng = random.Random(SEED)
    pos = {k: [anchors[k][0] + rng.uniform(-30, 30), anchors[k][1] + rng.uniform(-30, 30)] for k in keys}
    if len(keys) < 2:
        return pos
    spacing = spread * math.sqrt(width * height / len(keys))
    margin = 60
    for step in range(ITERATIONS):
        disp = {k: [0.0, 0.0] for k in keys}
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 0.01
                f = spacing * spacing / d
                disp[a][0] += dx / d * f
                disp[a][1] += dy / d * f
                disp[b][0] -= dx / d * f
                disp[b][1] -= dy / d * f
        for (a, b), w in weights.items():
            dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 0.01
            f = d * d / spacing * w
            disp[a][0] -= dx / d * f
            disp[a][1] -= dy / d * f
            disp[b][0] += dx / d * f
            disp[b][1] += dy / d * f
        temp = width / 12 * (1 - step / ITERATIONS) + 1
        for k in keys:
            disp[k][0] += (anchors[k][0] - pos[k][0]) * gravity
            disp[k][1] += (anchors[k][1] - pos[k][1]) * gravity
            d = math.hypot(*disp[k]) or 0.01
            move = min(d, temp)
            pos[k][0] = min(width - margin, max(margin, pos[k][0] + disp[k][0] / d * move))
            pos[k][1] = min(height - margin, max(margin, pos[k][1] + disp[k][1] / d * move))
    return pos


def circle(n: int, cx: float, cy: float, radius: float) -> list[tuple[float, float]]:
    return [(cx + radius * math.cos(2 * math.pi * i / n - math.pi / 2),
             cy + radius * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]


def node(x: float, y: float, r: float, fill: str, title: str, lines: list[str], href: str | None) -> str:
    labels = "".join(
        f'<text class="km-label" x="{x:.1f}" y="{y + r + 15 + i * 15:.1f}">{html.escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    body = (f'<title>{html.escape(title)}</title>'
            f'<circle class="km-node" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"/>{labels}')
    if href:
        body = f'<a href="{html.escape(href)}">{body}</a>'
    return f"<g>{body}</g>"


def svg(width: int, height: int, body: str, label: str, style: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" '
            f'aria-label="{html.escape(label)}" style="{style}"><style>{SVG_STYLE}</style>{body}</svg>')


class Renderer:
    """Turns the graph into HTML for one page, with links relative to that page."""

    def __init__(self, graph: Graph, docs: Path, lang: str, page_url: str, files):
        self.graph, self.docs, self.lang, self.files = graph, docs, lang, files
        self.here = page_url or "."
        self.text = TEXT[lang]

    def href(self, rel: str) -> str | None:
        file = self.files.get_file_from_path(rel)
        if file is None:
            return None
        return posixpath.relpath(file.url or ".", self.here) + "/"

    def legend(self) -> str:
        swatches = " ".join(
            f'<span style="color:{STATUS_FILL[s]}">●</span> {STATUS_NAME[self.lang][s]}' for s in STATUS_FILL
        )
        return f'<p>{self.text["legend"]} {self.text["colour"]} {swatches}</p>'

    def overview(self) -> str:
        width, height = 900, 540
        counts = Counter(t["section"] for t in self.graph.topics.values())
        sections = sorted(self.graph.sections)
        anchors = dict(zip(sections, circle(len(sections), width / 2, height / 2 - 10, 190)))
        weights: Counter = Counter()
        for a, b in self.graph.pairs:
            sa, sb = self.graph.topics[a]["section"], self.graph.topics[b]["section"]
            if sa != sb:
                weights[tuple(sorted((sa, sb)))] += 1
        pos = layout(sections, {k: min(w, 4) / 4 for k, w in weights.items()}, anchors, width, height, 0.05)

        lines = []
        for (sa, sb), w in weights.items():
            (x1, y1), (x2, y2) = pos[sa], pos[sb]
            tip = f"{self.title(sa)} ↔ {self.title(sb)}: {w} {self.text['links']}"
            lines.append(f'<line class="km-line" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                         f'stroke-width="{1 + 1.2 * w:.1f}"><title>{html.escape(tip)}</title></line>')
        nodes = []
        for s in sections:
            r = 16 + 4 * math.sqrt(counts[s])
            tip = f"{self.title(s)} ({counts[s]} {self.text['topics']})"
            nodes.append(node(*pos[s], r, SECTION_FILL, tip, textwrap.wrap(self.title(s), 18)[:3],
                              self.href(self.graph.sections[s])))
        return svg(width, height, "".join(lines) + "".join(nodes), self.text["aria"], "width:100%;height:auto")

    def full(self) -> str:
        sections = sorted(self.graph.sections)
        width, height = 1600, 1100
        anchors_by_section = dict(zip(sections, circle(len(sections), width / 2, height / 2, 390)))
        keys = list(self.graph.topics)
        anchors = {k: anchors_by_section[self.graph.topics[k]["section"]] for k in keys}
        pos = layout(keys, self.weights(keys), anchors, width, height, 0.04, spread=1.4)
        body = self.lines(keys, pos)
        for s in sections:
            x, y = anchors_by_section[s]
            body += f'<text class="km-section" x="{x:.1f}" y="{y:.1f}">{html.escape(self.title(s))}</text>'
        body += "".join(self.topic_node(k, pos[k]) for k in keys)
        out = [f'<div style="overflow-x:auto">{svg(width, height, body, self.text["aria"], "width:100%;min-width:1000px;height:auto")}</div>',
               self.legend()]
        out.extend(self.section_map(s) for s in sections)
        return "".join(out)

    def section_map(self, section: str) -> str:
        width, height = 1000, 640
        keys = [k for k, t in self.graph.topics.items() if t["section"] == section]
        center = {k: (width / 2, height / 2) for k in keys}
        pos = layout(keys, self.weights(keys), center, width, height, 0.02)
        body = self.lines(keys, pos) + "".join(self.topic_node(k, pos[k]) for k in keys)
        summary = self.text["section_map"].format(title=html.escape(self.title(section)), count=len(keys))
        map_svg = svg(width, height, body, self.title(section), "width:100%;min-width:760px;height:auto")
        return (f'<details><summary>{summary}</summary>'
                f'<div style="overflow-x:auto">{map_svg}</div></details>')

    def weights(self, keys: list[str]) -> dict[tuple[str, str], float]:
        chosen = set(keys)
        return {p: 1.0 for p in self.graph.pairs if p[0] in chosen and p[1] in chosen}

    def lines(self, keys: list[str], pos: dict) -> str:
        chosen = set(keys)
        out = []
        for a, b in sorted(self.graph.pairs):
            if a in chosen and b in chosen:
                (x1, y1), (x2, y2) = pos[a], pos[b]
                out.append(f'<line class="km-line" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="1"/>')
        return "".join(out)

    def topic_node(self, key: str, xy) -> str:
        info = self.graph.topics[key]
        x, y = xy
        title = self.title(key)
        status = STATUS_NAME[self.lang][info["status"]]
        lines = textwrap.wrap(title, 22)[:3]
        return node(x, y, 9, STATUS_FILL[info["status"]], f"{title} ({status})", lines, self.href(key))

    def title(self, key: str) -> str:
        """Title of a topic page, or of a section given by its name."""
        return title_in(self.docs, self.graph.sections.get(key, key), self.lang)


def on_config(config, **kwargs):
    global _graph
    _graph = None
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    if not MARKER.search(markdown):
        return markdown
    global _graph
    docs = Path(config["docs_dir"])
    if _graph is None:
        _graph = build_graph(docs)
    lang = "zh-TW" if config["theme"].get("language", "en").lower().startswith("zh") else "en"
    renderer = Renderer(_graph, docs, lang, page.url, files)

    def replace(match):
        if match.group(1) == "overview":
            return renderer.overview()
        return renderer.full()

    return MARKER.sub(lambda m: f"\n{replace(m)}\n", markdown)
