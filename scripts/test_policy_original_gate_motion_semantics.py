"""Original 24 SVG/player cases and union48 built labs cannot silently disappear."""
import copy,hashlib,json,unittest,ast
from pathlib import Path
from motion_shard_contract import validate_support,support_registry,report_digest
from test_motion_shard_ci import support_fixture
from test_policy_gradient_motion_browser import cases,TIMES
ROOT=Path(__file__).resolve().parents[1]
class OriginalPolicy(unittest.TestCase):
 def test_registry_exact_original_cases_and_union_widths(self):
  suite=next(s for s in support_registry()['suites'] if s['id']=='policy-gradient-motion')
  expected=[dict(id=f'case-{i+1:02}',**c)for i,c in enumerate(cases())]
  self.assertEqual(suite['expected_case_specs'],expected);self.assertEqual(len(expected),24)
  self.assertEqual(TIMES,[0,2,4,6,9,11]);self.assertEqual(len(suite['expected_pngs']),114)
  labs=next(s for s in support_registry()['suites'] if s['id']=='policy-credit-labs')
  self.assertEqual(len(labs['expected_cases']),48)
  self.assertEqual({c[2]for c in labs['expected_cases']},{320,360,390,720,1024,1280})
 def test_each_original_coverage_or_evidence_loss_fails(self):
  for kind in ['suite','case','duplicate','width','reduced','language','time','samples','glyphs','screenshots','png','pageerror','requesterror']:
   m,r,a,p=support_fixture();report=r['reports']['policy-gradient-motion'];case=report['cases'][0]
   if kind=='suite':r['execution']['suites']=[s for s in r['execution']['suites']if s['suite']!='policy-gradient-motion']
   elif kind=='case':report['cases'].pop()
   elif kind=='duplicate':report['cases'].append(copy.deepcopy(case))
   elif kind in ['width','reduced','language']:
    c=next(c for c in report['cases']if c['test']=='player');c[{'language':'lang'}.get(kind,kind)]={'width':390,'reduced':True,'language':'wrong'}[kind]
   elif kind=='time':case['times']=[0,2,4,6,11]
   elif kind=='samples':case['samples'].pop()
   elif kind=='glyphs':case['samples'][0]['boxes']=[]
   elif kind=='screenshots':case['screenshots'].pop()
   elif kind=='pageerror':case['page_errors']=['error']
   elif kind=='requesterror':case['failed_requests']=['error']
   else:r['pack']['files']=[f for f in r['pack']['files']if f['path']!='policy-gradient-motion/case-01/time-0.png']
   for f in r['pack']['files']:
    if f['path']=='policy-gradient-motion/report.json':f['sha256']=hashlib.sha256(json.dumps(report,ensure_ascii=False,indent=2).encode()).hexdigest()
    if f['path']=='support-execution/report.json':f['sha256']=report_digest(r['execution'])
   pack=r['pack'];pack['file_count']=len(pack['files']);pack['raw_bytes']=sum(f['size']for f in pack['files']);pack['groups'][0].update(file_count=pack['file_count'],raw_bytes=pack['raw_bytes'])
   with self.subTest(kind=kind),self.assertRaises(ValueError):validate_support(m,r,a,p)
 def test_every_union_case_is_required(self):
  for index in range(48):
   m,r,a,p=support_fixture();report=r['reports']['policy-credit-labs'];report['cases'].pop(index)
   next(f for f in r['pack']['files']if f['path']=='policy-credit-labs/report.json')['sha256']=hashlib.sha256(json.dumps(report,ensure_ascii=False,indent=2).encode()).hexdigest()
   with self.subTest(index=index),self.assertRaises(ValueError):validate_support(m,r,a,p)
if __name__=='__main__':unittest.main()
