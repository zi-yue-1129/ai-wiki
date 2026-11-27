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

    def assert_labels(self, stem, labels):
        for kind in ("motion", "still"):
            root = ET.parse(ASSETS / f"{stem}-{kind}.svg").getroot()
            texts = [e.text for e in root.iter("{http://www.w3.org/2000/svg}text")]
            for label in labels:
                self.assertIn(label, texts)


if __name__ == "__main__":
    unittest.main()
