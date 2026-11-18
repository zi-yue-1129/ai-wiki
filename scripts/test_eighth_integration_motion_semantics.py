"""Integration guards: preserve executable source suites, not YAML-shaped comments."""
from pathlib import Path
import re
import subprocess
import unittest
import yaml
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {'test_bandit_actual_labs.cjs','verify_bandit_motion.py','test_bandit_motion_browser.py','test_bandit_labs_browser.py',
 'verify_norm_seq_motion.py','test_norm_seq_actual_motion_semantics.py','test_norm_seq_actual_math.cjs','test_norm_seq_actual_ui.cjs','test_norm_seq_motion_browser.py','test_norm_seq_labs_browser.py',
 'test_lime_shap_motion_browser.py','test_explanation_labs_browser.py','test_explanation_math.cjs','test_explanation_motion_semantics.py',
 'test_attention_review_semantics.py','test_attention_actual_ui.cjs','test_attention_labs_browser.py','test_attention_variants_browser.py','test_flashattention_online_browser.py',
 'test_causal_motion_browser.py','test_causal_labs_browser.py','test_causal_motion_semantics.py','test_gqa_source_semantics.py','test_gqa_player.cjs','test_gqa_source_browser.py'}

def check_workflow(test, text):
    workflow=yaml.safe_load(text);commands=[]
    for job in workflow['jobs'].values():
        for step in job.get('steps',[]):
            test.assertTrue(('run' in step)^('uses' in step),'Every step must remain executable')
            commands.append(step.get('run',''))
    # Includes direct script calls and unittest-discovery quoted -p patterns.
    called=set(re.findall(r'(?:scripts/|["\'])([\w-]+\.(?:py|cjs))', '\n'.join(commands)))
    test.assertTrue(REQUIRED<=called,REQUIRED-called)

class EighthIntegration(unittest.TestCase):
    def test_workflow_and_lost_run_negative(self):
        text=(ROOT/'.github/workflows/concept-animation-validation.yml').read_text()
        check_workflow(self,text)
        marker='      - name: Check LayerNorm and Seq2Seq SVG, fallback and maths\n        run: |'
        self.assertIn(marker,text)
        with self.assertRaises(AssertionError):check_workflow(self,text.replace(marker,marker.split('\n')[0],1))
    def test_actual_player_scope(self):
        subprocess.run(['node','scripts/test_eighth_player_scope.cjs'],cwd=ROOT,check=True)

if __name__=='__main__':unittest.main()
