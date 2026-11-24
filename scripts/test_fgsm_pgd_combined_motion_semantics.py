"""Independent actual-SVG trajectory/reveal synchronization and source preservation."""
import math,re,unittest,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SVG=ROOT/'docs/assets/concept-animations/fgsm-pgd-trajectory.svg';N='{http://www.w3.org/2000/svg}'
def interpolate(node,t,attr='values'):
    ts=list(map(float,node.get('keyTimes').split(';')));vs=list(map(float,node.get(attr).split(';')))
    if t>=ts[-1]:return vs[-1]
    i=next(i for i in range(len(ts)-1) if ts[i]<=t<ts[i+1])
    if node.get('calcMode')=='discrete':return vs[i]
    return vs[i]+(vs[i+1]-vs[i])*(t-ts[i])/(ts[i+1]-ts[i])
def points(d):
    parts=re.findall(r'([MLH])([^MLH]+)',d);out=[]
    for command,arg in parts:
        values=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',arg)))
        out.append((values[0],out[-1][1]) if command=='H' else tuple(values))
    return out

def lengths(ps):return [math.dist(a,b) for a,b in zip(ps,ps[1:])]
def point_at(ps,f):
    ls=lengths(ps);distance=sum(ls)*f
    for a,b,l in zip(ps,ps[1:],ls):
        if distance<=l+1e-9:return tuple(x+(y-x)*min(1,distance/l) for x,y in zip(a,b))
        distance-=l
    return ps[-1]

class CombinedSVG(unittest.TestCase):
    def test_all_10001_marker_and_reveal_positions(self):
        root=ET.parse(SVG).getroot();strokes=[p for p in root.iter(N+'path') if p.find(N+'animate') is not None and p.find(N+'animate').get('attributeName')=='stroke-dashoffset']
        markers=[c for c in root.iter(N+'circle') if c.find(N+'animateMotion') is not None]
        self.assertEqual(len(strokes),4)
        for stroke in strokes:
            ps=points(stroke.get('d'));length=sum(lengths(ps));self.assertAlmostEqual(float(stroke.get('stroke-dasharray')),length,9)
            marker=next(c for c in markers if (float(c.get('cx')),float(c.get('cy')))==ps[0]);motion=marker.find(N+'animateMotion');origin=ps[0]
            marker_ps=[(a+origin[0],b+origin[1]) for a,b in points(motion.get('path'))]
            self.assertEqual(marker_ps,ps)
            for i in range(10001):
                t=i/10000;f=interpolate(motion,t,'keyPoints');shown=length-interpolate(stroke.find(N+'animate'),t)
                self.assertAlmostEqual(shown,length*f,5,(stroke.get('d'),t))
                self.assertLess(math.dist(point_at(ps,shown/length),point_at(marker_ps,f)),1e-5)
    def test_proposal_visibility_and_exact_handoff(self):
        root=ET.parse(SVG).getroot();marker=next(c for c in root.iter(N+'circle') if c.get('class')=='moving-marker' and c.get('cx')=='595')
        opacity=marker.find(N+'animate');self.assertEqual(interpolate(opacity,.50001),1);self.assertEqual(interpolate(opacity,.7),0)
        endpoint=next(c for c in root.iter(N+'circle') if c.get('class')=='phase-candidate')
        self.assertEqual(interpolate(endpoint.find(N+'animate'),.69999),0);self.assertEqual(interpolate(endpoint.find(N+'animate'),.7),1)
    def test_bilingual_native_width_source_hooks_and_existing_tests(self):
        from html.parser import HTMLParser
        class Images(HTMLParser):
            def __init__(self):super().__init__();self.attrs=[]
            def handle_starttag(self,tag,attrs):
                if tag=='img':self.attrs.append(dict(attrs))
        for name in ('fgsm','pgd-adversarial-training'):
            for suffix in ('','.zh-TW'):
                text=(ROOT/f'docs/theory/machine-learning/adversarial-robustness/{name}{suffix}.md').read_text();parser=Images();parser.feed(text)
                image=next(i for i in parser.attrs if 'fgsm-pgd-trajectory.svg' in i.get('src',''))
                self.assertEqual(image['src'],image['data-source-asset-urls']);self.assertIn('min-width:720px',image['style'])
                self.assertIn('tabindex="0"',text);self.assertIn('overflow-x:auto',text)
        workflow=(ROOT/'.github/workflows/fgsm-pgd-animation.yml').read_text()
        for script in ('check_fgsm_pgd_projection.py','check_fgsm_pgd_timeline.py','test_fgsm_pgd_combined_motion_semantics.py','test_fgsm_pgd_combined_built_browser.py'):
            self.assertIn('python scripts/'+script,workflow)
        self.assertIn('if: always()',workflow)


def require_supported_runner(workflow):
    # This one-job workflow intentionally pins the OS alongside Playwright.
    jobs=re.findall(r'^  ([A-Za-z_][\w-]*):\s*$',workflow.split('jobs:',1)[1],re.M)
    assert jobs==['semantics'], 'Review each new job before changing the runner contract'
    runners=re.findall(r'^    runs-on:\s*(.*?)\s*$',workflow,re.M)
    assert runners==['ubuntu-24.04'], 'Playwright 1.56 requires the pinned supported runner'
    install=re.search(r'^      - name: Install Chromium for actual SMIL frame capture\n        run: \|\n((?:          .*\n)+)',workflow,re.M)
    assert install, 'Browser installation must remain an unconditional run step'
    commands=[line.strip() for line in install[1].splitlines()]
    assert commands==["python -m pip install 'playwright==1.56.0'",'python -m playwright install --with-deps chromium']
    assert 'PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS' not in workflow
    assert 'PLAYWRIGHT_HOST_PLATFORM_OVERRIDE' not in workflow

class SupportedRunner(unittest.TestCase):
    def test_actual_workflow_and_unsupported_drift_negatives(self):
        workflow=(ROOT/'.github/workflows/fgsm-pgd-animation.yml').read_text()
        require_supported_runner(workflow)
        for runner in ('ubuntu-latest','ubuntu-26.04','${{ matrix.os }}','[ubuntu-24.04, self-hosted]',''):
            with self.subTest(runner=runner),self.assertRaises(AssertionError):
                require_supported_runner(workflow.replace('runs-on: ubuntu-24.04','runs-on: '+runner))
        for token in ("python -m pip install 'playwright==1.56.0'",'python -m playwright install --with-deps chromium'):
            with self.assertRaises(AssertionError):require_supported_runner(workflow.replace(token,''))
        for replacement in ('python -m playwright install chromium','# python -m playwright install --with-deps chromium','python -m playwright install --with-deps chromium || true'):
            with self.assertRaises(AssertionError):require_supported_runner(workflow.replace('python -m playwright install --with-deps chromium',replacement))
        for override in ('PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS','PLAYWRIGHT_HOST_PLATFORM_OVERRIDE'):
            with self.assertRaises(AssertionError):require_supported_runner(workflow+'\n# '+override)

if __name__=='__main__':unittest.main()
