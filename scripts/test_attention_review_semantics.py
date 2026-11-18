"""Source regression for relative motion, scoped player and numeric contracts."""
import unittest,xml.etree.ElementTree as E,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1];N='{http://www.w3.org/2000/svg}'
class AttentionReview(unittest.TestCase):
 def test_backward_motion_uses_zero_base(self):
  r=E.parse(R/'docs/assets/concept-animations/flashattention-backward-remat-motion.svg').getroot();items=[e for e in r.iter() if e.find(N+'animateMotion') is not None];self.assertEqual(len(items),4)
  for e in items:self.assertEqual((e.get('cx'),e.get('cy')),('0','0'))
 def test_all_attention_sources_and_dimensions(self):
  from verify_concept_motion import verify_source_pair, MotionImages
  groups={'sliding-window-mask':(800,432),'linear-attention-recurrence':(800,432),'sliding-window-depth-reach':(860,440),'linear-attention-work-growth':(860,440),'gqa-cache-growth':(640,360),'global-local-pair-count':(640,360)}
  for stem,(w,h) in groups.items():
   for kind in ['motion','still']:
    r=E.parse(R/f'docs/assets/concept-animations/{stem}-{kind}.svg').getroot();self.assertEqual(r.get('viewBox'),f'0 0 {w} {h}')
    animations=[e for e in r.iter() if e.tag in [N+'animate',N+'animateMotion']];self.assertEqual(bool(animations),kind=='motion')
   for lang in ['.md','.zh-TW.md']:
    p=R/f'docs/theory/models/transformer/attention-variants/index{lang}';self.assertEqual(verify_source_pair(p,p.read_text(),stem),[])
 def test_sparse_edges_independently(self):
  for n in range(4,13):
   local={(i,j) for i in range(1,n+1) for j in range(1,n+1) if abs(i-j)<=1};glob={(i,3) for i in range(1,n+1)}|{(3,j) for j in range(1,n+1)}
   self.assertEqual(len(local),3*n-2);self.assertEqual(len(local|glob),5*n-8)
  for L in range(1,5):
   reach={12}
   for _ in range(L):reach={j for i in reach for j in range(max(1,i-3),i+1)}
   self.assertEqual(reach,set(range(max(1,12-3*L),13)))
 def test_numeric_flash_contracts(self):
  p=R/'scripts/test_flashattention_online_browser.py';spec=importlib.util.spec_from_file_location('fa',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  m.check_numeric_bars();m.check_causal_block_counts();m.check_pipeline_schedule()
 def test_scope_and_bilingual_source_hooks(self):
  js=(R/'docs/javascripts/concept-motion.js').read_text();self.assertIn('isAttentionTopic',js)
  css=(R/'docs/stylesheets/concept-motion.css').read_text().split('/* Keep wide causal-attention')[1];self.assertNotIn('.concept-motion-player.concept-motion-wide',css)
  for lang in ['.md','.zh-TW.md']:
   for sub in ['','flash-attention/']:
    text=(R/f'docs/theory/models/transformer/attention-variants/{sub}index{lang}').read_text();self.assertIn('data-source-asset-urls',text);self.assertIn('tabindex="0"',text)
if __name__=='__main__':unittest.main()
