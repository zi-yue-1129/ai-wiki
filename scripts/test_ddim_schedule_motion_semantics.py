"""Evaluate the actual bilingual DDIM sigma display, not a copied formula snapshot."""
import math,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGES=[ROOT/'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion'/f'ddim{s}.md' for s in ('','.zh-TW')]

def source_sigma(text,at,ap,eta):
    block=next(b for b in re.findall(r'\\\[(.*?)\\\]',text,re.S) if r'\sigma_{t\to s}(\eta)' in b)
    expr=block.split('=',1)[1].strip().rstrip('.')
    expr=expr.replace(r'\bar\alpha_s',str(ap)).replace(r'\bar\alpha_t',str(at)).replace(r'\eta',str(eta))
    # Small recursive evaluator for the arithmetic grammar used by this display.
    # Unsupported notation fails rather than silently substituting a known answer.
    def group(s,i):
        assert s[i]=='{'; depth=1;j=i+1
        while depth:
            if s[j]=='{':depth+=1
            if s[j]=='}':depth-=1
            j+=1
        return s[i+1:j-1],j
    def convert(s):
        out='';i=0
        while i<len(s):
            if s.startswith(r'\frac',i):
                a,j=group(s,i+5);b,i=group(s,j);out+='(('+convert(a)+')/('+convert(b)+'))'
            elif s.startswith(r'\sqrt',i):
                a,i=group(s,i+5);out+='sqrt('+convert(a)+')'
            else:out+=s[i];i+=1
        return out
    expr=re.sub(r'\s+','',convert(expr));expr=re.sub(r'(?<=[0-9)])(?=sqrt)', '*', expr)
    assert re.fullmatch(r'[0-9.+*/()\-sqrt]+',expr),expr
    return eval(expr,{'__builtins__':{},'sqrt':math.sqrt})

class DDIMSchedule(unittest.TestCase):
    def values(self,at,ap,eta):return [source_sigma(p.read_text(),at,ap,eta) for p in PAGES]
    def test_actual_formula_grid_and_bilingual_parity(self):
        for at in (.01,.1,.36,.8):
            for ap in ((at+1)/2,1):
                for eta in (0,.25,.5,1):
                    actual=self.values(at,ap,eta)
                    expected=eta*math.sqrt((1-at/ap)*(1-ap)/(1-at))
                    for x in actual:self.assertAlmostEqual(x,expected,14);self.assertGreaterEqual(1-ap-x*x,-1e-14)
                    self.assertEqual(actual[0],actual[1])
    def test_eta_not_sigma_and_squared_coefficient_budget(self):
        for x in self.values(.36,.64,1):
            self.assertAlmostEqual(x*x,.24609375);self.assertNotAlmostEqual(x,1)
            self.assertAlmostEqual(.64+(.36-x*x)+x*x,1)
        self.assertNotEqual(self.values(.36,.64,1),self.values(.1,.64,1))
    def test_adjacent_posterior_variance_and_mean(self):
        for beta in (.001,.02,.3):
            for ap in (.2,.9):
                at=ap*(1-beta)
                for sigma in self.values(at,ap,1):
                    self.assertAlmostEqual(sigma*sigma,beta*(1-ap)/(1-at))
                    xt,eps=.7,-.2;x0=(xt-math.sqrt(1-at)*eps)/math.sqrt(at)
                    ddim=math.sqrt(ap)*x0+math.sqrt(1-ap-sigma*sigma)*eps
                    ddpm=(xt-beta*eps/math.sqrt(1-at))/math.sqrt(1-beta)
                    self.assertAlmostEqual(ddim,ddpm)
    def test_skipping_is_not_original_adjacent_transition(self):
        a=[1,.9,.72,.36]
        skipped=self.values(a[3],a[1],1)[0]**2
        adjacent=self.values(a[3],a[2],1)[0]**2
        self.assertNotAlmostEqual(skipped,adjacent)
        for p in PAGES:
            text=p.read_text();self.assertIn('https://arxiv.org/abs/2010.02502',text)
            self.assertNotIn("is the paper's name for",text);self.assertNotIn('是論文對',text)
    def test_numeric_guard_rejects_wrong_coefficient_not_just_snapshot(self):
        for p in PAGES:
            bad=p.read_text().replace(r'\frac{\bar\alpha_t}{\bar\alpha_s}',r'\frac{\bar\alpha_s}{\bar\alpha_t}')
            with self.assertRaises(ValueError):source_sigma(bad,.36,.64,1)

if __name__=='__main__':unittest.main()
