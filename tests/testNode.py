import unittest
import random
from Node import Node, BoundaryDof, ActiveDof, Point
from Integrator import Newmark
from math import isclose
from numpy import array

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.node = Node(1, Point(1, 2, 3))
    
    def tearDown(self):
        self.node = None
    
    #寫一個驗證is_restrained的test

    #先驗證非restrained，鎖完之後再驗證是restrained
    def test_restrain_dof(self):
        n = self.node
        restrain_dof = n.restrain_dof
        expect = [type(BoundaryDof())]*6
        Equal = self.assertEqual
        for i in range(6):
            restrain_dof(i)
            Equal(type(n.dofs[i]), expect[i])
    

    def test_restrain(self):
        n = self.node
        expect = [type(BoundaryDof())]*6
        Equal = self.assertEqual
        n.restrain()
        for i in range(6):
            Equal(type(n.dofs[i]), expect[i])

    def test_assign_eq_number(self):
        n = self.node
        Equal = self.assertEqual
        n.restrain_dof(2)
        n.restrain_dof(5)
        n.assign_eq_number(1)
        Equal(n.dofs[0].eq_number,  1)
        Equal(n.dofs[1].eq_number,  2)
        Equal(n.dofs[2].eq_number,  None)
        Equal(n.dofs[3].eq_number,  3)
        Equal(n.dofs[4].eq_number,  4)
        Equal(n.dofs[5].eq_number,  None)
    

    def test_Newmark(self):
        newmark = Newmark(0.01)
        n = self.node
        true = self.assertTrue        

        for i in range(6):
            dof = n.dofs[i]
            dof.d_try = i*0.5 - 1.5
            dof.v = i*0.5 - 1.5
            dof.a = i*0.5 - 1.5

        n.integrate(newmark)

        dofs = n.dofs
        true(isclose(dofs[0].a_try, -59398.5) and isclose(dofs[0].v_try, -298.5))
        true(isclose(dofs[1].a_try, -39599.0) and isclose(dofs[1].v_try, -199.0))
        true(isclose(dofs[2].a_try, -19799.5) and isclose(dofs[2].v_try, -99.5))
        true(isclose(dofs[3].a_try, 0.0) and isclose(dofs[3].v_try, 0.0))
        true(isclose(dofs[4].a_try, 19799.5) and isclose(dofs[4].v_try, 99.5))
        true(isclose(dofs[5].a_try, 39599.0) and isclose(dofs[5].v_try, 199.0))
        

    def test_inc_d_try(self):
        d = array([[2], [3], [4], [5], [6], [7]])
        n = self.node
        Equal = self.assertEqual
        dofs = n.dofs
        n.assign_eq_number(0)
        for i in range(6):
            n.dofs[i].d_try = 1.0
        
        n.inc_d_try(d)

        for i in range(6):
            Equal(dofs[i].d_try_last, 1.0)
            Equal(dofs[i].d_try, i+3)

    def test_commit(self):
        n = self.node
        Equal = self.assertEqual
        dis = [random.uniform(0, 3) for i in range(6)]
        d_try = [random.uniform(0, 3) for i in range(6)]
        v_try = [random.uniform(0, 3) for i in range(6)]
        a_try = [random.uniform(0, 3) for i in range(6)]

        for dof, d, dt, vt, at in zip(n.dofs, dis, d_try, v_try, a_try):
            dof.d = d
            dof.d_try = dt
            dof.v_try = vt
            dof.a_try = at
        
        n.commit()

        for dof, d, dt, vt, at in zip(n.dofs, dis, d_try, v_try, a_try):
            Equal(dof.d_last, d)
            Equal(dof.d, dt)
            Equal(dof.v, vt)
            Equal(dof.a, at)


if __name__ == '__main__':
    unittest.main()