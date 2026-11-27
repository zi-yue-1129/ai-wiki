"""Exact arithmetic checks for the two compression teaching examples."""
from fractions import Fraction as F
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"


class CompressionMotionTests(unittest.TestCase):
    def test_codebook_payload(self):
        weights = list(map(F, ["0.1", "0.9", "1.1", "-1.8", "0.05", "1.0", "-2.1", "3.0"]))
        codebook = [1, -2, 3]
        ids = [min(range(3), key=lambda j: abs(w-codebook[j])) for w in weights if abs(w) > F("0.2")]
        self.assertEqual(ids, [0, 0, 1, 0, 1, 2])
        codes = ["0", "10", "11"]
        stream = "".join(codes[i] for i in ids)
        self.assertEqual(stream, "001001011")
        self.assertEqual(len(stream), 9)
        self.assertEqual(len(ids)*2, 12)
        for a in codes:
            for b in codes:
                if a != b:
                    self.assertFalse(b.startswith(a))
        self.assert_labels("deep-compression-codebook-stream", ["Fixed: 12 bits", "Huffman: 9 bits"])

    def test_filter_compaction(self):
        w1 = [[F(2), F(-1)], [F("0.1"), F("0.1")], [F(-1), F(3)]]
        w2 = [[1, 2, 3], [-1, 4, 2]]
        scores = [sum(map(abs, row)) for row in w1]
        self.assertEqual(scores, [3, F("0.2"), 4])
        keep = [i for i in range(3) if i != scores.index(min(scores))]
        self.assertEqual(keep, [0, 2])
        x = [2, 1]
        hidden = [max(0, sum(a*b for a,b in zip(row,x))) for row in w1]
        masked = [v if i in keep else 0 for i,v in enumerate(hidden)]
        direct = [sum(a*b for a,b in zip(row,masked)) for row in w2]
        compact = [sum(row[i]*hidden[i] for i in keep) for row in w2]
        self.assertEqual(compact, direct)
        self.assertEqual(3*2+2*3, 12)
        self.assertEqual(2*2+2*2, 8)
        self.assert_labels("filter-pruning-channel-compaction", ["Remove channel 2", "12 → 8 weights"])

    def test_packed_prefix_stream(self):
        expected = ["0", "0", "10", "0", "10", "11"]
        codes = {"0": "A", "10": "B", "11": "C"}
        for kind in ("motion", "still"):
            root = ET.parse(ASSETS / f"deep-compression-codebook-stream-{kind}.svg").getroot()
            ns = "{http://www.w3.org/2000/svg}"
            groups = [e for e in root.iter(ns + "g") if e.get("id", "").startswith("packed-")]
            actual = [g.find(ns + "text").text for g in groups]
            self.assertEqual(actual, expected)
            self.assertEqual([int(g.find(ns + "rect").get("width")) for g in groups],
                             [35*len(code)-4 for code in expected])
            self.assertEqual([int(g.find(ns + "rect").get("x")) for g in groups],
                             [128, 163, 198, 268, 303, 373])
            decoded, prefix = [], ""
            for bit in "".join(actual):
                prefix += bit
                if prefix in codes:
                    decoded.append(codes[prefix])
                    prefix = ""
            self.assertEqual(prefix, "")
            self.assertEqual(decoded, list("AABABC"))

    def test_positive_channel_rescaling(self):
        w1 = [[F(2), F(-1)], [F("0.1"), F("0.1")], [F(-1), F(3)]]
        w2 = [[F(1), F(2), F(3)], [F(-1), F(4), F(2)]]
        scales = [F(1), F(30), F(1)]
        v1 = [[d*a for a in row] for d,row in zip(scales,w1)]
        v2 = [[a/d for a,d in zip(row,scales)] for row in w2]
        def scores(w):
            return [sum(map(abs,row)) for row in w]
        def output(a,b,x,remove=None):
            h = [max(0,sum(v*z for v,z in zip(row,x))) for row in a]
            return [sum(v*z for i,(v,z) in enumerate(zip(row,h)) if i != remove) for row in b]
        self.assertEqual(scores(w1), [3,F("0.2"),4])
        self.assertEqual(scores(v1), [3,6,4])
        for x in [(2,1),(-2,1),(0,0),(2,-1),(-3,-2)]:
            self.assertEqual(output(w1,w2,x),output(v1,v2,x))
        self.assertEqual(output(w1,w2,(2,1)),[F("6.6"),F("0.2")])
        self.assertEqual(output(w1,w2,(2,1),1),[6,-1])
        self.assertEqual(output(v1,v2,(2,1),0),[F("3.6"),F("3.2")])

    def assert_labels(self, stem, labels):
        for kind in ("motion", "still"):
            root = ET.parse(ASSETS / f"{stem}-{kind}.svg").getroot()
            texts = [e.text for e in root.iter("{http://www.w3.org/2000/svg}text")]
            for label in labels:
                self.assertIn(label, texts)


if __name__ == "__main__":
    unittest.main()
