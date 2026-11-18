"""Read actual SVG attributes to check a single ant-system update."""
from pathlib import Path
import bisect
import re
import unittest
import xml.etree.ElementTree as E

B = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = "{http://www.w3.org/2000/svg}"


def value(a, t):
    times = list(map(float, a.get("keyTimes").split(";")))
    vals = list(map(float, a.get("values").split(";")))
    k = min(bisect.bisect_right(times, t)-1, len(times)-2)
    if a.get("calcMode") == "discrete":
        return vals[k]
    u = (t-times[k])/(times[k+1]-times[k])
    return vals[k]*(1-u)+vals[k+1]*u


def expected(t, length):
    if t <= .35:
        return 1
    if t <= .45:
        return 1-.25*(t-.35)/.1
    if t <= .65:
        return .75+(4/length)*(t-.45)/.2
    return .75+4/length


class PheromoneUpdate(unittest.TestCase):
    def test_same_scale_evaporation_then_deposit_after_both_ants_arrive(self):
        r = E.parse(B/"ant-colony-pheromone-motion.svg").getroot()
        for colour, length in [("#159a90",4),("#e6a33d",6)]:
            lines=[e for e in r.iter(NS+"line") if e.get("stroke")==colour]
            bars=[e for e in r.iter(NS+"rect") if e.get("fill")==colour]
            self.assertEqual(len(lines),2)
            self.assertEqual(len(bars),1)
            for j in range(10001):
                t=j/10000
                tau=expected(t,length)
                self.assertAlmostEqual(value(bars[0].find(NS+"animate"),t)/64,tau,places=8)
                for line in lines:
                    self.assertAlmostEqual(value(line.find(NS+"animate"),t)/4,tau,places=8)
        paths=list(r.iter(NS+"animateMotion"))
        self.assertEqual(len(paths),2)
        for a in paths:
            self.assertEqual(a.get("keyTimes"),"0;0.35;1")
            self.assertEqual(a.get("keyPoints"),"0;1;1")
            pts=re.findall(r"[ML] ?([\d.]+) ([\d.]+)",a.get("path"))
            self.assertEqual(tuple(map(float,pts[-1])),(371.,205.))
        # Endpoints are a single evaporation/deposit operation, not accumulated frames.
        self.assertEqual(expected(1,4),1.75)
        self.assertAlmostEqual(expected(1,6),17/12)

    def test_static_fallback_and_source_hooks(self):
        r=E.parse(B/"ant-colony-pheromone-still.svg").getroot()
        for colour,length in [("#159a90",4),("#e6a33d",6)]:
            for el in r.iter(NS+"line"):
                if el.get("stroke")==colour:
                    self.assertAlmostEqual(float(el.get("stroke-width"))/4,.75+4/length)
            bar=next(el for el in r.iter(NS+"rect") if el.get("fill")==colour)
            self.assertAlmostEqual(float(bar.get("width"))/64,.75+4/length)
        self.assertFalse(list(r.iter(NS+"animate")))
        for lang in ["",".zh-TW"]:
            for page in ["ant-colony","particle-swarm"]:
                s=(B.parents[1]/f"theory/paradigms/evolutionary/{page}{lang}.md").read_text()
                self.assertIn("<img data-source-asset-urls",s)
                self.assertIn("data-still-src=",s)
                self.assertIn("overflow-x:auto",s)
                self.assertIn('tabindex="0"',s)
            s=(B.parents[1]/f"theory/paradigms/evolutionary/ant-colony{lang}.md").read_text()
            self.assertIn(r"\begin{gathered}",s)
            self.assertNotIn(r"1.75,\qquad",s)


if __name__ == "__main__":
    unittest.main()
