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
GUARDED_MATH_PAGES = ['docs/theory/math/automatic-differentiation/forward-mode.md', 'docs/theory/math/automatic-differentiation/forward-mode.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.zh-TW.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/exploration/icm/index.md', 'docs/theory/paradigms/reinforcement-learning/exploration/icm/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index.md', 'docs/theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/value-based-methods/sarsa/index.md', 'docs/theory/paradigms/reinforcement-learning/value-based-methods/sarsa/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.zh-TW.md', 'docs/theory/causal-inference/double-machine-learning.md', 'docs/theory/causal-inference/double-machine-learning.zh-TW.md']
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
    def test_confirmed_mobile_inline_formulas_are_display_and_tokens_preserved(self):
        import re
        records = [('docs/theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index.md', "\\(Q(s, a) \\leftarrow Q(s, a) + \\alpha \\left[ r + \\gamma \\max_{b} Q(s', b) - Q(s, a) \\right]\\)", "\\begin{aligned} Q(s, a) &\\leftarrow Q(s, a) \\\\ &+ \\alpha \\left[ r + \\gamma \\max_{b} Q(s', b) - Q(s, a) \\right] \\end{aligned}", "\n\n    $$\n    \\begin{aligned} Q(s, a) &\\leftarrow Q(s, a) \\\\ &+ \\alpha \\left[ r + \\gamma \\max_{b} Q(s', b) - Q(s, a) \\right] \\end{aligned}\n    $$\n\n    "), ('docs/theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index.zh-TW.md', "\\(Q(s, a) \\leftarrow Q(s, a) + \\alpha \\left[ r + \\gamma \\max_{b} Q(s', b) - Q(s, a) \\right]\\)", "\\begin{aligned} Q(s, a) &\\leftarrow Q(s, a) \\\\ &+ \\alpha \\left[ r + \\gamma \\max_{b} Q(s', b) - Q(s, a) \\right] \\end{aligned}", "\n\n    $$\n    \\begin{aligned} Q(s, a) &\\leftarrow Q(s, a) \\\\ &+ \\alpha \\left[ r + \\gamma \\max_{b} Q(s', b) - Q(s, a) \\right] \\end{aligned}\n    $$\n\n    "), ('docs/theory/paradigms/reinforcement-learning/value-based-methods/sarsa/index.md', '$G^\\lambda_{t:t+3}=0.20(3.700)+0.16(0.910)+0.64(4.798)=\\mathbf{3.95632}$', '\\begin{aligned} G^\\lambda_{t:t+3} &=0.20(3.700)+0.16(0.910) \\\\ &+0.64(4.798) \\\\ &=\\mathbf{3.95632} \\end{aligned}', '\n\n$$\n\\begin{aligned} G^\\lambda_{t:t+3} &=0.20(3.700)+0.16(0.910) \\\\ &+0.64(4.798) \\\\ &=\\mathbf{3.95632} \\end{aligned}\n$$\n\n'), ('docs/theory/paradigms/reinforcement-learning/value-based-methods/sarsa/index.zh-TW.md', '$G^\\lambda_{t:t+3}=0.20(3.700)+0.16(0.910)+0.64(4.798)=\\mathbf{3.95632}$', '\\begin{aligned} G^\\lambda_{t:t+3} &=0.20(3.700)+0.16(0.910) \\\\ &+0.64(4.798) \\\\ &=\\mathbf{3.95632} \\end{aligned}', '\n\n$$\n\\begin{aligned} G^\\lambda_{t:t+3} &=0.20(3.700)+0.16(0.910) \\\\ &+0.64(4.798) \\\\ &=\\mathbf{3.95632} \\end{aligned}\n$$\n\n')]
        def tokens(s):
            s=s.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('\\\\','').replace('&','')
            return ''.join(s.split())
        for path,old,body,new in records:
            new=new.strip()
            source=(ROOT/path).read_text()
            self.assertEqual(source.count(new),1)
            original=old[2:-2] if old.startswith('\\(') else old[1:-1]
            self.assertEqual(tokens(body),tokens(original))
            def check(text):
                blocks=[''.join(x.split()) for x in MathContainers(render(text)).blocks]
                assert blocks.count(r'\['+''.join(body.split())+r'\]')==1
            check(source)
            with self.assertRaises(AssertionError):check(source.replace(new,old))


    def test_standalone_mathjax_route_has_same_job_dependency_and_evidence(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/concept-animation-validation.yml').read_text())
        def check(w):
            paths=w.get('on',w.get(True))['pull_request']['paths']
            assert 'scripts/verify_icm_mathjax_structure.py' in paths
            assert 'scripts/render_mathjax_structure.cjs' in paths
            job=w['jobs']['build-docs']
            assert 'if' not in job
            assert job.get('continue-on-error') is None or job.get('continue-on-error') is False
            steps=job['steps']
            dep=next(i for i,x in enumerate(steps) if x.get('run')=='pip install -r requirements.txt')
            entry=next((i,x) for i,x in enumerate(steps) if 'python scripts/verify_icm_mathjax_structure.py' in x.get('run',''))
            i,step=entry;run=step['run']
            install='npm install --prefix "$RUNNER_TEMP/wiki-mathjax" --no-audit --no-fund --ignore-scripts mathjax-full@3.2.2'
            execute='NODE_PATH="$RUNNER_TEMP/wiki-mathjax/node_modules" python scripts/verify_icm_mathjax_structure.py'
            # This two-command shell block must execute exactly these commands.
            # Substring matches accept commented commands and masked failures.
            lines=[line.strip() for line in run.splitlines() if line.strip()]
            assert dep<i and lines == [install, execute]
            for required in [steps[dep], step]:
                assert 'if' not in required
                assert required.get('continue-on-error') is None or required.get('continue-on-error') is False
            upload=next(x for x in steps if x.get('with',{}).get('name')=='icm-mathjax-structure')
            assert upload.get('if')=='always()' and upload['with']['path']=='artifacts/icm-mathjax-structure/*.json'
        check(workflow)
        for mutation in ['install','version','order','conditional','path','upload','install-comment','install-softfail','execute-comment','execute-softfail','coe-zero','coe-true','job-coe-zero','dependency-coe-zero']:
            bad=copy.deepcopy(workflow);steps=bad['jobs']['build-docs']['steps']
            step=next(x for x in steps if 'python scripts/verify_icm_mathjax_structure.py' in x.get('run',''))
            if mutation=='install':step['run']='\n'.join(step['run'].splitlines()[1:])
            elif mutation=='version':step['run']=step['run'].replace('@3.2.2','@latest')
            elif mutation=='order':step['run']='\n'.join(reversed(step['run'].splitlines()))
            elif mutation=='conditional':step['if']='false'
            elif mutation=='path':bad.get('on',bad.get(True))['pull_request']['paths'].remove('scripts/verify_icm_mathjax_structure.py')
            elif mutation=='upload':steps.remove(next(x for x in steps if x.get('with',{}).get('name')=='icm-mathjax-structure'))
            elif mutation in ['install-comment','install-softfail','execute-comment','execute-softfail']:
                lines=step['run'].splitlines();index=0 if mutation.startswith('install') else 1
                lines[index]=('# '+lines[index]) if mutation.endswith('comment') else (lines[index]+' || true')
                step['run']='\n'.join(lines)
            elif mutation=='coe-zero':step['continue-on-error']=0
            elif mutation=='coe-true':step['continue-on-error']=True
            elif mutation=='job-coe-zero':bad['jobs']['build-docs']['continue-on-error']=0
            elif mutation=='dependency-coe-zero':next(x for x in steps if x.get('run')=='pip install -r requirements.txt')['continue-on-error']=0
            with self.assertRaises((AssertionError,StopIteration)):check(bad)

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
ADDITIONAL_PAGES = [('docs/theory/paradigms/reinforcement-learning/exploration/icm/index.md', 7, ['\\bar L_n=\\sum_{i=1}^3\\frac{N_i}{n}\\ell_i,\\qquad\nL=\\sum_{i=1}^3 p_i\\ell_i.']), ('docs/theory/paradigms/reinforcement-learning/exploration/icm/index.zh-TW.md', 7, ['\\bar L_n=\\sum_{i=1}^3\\frac{N_i}{n}\\ell_i,\\qquad\nL=\\sum_{i=1}^3 p_i\\ell_i.']), ('docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.md', 2, ['G_{t+1}=G_t-r_t.']), ('docs/theory/paradigms/reinforcement-learning/offline-rl/decision-transformer/index.zh-TW.md', 2, ['G_{t+1}=G_t-r_t.']), ('docs/theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index.md', 4, ['y_{\\mathrm{Q}}=1+0.9(5)=5.5,\\qquad Q_{\\mathrm{new}}=2+0.5(5.5-2)=3.75.', '\\mathbb{E}[\\max(\\hat Q_A,\\hat Q_B)]=\\tfrac{5+5+5+3}{4}=\\mathbf{4.5},\\qquad\n\\mathbb{E}[\\hat Q_B]=\\tfrac{5+3+5+3}{4}=\\mathbf{4}.']), ('docs/theory/paradigms/reinforcement-learning/value-based-methods/q-learning/index.zh-TW.md', 4, ['y_{\\mathrm{Q}}=1+0.9(5)=5.5,\\qquad Q_{\\mathrm{new}}=2+0.5(5.5-2)=3.75.', '\\mathbb{E}[\\max(\\hat Q_A,\\hat Q_B)]=\\tfrac{5+5+5+3}{4}=\\mathbf{4.5},\\qquad\n\\mathbb{E}[\\hat Q_B]=\\tfrac{5+3+5+3}{4}=\\mathbf{4}.']), ('docs/theory/paradigms/reinforcement-learning/value-based-methods/sarsa/index.md', 4, ['y_{\\mathrm{SARSA}}=1+0.9(2)=2.8,\\qquad\nQ_{\\mathrm{new}}=2+0.5(2.8-2)=2.40.']), ('docs/theory/paradigms/reinforcement-learning/value-based-methods/sarsa/index.zh-TW.md', 4, ['y_{\\mathrm{SARSA}}=1+0.9(2)=2.8,\\qquad\nQ_{\\mathrm{new}}=2+0.5(2.8-2)=2.40.'])]

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


class DmlLimitationsMarkupTests(unittest.TestCase):
    BODY = r"""\begin{aligned}
a_n&=\|\hat m-m_0\|_2,\\b_n&=\|\hat\ell-\ell_0\|_2,\\
a_n(a_n+b_n)&=o_p(n^{-1/2}).
\end{aligned}"""
    RECORDS = [('', 'Limitations', 'limitations',
                ['No unmeasured confounding.', 'Nuisance accuracy.', 'Target scope.', 'Model form.', 'Compute.'],
                'This includes a squared treatment-nuisance error, not just the product of the two errors; additional consistency and moment assumptions also apply.'),
               ('.zh-TW', '限制', '限制',
                ['未測量混淆。', '干擾函數精度。', '目標範圍。', '模型形式。', '計算。'],
                '條件包含處理干擾誤差的平方，不只是兩種誤差的乘積；另需一致性與矩條件。')]

    def require_structure(self, source, heading_id, titles, explanation):
        import re
        import xml.etree.ElementTree as ET
        # Parse the actual full page, then inspect the confirmed section rather
        # than counting only math blocks that the Markdown parser already found.
        html = render(source)
        require_no_outside_tex(html)
        match = re.search(r'<h2 id="'+re.escape(heading_id)+r'"[^>]*>.*?(?=<h2\b|\Z)', html, re.S)
        self.assertIsNotNone(match)
        region = ET.fromstring('<root>'+match.group().replace('&para;', '¶')+'</root>')
        lists = region.findall('ul'); self.assertEqual(len(lists), 1)
        items = lists[0].findall('li'); self.assertEqual(len(items), 5)
        for item, title in zip(items, titles):
            labels = item.findall('.//strong')
            self.assertEqual([''.join(x.itertext()) for x in labels], [title])
        expected = ''.join((r'\['+self.BODY+r'\]').split())
        math = [x for x in region.iter('div') if 'arithmatex' in x.get('class','').split()]
        self.assertEqual(len(math), 1)
        self.assertIn(math[0], list(items[1].iter()))
        self.assertEqual(''.join(''.join(math[0].itertext()).split()), expected)
        self.assertTrue(any(''.join(x.itertext()) == explanation for x in items[1].findall('p')))
        # Any raw TeX outside the expected math node is a failure, even if an
        # unrelated display elsewhere would keep a global container count stable.
        for parent in region.iter():
            for child in list(parent):
                if 'arithmatex' in child.get('class','').split(): parent.remove(child)
        residue = ''.join(region.itertext())
        for raw in [r'\begin', r'\end', 'a_n', 'b_n', r'\hat']:
            self.assertNotIn(raw, residue)

    def test_bilingual_full_page_math_and_all_five_list_items(self):
        for lang,heading,heading_id,titles,explanation in self.RECORDS:
            source=(ROOT/f'docs/theory/causal-inference/double-machine-learning{lang}.md').read_text()
            with self.subTest(language=lang): self.require_structure(source,heading_id,titles,explanation)

    def test_dml_pooling_equations_are_separate_display_blocks(self):
        # Check both formulas, not merely the absence of leaked TeX: deleting
        # either equation must also fail this contract.
        bodies = [
            r'\hat\theta_{\mathrm{DML2}}=\sum_k\frac{b_k}{\sum_j b_j}\frac{a_k}{b_k},',
            r'\hat\theta_{\mathrm{DML1}}=\frac1K\sum_k\frac{a_k}{b_k}.',
        ]
        for lang, *_ in self.RECORDS:
            source = (ROOT / f'docs/theory/causal-inference/double-machine-learning{lang}.md').read_text()
            with self.subTest(language=lang):
                html = render(source)
                require_no_outside_tex(html)
                blocks = [''.join(x.split()) for x in MathContainers(html).blocks]
                for body in bodies:
                    self.assertEqual(blocks.count(r'\[' + ''.join(body.split()) + r'\]'), 1)
                    self.assertEqual(source.count('\n\n$\n' + body + '\n$\n\n'), 1)

    def test_each_original_root_cause_and_detached_or_missing_formula_rejected(self):
        import re
        for lang,heading,heading_id,titles,explanation in self.RECORDS:
            source=(ROOT/f'docs/theory/causal-inference/double-machine-learning{lang}.md').read_text()
            start=source.index('## '+heading+'\n');end=source.index('\n## ',start+3)
            section=source[start:end]
            marker='\n\n- **'+titles[2]
            self.assertIn(marker,section)
            formula='    \\[\n'+'\n'.join('    '+line for line in self.BODY.splitlines())+'\n    \\]'
            self.assertEqual(section.count(formula),1)
            variants={
                'original-two-space':re.sub(r'(?m)^    (?=\S)','  ',section),
                'missing-list-boundary':section.replace(marker,'\n- **'+titles[2],1),
                'missing-formula':section.replace(formula,''),
                'detached-formula':section.replace(formula,'')+'\n\n'+formula.replace('    ','')+'\n',
            }
            for label,bad in variants.items():
                self.assertNotEqual(bad,section)
                with self.subTest(language=lang,mutation=label), self.assertRaises(AssertionError):
                    self.require_structure(source[:start]+bad+source[end:],heading_id,titles,explanation)

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
