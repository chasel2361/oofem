import unittest
from Section import Section
from Beam2D import Beam2D
from Point import Point
from Node import Node
from math import isclose, acos, pi
from numpy import array

class Beam2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point(0, 0, 0))
        n2 = Node(2, Point(0, 1, 0))
        material = Section(1, 1.0, 10000, 0, 100, 1000, 1000, 2000)
        rayleigh = 'damping' 
        self.beam = Beam2D(1, n1, n2, material, rayleigh)

    def tearDown(self):
        self.beam = None
    
    def test_lumped_mass(self):
        true = self.assertTrue
        lumped = self.beam.lumped_mass

        true(isclose(lumped[0], 0.5))
        true(isclose(lumped[1], 0.5))
        true(isclose(lumped[2], 5))
        true(isclose(lumped[3], 0.5))
        true(isclose(lumped[4], 0.5))
        true(isclose(lumped[5], 5))
    
    def test_get_internal_force(self):
        true = self.assertTrue
        n1 = Node(1, Point())
        n2 = Node(2, Point(4, 3, 0))
        section = Section(1, 0, 1000, 0, 0.1, 0, 0.001, 0)
        beam = Beam2D(1, n1, n2, section, 0)
        dofs1 = beam.node1.dofs

        dofs1[0].d = 0.1
        dofs1[1].d = 0.1

        force = beam.get_internal_force('d', 'pos_origin')
        ans = array([
            [ 2.238848],
            [ 1.681536],
            [-0.0048  ],
            [-2.238848],
            [-1.681536],
            [-0.0048  ]])

        for i in range(6):
            true(isclose(force[i, 0], ans[i, 0]))
    
    # def test_formal_get_internal_force(self):
    #     beam = self.beam
    #     dofs1 = beam.node1.dofs
    #     dofs2 = beam.node2.dofs
    #     true = self.assertTrue

    #     dofs1[0].d = 0.1
    #     dofs1[1].d = 0.0
        
    #     dofs2[0].d = -0.1
    #     dofs2[1].d = 0.0

    #     force = beam.get_internal_force('d', 'pos')
    #     ans = [23231356.439579837, 4626075.190634524, -11843733.590992844, -23231356.439579837, -4626075.190634524, -11843733.590992844]

    #     for (f, a) in zip(force, ans):
    #         true(isclose(f, a))

    
    def test_get_local_stiffness(self):
        beam = self.beam
        true = self.assertTrue

        question = beam.get_local_stiffness()
        answer = array([
            [1000000,   0,          0,          -1000000,   0,          0],
            [0,         120000000,  -60000000,  0,          -120000000, -60000000],
            [0,         -60000000,  40000000,   0,          60000000,   20000000],
            [-1000000,  0,          0,          1000000,    0,          0],
            [0,         -120000000, 60000000,   0,          120000000,  60000000],
            [0,         -60000000,  20000000,   0,          60000000,   40000000]
        ])
        for i in range(6):
            for j in range(6):
                true(isclose(question[i, j], answer[i, j]))

    def test_get_global_stiffness(self):
        true = self.assertTrue
        n1 = Node(1, Point())
        n2 = Node(2, Point(4, 3, 0))
        section = Section(1, 0, 1000, 0, 0.1, 0, 0.001, 0)
        beam = Beam2D(1, n1, n2, section, 0)
        
        q = beam.get_global_stiffness('pos_origin')
        a = array([[ 12.83456,   9.55392,   0.144  , -12.83456,  -9.55392,   0.144  ],
            [  9.55392,   7.26144,  -0.192  ,  -9.55392,  -7.26144,  -0.192  ],
            [  0.144  ,  -0.192  ,   0.8    ,  -0.144  ,   0.192  ,   0.4    ],
            [-12.83456,  -9.55392,  -0.144  ,  12.83456,   9.55392,  -0.144  ],
            [ -9.55392,  -7.26144,   0.192  ,   9.55392,   7.26144,   0.192  ],
            [  0.144  ,  -0.192  ,   0.4    ,  -0.144  ,   0.192  ,   0.8    ]])
        for i in range(6):
            for j in range(6):
                true(isclose(q[i, j], a[i, j]))

if __name__ == '__main__':
    unittest.main()
