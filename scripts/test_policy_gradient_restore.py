"""Real suite inventory, collision negatives, failure reports and CI wiring."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import yaml

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('policy_svg_browser',ROOT/'scripts/test_policy_gradient_motion_browser.py')
suite=importlib.util.module_from_spec(spec);spec.loader.exec_module(suite)

class Coverage(unittest.TestCase):
    def test_original_24_cases_and_every_time(self):
        cases=suite.cases();self.assertEqual(len(cases),24)
        for stem in suite.STEMS:
            own=[x for x in cases if x['stem']==stem]
            svg=[x for x in own if x['test']=='svg'];self.assertEqual(len(svg),2)
            self.assertEqual(next(x['times']for x in svg if x['kind']=='motion'),[0,2,4,6,9,11])
            self.assertEqual(next(x['times']for x in svg if x['kind']=='still'),[0])
            for lang in ['en','zh']:
                players=[x for x in own if x.get('lang')==lang]
                self.assertEqual({(x['width'],x['reduced'])for x in players},{(320,False),(360,False),(720,False),(1024,False),(320,True)})
    def test_collision_negative(self):
        with self.assertRaises(AssertionError):suite.check_boxes([dict(label='a',x=20,y=20,w=20,h=20),dict(label='b',x=25,y=25,w=20,h=20)],'s','motion',6)
    def test_bound_negative(self):
        for box in [dict(x=-3,y=10,w=1,h=1),dict(x=10,y=-3,w=1,h=1),dict(x=760,y=10,w=3,h=1),dict(x=10,y=400,w=1,h=3)]:
            with self.assertRaises(AssertionError):suite.check_boxes([dict(label='bad',**box)],'s','still',0)
    def test_original_tolerance(self):
        suite.check_boxes([dict(label='a',x=20,y=20,w=20,h=20),dict(label='b',x=37,y=20,w=20,h=20)],'s','motion',0)
    def test_launch_failure_retains_all_cases(self):
        with tempfile.TemporaryDirectory() as d,patch.object(suite,'OUT',Path(d)),patch.object(suite,'sync_playwright',side_effect=RuntimeError('launch blocked canary')):
            self.assertEqual(suite.main(),1);r=json.loads((Path(d)/'report.json').read_text());self.assertEqual(r['status'],'failed');self.assertEqual(len(r['cases']),24);self.assertTrue(all(x['status']=='blocked'for x in r['cases']));self.assertIn('launch blocked canary',r['error'])
    def test_ci_execution_and_evidence(self):
        path=ROOT/'.github/workflows/built-motion-browser.yml';d=yaml.safe_load(path.read_text());steps=d['jobs']['built-motion-browser']['steps'];self.assertTrue(any(x.get('run')=='python scripts/test_policy_gradient_motion_browser.py'for x in steps));self.assertTrue(any(x.get('run')=='python scripts/test_policy_gradient_restore.py'for x in steps));upload=next(x for x in steps if x.get('with',{}).get('name')=='policy-gradient-motion-review');self.assertEqual(upload['if'],'always()');self.assertEqual(upload['with']['path'],'artifacts/policy-gradient-motion/');self.assertEqual(upload['with']['if-no-files-found'],'error')
    def test_controls_and_native_glyph_contract_retained(self):
        src=(ROOT/'scripts/test_policy_gradient_motion_browser.py').read_text()
        for token in ['getBBox()','page.keyboard.press("Enter")','page.keyboard.press("Space")','i.naturalWidth===760','dimensions["scroll"]>=760','region.focus()','s.pauseAnimations(); s.setCurrentTime(t)']:self.assertIn(token,src)

if __name__=='__main__':unittest.main()
