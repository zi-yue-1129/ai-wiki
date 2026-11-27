"""Numerical and visual contracts for within-network and sequence distillation."""
from pathlib import Path
import math
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = "{http://www.w3.org/2000/svg}"


class DistillationTargetSemantics(unittest.TestCase):
    def test_deep_head_targets(self):
        shallow, deep = (.5, .3, .2), (.7, .2, .1)
        self.assertAlmostEqual(-math.log(shallow[0]), .69314718056)
        self.assertAlmostEqual(-math.log(deep[0]), .35667494394)
        self.assertAlmostEqual(sum(a * math.log(a / b) for a, b in zip(shallow, deep)), .09203285023)
        self.assertAlmostEqual(sum((a-b)**2 for a,b in zip((.2,.6),(.5,.4))), .13)
        for kind in ("motion", "still"):
            root = ET.parse(ASSETS / f"byot-deep-head-targets-{kind}.svg").getroot()
            labels = {n.text for n in root.iter(NS + "text")}
            self.assertTrue({"Head 1", "Head C", "Feature target", "KL", "CE", "Label"} <= labels)
            paths = {n.get("d") for n in root.iter(NS + "path")}
            self.assertTrue({"M430 116V70H210V116", "M362 240H278",
                             "M320 310V292H210V264", "M320 310V292H430V264"} <= paths)

    def test_trace_filter_and_nll(self):
        traces = [("A","B","4"), ("A","C","5"), ("B","A","4")]
        self.assertEqual([x for x in traces if x[-1]=="4"], [traces[0],traces[2]])
        nll = -sum(math.log(p) for p in (.5,.25,.8))
        self.assertAlmostEqual(nll, math.log(10))
        self.assertEqual(f"{nll:.3f}", "2.303")
        for kind in ("motion", "still"):
            root = ET.parse(ASSETS / f"r1-trace-filter-sft-{kind}.svg").getroot()
            labels = [n.text for n in root.iter(NS + "text")]
            self.assertEqual(labels.count("Keep"), 2)
            self.assertEqual(labels.count("Reject"), 1)
            self.assertTrue({"0.50", "0.25", "0.80", "NLL = 2.303", "Pool"} <= set(labels))
            self.assertTrue(any(n.get("d") == "M371 111H405V223H371" for n in root.iter(NS+"path")))


if __name__ == "__main__":
    unittest.main()
