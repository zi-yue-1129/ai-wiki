"""Semantic audit of the GitHub-visible selective-classification fallback panels.

The static SVGs are independent teaching surfaces: each displayed rate must
agree with its own check/cross glyphs and acceptance mask, without executing
SVG animation, scripts, or a built-site player.
"""
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path("docs/assets/concept-animations")
NS = "{http://www.w3.org/2000/svg}"
GREEN, RED = "#16845b", "#cc594c"


def panel_cells(root, headings, *, cell_height):
    """Read panels in SVG document order, binding every glyph to its cell."""
    panels = {}
    active = None
    last_cell = None
    for node in root:
        if node.tag == NS + "text":
            label = "".join(node.itertext()).strip()
            if label in headings:
                assert label not in panels, label
                active = label
                panels[label] = {"labels": [], "cells": []}
            elif active is not None:
                panels[active]["labels"].append(label)
        elif (active is not None and node.tag == NS + "rect"
              and node.get("height") == str(cell_height)):
            last_cell = node
        elif active is not None and node.tag == NS + "g":
            path = node.find(NS + "path")
            if path is None:
                continue
            assert last_cell is not None, "glyph not bound to a cell"
            assert path.get("stroke") in (GREEN, RED), "unknown correctness icon"
            opacity = float(node.get("opacity", "1"))
            assert opacity in (1.0, 0.3, 0.25), "unexpected rejection opacity"
            panels[active]["cells"].append((
                path.get("stroke") == GREEN, opacity == 1.0,
                last_cell.get("fill"),
            ))
            last_cell = None
    assert set(panels) == set(headings), (panels.keys(), headings)
    return panels


def still(stem):
    root = ET.parse(ASSETS / (stem + "-still.svg")).getroot()
    assert root.get("viewBox") == "0 0 640 360"
    assert root.find(NS + "title") is not None
    assert root.find(NS + "desc") is not None
    assert not any(n.tag in (NS + "animate", NS + "script", NS + "foreignObject")
                   for n in root.iter())
    return root


# Topic 1: fixed six-case ranking, three distinct acceptance cutoffs.
truth = (True, True, False, True, False, True)
coverage = panel_cells(
    still("accuracy-selective-coverage"), ("TOP 2", "TOP 4", "TOP 6"),
    cell_height=44,
)
for k in (2, 4, 6):
    panel = coverage[f"TOP {k}"]
    cells = panel["cells"]
    assert len(cells) == 6
    assert tuple(good for good, _, _ in cells) == truth
    accepted = tuple(keep for _, keep, _ in cells)
    assert accepted == tuple(i < k for i in range(6))
    for _, keep, fill in cells:
        assert fill == ("#e8f6f2" if keep else "#f2f4f8")
    hits = sum(good and keep for good, keep, _ in cells)
    expected = {
        f"{sum(accepted)}/6 covered",
        f"Acc  {hits}/{sum(accepted)}",
        f"Risk  {float(Fraction(sum(accepted)-hits, sum(accepted))):.3f}",
    }
    assert expected <= set(panel["labels"]), (k, expected, panel["labels"])

# Topic 2: class-specific rejection can hide behind perfect retained accuracy.
truth = (True, False, False, True, True, True, True, True)
by_class = panel_cells(
    still("accuracy-selective-class-coverage"), ("ALL", "SELECTIVE"),
    cell_height=40,
)
for name, mask in (
    ("ALL", (True,) * 8),
    ("SELECTIVE", (True, False, False, False, True, True, True, True)),
):
    panel = by_class[name]
    cells = panel["cells"]
    assert len(cells) == 8
    assert tuple(good for good, _, _ in cells) == truth
    accepted = tuple(keep for _, keep, _ in cells)
    assert accepted == mask
    for _, keep, fill in cells:
        assert fill == ("#e7f5f1" if keep else "#eef2f6")
    hits = sum(good and keep for good, keep, _ in cells)
    expected = {
        f"{hits}/{sum(accepted)} ACC",
        f"POS {sum(accepted[:4])}/4   ·   NEG {sum(accepted[4:])}/4",
    }
    assert expected <= set(panel["labels"]), (name, expected, panel["labels"])

assert Fraction(1, 4) < Fraction(4, 4)
print("Selective static fallback glyph, mask, and arithmetic bindings OK")
