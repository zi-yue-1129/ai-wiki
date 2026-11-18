"""Recompute-before-backward ordering and binary16 rounding semantics."""
import struct,unittest,xml.etree.ElementTree as E
from pathlib import Path
N='{http://www.w3.org/2000/svg}';A=Path(__file__).resolve().parents[1]/'docs/assets/concept-animations'
def value(n,attr,t):
 a=next((a for a in n if a.get('attributeName')==attr),None)
 if a is None:return float(n.get(attr,'1'))
 ts=list(map(float,a.get('keyTimes').split(';')));vs=[list(map(float,v.split())) for v in a.get('values').split(';')]
 for i in range(len(ts)-1):
  if t<=ts[i+1]:
   v=[x+(y-x)*(t-ts[i])/(ts[i+1]-ts[i]) for x,y in zip(vs[i],vs[i+1])];return v if attr=='transform' else v[0]
 return vs[-1] if attr=='transform' else vs[-1][0]
class CheckpointScaling(unittest.TestCase):
 def test_segment_buffers_precede_backward_and_release(self):
  r=E.parse(A/'checkpoint-recompute-motion.svg').getroot();nodes={n.get('id'):n for n in r.iter() if n.get('id')};b=nodes['backward-cursor'];re=nodes['recompute-cursor']
  for t in [i/2000 for i in range(2001)]:
   if value(b,'opacity',t)>.999:
    second=t<.7;indices=(5,6,7) if second else (1,2,3)
    for i in indices:self.assertAlmostEqual(value(nodes[f'temporary-a{i}'],'opacity',t),1)
    self.assertEqual(value(re,'opacity',t),0)
  for start,end,left,right,indices in [(.30,.42,314,570,(5,6,7)),(.64,.76,58,314,(1,2,3))]:
   self.assertAlmostEqual(value(re,'cx',start),left);self.assertAlmostEqual(value(re,'cx',end),right)
   for i in indices:
    hit=start+.03*(i-indices[0]+1);self.assertAlmostEqual(value(re,'cx',hit),58+64*i)
    self.assertAlmostEqual(value(nodes[f'temporary-a{i}'],'opacity',hit),1)
  for i in range(1,8):
   if i!=4:self.assertEqual(value(nodes[f'temporary-a{i}'],'opacity',.97),0)
  self.assertGreater(value(b,'transform',.45)[0],value(b,'transform',.59)[0]);self.assertGreater(value(b,'transform',.79)[0],value(b,'transform',.93)[0]);self.assertIn('L-8',b.get('d'))
 def test_binary16_underflow_and_fp32_unscale(self):
  half=lambda x:struct.unpack('e',struct.pack('e',x))[0]
  single=lambda x:struct.unpack('f',struct.pack('f',x))[0]
  g=2**-27;s=2**10
  self.assertEqual(half(g),0);self.assertEqual(half(g*s),2**-17);self.assertEqual(single(half(g*s))/s,g)
  self.assertEqual(half(2**-25),0);self.assertEqual(half(2**-25+2**-35),2**-24)
  for mode in ('motion','still'):
   r=E.parse(A/f'fp16-loss-scaling-{mode}.svg').getroot();self.assertTrue(any(n.text=='FP32 ÷ 2^10' for n in r.iter()))
 def test_scaled_flow_reaches_stage_centers(self):
  r=E.parse(A/'fp16-loss-scaling-motion.svg').getroot();flow=next(n for n in r.iter() if n.get('id')=='scaled-flow');out=[n for n in r.iter() if n.get('stroke')=='#c2fff1']
  for t,x,o in zip((.36,.50,.65,.80),(88,231,379.5,535),out):
   self.assertAlmostEqual(float(flow.get('cx'))+value(flow,'transform',t)[0],x);self.assertAlmostEqual(value(o,'opacity',t),1)
  for topic in ('checkpoint-recompute','fp16-loss-scaling'):
   r=E.parse(A/f'{topic}-still.svg').getroot();self.assertFalse(r.findall('.//'+N+'animate'));self.assertFalse(r.findall('.//'+N+'animateTransform'))
if __name__=='__main__':unittest.main()
