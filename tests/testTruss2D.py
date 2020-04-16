import unittest

from Node import Node, Point
from Truss2D import Truss2D
from Section import Section
from math import isclose
from numpy import array

class Truss2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point())
        n2 = Node(2, Point(3, 4, 0))
        section = Section(1, 1, 1000, 0, 0.1, 0.001, 0, 0)
        self.truss = Truss2D(1, n1, n2, section, 0.1)

    def tearDown(self):
        self.truss = None
    
    def test_lumped_mass(self):
        true = self.assertTrue
        
        q = self.truss.lumped_mass
        a = [2.5, 2.5, 2.5, 2.5]
        for i in range(4):
            true(isclose(q[i, 0], a[i]))

    def test_get_local_stiffness(self):
        true = self.assertTrue
        
        q = self.truss.get_local_stiffness()
        a = array([[ 20., -20.],       
            [-20.,  20.]])

        for i in range(2):
            for j in range(2):
                true(isclose(q[i, j], a[i, j]))
    
    def test_get_global_stiffness(self):
        true = self.assertTrue
        
        q = self.truss.get_global_stiffness('pos_origin')
        a = array([[  7.2,   9.6,  -7.2,  -9.6],
            [  9.6,  12.8,  -9.6, -12.8],
            [ -7.2,  -9.6,   7.2,   9.6],
            [ -9.6, -12.8,   9.6,  12.8]])
        
        for i in range(4):
            for j in range(4):
                true(isclose(q[i, j], a[i, j]))

    def test_get_internal_force(self):
        true = self.assertTrue
        truss = self.truss
        dofs = truss.dofs

        dofs[0].d_try = 0.1
        dofs[3].d_try = 0.1

        q = truss.get_internal_force('d_try', 'pos_origin')        
        a = array([[-0.24],
            [-0.32],
            [ 0.24],
            [ 0.32]])

        for i in range(4):
           true(isclose(q[i, 0], a[i, 0]))
