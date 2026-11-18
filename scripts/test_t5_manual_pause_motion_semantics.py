"""Manual pause after live speed change and automatic completion are independent contracts."""
import ast,unittest,re,fnmatch
from pathlib import Path
P=Path(__file__).with_name('test_t5_deit_labs_browser.py');TREE=ast.parse(P.read_text())
node=next(n for n in TREE.body if isinstance(n,ast.FunctionDef)and n.name=='check_manual_pause');ns={};exec(compile(ast.Module(body=[node],type_ignores=[]),str(P),'exec'),ns);check=ns['check_manual_pause']
class Page:
 def __init__(self,lang,broken=False,ended=False):self.lang=lang;self.playing=not ended;self.step=3 if ended else 2;self.broken=broken;self.leak=False;self.clicked=0;self.waited=0
 def locator(self,s):return Locator(self,s)
 def wait_for_timeout(self,t):self.waited=t;self.step+=int(t/350)if self.playing or self.leak else 0
class Locator:
 def __init__(self,p,s):self.p=p;self.s=s
 def inner_text(self):return ('Pause'if self.p.playing else'Play')if self.p.lang=='en'else('暫停'if self.p.playing else'播放')
 def input_value(self):return str(self.p.step)
 def click(self):self.p.clicked+=1;self.p.playing=self.p.broken
def validate_concept_route(source):
 paths=re.search(r'^  pull_request:\n    paths:\n(.*?)(?=^  [^ ]|\Z)',source,re.M|re.S).group(1)
 patterns=re.findall(r'^      - [\"\']([^\"\']+)[\"\']$',paths,re.M)
 for file in ('scripts/test_t5_deit_labs_browser.py','scripts/test_t5_manual_pause_motion_semantics.py'):
  assert any(fnmatch.fnmatchcase(file,p) for p in patterns),'Missing only-change trigger: '+file
 job=re.search(r'^  validate-motion:\n(.*?)(?=^  [A-Za-z0-9_-]+:|\Z)',source,re.M|re.S).group(1)
 assert not re.search(r'^    (if|continue-on-error):',job,re.M),'Conditional job'
 steps=re.split(r'^      - ',job,flags=re.M)[1:]
 for script in ('test_t5_deit_labs_browser.py','test_t5_manual_pause_motion_semantics.py'):
  matches=[step for step in steps if re.search(r'^        run: python scripts/'+re.escape(script)+r'$',step,re.M)]
  assert len(matches)==1,'Missing executable run step: '+script
  assert not re.search(r'^        (if|continue-on-error):',matches[0],re.M),'Conditional step'

class ManualPause(unittest.TestCase):
 def test_bilingual_real_click_and_wait(self):
  for lang in ['en','zh-TW']:
   p=Page(lang);self.assertEqual(check(p,lang),'2');self.assertEqual(p.clicked,1);self.assertGreater(p.waited,700)
 def test_broken_pause_rejected(self):
  with self.assertRaises(AssertionError):check(Page('en',broken=True),'en')
 def test_label_only_pause_with_running_timer_rejected(self):
  p=Page("en");p.leak=True
  with self.assertRaisesRegex(AssertionError,"did not stop"):check(p,"en")
 def test_auto_end_does_not_substitute_for_manual_pause(self):
  with self.assertRaises(AssertionError):check(Page('en',ended=True),'en')
 def test_matrix_and_both_paths_wired(self):
  loops={ast.unparse(n.target):ast.literal_eval(n.iter)for n in ast.walk(TREE)if isinstance(n,ast.For)and isinstance(n.iter,ast.Tuple)}
  self.assertEqual(loops['lang'],('en','zh-TW'));self.assertEqual(loops['width'],(320,360,760,1024));self.assertEqual(loops['reduce'],(False,True))
  s=P.read_text();start=s.index("select_option('0.5')");pause=s.index('check_manual_pause(page, lang)',start);resume=s.index('# Resume and retain auto-end coverage.',pause);end=s.index('page.wait_for_function(',resume);self.assertLess(start,pause);self.assertLess(pause,resume);self.assertLess(resume,end)
  self.assertIn('manual-paused-{lang}-{width}-{reduce}.png',s)
 def test_future_only_browser_or_negative_change_routes(self):
  validate_concept_route((P.parents[1]/'.github/workflows/concept-animation-validation.yml').read_text())
 def test_future_route_deletions_rejected(self):
  source=(P.parents[1]/'.github/workflows/concept-animation-validation.yml').read_text()
  for file in ('test_t5_deit_labs_browser.py','test_t5_manual_pause_motion_semantics.py'):
   line='      - "scripts/'+file+'"\n';command='        run: python scripts/'+file
   for bad in (source.replace(line,''),source.replace(command,'        # '+command.strip()),source.replace(command,command+'\n        if: false')):
    with self.subTest(file=file),self.assertRaises(AssertionError):validate_concept_route(bad)
if __name__=='__main__':unittest.main()
