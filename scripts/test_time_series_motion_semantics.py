from pathlib import Path
import math, unittest
R=Path(__file__).resolve().parents[1]/'docs/theory/models/time-series'
def mase(train,errors,m):
 if not 0<m<len(train):raise ValueError('insufficient training history')
 d=sum(abs(train[t]-train[t-m]) for t in range(m,len(train)))/(len(train)-m)
 if not d:raise ValueError('undefined zero denominator')
 return sum(abs(e) for e in errors)/len(errors)/d
def scores(v):
 b=max(v);lse=b+math.log(sum(math.exp(x-b) for x in v));mean=sum(v)/len(v);return lse-mean,b-mean
class TimeSeries(unittest.TestCase):
 def test_mase_examples_and_scale_invariance(self):
  self.assertEqual(mase([1,3,5],[2,-2],1),1)
  self.assertEqual(mase([10,30,50],[20,-20],1),1)
  self.assertEqual(mase([1,10,2,11],[1,-1],2),1)
 def test_mase_undefined_and_short_history(self):
  for x,m in [([2,2,2],1),([1,2],2)]:
   with self.assertRaises(ValueError):mase(x,[1],m)
 def test_original_vs_max_mean(self):
  for v in [[0,0,0],[1,2,5],[-1000,-999,-998]]:
   a,b=scores(v);self.assertGreaterEqual(a,math.log(len(v))-1e-12);self.assertLessEqual(a,b+math.log(len(v))+1e-12);self.assertAlmostEqual(scores([x+3 for x in v])[0],a)
  a,b=scores([0,0]);self.assertEqual(b,0);self.assertAlmostEqual(a,math.log(2))
 def test_kl_direction(self):
  v=[0,2];z=sum(math.exp(x) for x in v);p=[math.exp(x)/z for x in v];kl=sum(.5*math.log(.5/x) for x in p);self.assertAlmostEqual(scores(v)[0]-math.log(2),kl)
 def test_owa_not_accuracy(self):
  self.assertAlmostEqual((.821-.795)/.821, .0316686967)
  self.assertGreater((.861-.797)/.861,0)
 def test_bilingual_source_math_and_preserved_methods(self):
  for suffix in ['.md','.zh-TW.md']:
   overview=(R/('index'+suffix)).read_text();assert r'\frac{1}{T-m}' in overview and r'\frac{|y_{T+h}-\hat y_{T+h|T}|}{d_m}' in overview
   assert all(x in overview for x in ['deepar.md','n-beats.md','informer.md'])
   informer=(R/('informer'+suffix)).read_text();assert r'\overline M' in informer and r'D_{\mathrm{KL}}(U\Vert p)' in informer
   nb=(R/('n-beats'+suffix)).read_text();assert all(x in nb for x in ['0.797','0.861','0.795','0.821','TOURISM','MAPE'])
if __name__=='__main__':unittest.main()
