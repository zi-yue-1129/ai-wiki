"""Keep the baseline-score identity equivalent and out of unbreakable inline math."""
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IDENTITY = r'\mathbb{E}_{a_t\sim\pi}[b(s_t)\nabla\log\pi(a_t\mid s_t)]=b(s_t)\nabla\sum_a\pi(a\mid s_t)=0'


def check_identity(test, text):
    blocks = re.findall(r'\\\[(.*?)\\\]', text, re.S)
    identity = [b for b in blocks if r'\mathbb{E}_{a_t\sim\pi}[b(s_t)' in b]
    test.assertEqual(len(identity), 1, 'baseline identity must be display math')
    block = identity[0]
    test.assertIn(r'\begin{aligned}', block)
    test.assertEqual(block.count(r'\\'), 2, 'three short equivalent lines')
    normalized = block.replace(r'\begin{aligned}', '').replace(r'\end{aligned}', '').replace(r'\\', '').replace('&', '').replace('.', '')
    test.assertEqual(re.sub(r'\s+', '', normalized), re.sub(r'\s+', '', IDENTITY))


class ReinforceLayoutTests(unittest.TestCase):
    def test_bilingual_display_identity_and_inline_mutation(self):
        for lang in ('', '.zh-TW'):
            text = (ROOT / f'docs/theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/reinforce/index{lang}.md').read_text()
            with self.subTest(lang=lang):
                check_identity(self, text)
                block = next(b for b in re.findall(r'\\\[(.*?)\\\]', text, re.S) if r'\mathbb{E}_{a_t\sim\pi}[b(s_t)' in b)
                bad = text.replace(r'\[' + block + r'\]', '$' + IDENTITY + '$')
                with self.assertRaises(AssertionError):
                    check_identity(self, bad)


class ReinforceUpdateLayoutTests(unittest.TestCase):
    def test_update_equivalence_both_languages(self):
        canonical = r'\theta\leftarrow\theta+\alpha\,\widehatg,\\\widehatg=\sum_t\nabla_\theta\log\pi_\theta(a_t\mids_t)\\\qquad\cdot(G_t-b).'
        for lang in ('', '.zh-TW'):
            text = (ROOT / f'docs/theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/reinforce/index{lang}.md').read_text()
            blocks = re.findall(r'\\\[(.*?)\\\]', text, re.S)
            block = next(b for b in blocks if r'\leftarrow' in b)
            normalized = re.sub(r'\s+', '', block).replace(r'\begin{aligned}', '').replace(r'\end{aligned}', '').replace('&', '')
            self.assertEqual(normalized, canonical)
            self.assertEqual(block.count(r'\\'), 2)
            self.assertNotRegex(text, r'\\\([^\n]*\\leftarrow[^\n]*\\sum_t')
            # The introduced temporary is exactly the original score sum,
            # not an average, omitted baseline, or shared-gradient shortcut.
            for rewards, scores, baseline in [([0,0,4],[1,-2,3],2),([1,0,2],[-3,.5,2],1.9)]:
                returns=[rewards[0]+.8*rewards[1]+.64*rewards[2],rewards[1]+.8*rewards[2],rewards[2]]
                ghat=sum(score*(ret-baseline) for score,ret in zip(scores,returns))
                self.assertAlmostEqual(2+.1*ghat,2+sum(.1*score*(ret-baseline) for score,ret in zip(scores,returns)))

    def test_browser_320_original_negative_and_early_failure_diagnostics(self):
        import ast
        source=(ROOT/'scripts/test_policy_credit_labs_browser.py').read_text()
        tree=ast.parse(source)
        functions={x.name:x for x in tree.body if isinstance(x,ast.FunctionDef)}
        negative=ast.get_source_segment(source,functions['check_320_update_negative'])
        self.assertIn('await MathJax.typesetPromise([wrapper])',negative)
        self.assertIn("wrapper.className = 'arithmatex'",negative)
        self.assertNotIn('await MathJax.tex2chtmlPromise',negative)
        self.assertIn("result['width'] > 320",negative)
        self.assertIn('MathJax.typesetClear([wrapper])',negative)
        self.assertIn('item.replaceChildren(...saved)',negative)
        self.assertIn("assert_document_fits(page, {'width':320})",negative)
        main=functions['main']
        # Diagnostics must run inside the still-live Playwright context,
        # not only after the context managers close the page on exception.
        with_block=next(x for x in ast.walk(main) if isinstance(x,ast.With))
        handler_calls=[n for x in with_block.body if isinstance(x,ast.Try) for h in x.handlers for n in ast.walk(h) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)]
        self.assertIn('failure_evidence',[n.func.id for n in handler_calls])
        self.assertIn("report['status'] = 'failed'",source)

if __name__ == '__main__':
    unittest.main()
