"""Exact token-clock, statistic geometry, trust-boundary and locale regressions."""
from pathlib import Path
import math,re,unittest,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'docs/assets/concept-animations';N='{http://www.w3.org/2000/svg}'
def value(e,t):
 v=list(map(float,e.get('values').split(';')));ts=list(map(float,e.get('keyTimes').split(';')));i=max(i for i,k in enumerate(ts) if k<=t)
 return v[i] if e.get('calcMode')=='discrete' or i==len(v)-1 else v[i]+(v[i+1]-v[i])*(t-ts[i])/(ts[i+1]-ts[i])
class SecuritySemantics(unittest.TestCase):
 def test_score_and_tokens_share_discrete_clock(self):
  r=E.parse(A/'watermark-greenlist-score-motion.svg').getroot();tiles=[e for e in r.iter(N+'rect') if e.get('y')=='119'];self.assertEqual(len(tiles),16)
  c=next(e for e in r.iter(N+'circle') if e.get('r')=='6');an={e.get('attributeName'):e for e in c};clip=next(e for e in r.iter(N+'clipPath') if e.get('id')=='score-reveal')[0][0]
  for j in range(10001):
   t=j/10001;n=sum(value(e[0],t)>.5 for e in tiles)
   self.assertEqual(value(an['opacity'],t),int(n>0))
   if not n:self.assertEqual(value(clip,t),0);continue
   green=sum(e.get('fill')=='#46d7bc' for e in tiles[:n]);z=(green-.5*n)/math.sqrt(n*.25)
   self.assertAlmostEqual(value(an['cx'],t),82+39*(n-1));self.assertAlmostEqual(value(an['cy'],t),354-53.5*z,places=7)
   self.assertAlmostEqual(value(clip,t),value(an['cx'],t)-75)
  self.assertEqual(sum(e.get('fill')=='#46d7bc' for e in tiles),13)
  self.assertAlmostEqual(value(an['cy'],.99),220.25)
 def test_reference_geometry_and_boundary(self):
  r=E.parse(A/'watermark-greenlist-score-motion.svg').getroot()
  guide=next(e for e in r.iter(N+'line') if e.get('stroke-dasharray'));self.assertEqual(float(guide.get('y1')),354-53.5*2)
  r=E.parse(A/'prompt-injection-boundary-motion.svg').getroot();motions=list(r.iter(N+'animateMotion'));self.assertEqual(len(motions),3)
  # Lower red information route stops at denial marker, never reaches tools.
  self.assertEqual(motions[2].get('path'),'M 208 330 L 294 330')
  self.assertIn('policy must be enforced outside the model',' '.join(r.itertext()))
 def test_locale_sources_and_scope(self):
  for topic,stem in [('watermarking','watermark-greenlist-score'),('indirect-prompt-injection','prompt-injection-boundary')]:
   for locale in ['', '.zh-TW']:
    s=(ROOT/f'docs/engineering/llm-security/{topic}{locale}.md').read_text()
    for v in ['data-source-asset-urls','concept-motion-scroll','tabindex="0"','min-width:640px',stem+'-motion.svg',stem+'-still.svg']:self.assertIn(v,s)
    self.assertIn('迴圈會重設' if locale else 'loop resets',s)
    if topic=='watermarking':self.assertIn('\\begin{gathered}',s);self.assertIn('2301.10226',s)
    else:self.assertIn('2302.12173',s)
if __name__=='__main__':unittest.main()
