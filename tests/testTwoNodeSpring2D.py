import unittest

from TwoNodeSpring2D import TwoNodeSpring2D, TwoNodeAxialSpring2D, TwoNodeShearSpring2D, TwoNodeRotationSpring2D
from Node import Node, Point
from Material import LinearMaterial
from math import isclose
from numpy import array, zeros

class TwoNodeSpring2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point())
        n2 = Node(2, Point(1.0, 1.0, 1.0))
        material = LinearMaterial(1, 10)
        self.spring = TwoNodeSpring2D(1, n1, n2, material, 1, 2)
    
    def tearDown(self):
        self.spring = None
    
    def test_lumped_mass(self):
        true = self.assertTrue
        sp = self.spring

        q = sp.lumped_mass
        a = [1, 1, 2, 1, 1, 2]
        for i in range(6):
            true(isclose(q[i, 0], a[i]))

    def test_length(self):
        sp = self.spring
        dofs1 = sp.node1.dofs
        dofs2 = sp.node2.dofs
        true = self.assertTrue

        dofs1[0].d = dofs1[1].d = dofs1[2].d = 1
        dofs1[0].d_last = dofs1[1].d_last = dofs1[2].d_last = -1
        dofs2[0].d_try = dofs2[1].d_try = dofs2[2].d_try = 2
        dofs2[0].d_try_last = 2
        dofs2[1].d_try_last = -2
        dofs2[2].d_try_last = 1


        true(isclose(sp.get_length('pos_origin'), 3**0.5))
        true(isclose(sp.get_length('pos'), 0.0))
        true(isclose(sp.get_length('pos_last'), 12**0.5))
        true(isclose(sp.get_length('pos_try'), 27**0.5))
        true(isclose(sp.get_length('pos_try_last'), 14**0.5))
    
    def test_get_axial_vector(self):
        sp = self.spring
        dofs1 = sp.node1.dofs
        dofs2 = sp.node2.dofs
        axial = sp._get_axial_vector
        true = self.assertTrue

        dofs2[1].d = -1
        dofs2[2].d = -1

        dofs1[0].d_last = 1
        dofs1[2].d_last = 1

        dofs2[0].d_try = -1
        dofs2[1].d_try = -1

        for dof in [dofs1, dofs2]:
            for i in range(3):
                dof[i].d_try_last = 2
        
        pos_type = ['pos_origin', 'pos', 'pos_last', 'pos_try', 'pos_try_last']
        question = [axial(pos).direction.value for pos in pos_type]
        
        ans = [[1/3**0.5]*3,
               [1, 0, 0], 
               [0, 1, 0],
               [0, 0, 1],
               [1/3**0.5]*3]        

        for (que, an) in zip(question, ans):
            for (q, a) in zip(que, an):
                true(isclose(q, a))
    
    def test_orient_to_local(self):
        n1 = Node(1, Point(0, 1, 0))
        n2 = Node(2, Point())
        material = LinearMaterial(1, 10)
        sp = TwoNodeSpring2D(1, n1, n2, material, 0, 0)
 
        true = self.assertTrue
        question = [0, -1, 0,  0, 1, 0]
        sp.orient_to_local(question, 'pos_origin')
        answer = [1, 0, 0, -1, 0, 0]

        for (q, a) in zip(question, answer):
            true(isclose(q, a))
    
    def test_orient_to_global(self):
        n1 = Node(1, Point(0, 1, 0))
        n2 = Node(2, Point())
        material = LinearMaterial(1, 10)
        sp = TwoNodeSpring2D(1, n1, n2, material, 0, 0)
 
        true = self.assertTrue
        question = [-1, 0, 0, 1, 0, 0]
        sp.orient_to_global(question, 'pos_origin')
        answer = [0, 1, 0, 0, -1, 0]

        for (q, a) in zip(question, answer):
            true(isclose(q, a))

class TwoNodeAxialSpring2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point(0, 1, 0))
        n2 = Node(2, Point())
        material = LinearMaterial(1, 10)
        self.spring = TwoNodeAxialSpring2D(1, n1, n2, material, 0, 0)
    
    def tearDown(self):
        self.spring = None
    
    def test_get_local_stiffness(self):
        true = self.assertTrue

        q = self.spring.get_local_stiffness()
        a = zeros((6, 6))
        a[0, 0], a[3, 3] = 10.0, 10.0
        a[0, 3], a[3, 0] = -10.0, -10.0

        for i in range(6):
            for j in range(6):
                true(isclose(q[i, j], a[i, j]))

    def test_get_internal_force(self):
        sp = self.spring
        true = self.assertTrue
        dofs = sp.dofs

        dofs[2].d_try = -1.5
        q = sp.get_internal_force('d_try', 'pos_try')
        a = array([[0.0], [0.0], [0.0], [0.0], [0.0], [0.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 7
        dofs[4].d_try = -7
        q = sp.get_internal_force('d_try', 'pos_try')
        a = array([[0.0], [140.0], [0.0], [0.0], [-140.0], [0.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[0].d_try = 3.2
        dofs[3].d_try = -3.2
        q = sp.get_internal_force('d_try', 'pos_try')
        a = array([[0.0], [140.0], [0.0], [0.0], [-140.0], [0.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 2
        q = sp.get_internal_force('d_try', 'pos_try')
        a = array([[0.0], [90.0], [0.0], [0.0], [-90.0], [0.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 0
        dofs[4].d_try = 0.9
        q = sp.get_internal_force('d_try', 'pos_try')
        a = array([[0.0], [-9.0], [0.0], [0.0], [9.0], [0.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[4].d_try = -1.3
        q = sp.get_internal_force('d_try', 'pos_try')
        a = array([[0.0], [13.0], [0.0], [0.0], [-13.0], [0.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))


class TwoNodeShearSpring2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point(0, 1, 0))
        n2 = Node(2, Point())
        material = LinearMaterial(1, 10)
        self.spring = TwoNodeShearSpring2D(1, n1, n2, material, 0, 0, 0.5)
    
    def tearDown(self):
        self.spring = None

    def test_get_local_stiffness(self):
        true = self.assertTrue

        q = self.spring.get_local_stiffness()
        a = zeros((6, 6))
        a[1, 1], a[4, 4] = 10.0, 10.0
        a[1, 4], a[4, 1] = -10.0, -10.0
        a[1, 2], a[2, 1], a[1, 5], a[5, 1] = 5, 5, 5, 5
        a[2, 4], a[4, 2], a[4, 5], a[5, 4] = -5, -5, -5, -5
        a[2, 5], a[5, 2], a[2, 2], a[5, 5] = 2.5, 2.5, 2.5, 2.5

        for i in range(6):
            for j in range(6):
                true(isclose(q[i, j], a[i, j]))
    
    def test_get_internal_force(self):
        sp = self.spring
        true = self.assertTrue
        dofs = sp.dofs

        dofs[0].d_try = 1.5
        q = sp.get_internal_force('d_try', '')
        a = array([[15.0], [0.0], [7.5], [-15.0], [0.0], [7.5]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 7
        dofs[4].d_try = -7
        q = sp.get_internal_force('d_try', '')
        a = array([[15.0], [0.0], [7.5], [-15.0], [0.0], [7.5]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[3].d_try = -3.2
        q = sp.get_internal_force('d_try', '')
        a = array([[47.0], [0.0], [23.5], [-47.0], [0.0], [23.5]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[5].d_try = -1
        q = sp.get_internal_force('d_try', '')
        a = array([[42.0], [0.0], [21.0], [-42.0], [0.0], [21.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))


class TwoNodeRotationSpring2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point(0.0, 1.0, 0.0))
        n2 = Node(2, Point())
        material = LinearMaterial(1, 10)
        self.spring = TwoNodeRotationSpring2D(1, n1, n2, material, 0, 0)
    
    def tearDown(self):
        self.spring = None
    
    def test_get_local_stiffness(self):
        true = self.assertTrue

        q = self.spring.get_local_stiffness()
        a = zeros((6, 6))
        a[2, 2], a[5, 5] = 10, 10
        a[2, 5], a[5, 2] = -10, -10

        for i in range(6):
            for j in range(6):
                true(isclose(q[i, j], a[i, j]))
    
    def test_get_internal_force(self):
        sp = self.spring
        true = self.assertTrue
        dofs = sp.dofs

        dofs[5].d_try = 1.5
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [-15.0], [0.0], [0.0], [15.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[0].d_try = 7
        dofs[3].d_try = -7
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [-15.0], [0.0], [0.0], [15.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 3.2
        dofs[4].d_try = -3.2
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [-15.0], [0.0], [0.0], [15.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[2].d_try = -2.6
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [-41.0], [0.0], [0.0], [41.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[2].d_try = 0
        dofs[5].d_try = 0.9
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [-9.0], [0.0], [0.0], [9.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[5].d_try = -1.3
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [13.0], [0.0], [0.0], [-13.0]])
        for i in range(6):
            true(isclose(q[i, 0], a[i, 0]))


if __name__ == '__main__':
    unittest.main()