import unittest

from Node import ActiveDof
from Integrator import Newmark
from math import isclose

class NewmarkTest(unittest.TestCase):
    def setUp(self):
        self.newmark = Newmark(0.01)
    
    def tearDown(self):
        self.newmark = None
    
    def test_integrate(self):
        dof = ActiveDof()
        dof.d = 0.005
        dof.d_try = 0.01
        dof.v = 0.5
        dof.a = -1
        self.newmark.integrate(dof)

        assertEqual = self.assertTrue
        assertEqual(isclose(dof.a_try, 1.0))
        assertEqual(isclose(dof.v_try, 0.5))

    def test_update_beta(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark.update_beta(0.5)
        true(isclose(newmark._b1, 20000))
        true(isclose(newmark._b2, -200))
        true(isclose(newmark._b3, 0))
    
    def test_update_gamma(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark.update_gamma(0.25)
        true(isclose(newmark._b4, 100))
        true(isclose(newmark._b5, 0))
        true(isclose(newmark._b6, 0.005))
    
    def test_update_delta_t(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark.update_delta_t(0.1)
        true(isclose(newmark._b1, 399.9999999999999))
        true(isclose(newmark._b2, -40))
        true(isclose(newmark._b4, 20))
        true(isclose(newmark._b6, 0))
    
    def test_update_b1(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark._update_b1(0.1, 0.5, 0.25)
        true(isclose(newmark._b1, 199.9999999999999))
    
    def test_update_b2(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark._update_b2(0.1, 0.5, 0.25)
        true(isclose(newmark._b2, -20))
    
    def test_update_b3(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark._update_b3(0.1, 0.5, 0.25)
        true(isclose(newmark._b3, 0))
    
    def test_update_b4(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark._update_b4(0.1, 0.5, 0.25)
        true(isclose(newmark._b4, 5))
        
    def test_update_b5(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark._update_b5(0.1, 0.5, 0.25)
        true(isclose(newmark._b5, 0.5))
    
    def test_update_b6(self):
        true = self.assertTrue
        newmark = self.newmark

        newmark._update_b6(0.1, 0.5, 0.25)
        true(isclose(newmark._b6, 0.075))


if __name__ == '__main__':
    unittest.main()