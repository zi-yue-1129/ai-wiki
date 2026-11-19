"""Production Markdown -> real MathJax 3.2.2 CHTML/MathML; not native pixel QA."""
import json, subprocess, unittest, re, os
from pathlib import Path
import xml.etree.ElementTree as E
from test_forward_math_markup import ROOT, render, MathContainers
N='{http://www.w3.org/1998/Math/MathML}'
OUT=ROOT/'artifacts/icm-mathjax-structure'
def convert(tex):
 p=subprocess.run(['node',str(ROOT/'scripts/render_mathjax_structure.cjs')],input=json.dumps(tex),text=True,capture_output=True,check=True)
 return json.loads(p.stdout)
def validate(record):
 assert not record['errors'], record['errors']
 r=E.fromstring(record['mathml'])
 assert not list(r.iter(N+'merror'))
 assert len(list(r.iter(N+'mover')))==1
 mover=next(r.iter(N+'mover'));assert [''.join(e.itertext()) for e in mover]==['L','¯']
 sums=list(r.iter(N+'munderover'));assert len(sums)==2
 for s in sums:assert [''.join(''.join(e.itertext()).split()) for e in s]==['∑','i=1','3']
 fractions=list(r.iter(N+'mfrac'));assert len(fractions)==1
 assert [''.join(''.join(e.itertext()).split()) for e in fractions[0]]==['Ni','n']
 assert sum(e.text=='ℓ' for e in r.iter(N+'mi'))==2
 assert sum(e.text=='=' for e in r.iter(N+'mo'))==4
 assert len([e for e in r.iter(N+'mspace') if e.get('width')=='2em'])==1
 assert not any(e.get('linebreak') for e in r.iter())
 assert '<mjx-container' in record['chtml'] and 'mjx-merror' not in record['chtml']
class MathJaxStructure(unittest.TestCase):
 def test_bilingual_real_structure_and_bad_escaping_counterfactuals(self):
  OUT.mkdir(parents=True,exist_ok=True)
  for lang in ['', '.zh-TW']:
   source=(ROOT/f'docs/theory/paradigms/reinforcement-learning/exploration/icm/index{lang}.md').read_text()
   blocks=MathContainers(render(source)).blocks
   selected=[b[2:-2] for b in blocks if 'N_i' in b and 'p_i' in b and 'L_n=' in b]
   self.assertEqual(len(selected),1)
   tex=selected[0]
   commands=['bar','sum','frac','ell','qquad']
   bad=[re.sub(r'(?<!\\)\\('+ '|'.join(commands)+r')(?![A-Za-z])',lambda m:'\\'+m.group(),tex)]
   bad += [tex.replace('\\'+c,'\\\\'+c) for c in commands]
   records=convert([tex]+bad)
   (OUT/f'{lang or "en"}-mathjax.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
   validate(records[0])
   for record in records[1:]:
    with self.assertRaises(AssertionError):validate(record)
if __name__=='__main__':unittest.main()
