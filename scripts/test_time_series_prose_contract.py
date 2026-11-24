"""Fail-closed matrix and actual JS geometry adapter regression tests."""
import copy,json,subprocess,unittest
from test_time_series_prose_browser import SOURCES,WIDTHS,target,validate_coverage,validate_formula,MEASURE_FORMULA,RESET_FORMULA
class ProseContract(unittest.TestCase):
 def cases(self):return [dict(source=s,lang=target(s)[0],width=w,status='passed',errors=[]) for s in SOURCES for w in WIDTHS]
 def test_exact_matrix(self):validate_coverage(self.cases())
 def test_missing_duplicate_failed_extra(self):
  cases=self.cases()
  bads=[cases[:-1],cases[:-1]+[cases[0]],cases+[cases[0]]]
  failed=copy.deepcopy(cases);failed[3]['status']='failed';bads.append(failed)
  running=copy.deepcopy(cases);running[0]['status']='running';bads.append(running)
  unexpected=copy.deepcopy(cases);unexpected[0]['width']=321;bads.append(unexpected)
  error=copy.deepcopy(cases);error[0]['errors']=['MathJax error'];bads.append(error)
  for bad in bads:
   with self.assertRaises(AssertionError):validate_coverage(bad)
 def actual_js(self,display=True,overflow='auto',stuck=False,wide=True):
  script='const measure='+MEASURE_FORMULA+'; const reset='+RESET_FORMULA+';\n'+'''global.innerWidth=320;global.requestAnimationFrame=f=>f();global.getComputedStyle=e=>({overflowX:e.overflowX||'visible'});
const config=CONFIG;
let left=0;
const scroller={clientWidth:200,scrollWidth:config.wide?400:200,clientLeft:0,overflowX:config.overflow,classList:{contains:()=>false},parentElement:null,getBoundingClientRect:()=>({left:5,right:205})};
Object.defineProperty(scroller,'scrollLeft',{get:()=>left,set:x=>{if(!config.stuck)left=x}});
const math={getBoundingClientRect:()=>({left:5-left,right:5-left+(config.wide?400:100),width:config.wide?400:100})};
const node={parentElement:scroller,classList:{contains:()=>false},getAttribute:()=>config.display?'true':null,querySelector:()=>math};
(async()=>{const m=await measure(node);reset(node);process.stdout.write(JSON.stringify({measurement:m,reset:left}));})().catch(e=>{console.error(e);process.exit(1)});
'''.replace('CONFIG',json.dumps(dict(display=display,overflow=overflow,stuck=stuck,wide=wide)))
  return json.loads(subprocess.check_output(['node','-e',script],text=True))
 def test_actual_js_scroll_right_and_restore(self):
  result=self.actual_js();validate_formula(result['measurement']);self.assertEqual(result['reset'],0);self.assertEqual(result['measurement']['after'],200)
 def test_actual_js_nonoverflow(self):validate_formula(self.actual_js(wide=False)['measurement'])
 def test_actual_js_inline_hidden_unreachable_rejected(self):
  for args in [dict(display=False),dict(overflow='hidden'),dict(stuck=True)]:
   with self.assertRaises(AssertionError):validate_formula(self.actual_js(**args)['measurement'])
 def test_workflow_execution(self):
  from pathlib import Path
  import yaml
  w=yaml.safe_load((Path(__file__).resolve().parents[1]/'.github/workflows/concept-animation-validation.yml').read_text())
  runs=[s.get('run','') for job in w['jobs'].values() for s in job['steps']]
  self.assertTrue(any('python scripts/test_time_series_prose_browser.py' in r for r in runs));self.assertTrue(any('python scripts/test_time_series_prose_contract.py' in r for r in runs))
if __name__=='__main__':unittest.main()
