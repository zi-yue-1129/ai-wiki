"""Fail closed on lost original or new built-policy viewport cases."""
import unittest,itertools,copy,ast
from pathlib import Path
from test_policy_credit_labs_browser import validate_complete_cases
class UnionCoverage(unittest.TestCase):
 def cases(self):return [dict(topic=t,lang=l,width=w,reduced=r,status='passed',errors=[]) for t,l,w,r in itertools.product(('reinforce','grpo'),('en','zh-TW'),(320,360,390,720,1024,1280),(False,True))]
 def test_complete_union(self):validate_complete_cases(self.cases())
 def test_every_missing_case(self):
  for i in range(48):
   c=self.cases();c.pop(i)
   with self.subTest(i=i),self.assertRaises(AssertionError):validate_complete_cases(c)
 def test_duplicate_wrong_width_and_failure(self):
  for k in ['duplicate','width','failed','errors']:
   c=self.cases()
   if k=='duplicate':c[-1]=copy.deepcopy(c[0])
   elif k=='width':c[0]['width']=375
   elif k=='failed':c[0]['status']='failed'
   else:c[0]['errors']=['page error']
   with self.subTest(k=k),self.assertRaises(AssertionError):validate_complete_cases(c)
 def test_real_runner_calls_failclosed_checker_before_success(self):
  src=(Path(__file__).parent/'test_policy_credit_labs_browser.py').read_text();tree=ast.parse(src)
  main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
  calls=[n for n in ast.walk(main)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='validate_complete_cases'];self.assertEqual(len(calls),1)
  self.assertIn("validate_complete_cases(report['cases'])\n        report['status']='passed'",src)
if __name__=='__main__':unittest.main()
