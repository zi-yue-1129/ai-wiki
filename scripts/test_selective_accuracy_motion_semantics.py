"""Synthetic selective-classification arithmetic and SVG stage contracts."""
from fractions import Fraction
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ASSETS = Path("docs/assets/concept-animations")
PAGES = Path("docs/theory/evaluation/metrics/classification")
outcomes = [1, 1, 0, 1, 0, 1]
for k, hits in ((2, 2), (4, 3), (6, 4)):
    assert sum(outcomes[:k]) == hits
    assert Fraction(hits,k) + Fraction(k-hits,k) == 1
assert [Fraction(sum(outcomes[:k]),k) for k in (2,4,6)] == [1,Fraction(3,4),Fraction(2,3)]
positive = [1,0,0,1]
negative = [1,1,1,1]
assert sum(positive + negative) == 6
assert sum([positive[0]] + negative) == 5
assert Fraction(1,4) != Fraction(4,4)
for stem, n, duration in (
    ("accuracy-selective-coverage",3,"12s"),
    ("accuracy-selective-class-coverage",2,"8s"),
):
    motion=ASSETS/(stem+"-motion.svg")
    still=ASSETS/(stem+"-still.svg")
    ns="{http://www.w3.org/2000/svg}"
    m=ET.parse(motion).getroot()
    s=ET.parse(still).getroot()
    assert m.attrib["viewBox"] == s.attrib["viewBox"] == "0 0 640 360"
    stages=list(m.iter(ns+"animate"))
    assert len(stages) == n
    for a in stages:
        assert a.get("dur")==duration
        assert a.get("calcMode")=="discrete"
        assert a.get("repeatCount")=="indefinite"
        times=list(map(float,a.get("keyTimes").split(";")))
        assert len(times)==n+1 and times[0]==0 and times[-1]==1
        assert all(x<y for x,y in zip(times,times[1:]))
    assert not list(s.iter(ns+"animate"))
    assert "prefers-reduced-motion" in motion.read_text()
    assert "<script" not in motion.read_text()
    for suffix in (".md",".zh-TW.md"):
        page=(PAGES/("accuracy"+suffix)).read_text()
        assert f'src="../../../../assets/concept-animations/{stem}-still.svg"' in page
        assert f'data-motion-src="../../../../assets/concept-animations/{stem}-motion.svg"' in page
        assert f'](../../../../assets/concept-animations/{stem}-still.svg)' in page
# Regression: a previous CI test expected a lone "$" even after the bilingual
# chapters had been corrected to display MathJax "$$". Assert semantic fences
# rather than hard-coding the obsolete (and mobile-overflow-prone) delimiter.
for suffix, explanation in (
    (".md", "not a deployable rule"),
    (".zh-TW.md", "不是部署時能讀取未知真實標籤"),
):
    text = (PAGES / ("accuracy" + suffix)).read_text(encoding="utf-8")
    display_blocks = re.findall(r"(?ms)^\\$\\$[ \\t]*\\n(.*?)\\n\\$\\$[ \\t]*$", text)
    weighted = [block for block in display_blocks
                if block.lstrip().startswith(r"\\mathrm{WeightedAccuracy}=")]
    assert len(weighted) == 1, (suffix, "missing or duplicated display-math formula")
    assert r"\\frac{\\sum_i w_i" in weighted[0]
    assert r"\\sum_i w_i>0" in weighted[0]
    # A standalone single-dollar line creates inline MathJax on narrow screens.
    assert not re.search(r"(?m)^\\$[ \\t]*$", text), (suffix, "inline-math fence")
    assert "1705.08500" in text
    # True labels may be used to audit coverage, but cannot drive a deployable
    # rejection rule at inference time.
    assert explanation in text, (suffix, "missing deployability caveat")
print("Selective coverage, bilingual display math and rejection caveats verified")
