"""Real configured MkDocs Markdown parsing, run only with wiki dependencies installed."""
from pathlib import Path
from html.parser import HTMLParser
import os
import unittest
import copy
import yaml
import markdown
from mkdocs.config import load_config

ROOT = Path(__file__).resolve().parents[1]
class MathContainers(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.depth = 0; self.parts = []; self.blocks = []; self.feed(html)
    def handle_starttag(self, tag, attrs):
        if self.depth: self.depth += 1
        elif tag == 'div' and 'arithmatex' in dict(attrs).get('class', '').split():
            self.depth = 1; self.parts = []
    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= 1
            if not self.depth: self.blocks.append(''.join(self.parts))
    def handle_data(self, data):
        if self.depth: self.parts.append(data)

def render(source):
    previous = Path.cwd()
    try:
        os.chdir(ROOT)
        config = load_config(config_file=str(ROOT / 'mkdocs.yml'))
        return markdown.markdown(source, extensions=config['markdown_extensions'], extension_configs=config['mdx_configs'])
    finally: os.chdir(previous)

def require_formulas(html):
    blocks = [''.join(x.split()) for x in MathContainers(html).blocks]
    for body in [r'\dot C=\dot A B+A\dot B.', r'\dot p_i=p_i\left(v_i-\sum_jp_jv_j\right),\qquad\dot p(0)=(3/8,-1/16,-5/16).']:
        expected = r'\[' + ''.join(body.split()) + r'\]'
        assert blocks.count(expected) == 1, (expected, blocks)

class ForwardMathMarkupTests(unittest.TestCase):
    def test_production_parser_ci_route_requires_wiki_dependencies(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/concept-animation-validation.yml').read_text())
        def check(w):
            paths = w.get('on', w.get(True))['pull_request']['paths']
            assert 'scripts/test_forward_math_markup.py' in paths
            job = w['jobs']['build-docs']; assert 'if' not in job
            assert job.get('continue-on-error') is None or job.get('continue-on-error') is False
            steps = job['steps']
            dep = next(i for i,x in enumerate(steps) if x.get('run') == 'pip install -r requirements.txt')
            run = next(i for i,x in enumerate(steps) if x.get('run') == 'python scripts/test_forward_math_markup.py')
            assert dep < run
            for i in [dep,run]:
                assert 'if' not in steps[i]
                assert steps[i].get('continue-on-error') is None or steps[i].get('continue-on-error') is False
        check(workflow)
        for mutation in ['dependency', 'test', 'path', 'conditional', 'softfailure', 'order']:
            bad = copy.deepcopy(workflow); steps=bad['jobs']['build-docs']['steps']
            dep=next(x for x in steps if x.get('run')=='pip install -r requirements.txt')
            run=next(x for x in steps if x.get('run')=='python scripts/test_forward_math_markup.py')
            if mutation=='dependency':steps.remove(dep)
            elif mutation=='test':steps.remove(run)
            elif mutation=='path':bad.get('on',bad.get(True))['pull_request']['paths'].remove('scripts/test_forward_math_markup.py')
            elif mutation=='conditional':run['if']=False
            elif mutation=='softfailure':run['continue-on-error']=True
            else:steps.remove(run);steps.insert(0,run)
            with self.subTest(mutation=mutation), self.assertRaises((AssertionError,StopIteration)):check(bad)

    def test_actual_bilingual_pages_and_original_markup_counterfactual(self):
        for lang in ['', '.zh-TW']:
            with self.subTest(language=lang):
                source = (ROOT / f'docs/theory/math/automatic-differentiation/forward-mode{lang}.md').read_text()
                require_formulas(render(source))
                # Restore each original malformed display independently: either must fail.
                for prefix in [r'\dot C=', r'\dot p_i=']:
                    start = source.index('$$\n'+prefix); end = source.index('\n$$', start)
                    old = source[:start] + '$' + source[start+2:end] + '\n$' + source[end+3:]
                    self.assertNotEqual(old, source)
                    with self.assertRaises(AssertionError): require_formulas(render(old))

if __name__ == '__main__': unittest.main()
