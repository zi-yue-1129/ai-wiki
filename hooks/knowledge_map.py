"""MkDocs hook: draw the knowledge map from the wiki's own pages.

The map is built at site build time, so it always matches the current content. It opens on the
sections and drills down on click, so no screen has to show every topic at once:
- level 1: one circle per section, lines weighted by the links between sections;
- level 2: the groups inside a section (the folder two levels down, e.g. theory/paradigms);
- level 3: the topics of one group, pulled into clusters by their subfolder.

A node's colour is its section, and a hollow circle marks a draft page. A line joins two topics that
link to each other, either through `related:` front matter (see hooks/related.py) or through a link in
the text. The layout is a small deterministic force-directed pass, so the same content always gives the
same picture. The page carries the layout as JSON; docs/javascripts/knowledge-map.js adds zoom, pan,
full screen, drill-down and search.

A page marks where a map belongs with one of these lines, on its own:

    <!-- knowledge-map:overview -->   the explorer, as used on the home page
    <!-- knowledge-map:full -->       the explorer, as used on the knowledge map page
"""

from __future__ import annotations

import html
import json
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

SECTION_FILL = {  # in reading order; a section keeps its colour on every level of the map
    "theory": "#5c6bc0",
    "brain-mind": "#00897b",
    "engineering": "#ef6c00",
    "applications": "#8e24aa",
    "society": "#6d4c41",
}
FALLBACK_FILL = "#607d8b"
LABEL_WIDTH = {"en": 22, "zh-TW": 11}  # characters per label line; CJK text has no spaces to wrap at
ICONS = {
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "fit": '<circle cx="12" cy="12" r="6"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/>',
    "full": ('<path class="km-enter" d="M9 4H4v5M15 4h5v5M20 15v5h-5M9 20H4v-5"/>'
             '<path class="km-exit" d="M4 9h5V4M15 4v5h5M15 20v-5h5M4 15h5v5"/>'),  # one button, two states
}
TEXT = {
    "en": {
        "legend": "Click a circle to open it. Drag to pan, scroll or pinch to zoom. Lines join pages that link to each other.",
        "colour": "Colour shows the section.",
        "complete": "complete",
        "draft": "draft",
        "all": "All sections",
        "topics": "topics",
        "links": "links",
        "open": "Open page",
        "clear": "Clear selection",
        "search": "Search topics",
        "no_match": "No matching topics",
        "zoom_in": "Zoom in",
        "zoom_out": "Zoom out",
        "fit": "Fit to screen",
        "full": "Full screen",
        "exit": "Exit full screen",
        "crumbs": "Map location",
        "aria": "Knowledge map",
    },
    "zh-TW": {
        "legend": "點選圓圈即可開啟。拖曳可平移，滾輪或雙指捏合可縮放。連線表示兩個頁面彼此連結。",
        "colour": "顏色表示領域。",
        "complete": "完成",
        "draft": "草稿",
        "all": "所有領域",
        "topics": "個主題",
        "links": "條連結",
        "open": "開啟頁面",
        "clear": "取消選取",
        "search": "搜尋主題",
        "no_match": "沒有符合的主題",
        "zoom_in": "放大",
        "zoom_out": "縮小",
        "fit": "符合畫面",
        "full": "全螢幕",
        "exit": "結束全螢幕",
        "crumbs": "地圖位置",
        "aria": "知識地圖",
    },
}


@dataclass
class Graph:
    topics: dict[str, dict] = field(default_factory=dict)  # docs-relative path -> info
    sections: dict[str, str] = field(default_factory=dict)  # section -> docs-relative index path
    pairs: set[tuple[str, str]] = field(default_factory=set)


_graph: Graph | None = None
_explorers: dict[str, Explorer] = {}


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
            graph.topics[rel] = {"status": wiki_status.load_page(path).status}

    for rel in graph.topics:
        meta, body = wiki_status.read(docs / rel)
        for target in linked_pages(rel, meta, body):
            if target in graph.topics:
                graph.pairs.add(tuple(sorted((rel, target))))
    return graph


def section_of(rel: str) -> str:
    return rel.split("/")[0]


def group_of(rel: str) -> str:
    """The folder two levels down, which holds one group of topics (theory/paradigms)."""
    return "/".join(rel.split("/")[:2])


def sub_of(rel: str) -> str:
    """The folder under a group that holds a topic, or "" when the topic sits directly in the group."""
    parts = rel.split("/")
    return "/".join(parts[:3]) if len(parts) > 3 else ""


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


def canvas(count: int) -> float:
    """Side of a view's square canvas. It grows with the node count, so the spacing stays even."""
    return max(560.0, 260 + 46 * math.sqrt(count))


def label_lines(title: str, width: int) -> list[str]:
    lines = textwrap.wrap(title, width, break_long_words=True) or [title]
    if len(lines) > 3:
        lines = lines[:3]
        lines[2] = lines[2][: width - 1] + "…"
    return lines


class Explorer:
    """Lays out every view of the map for one language. The layout does not depend on the page, so it is
    worked out once per build; each page then adds its own links."""

    def __init__(self, graph: Graph, docs: Path, lang: str):
        self.graph, self.docs, self.lang = graph, docs, lang
        self.text = TEXT[lang]
        self.width = LABEL_WIDTH[lang]
        self.sections = [s for s in SECTION_FILL if s in graph.sections]
        self.sections += sorted(s for s in graph.sections if s not in SECTION_FILL)
        self.members: dict[str, list[str]] = {}  # group -> its topics
        for rel in sorted(graph.topics):
            self.members.setdefault(group_of(rel), []).append(rel)
        self.groups = {s: [g for g in self.members if section_of(g) == s] for s in self.sections}
        self.views: dict[str, dict] = {"": self.root_view()}
        for s in self.sections:
            self.views[s] = self.section_view(s)
            for g in self.groups[s]:
                self.views[g] = self.group_view(g)
        self.search = [
            {"t": node["title"], "v": key, "i": i, "s": node["section"]}
            for key, view in self.views.items()
            for i, node in enumerate(view["nodes"])
        ]

    def title(self, rel: str) -> str:
        return title_in(self.docs, rel, self.lang)

    def folder(self, folder: str) -> str:
        """Title of a group or subfolder: its index page's title, or else its folder name."""
        index = f"{folder}/index.md"
        if index in self.graph.topics:
            return self.title(index)
        return folder.split("/")[-1].replace("-", " ").capitalize()

    def page_of(self, folder: str) -> str | None:
        index = f"{folder}/index.md"
        return index if index in self.graph.topics else None

    def pair_weights(self, key, scope=None) -> Counter:
        """Links between two different keys (sections, groups or topics), counted once per topic pair."""
        weights: Counter = Counter()
        for a, b in sorted(self.graph.pairs):
            ka, kb = key(a), key(b)
            if ka != kb and (scope is None or (ka in scope and kb in scope)):
                weights[tuple(sorted((ka, kb)))] += 1
        return weights

    def node(self, kind, key, title, xy, r, section, page, **extra) -> dict:
        return {"kind": kind, "key": key, "title": title, "lines": label_lines(title, self.width),
                "x": xy[0], "y": xy[1], "r": r, "fill": SECTION_FILL.get(section, FALLBACK_FILL),
                "section": section, "page": page, **extra}

    def root_view(self) -> dict:
        counts = Counter(section_of(rel) for rel in self.graph.topics)
        weights = self.pair_weights(section_of)
        side = canvas(len(self.sections))
        anchors = dict(zip(self.sections, circle(len(self.sections), side / 2, side / 2, side * 0.34)))
        pos = layout(self.sections, {p: min(w, 4) / 4 for p, w in weights.items()}, anchors, side, side, 0.05)
        nodes = [self.node("section", s, self.title(self.graph.sections[s]), pos[s],
                           20 + 3 * math.sqrt(counts[s]), s, self.graph.sections[s], count=counts[s], view=s)
                 for s in self.sections]
        index = {s: i for i, s in enumerate(self.sections)}
        return {"title": self.text["all"], "parent": None, "page": None, "w": side, "h": side,
                "nodes": nodes, "edges": self.edges(weights, index), "clusters": []}

    def section_view(self, section: str) -> dict:
        groups = self.groups[section]
        side = canvas(len(groups))
        anchors = dict(zip(groups, circle(len(groups), side / 2, side / 2, side * 0.36)))
        weights = self.pair_weights(group_of, scope=set(groups))
        pos = layout(groups, {p: min(w, 3) / 3 for p, w in weights.items()}, anchors, side, side, 0.04, spread=1.1)
        nodes = [self.node("group", g, self.folder(g), pos[g], 10 + 2.4 * math.sqrt(len(self.members[g])),
                           section, self.page_of(g), count=len(self.members[g]), view=g)
                 for g in groups]
        index = {g: i for i, g in enumerate(groups)}
        return {"title": self.title(self.graph.sections[section]), "parent": "",
                "page": self.graph.sections[section], "w": side, "h": side,
                "nodes": nodes, "edges": self.edges(weights, index), "clusters": []}

    def group_view(self, group: str) -> dict:
        topics = self.members[group]
        section = section_of(group)
        side = canvas(len(topics))
        centre = side / 2
        subs = sorted({sub_of(rel) for rel in topics} - {""})
        ring = circle(len(subs), centre, centre, side * 0.2) if len(subs) > 1 else [(centre, centre)] * len(subs)
        sub_at = dict(zip(subs, ring))
        anchors = {rel: sub_at.get(sub_of(rel), (centre, centre)) for rel in topics}
        weights = self.pair_weights(lambda rel: rel, scope=set(topics))
        pos = layout(topics, {p: 1.0 for p in weights}, anchors, side, side, 0.16, spread=0.75)
        nodes = [self.node("topic", rel, self.title(rel), pos[rel], 7.5, section, rel,
                           status=self.graph.topics[rel]["status"])
                 for rel in topics]
        clusters = []
        for sub in subs:
            xs = [pos[rel] for rel in topics if sub_of(rel) == sub]
            cx = sum(p[0] for p in xs) / len(xs)
            cy = sum(p[1] for p in xs) / len(xs)
            clusters.append({"x": cx, "y": cy, "text": self.folder(sub)})
        index = {rel: i for i, rel in enumerate(topics)}
        return {"title": self.folder(group), "parent": section, "page": self.page_of(group),
                "w": side, "h": side, "nodes": nodes, "edges": self.edges(weights, index), "clusters": clusters}

    @staticmethod
    def edges(weights: Counter, index: dict) -> list[list]:
        return [{"a": index[a], "b": index[b], "w": w} for (a, b), w in sorted(weights.items())]

    def href(self, rel: str, here: str, files) -> str | None:
        file = files.get_file_from_path(rel)
        if file is None:
            return None
        return posixpath.relpath(file.url or ".", here) + "/"

    def public_view(self, view: dict, here: str, files) -> dict:
        """The view as the page's script reads it: positions rounded, page paths made relative to the page."""
        nodes = [{
            "kind": n["kind"], "title": n["title"], "lines": n["lines"], "section": n["section"],
            "x": round(n["x"], 1), "y": round(n["y"], 1), "r": round(n["r"], 1), "fill": n["fill"],
            "status": n.get("status"), "view": n.get("view"),
            "href": self.href(n["page"], here, files) if n["page"] else None,
        } for n in view["nodes"]]
        clusters = [{"x": round(c["x"], 1), "y": round(c["y"], 1), "text": c["text"]} for c in view["clusters"]]
        return {"title": view["title"], "parent": view["parent"], "w": view["w"], "h": view["h"],
                "href": self.href(view["page"], here, files) if view["page"] else None,
                "nodes": nodes, "edges": view["edges"], "clusters": clusters}

    def markup(self, here: str, files) -> str:
        """The whole explorer for one page, on a single line so Markdown leaves it alone."""
        t = self.text
        data = {
            "text": t,
            "titles": {s: self.title(self.graph.sections[s]) for s in self.sections},
            "views": {key: self.public_view(view, here, files) for key, view in self.views.items()},
            "search": self.search,
        }
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        chips = "".join(
            f'<span class="km-chip" style="--km-c:{SECTION_FILL.get(s, FALLBACK_FILL)}">'
            f'{html.escape(self.title(self.graph.sections[s]))}</span>'
            for s in self.sections
        )
        legend = (f'<div class="km-legend"><p>{t["legend"]} {t["colour"]}</p>{chips}'
                  f'<span class="km-chip km-solid">{t["complete"]}</span>'
                  f'<span class="km-chip km-hollow">{t["draft"]}</span></div>')
        buttons = [("km-zoom-out", "minus", t["zoom_out"]), ("km-zoom-in", "plus", t["zoom_in"]),
                   ("km-fit", "fit", t["fit"]), ("km-full", "full", t["full"])]
        toolbar = (f'<div class="km-toolbar"><nav class="km-crumbs km-js" aria-label="{t["crumbs"]}"></nav>'
                   f'<div class="km-tools">'
                   f'<div class="km-search km-js"><input type="search" class="km-search-input" '
                   f'placeholder="{t["search"]}" aria-label="{t["search"]}" autocomplete="off">'
                   f'<ul class="km-results" hidden></ul></div>'
                   + "".join(
                       f'<button type="button" class="km-icon km-js {cls}" aria-label="{label}" title="{label}">'
                       f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg></button>'
                       for cls, name, label in buttons)
                   + '</div></div>')
        stage = '<div class="km-stage km-js"></div>'
        info = '<div class="km-info km-js" hidden></div>'
        return (f'<div class="km-explorer" role="region" aria-label="{t["aria"]}">'
                f'{toolbar}{stage}{info}{legend}'
                f'<script type="application/json" class="km-data">{payload}</script>'
                '</div>')


def on_config(config, **kwargs):
    global _graph
    _graph = None
    _explorers.clear()
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    if not MARKER.search(markdown):
        return markdown
    global _graph
    docs = Path(config["docs_dir"])
    if _graph is None:
        _graph = build_graph(docs)
    lang = "zh-TW" if config["theme"].get("language", "en").lower().startswith("zh") else "en"
    if lang not in _explorers:
        _explorers[lang] = Explorer(_graph, docs, lang)
    explorer = _explorers[lang]
    return MARKER.sub(lambda m: f"\n{explorer.markup(page.url or '.', files)}\n", markdown)
