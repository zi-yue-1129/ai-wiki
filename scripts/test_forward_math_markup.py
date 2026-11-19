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
GUARDED_MATH_PAGES = ['docs/theory/math/automatic-differentiation/forward-mode.md', 'docs/theory/math/automatic-differentiation/forward-mode.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.zh-TW.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.zh-TW.md']
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
            for page in GUARDED_MATH_PAGES: assert page in paths
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
        for page in GUARDED_MATH_PAGES:
            bad = copy.deepcopy(workflow)
            bad.get('on',bad.get(True))['pull_request']['paths'].remove(page)
            with self.subTest(only_changed_page=page), self.assertRaises(AssertionError): check(bad)
        for mutation in ['dependency', 'test', 'path', 'conditional', 'softfailure', 'order', 'test-comment', 'dependency-comment', 'dependency-conditional', 'dependency-softfailure', 'job-conditional', 'job-softfailure']:
            bad = copy.deepcopy(workflow); steps=bad['jobs']['build-docs']['steps']
            dep=next(x for x in steps if x.get('run')=='pip install -r requirements.txt')
            run=next(x for x in steps if x.get('run')=='python scripts/test_forward_math_markup.py')
            if mutation=='dependency':steps.remove(dep)
            elif mutation=='test':steps.remove(run)
            elif mutation=='path':bad.get('on',bad.get(True))['pull_request']['paths'].remove('scripts/test_forward_math_markup.py')
            elif mutation=='conditional':run['if']=False
            elif mutation=='softfailure':run['continue-on-error']=True
            elif mutation=='test-comment':run['run']='# '+run['run']
            elif mutation=='dependency-comment':dep['run']='# '+dep['run']
            elif mutation=='dependency-conditional':dep['if']=False
            elif mutation=='dependency-softfailure':dep['continue-on-error']=True
            elif mutation=='job-conditional':bad['jobs']['build-docs']['if']=False
            elif mutation=='job-softfailure':bad['jobs']['build-docs']['continue-on-error']=True
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


# Independently enumerated original malformed blocks; not derived from current document.
ADDITIONAL_PAGES = [('docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.md', 2, ['G_{t+1}=G_t-r_t.']), ('docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.zh-TW.md', 2, ['G_{t+1}=G_t-r_t.'])]

class AdditionalMathMarkupTests(unittest.TestCase):
    def test_actual_pages_and_each_original_delimiter_counterfactual(self):
        for path, expected_count, bodies in ADDITIONAL_PAGES:
            source = (ROOT / path).read_text()
            def check(doc):
                blocks = ["".join(x.split()) for x in MathContainers(render(doc)).blocks]
                self.assertEqual(len(blocks), expected_count, path)
                for body in bodies:
                    expected = r"\[" + "".join(body.split()) + r"\]"
                    self.assertEqual(blocks.count(expected), 1, (path, body))
            with self.subTest(path=path):
                check(source)
                for body in bodies:
                    fixed = "$$\n" + body + "\n$$"
                    self.assertEqual(source.count(fixed), 1)
                    old = source.replace(fixed, "$\n" + body + "\n$", 1)
                    self.assertNotEqual(old, source)
                    with self.assertRaises(AssertionError): check(old)


class CqlObjectiveMarkupTests(unittest.TestCase):
    BODY = r"""\begin{aligned}L(Q_A,Q_B)&=\log(e^{Q_A}+e^{Q_B})-Q_A\\
&+\tfrac12(Q_A-2)^2.\end{aligned}"""
    def require_objective(self, source):
        expected=r'\['+''.join(self.BODY.split())+r'\]'
        html=render(source);require_no_outside_tex(html)
        blocks=[''.join(x.split()) for x in MathContainers(html).blocks]
        self.assertEqual(blocks.count(expected),1)
    def test_bilingual_actual_objective_and_each_missing_boundary_negative(self):
        for lang in ['', '.zh-TW']:
            source=(ROOT/f'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index{lang}.md').read_text()
            exact='\\[\n'+self.BODY+'\n\\]'
            self.assertEqual(source.count(exact),1)
            self.assertEqual(source.count('\n\n'+exact+'\n\n'),1)
            self.require_objective(source)
            variants=[source.replace('\n\n'+exact+'\n\n','\n'+exact+'\n',1),
                      source.replace('\n\n'+exact,'\n'+exact,1),
                      source.replace(exact+'\n\n',exact+'\n',1),
                      source.replace(exact,'',1)]
            for i,bad in enumerate(variants):
                self.assertNotEqual(bad,source)
                with self.subTest(language=lang,mutation=i),self.assertRaises(AssertionError):
                    self.require_objective(bad)

class OutsideMathTex(HTMLParser):
    """High-signal leaked TeX, not a claim to recognize every malformed formula."""
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, html):
        super().__init__(); self.stack=[]; self.fragments=[]; self.feed(html); self.close()
    def handle_starttag(self, tag, attrs):
        if tag in self.VOID: return
        excluded = tag in {'code','pre','script','style'} or (
            tag in {'div','span'} and 'arithmatex' in dict(attrs).get('class','').split())
        self.stack.append((tag, excluded))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0] == tag:
                self.stack=self.stack[:i]; break
    def handle_data(self, data):
        if not any(excluded for _,excluded in self.stack): self.fragments.append(data)
    def findings(self):
        import re
        pattern=r'\\(?:[A-Za-z]+|[,;!])'
        return [text for text in self.fragments if re.search(pattern,text)]

def require_no_outside_tex(html):
    findings=OutsideMathTex(html).findings()
    assert not findings, findings

class OutsideMathTexGuardTests(unittest.TestCase):
    def test_actual_parser_excludes_legal_math_and_markdown_code(self):
        examples=[r'$\hat A_t$'+'\n\n'+r'$$\sum_i x_i$$',
                  '`'+r'\frac{x}{y}'+'`',
                  '```tex\n'+r'\begin{aligned}x&=\sum_i x_i\end{aligned}'+'\n```',
                  '    '+r'\hat A_t=\gamma'+ '\n']
        for source in examples:
            with self.subTest(source=source): require_no_outside_tex(render(source))
        for tag in ['code','pre','script','style']:
            require_no_outside_tex('<'+tag+'>'+r'\frac{x}{y}\begin{aligned}'+'</'+tag+'>')
        for tag in ['div','span']:
            require_no_outside_tex('<'+tag+' class="arithmatex">'+r'\sum_i x_i'+'</'+tag+'>')

    def test_real_text_leaks_and_closed_exclusion_do_not_get_hidden(self):
        leaks=[r'<p>\mu_i=\rho</p>', r'<p>f(x)\,dt</p>', r'<p>\custommacro_z</p>', r'<p>[\begin{aligned}x=\frac{1}{2}\end{aligned}]</p>',
               r'<p>\hat A_t=\delta_t</p>',
               r'<span class="not-arithmatex">\sum_i x_i</span>',
               r'<code>\sum_i</code><br><p>\frac{x}{y}</p>',
               r'<div class="arithmatex">\[x=1\]</div><hr><p>\hat A_t</p>']
        for html in leaks:
            with self.subTest(html=html),self.assertRaises(AssertionError): require_no_outside_tex(html)

class MappoRecurrenceMarkupTests(unittest.TestCase):
    BODIES = [r'\delta_t=r_t+\gamma(1-d_t)V(s_{t+1})-V(s_t).',
              r'\hat A_t=\delta_t+\gamma\lambda(1-d_t)\hat A_{t+1}.']
    def require_recurrence(self, source):
        html=render(source)
        require_no_outside_tex(html)
        blocks=[''.join(x.split()) for x in MathContainers(html).blocks]
        for body in self.BODIES:
            expected=r'\['+''.join(body.split())+r'\]'
            self.assertEqual(blocks.count(expected),1)

    def test_bilingual_actual_source_recurrence_and_each_boundary_negative(self):
        for lang in ['', '.zh-TW']:
            source=(ROOT/f'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index{lang}.md').read_text()
            self.require_recurrence(source)
            for body in self.BODIES:
                exact='\\[\n'+body+'\n\\]'
                self.assertEqual(source.count(exact),1)
                self.assertEqual(source.count('\n\n'+exact+'\n\n'),1)
                for label,old,new in [('missing-trailing-boundary',exact+'\n\n',exact+'\n'),
                                      ('missing-leading-boundary','\n\n'+exact,'\n'+exact),
                                      ('missing-formula',exact,''),
                                      ('extra-raw-formula',exact,exact+'\n\n<p>'+body+'</p>')]:
                    bad=source.replace(old,new,1);self.assertNotEqual(bad,source)
                    with self.subTest(language=lang,body=body,mutation=label),self.assertRaises(AssertionError):
                        self.require_recurrence(bad)

class RetainedDeployedMathTests(unittest.TestCase):
    MADDPG = r"""a'_j=\mu'_j(o'_j),\qquad
y_1=r_1+\gamma(1-d)Q'_1(x',a'_1,\ldots,a'_N)."""
    SDE = [r'dx = f(x,t)\,dt + g(t)\,dw',
           r'dx = \big[f(x,t) - g(t)^2 \nabla_x \log p_t(x)\big]\,dt + g(t)\,d\bar w',
           r'dx = \big[f(x,t) - \tfrac{1}{2} g(t)^2 \nabla_x \log p_t(x)\big]\,dt']
    def require_bodies(self, source, bodies):
        html=render(source);require_no_outside_tex(html)
        blocks=[''.join(x.split()) for x in MathContainers(html).blocks]
        for body in bodies:self.assertEqual(blocks.count(r'\['+''.join(body.split())+r'\]'),1)
        return html
    def test_maddpg_target_actual_bilingual_source_and_boundary_negatives(self):
        for lang in ['', '.zh-TW']:
            source=(ROOT/f'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index{lang}.md').read_text()
            block='\\[\n'+self.MADDPG+'\n\\]'
            self.require_bodies(source,[self.MADDPG]);self.assertEqual(source.count('\n\n'+block+'\n\n'),1)
            for old,new in [('\n\n'+block,'\n'+block),(block+'\n\n',block+'\n'),(block,''),(block,block+'\n\n<p>'+self.MADDPG+'</p>')]:
                bad=source.replace(old,new,1);self.assertNotEqual(bad,source)
                with self.subTest(language=lang,mutation=old),self.assertRaises(AssertionError):self.require_bodies(bad,[self.MADDPG])
    def require_sde_list(self, source, lang):
        import re,xml.etree.ElementTree as ET
        html=self.require_bodies(source,self.SDE)
        section_id='核心想法'if lang else 'core-idea'
        match=re.search('<h2 id="'+section_id+r'"[^>]*>.*?(?=<h[23]\b|\Z)',html,re.S);self.assertIsNotNone(match)
        region=ET.fromstring('<root>'+match[0].replace('&para;','¶')+'</root>');lists=region.findall('ul');self.assertEqual(len(lists),1)
        items=lists[0].findall('li');self.assertEqual(len(items),3)
        titles=['前向 SDE。','逆時 SDE。','機率流 ODE。']if lang else ['Forward SDE.','Reverse-time SDE.','Probability flow ODE.']
        for item,title,body in zip(items,titles,self.SDE):
            self.assertEqual([''.join(x.itertext())for x in item.findall('.//strong')],[title])
            formulas=[x for x in item.iter('div')if 'arithmatex'in x.get('class','').split()];self.assertEqual(len(formulas),1)
            self.assertEqual(''.join(''.join(formulas[0].itertext()).split()),r'\['+''.join(body.split())+r'\]')
            self.assertEqual(len(item.findall('p')),2)
    def test_sde_three_bilingual_literal_formulas_and_list_ownership(self):
        # Forward SDE contains only punctuation commands, so an alphabetic-TeX
        # scan alone cannot establish completeness. All three bodies are literal.
        for lang in ['', '.zh-TW']:
            source=(ROOT/f'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde{lang}.md').read_text()
            self.require_sde_list(source,lang)
            for body in self.SDE:
                block='    \\[\n    '+body+'\n    \\]';self.assertEqual(source.count(block),1)
                for label,badblock in [('unindented',block.replace('    ','')),('missing',''),('raw-repeat',block+'\n\n    <p>'+body+'</p>')]:
                    bad=source.replace(block,badblock,1)
                    with self.subTest(language=lang,body=body,mutation=label),self.assertRaises(AssertionError):self.require_sde_list(bad,lang)
            # Missing list separation is also caught independently of formula count.
            title='逆時 SDE。'if lang else 'Reverse-time SDE.'
            bad=source.replace('\n\n- **'+title,'\n- **'+title,1);self.assertNotEqual(bad,source)
            with self.assertRaises(AssertionError):self.require_sde_list(bad,lang)

if __name__ == '__main__': unittest.main()
