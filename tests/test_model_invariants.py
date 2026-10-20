"""Lightweight independent numerical invariants for continuous integration."""
import math
import unittest
import numpy as np


def F(s, drive, precision):
    return .5 * (s-drive)**2 + precision * s*s * (1-s)**2


def derivative(s, drive, precision):
    return (s-drive) + 2*precision*s*(1-s)*(1-2*s)


def curvature(s, precision):
    return 1 + 2*precision*(1-6*s+6*s*s)


class DynamicsTests(unittest.TestCase):
    def test_figure1_logistic_folds(self):
        G, k = 8., 1.
        low = (1-math.sqrt(1-4/(k*G)))/2
        high = (1+math.sqrt(1-4/(k*G)))/2
        drives = [math.log(s/(1-s))/k-G*s for s in (low,high)]
        np.testing.assert_allclose(drives,[-2.93432005,-5.06567995],atol=1e-7)

    def test_figure2_folds(self):
        for P, targets in ((2.,(.36391724,.63608276)),(3.,(.18573032,.81426968))):
            # Fold states are roots of 12P*s^2-12P*s+(1+2P)=0.
            states = np.sort(np.roots([12*P,-12*P,1+2*P]))
            drives = sorted(float(s+2*P*s*(1-s)*(1-2*s)) for s in states)
            np.testing.assert_allclose(drives,targets,atol=1e-7)
            for s in states:
                self.assertAlmostEqual(curvature(s,P),0.,places=12)

    def test_figure2_differentiation(self):
        s,drive,P=.28,.47,2.4
        eps=1e-6
        numerical=(F(s+eps,drive,P)-F(s-eps,drive,P))/(2*eps)
        self.assertAlmostEqual(numerical,derivative(s,drive,P),places=7)

    def test_fig4_reset_is_input_dependent(self):
        # h=1.3: lower fold drive >0 and upper fold drive >0.
        G=1.3; k=4.; th=.75
        states=[(1+sign*math.sqrt(1-4/(k*G)))/2 for sign in (-1,1)]
        drives=[th+math.log(s/(1-s))/k-G*s for s in states]
        self.assertGreater(min(drives),0.)
        self.assertLess(min(drives),.1)
        self.assertGreater(max(drives),.1)


if __name__ == '__main__':
    unittest.main()
