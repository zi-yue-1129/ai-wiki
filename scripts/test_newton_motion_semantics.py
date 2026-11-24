"""Independent numerical and geometric checks of the actual Newton SVGs."""
from pathlib import Path
import bisect
import math
import re
import unittest
import xml.etree.ElementTree as ET

B = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = "{http://www.w3.org/2000/svg}"


def root(name, kind="motion"):
    return ET.parse(B / f"{name}-{kind}.svg").getroot()


def value(a, t):
    times = list(map(float, a.get("keyTimes").split(";")))
    values = list(map(float, a.get("values").split(";")))
    i = min(bisect.bisect_right(times, t) - 1, len(times) - 2)
    if a.get("calcMode") == "discrete":
        return values[i]
    u = (t - times[i]) / (times[i + 1] - times[i])
    return values[i] * (1-u) + values[i+1] * u


class NewtonGeometry(unittest.TestCase):
    def test_bilingual_iterate_sequence_uses_display_math(self):
        for lang in ["", ".zh-TW"]:
            path = B.parents[1] / f"theory/math/calculus/newtons-method{lang}.md"
            source = path.read_text()
            blocks = re.findall(r"^\$\$\n(.*?)\n\$\$$", source, re.M | re.S)
            self.assertTrue(any("2.2" in b and "0.00034" in b and
                                r"\begin{gathered}" in b for b in blocks))

    def test_convex_iterates_and_curve(self):
        r = root("newton-curvature-steps")
        marker = next(c for c in r.iter(NS+"circle") if c.find(NS+"animate") is not None)
        ax, ay = marker.findall(NS+"animate")
        anchors = [2.2]
        for _ in range(6):
            x = anchors[-1]
            anchors.append(x-(x**3+x)/(3*x*x+1))
        for k, x in enumerate(anchors):
            self.assertAlmostEqual(value(ax, k/6), 70+150*x, delta=.0002)
            self.assertAlmostEqual(value(ay, k/6), 296-15.6*(x**4/4+x*x/2), delta=.0002)
        # Every displayed in-between dot remains on f, not a straight endpoint chord.
        for j in range(10001):
            t=j/10000
            x=(value(ax,t)-70)/150
            self.assertAlmostEqual(value(ay,t),296-15.6*(x**4/4+x*x/2),delta=.02)
        models=[p for p in r.iter(NS+"path") if p.find(NS+"animate") is not None]
        self.assertEqual(len(models),6)
        for k,p in enumerate(models):
            points=re.findall(r"[ML]([\d.]+)[ ,]([\d.]+)",p.get("d"))
            self.assertGreater(len(points),10)
            x0=anchors[k];f0=x0**4/4+x0*x0/2;g=x0**3+x0;h=3*x0*x0+1
            for X,Y in points:
                x=(float(X)-70)/150
                model=f0+g*(x-x0)+h*(x-x0)**2/2
                self.assertAlmostEqual(float(Y),296-15.6*model,delta=.02)
            anim=p.find(NS+"animate")
            self.assertEqual(value(anim,(k+.5)/6),1)
            self.assertEqual(value(anim,((k+1)%6+.5)/6),0)

    def test_indefinite_and_shifted_steps(self):
        r=root("newton-indefinite-curvature")
        markers=[c for c in r.iter(NS+"circle") if c.find(NS+"animate") is not None]
        self.assertEqual(len(markers),2)
        f=lambda x:x**4/4-x*x/2
        self.assertGreater(f(-16/65),f(.4))
        self.assertLess(f(1.1),f(.4))
        for c,centre,end in zip(markers,[165,475],[-16/65,1.1]):
            ax,ay=c.findall(NS+"animate")
            self.assertAlmostEqual((value(ax,.5)-centre)*2.9/250,end,delta=1e-6)
            for j in range(10001):
                t=j/10000;x=(value(ax,t)-centre)*2.9/250
                self.assertAlmostEqual(value(ay,t),197.5-250*f(x),delta=.01)

    def test_armijo_candidates_curve_and_tick_scale(self):
        r=root("newton-armijo-backtracking")
        marker=next(c for c in r.iter(NS+"circle") if c.find(NS+"animate") is not None)
        ax,ay=marker.findall(NS+"animate")
        bar=next(a for a in r.iter(NS+"animate") if a.get("attributeName")=="width")
        for t,alpha,passes in [(0,1,False),(.25,.5,False),(.5,.25,True)]:
            self.assertAlmostEqual(value(bar,t)/295,alpha,delta=1e-6)
            x=2-10*alpha
            self.assertEqual(math.sqrt(1+x*x)<=math.sqrt(5)+1e-4*alpha*(-10)*(2/math.sqrt(5)),passes)
        for j in range(10001):
            t=j/10000;alpha=value(bar,t)/295;x=2-10*alpha
            self.assertAlmostEqual(value(ax,t),86+(x+8.5)*456/11.1,delta=.0002)
            self.assertAlmostEqual(value(ay,t),269-math.sqrt(1+x*x)*186/8.5,delta=.02)
        for kind in ["motion","still"]:
            for text in root("newton-armijo-backtracking",kind).iter(NS+"text"):
                if text.get("x")=="69":
                    self.assertAlmostEqual(float(text.get("y"))-4,269-int(text.text)*186/8.5,delta=1e-6)


if __name__ == "__main__":
    unittest.main()
