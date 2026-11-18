"""Exact new prose matrices, executable registration, and fail-closed evidence."""
import ast,copy,hashlib,json,unittest
from pathlib import Path
from test_motion_shard_ci import support_fixture
from motion_shard_contract import validate_support,support_registry,report_digest
from prepare_browser_artifacts import DEFAULT_ROOTS
ROOT=Path(__file__).resolve().parents[1]
class ProseIntegration(unittest.TestCase):
 def test_complete_exact_source_width_language_matrix(self):
  from test_time_series_prose_browser import SOURCES as time_sources,WIDTHS as tw
  from test_causal_inference_prose_browser import SOURCES as causal_sources,WIDTHS as cw
  for name,sources,widths,script in [('time-series-prose',time_sources,tw,'test_time_series_prose_browser.py'),('causal-prose',causal_sources,cw,'test_causal_inference_prose_browser.py')]:
   suite=next(s for s in support_registry()['suites'] if s['id']==name)
   self.assertEqual(set(json.loads((ROOT/suite['sources_manifest']).read_text())),set(sources))
   self.assertEqual(suite['widths'],list(widths));self.assertEqual(widths,(320,390,1280))
   self.assertEqual(suite['command'],['scripts/'+script]);self.assertIn(name,DEFAULT_ROOTS)
   self.assertTrue(suite['require_case_language']);self.assertTrue(suite['require_reported_screenshots'])
  self.assertEqual(len(time_sources),8);self.assertEqual(len(causal_sources),6)
 def test_missing_duplicate_wrong_language_or_unpacked_screenshot_rejected(self):
  for suite in ['time-series-prose','causal-prose']:
   for kind in ['suite','missing-case','duplicate-case','wrong-source','wrong-width','wrong-language','empty-shots','missing-shot','unsafe-shot']:
    m,r,a,p=support_fixture();report=r['reports'][suite];case=report['cases'][0]
    if kind=='suite':r['execution']['suites']=[x for x in r['execution']['suites'] if x['suite']!=suite]
    elif kind=='missing-case':report['cases'].pop()
    elif kind=='duplicate-case':report['cases'].append(copy.deepcopy(case))
    elif kind=='wrong-source':case['source']='docs/wrong.md'
    elif kind=='wrong-width':case['width']=768
    elif kind=='wrong-language':case['lang']='wrong'
    elif kind=='empty-shots':case['screenshots']=[]
    elif kind=='missing-shot':case['screenshots'].append('missing.png')
    else:case['screenshots'].append('../escape.png')
    for f in r['pack']['files']:
     if f['path']==suite+'/report.json':f['sha256']=hashlib.sha256(json.dumps(report,ensure_ascii=False,indent=2).encode()).hexdigest()
     if f['path']=='support-execution/report.json':f['sha256']=report_digest(r['execution'])
    with self.subTest(suite=suite,kind=kind),self.assertRaises(ValueError):validate_support(m,r,a,p)
 def test_reference_contains_executable_not_commented_commands(self):
  import yaml
  d=yaml.safe_load((ROOT/'scripts/fixtures/built-motion-browser-unsharded-reference.yml').read_text())
  runs=[s.get('run','') for j in d['jobs'].values() for s in j['steps']]
  for script in ['test_time_series_prose_browser.py','test_causal_inference_prose_browser.py']:
   self.assertIn('python scripts/'+script,runs)
if __name__=='__main__':unittest.main()
