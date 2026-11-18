"""Prevent the six-page mobile overflow from long inline MathJax returning.

Source/Markdown checks complement, not replace, built Chromium viewport tests.
"""
from pathlib import Path
import re
import unittest
from markdown import Markdown
ROOT=Path(__file__).resolve().parents[1]
class ClassificationMathLayout(unittest.TestCase):
 def test_long_formulas_are_individual_display_blocks(self):
  expected={
   'accuracy':[r'\operatorname{Accuracy}(p)',r'= p(0.80)+(1-p)(0.90)',r'= 0.90-0.10p.'],
   'f1':[r'F_{1,A}(k)=\frac{180}{190-k}',r'F_{1,B}(k)=\frac{2k}{10+k}',r'F_{1,\mathrm{macro}}=\tfrac12(F_{1,A}+F_{1,B})',r'F_{1,\mathrm{micro}}=\frac{90+k}{100}'],
   'pr-auc':[r'(1/2)(1)+(1/2)(1/2+2/3)/2',r'=19/24\approx0.792.',r'AP=(1/2)(1)+(1/2)(2/3)',r'\\ =5/6\approx0.8333.'],
  }
  for topic,expressions in expected.items():
   for lang in ['', '.zh-TW']:
    source=(ROOT/f'docs/theory/evaluation/metrics/classification/{topic}{lang}.md').read_text()
    blocks=re.findall(r'^\$\$\n(.*?)\n\$\$$',source,re.M|re.S)
    for expression in expressions:
     matches=[b for b in blocks if expression in b]
     self.assertEqual(len(matches),1,(topic,lang,expression))
     markup=Markdown(extensions=['pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True}}).convert('$$\n'+matches[0]+'\n$$')
     self.assertIn('<div class="arithmatex">',markup)
     self.assertNotIn('<span class="arithmatex">',markup)
    if topic=='f1':
     for b in blocks:
      if any(e in b for e in expressions):self.assertNotIn(r'\qquad',b)
    else:
     self.assertTrue(any(r'\begin{gathered}' in b and r'\\' in b for b in blocks))
if __name__=='__main__':unittest.main()
