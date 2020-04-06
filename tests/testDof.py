import unittest
from Dof import ActiveDof, BoundaryDof
from math import isclose

class ActiveDofTest(unittest.TestCase):
    def setUp(self):
        dof = ActiveDof()
        dof.eq_number = 1
        dof.d = 1
        dof.d_try_last = 2
        dof.d_try = 3
        dof.v = 1
        dof.v_try_last = 2
        dof.v_try = 3
        dof.a_try = 1
        self.dof = dof
    
    def tearDown(self):
        self.dof = None
    
    def test_inc_d_try(self):
        true = self.assertTrue
        dof = self.dof
        delta_d = [0, -1]

        dof.inc_d_try(delta_d)
        true(isclose(dof.d_try_last, 3))
        true(isclose(dof.d_try, 2))

    def test_commit(self):
        true = self.assertTrue
        dof = self.dof

        dof.commit()
        true(isclose(dof.d_last, 1))
        true(isclose(dof.d, 3))
        true(isclose(dof.v, 3))
        true(isclose(dof.a, 1))
    
    def test_assemble_force(self):
        true = self.assertTrue
        dof = self.dof
        force = [0, 1, 2, 3, 4]

        dof.assemble_force(force, 10)
        answer = [0, 11, 2, 3, 4]
        for a, q in zip(answer, force):
            true(isclose(a, q))
    
