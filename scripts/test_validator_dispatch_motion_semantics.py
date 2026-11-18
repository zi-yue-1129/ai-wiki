"""Keep distinct source-asset validation contracts when integration sets are unioned."""
import ast
from pathlib import Path
import unittest

SOURCE=Path(__file__).with_name('verify_concept_motion.py').read_text()
TREE=ast.parse(SOURCE)

def branch(stem):
    clauses=[]
    for n in ast.walk(TREE):
        if not isinstance(n,ast.If): continue
        t=n.test
        if isinstance(t,ast.Compare) and isinstance(t.left,ast.Name) and t.left.id=='stem' and len(t.ops)==1 and isinstance(t.ops[0],ast.In) and isinstance(t.comparators[0],ast.Set):
            if stem in ast.literal_eval(t.comparators[0]): clauses.append(n)
    node=min(clauses,key=lambda n:n.lineno)
    return '\n'.join(ast.get_source_segment(SOURCE,n) for n in node.body)

class Dispatch(unittest.TestCase):
    def test_hmm_keeps_existing_source_pair_contract(self):
        for stem in ('hmm-forward-sum-product','hmm-filter-smooth','hmm-pairwise-posterior','hmm-baum-welch-transition'):
            body=branch(stem);self.assertIn('verify_source_pair',body);self.assertNotIn('missing GitHub static preview link',body)
    def test_security_keeps_strict_source_pair_contract(self):
        for stem in ('prompt-injection-boundary','watermark-greenlist-score'):
            self.assertIn('verify_source_pair',branch(stem))
    def test_classification_still_requires_explicit_preview_link(self):
        for stem in ('accuracy-prevalence','roc-cost-operating-point','f1-threshold-topk'):
            self.assertIn('missing GitHub static preview link',branch(stem))
    def test_static_first_contracts_remain_distinct(self):
        self.assertIn('static-first animation not registered',branch('paged-block-mapping'))
        self.assertIn('expected exactly one static-first motion image',branch('t5-span-corruption'))

if __name__=='__main__':unittest.main()
