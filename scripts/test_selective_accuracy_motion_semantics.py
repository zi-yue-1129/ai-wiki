"""Synthetic selective-classification arithmetic and SVG stage contracts."""
from fractions import Fraction
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
print("Selective coverage and class-conditional abstention examples verified")
