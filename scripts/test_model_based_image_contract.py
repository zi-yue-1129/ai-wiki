"""Fixture-only regressions: these are not native browser execution."""
import copy, unittest
from pathlib import Path
from test_model_based_source_browser import validate_image_state, TOPICS, WIDTHS
class Contract(unittest.TestCase):
 def setUp(self):
  self.url='https://wiki.test/fixture/expected.svg'
  self.good=dict(src=self.url,currentSrc=self.url,complete=True,naturalWidth=300,naturalHeight=169,width=640,height=360,viewBox=[0,0,640,360])
 def test_viewbox_intrinsic_and_css_are_independent(self):validate_image_state(self.good,self.url)
 def test_negative_wrong_source(self):
  for key in ['src','currentSrc']:
   s=copy.deepcopy(self.good);s[key]='https://wiki.test/fixture/other.svg'
   with self.assertRaises(AssertionError):validate_image_state(s,self.url)
 def test_negative_unloaded_or_failed_decode(self):
  for key,value in [('complete',False),('naturalWidth',0),('naturalHeight',0)]:
   s=copy.deepcopy(self.good);s[key]=value
   with self.assertRaises(AssertionError):validate_image_state(s,self.url)
 def test_negative_wrong_geometry_or_viewbox(self):
  for key,value in [('width',639),('height',359),('viewBox',[0,0,639,360])]:
   s=copy.deepcopy(self.good);s[key]=value
   with self.assertRaises(AssertionError):validate_image_state(s,self.url)
 def test_matrix_and_controls_preserved(self):
  self.assertEqual(len(TOPICS)*len(WIDTHS)*2*2,64)
  source=Path(__file__).with_name('test_model_based_source_browser.py').read_text()
  for token in ["page.keyboard.press('Enter')","page.keyboard.press('Space')","page.keyboard.press('ArrowRight')",'scrollWidth <= innerWidth','Math.abs(e.scrollLeft-(e.scrollWidth-e.clientWidth))<2','native_contract_negatives(browser)']:
   self.assertIn(token,source)
if __name__=='__main__':unittest.main()
