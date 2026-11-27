"""Numerical checks for two illustrative distillation motion examples."""
import math
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'docs/assets/concept-animations'


def softmax(z):
    exps = [math.exp(v) for v in z]
    return [v / sum(exps) for v in exps]


class DistillationGenerationMotion(unittest.TestCase):
    def labels(self, stem, mode):
        root = ET.parse(ASSETS / f'{stem}-{mode}.svg').getroot()
        self.assertEqual(root.get('viewBox'), '0 0 640 360')
        return {e.text for e in root.iter() if e.tag.endswith('}text')}

    def test_teacher_assistant_target_gradient(self):
        # Analytic gradient vs finite differences at the same student start.
        for p, expected in ((.8, -.3), (.65, -.15)):
            def loss(z):
                a = 1 / (1 + math.exp(-z))
                return -p * math.log(a) - (1-p) * math.log((1-a)/2)
            eps = 1e-5
            self.assertAlmostEqual((loss(eps)-loss(-eps))/(2*eps), expected, places=8)
        for mode in ('motion', 'still'):
            labels = self.labels('teacher-assistant-target-gradient', mode)
            self.assertTrue({'80.0%', '65.0%', '70.0%', '−0.30', '−0.15', '−0.10', '+0.05', 'P(A): 50.0% → 70.0%'} <= labels)

    def test_born_again_fresh_logits(self):
        p = [.7, .2, .1]
        expected = [(0.464, .281, .255), (.378, .315, .307)]
        for target in expected:
            z = [v - 1/3 for v in p]
            self.assertAlmostEqual(sum(z), 0)
            p = softmax(z)
            self.assertEqual(tuple(round(v, 3) for v in p), target)
        for mode in ('motion', 'still'):
            labels = self.labels('born-again-generation-step', mode)
            self.assertTrue({'46.4%', '28.1%', '25.5%', '37.8%', '31.5%', '30.7%'} <= labels)


    def test_target_sign_reversal(self):
        for a,expected in [(0.5,(-.3,-.15)),(.65,(-.15,0)),(.7,(-.1,.05))]:
            z=math.log(a/(1-a)); eps=1e-5
            for p,g in zip((.8,.65),expected):
                def loss(z):
                    q=1/(1+math.exp(-z))
                    return -p*math.log(q)-(1-p)*math.log((1-q)/2)
                self.assertAlmostEqual((loss(z+eps)-loss(z-eps))/(2*eps),g,places=8)

    def test_one_step_contraction(self):
        def step(p,eta):
            exp=[math.exp(eta*v) for v in p]
            return [v/sum(exp) for v in exp]
        def distance(p,q):
            return math.sqrt(sum((a-b)**2 for a,b in zip(p,q)))
        u=[1/3]*3
        for eta in (.1,1,1.9):
            p=[.7,.2,.1]
            for _ in range(12):
                q=step(p,eta)
                self.assertLessEqual(distance(q,u),eta/2*distance(p,u)+1e-12)
                p=q


if __name__ == '__main__':
    unittest.main()
